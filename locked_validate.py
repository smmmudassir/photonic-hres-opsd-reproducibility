#!/usr/bin/env python3
"""Frozen 2020 confirmation. This source MUST be committed before running.
All future evaluation labels are hidden until execution after the public lock.
"""
import argparse, hashlib, json, platform
from pathlib import Path
import numpy as np
import pandas as pd
import lightgbm
import scipy
from sklearn.ensemble import HistGradientBoostingRegressor
from lightgbm import LGBMRegressor
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

SEED=13
MODEL={'n_estimators':260,'num_leaves':25,'learning_rate':0.05,
       'min_child_samples':30,'reg_lambda':2,'random_state':SEED,
       'verbosity':-1,'n_jobs':3}
TARGETS=['pv','wind','load']
V=np.array([-.9,-.8,1.25])
BAT={'e0':1.0,'emin':0.3,'emax':1.8,'pmax':0.75,'eta':0.95,'wear':15.0,'feedin':.055}
PRESET_HASH='6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8'

def read_region(path, code):
    prefix={'DE':'DE','GB':'GB_GBN'}[code]
    needed=['utc_timestamp',f'{prefix}_load_actual_entsoe_transparency',f'{prefix}_solar_generation_actual',f'{prefix}_wind_generation_actual']
    x=pd.read_csv(path,usecols=needed,parse_dates=['utc_timestamp']).set_index('utc_timestamp').sort_index()
    x=x.rename(columns={needed[1]:'load',needed[2]:'pv',needed[3]:'wind'})[['pv','wind','load']]
    x=x.loc['2015':'2020-09-30'].asfreq('h')
    # Do not consult 2019 calibration or 2020 validation when deriving scales.
    scale=x.loc['2015':'2018'].quantile(.99).to_dict()
    if any((not np.isfinite(v) or v<=0) for v in scale.values()):raise ValueError('invalid train-only scaling')
    x=x / pd.Series(scale)
    return x,scale

def build_features(x,dayahead=False):
    f=pd.DataFrame(index=x.index)
    for var in TARGETS:
        lags=([24,25,48,168,169] if dayahead else [1,2,24,25,48,168])
        for t in lags:f[f'{var}_lag{t}']=x[var].shift(t)
        f[f'{var}_day_ramp']=x[var].shift(24)-x[var].shift(48)
        if not dayahead:
            f[f'{var}_hour_ramp']=x[var].shift(1)-x[var].shift(2)
            f[f'{var}_week_ramp']=x[var].shift(1)-x[var].shift(168)
    idx=f.index
    for name,arr,period in [('hour',idx.hour.to_numpy(),24),('dow',idx.dayofweek.to_numpy(),7),('doy',idx.dayofyear.to_numpy(),366)]:
        f[f'{name}_sin']=np.sin(2*np.pi*arr/period)
        f[f'{name}_cos']=np.cos(2*np.pi*arr/period)
    net_lag=24 if dayahead else 1
    f['net_known']=(x[TARGETS].shift(net_lag).to_numpy()@V)
    y=x[TARGETS].copy()
    return f,y

