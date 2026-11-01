# GPI-MPC — prospective-to-analysis pretest record (2026-11-01)

## Scope and nonclaims
Computational **gauge-invariant interference residual + safe grid-cap battery LP**. No fabricated photonic hardware, no measured energy/speed advantage, no assumption of performance superiority.

Data: official OPSD `time_series_60min_singleindex.csv`, user-supplied, 2020-10-06 release. Only **Austria (AT)** and **Czechia (CZ)** national series, not previously evaluated in earlier conversation. Raw load, solar generation and onshore wind. We will not use year 2020 for fitting preprocessing, residual weights, calibration, selection, control-scenario parameters, early stopping or hyperparameters. Training 2015–18; model selection+error calibration 2019; **locked confirmation 2020-01-01 through 2020-04-30**, selecting complete UTC calendar days. Historical holdout, not real-world forward-time validation.

## Method
Target: *day-ahead hourly* net-load (hourly load minus solar minus wind) in country-normalized units. At 00:00 UTC of target day, all lags 24,48,72,168,336 hours have been observed. No contemporaneous or future actual inputs. Normalize by load 99.5th percentile of 2015–18. Fit LightGBM (260 trees, learning rate .045, 24 leaves, min leaf 40, L2=3). Two out-of-fold 2017/2018 LightGBM residual windows train the phase-residual model. 2019 used only for selecting residual ensemble shrinkage among 0,0.25,0.5,1 and early stopping (max 38 epochs).

Novel *candidate* mechanism: two-reference co-phased quadrature interference, shared 3x24 trainable phase mixer, and learned electronic residual readout. Relative phases between lag-24/lag-48 and lag-24/lag-168 cancel any common phase disturbance by construction. Three fixed random seeds 13,37,73; average predictions. Physically meaningful ablations: random frozen phase matrix and single-branch nonreferenced cosine/sine encoding with same number of outputs. Gauge effect explicitly compared; exact digital equivalent has equal outputs, not an inferior photonic baseline. Jitter regularizer .005 is a modelled independent-branch Gaussian noise (c3=.12rad), not physical chip testing.

## Dispatch scenario (same solver for all methods)
Day-ahead 24-hour perfect price-knowledge LP, 2 MWh normalized battery, 0.75 MW power, efficiency 95%, SOC 0.3–2 MWh, start/finish SOC 1 MWh each UTC day. Grid import cap set to training 2015–18 **90th percentile net load**. Hourly 110/180/300 USD/MWh time-of-use import tariff; export credit 55; wear 15 USD/MWh throughput; load-shedding penalty 4000 USD/MWh; synthetic tariffs and network cap, NOT measured country retail or engineering sizing. Solar/wind normalization is a scenario scaling, not historical physical microgrid. Schedule optimized on predictions, settled against actual net-load with grid-cap recourse. Include perfect-foresight LP as unattainable lower bound. Hourly full-cost ledger.

Additional locked risk control: positive 85th quantile of 2019 base model errors separately for each UTC hour, multiplied by fixed factor 0.60 and added to predictions, both for LightGBM and gauge model. This *forecast buffer* is an engineering safety margin, not a statistically guaranteed conformal set.

## Predeclared superiority gates
A. **Forecast:** gauge ensemble beats LightGBM and fixed-phase under mean 2020 RMSE in **both countries**, with 7-day-block bootstrap difference in squared error negative upper 95% confidence bound in both.
B. **Control:** gauge_risk beats matched `LightGBM_risk` AND unbuffered LightGBM on average held-out daily total cost in both countries, with paired 7-day moving-block bootstrap upper 95% CI < 0 for both.
C. **Ablations:** gauge beats frozen mixer and noninvariant matched feature bank on forecasting AND gauge-perturbed output (quantify phase change); any mechanism-specific superiority claim requires clean-data ablation improvement beyond invariance alone.
D. **Correctness:** no SOC/power/energy-balance violations under the model, full hourly ledger reconciles to daily costs to <=1e-6, exact gauge-invariance test <=1e-5, no 2020 data touched before lock.

If ANY required gate fails, do not claim superiority. No retuning or reselection on 2020. Statistical intervals are exploratory under synthetic control and short four-month period; even significant findings cannot prove global novelty or hardware energy advantage. A comprehensive literature comparison is required before novelty assertions.