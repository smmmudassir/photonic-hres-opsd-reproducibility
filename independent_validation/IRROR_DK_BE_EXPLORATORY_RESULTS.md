# IRROR independent DK/BE 2020 validation: exploratory outcome

**Lock commit:** `79e57a40c5de4dc6c009da7e488bab010ebffe88` (protocol committed before execution).

**Execution deviation:** Frozen source (`c9336ec1257c79927bb6a0c1f4491aee0f460468607f606730de437263d005ff`) stopped on Belgium because its calibration-size assertion required over 3000 complete samples. A one-line patched version relaxed that **assertion only** to 1800 and was rerun. This makes the published numbers **exploratory, not clean preregistered confirmation**. Both exact source versions, all outputs and the hourly ledger are in the downloadable research package supplied with the ChatGPT response. The 2020 test period has now been used; it must never be described as fresh for subsequent model revisions.

## Forecasting
| Region | 2020 test observations | HGB RMSE | Interferometric residual RMSE | Lag-1 persistence RMSE | Selected shrinkage |
|---|---:|---:|---:|---:|---:|
| DK | 6569 | 0.061145 | **0.060508** | 0.107782 | 0.25 |
| BE | 4406 | 0.130958 | **0.128089** | **0.106112** | 0.75 |

IRROR−HGB paired MSE, 168h-block bootstrap (2,000 resamples), 95% CI: DK −0.00007749 [−0.00010371, −0.00005453]; BE −0.00074328 [−0.00115607, −0.00040689]. Belgium's lag-1 persistence beats both learning methods.

## Simulated closed-loop battery dispatch
| Region | Complete 24h days | Seasonal-forecast LP cost USD | Matched 6h-HGB LP USD | Matched 6h-IRROR LP USD |
|---|---:|---:|---:|---:|
| DK | 273 | 763254.72 | 762364.49 | **762356.27** |
| BE | 107 | 161394.40 | 160586.87 | **160566.71** |

Incremental IRROR−HGB cost/day and 7-day-block 95% CI: DK −$0.03013 [−$0.05705, −$0.00922]; BE −$0.18840 [−$0.39637, +$0.01039]. The **two-country demonstrated control superiority criterion FAILED** because Belgian CI crosses zero. Overall gains are tiny relative to annual-scale costs.

## Scientific interpretation
Software cosine interferometric random features + ridge residual readout and reoptimized constrained battery LP. No physical optical chip or measured photonic advantage; no local Hyderabad/Vizag metered resource/load trace; no claim of global algorithmic first or publication readiness. Input: official OPSD 2020-10-06 time-series file SHA256 `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`. No further 2020 tuning should be used as independent confirmation.