def forecast(x):
    features,y=build_features(x)
    xa,ya=features.to_numpy(),y.to_numpy()
    valid=np.isfinite(xa).all(axis=1)&np.isfinite(ya).all(axis=1)
    idx=x.index
    train=valid&(idx.year<=2018)
    cal=valid&(idx.year==2019)
    models=[]
    for j in range(3):
        m=HistGradientBoostingRegressor(max_iter=180,max_leaf_nodes=25,learning_rate=.06,
                   l2_regularization=1,random_state=SEED)
        m.fit(xa[train],ya[train,j]);models.append(m)
    direct=LGBMRegressor(**MODEL)
    direct.fit(xa[train],ya[train]@V)
    p_hgb=np.full(len(x),np.nan)
    p_direct=np.full(len(x),np.nan)
    p_hgb[valid]=np.column_stack([m.predict(xa[valid]) for m in models])@V
    p_direct[valid]=direct.predict(xa[valid])
    truth=ya@V
    d=p_direct[cal]-p_hgb[cal]
    target=truth[cal]-p_hgb[cal]
    denom=d@d
    alpha_global=float(np.clip((d@target)/denom if denom>0 else 0.5,0,1))
    reg=np.where(idx.hour<7,0,np.where((idx.hour>=17)&(idx.hour<22),2,1))
    reg_alpha=[]
    for r in range(3):
        mask=cal&(reg==r)
        delta=p_direct[mask]-p_hgb[mask]
        err=truth[mask]-p_hgb[mask]
        mass=float(delta@delta)
        alpha=float(np.clip((delta@err+.5*mass*alpha_global)/(1.5*mass),0,1)) if mass>0 else alpha_global
        reg_alpha.append(alpha)
    out=pd.DataFrame({'truth':truth,'hgb_components':p_hgb,'direct':p_direct,
             'global_reconcile':p_hgb+alpha_global*(p_direct-p_hgb),
             'tariff_regime':p_hgb+np.array(reg_alpha)[reg]*(p_direct-p_hgb)},index=idx)
    out.loc[~valid,['hgb_components','direct','global_reconcile','tariff_regime']]=np.nan
    # A separately trained predictor using only values known no later than t-24.
    fa,ya=build_features(x,dayahead=True)
    aa=fa.to_numpy();yy=ya.to_numpy()@V
    good=np.isfinite(aa).all(axis=1)&np.isfinite(yy)
    tr=good&(idx.year<=2018)
    da=LGBMRegressor(**MODEL);da.fit(aa[tr],yy[tr]);pred=np.full(len(x),np.nan)
    pred[good]=da.predict(aa[good]);out['day_ahead']=pred
    return out,{'alpha_global':alpha_global,'regime_alpha_offpeak_day_peak':reg_alpha,
                'n_training':int(train.sum()),'n_calibration':int(cal.sum())}

def price(hours):
    h=np.asarray(hours)
    return np.where((h>=17)&(h<22),.30,np.where(h<7,.11,.18))

# Cached equality constraints for LP with five state/action components per time step.
_MATS={}
def lp_matrix(n):
    if n in _MATS:return _MATS[n]
    a=lil_matrix((2*n+1,5*n),dtype=float)
    for j in range(n):
        a[j,2*n+j]=1; a[j,3*n+j]=-1; a[j,j]=-1; a[j,n+j]=1
        a[n+j,4*n+j]=1;a[n+j,j]=-BAT['eta'];a[n+j,n+j]=1/BAT['eta']
        if j:a[n+j,4*n+j-1]=-1
    a[2*n,5*n-1]=1
    _MATS[n]=a.tocsr()
    return _MATS[n]

def lp_plan(net,prices,e):
    n=len(net)
    obj=np.r_[np.full(n,BAT['wear']),np.full(n,BAT['wear']),1000*prices,-1000*BAT['feedin']*np.ones(n),np.zeros(n)]
    rhs=np.r_[net,[e],np.zeros(n-1),[BAT['e0']]]
    bounds=([(0,BAT['pmax'])]*(2*n)+[(0,None)]*(2*n)+[(BAT['emin'],BAT['emax'])]*n)
    res=linprog(obj,A_eq=lp_matrix(n),b_eq=rhs,bounds=bounds,method='highs')
    if not res.success:raise RuntimeError(f'LP infeasible: {res.message}, horizon={n}')
    return np.asarray(res.x[:n]),np.asarray(res.x[n:2*n])

def evaluate_day(day,candidate):
    idx=day.index
    p=price(idx.hour)
    truth=day.truth.to_numpy()
    future=day.day_ahead.to_numpy()
    e=BAT['e0'];nsolves=0;plan_start=0;ch_plan=di_plan=None
    rows=[]
    for h in range(24):
        if candidate=='dayahead_lp':trigger=h==0
        elif candidate.startswith('hourly_'):trigger=True
        elif candidate=='budgeted_regime':
            impact=1000*p[h]*abs(day.tariff_regime.iloc[h]-future[h])
            trigger=(h==0 or h==12 or impact>=12.)
        else:raise KeyError(candidate)
        if trigger:
            pred=future[h:].copy()
            if candidate in ('hourly_global',):pred[0]=day.global_reconcile.iloc[h]
            elif candidate in ('hourly_regime','budgeted_regime'):pred[0]=day.tariff_regime.iloc[h]
            ch_plan,di_plan=lp_plan(pred,p[h:],e)
            plan_start=h;nsolves+=1
        c=float(ch_plan[h-plan_start]);d=float(di_plan[h-plan_start]);e=e+BAT['eta']*c-d/BAT['eta']
        n=float(truth[h]);grid=n+c-d
        kwh_cost=1000*(p[h]*max(0,grid)-BAT['feedin']*max(0,-grid))
        wear=BAT['wear']*(c+d)
        cost=kwh_cost+wear
        if not (BAT['emin']-1e-6<=e<=BAT['emax']+1e-6) or c>BAT['pmax']+1e-6 or d>BAT['pmax']+1e-6:
            raise AssertionError('Battery constraints violated')
        rows.append({'utc_timestamp':idx[h],'policy':candidate,'cost_usd':cost,'electricity_cost_usd':kwh_cost,
                     'wear_cost_usd':wear,'grid_import_mwh':max(0,grid),'grid_export_mwh':max(0,-grid),
                     'charge_mwh':c,'discharge_mwh':d,'energy_mwh':e,'replan':int(trigger)})
    if abs(e-BAT['e0'])>1e-6:raise AssertionError('Terminal SOC equality violated')
    return float(sum(r['cost_usd'] for r in rows)),nsolves,rows

def blocks_ci(diffs,block,seed,rep=2000):
    a=np.asarray(diffs,dtype=float)
    n=len(a)
    if n<2:return {'lower_95':None,'upper_95':None,'lower_97_5':None,'upper_97_5':None,'mean':None}
    rng=np.random.default_rng(seed);counts=int(np.ceil(n/block));x=np.empty(rep)
    for j in range(rep):
        starts=rng.integers(0,n,size=counts)
        take=np.concatenate([(np.arange(s,s+block)%n) for s in starts])[:n]
        x[j]=np.mean(a[take])
    v=np.quantile(x,[.0125,.025,.975,.9875])
    return {'mean':float(np.mean(a)),'lower_95':float(v[1]),'upper_95':float(v[2]),
      'lower_97_5':float(v[0]),'upper_97_5':float(v[3])}

def valid_days(z):
    # Use exactly the 2020 window predeclared; do not exclude on performance.
    a=z.loc['2020-01-01':'2020-09-30'].copy()
    req=['truth','hgb_components','direct','global_reconcile','tariff_regime','day_ahead']
    days=[]
    for dt,d in a.groupby(a.index.floor('D')):
        if len(d)!=24 or not d[req].notna().all().all():continue
        if not (d.index.to_series().diff().dropna()==pd.Timedelta(hours=1)).all():continue
        days.append((dt,d))
    return days

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--input',required=True);pa.add_argument('--out',required=True)
    args=pa.parse_args();ip=Path(args.input);out=Path(args.out);out.mkdir(exist_ok=True,parents=True)
    h=hashlib.sha256()
    with ip.open('rb') as f:
        for piece in iter(lambda:f.read(2**20),b''):h.update(piece)
    checksum=h.hexdigest()
    if checksum != PRESET_HASH:raise RuntimeError('Unexpected data checksum; validation protocol locked to original source')
    all_summaries=[]; all_stats=[];audit={}; hourly=[];daily=[];preds=[]
    for country in ['DE','GB']:
        print('COUNTRY',country,'fit on 2015-2018; calibrate 2019; validate 2020',flush=True)
        raw,scale=read_region(ip,country)
        z,cal=forecast(raw);testdays=valid_days(z)
        print('complete 2020 days',country,len(testdays),flush=True)
        if len(testdays)<100:raise RuntimeError('Too few complete test days')
        valid_index=pd.DatetimeIndex(np.concatenate([d.index.to_numpy() for _,d in testdays]))
        te=z.loc[valid_index]
        y=te.truth.to_numpy()
        for key in ['hgb_components','direct','global_reconcile','tariff_regime','day_ahead']:
            q=te[key].to_numpy();rmse=float(np.sqrt(np.mean((y-q)**2)));mae=float(np.mean(np.abs(y-q)))
            all_summaries.append({'country':country,'predictor':key,'rmse':rmse,'mae':mae,'n_hours':len(y),'n_days':len(testdays)})
        diff=(y-te.tariff_regime.to_numpy())**2 - (y-te.global_reconcile.to_numpy())**2
        bs=blocks_ci(diff,168,20261101)
        all_stats.append({'country':country,'type':'forecast_regime_minus_global_mse','n':len(diff),**bs})
        p=te.copy();p['country']=country;p['utc_timestamp']=p.index;preds.append(p.reset_index(drop=True))
        audit[country]={'scale_train_only':scale,'calibration':cal,'complete_2020_days':len(testdays),'test_hours':len(te)}
        for i,(dt,d) in enumerate(testdays):
            for policy in ['dayahead_lp','hourly_global','hourly_regime','budgeted_regime']:
                cost,ns,rows=evaluate_day(d,policy)
                daily.append({'country':country,'day':dt,'policy':policy,'cost_usd':cost,'n_lp':ns})
                for row in rows:row['country']=country;hourly.append(row)
            if i%40==0:print(country,'completed',i+1,'/',len(testdays),'days',flush=True)
    daily_df=pd.DataFrame(daily);hourly_df=pd.DataFrame(hourly)
    for c in ['DE','GB']:
        pivot=daily_df.query('country==@c').pivot(index='day',columns='policy',values='cost_usd')
        dif=pivot.hourly_regime.to_numpy()-pivot.hourly_global.to_numpy()
        all_stats.append({'country':c,'type':'control_hourly_regime_minus_hourly_global_usd_day','n':len(dif),
                          **blocks_ci(dif,14,20261102)})
        costs=daily_df.query('country==@c').groupby('policy').agg(total_cost_usd=('cost_usd','sum'),n_lp=('n_lp','sum'))
        for pol,vals in costs.iterrows():
            all_summaries.append({'country':c,'policy':pol,'total_cost_usd':float(vals.total_cost_usd),'total_lp_calls':int(vals.n_lp),'n_days':int(len(pivot))})
    manifest={'sha256_input':checksum,'preregistered_name':'TRSR-BR','scope':'2020-01-01 through 2020-09-30 held-out','countries':audit,
              'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'lightgbm':lightgbm.__version__},
              'n_hourly_ledger_rows':len(hourly_df),'n_daily_policy_rows':len(daily_df)}
    pd.DataFrame(all_summaries).to_csv(out/'summary.csv',index=False)
    pd.DataFrame(all_stats).to_csv(out/'predeclared_statistical_tests.csv',index=False)
    pd.concat(preds,ignore_index=True).to_csv(out/'forecast_predictions_2020.csv',index=False)
    daily_df.to_csv(out/'dispatch_daily_2020.csv',index=False)
    hourly_df.to_csv(out/'dispatch_hourly_ledger_2020.csv',index=False)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,default=str))
    # Verify aggregation and ledger consistency for every daily cost and exact daily SOC reset.
    cmp=hourly_df.groupby(['country',hourly_df.utc_timestamp.dt.floor('D'),'policy']).cost_usd.sum().reset_index(name='ledger_cost')
    base=daily_df.copy();base['day']=pd.to_datetime(base.day,utc=True)
    comp=base.merge(cmp,left_on=['country','day','policy'],right_on=['country','utc_timestamp','policy'],validate='one_to_one')
    assert len(comp)==len(base)
    assert np.max(np.abs(comp.cost_usd-comp.ledger_cost))<1e-5
    assert not hourly_df.isna().any().any()
    print('FINAL METRICS',pd.DataFrame(all_summaries).to_string(index=False),flush=True)
    print('FINAL STATS',pd.DataFrame(all_stats).to_string(index=False),flush=True)
    print('validated ledger entries',len(hourly_df),flush=True)

if __name__=='__main__':main()

