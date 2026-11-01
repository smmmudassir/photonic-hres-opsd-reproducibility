# GAUDL-PQR on the independent Ausgrid 2012–2013 calendar holdout (negative confirmation)

**Protocol was committed before reading 2012–13 test targets:** [preregistration](https://github.com/smmmudassir/photonic-hres-opsd-reproducibility/blob/main/independent_validation/GAUDL_PQR_AUSGRID_2012_2013_PREREGISTRATION.md), commit `fa3b3cff53cbb0e50838051fd5075cf83a583fce`.

**Source:** user-supplied original Ausgrid 300-home archive, SHA-256 `5a766f52b6c8b3b72730380f4422e478934bc94640a4b089dd0e0e3c055c5d82`. Five fixed home IDs (12,32,44,78,101); 85 dates per home, July 8–Sept 30, 2012 (425 household-days). Measured half-hourly GC/GG meter data, synthetic battery cost tariff. This is not Hyderabad/Vizag field data. 2010–12 used for base training, residual learning, conformal-like Gaussian scaling and control-grid calibration.

## Frozen three-seed mean outcome
| Method | 48-slot net-load RMSE (kW) | Battery settled modeled cost (USD/home-day) |
|---|---:|---:|
| Strong refitted LightGBM | **0.495577** | **1.500651** |
| Base LightGBM | 0.503877 | 1.513982 |
| Matched digital residual | 0.513930 | 1.553643 |
| Trainable relative-phase residual | 0.516039 | 1.553485 |
| Frozen-phase residual | 0.515989 | 1.553428 |
| Single-arm/noninvariant residual | 0.515085 | 1.547527 |

Matched phase–digital realized cost difference = −$0.000157/home-day (−0.010%); paired calendar-day 7-day circular-block bootstrap 95% CI [−$0.002851,+$0.001972], includes zero.

Phase–strong LightGBM = **+$0.052835/home-day** (+3.52%), 95% CI [+$0.032054,+$0.072417], strong digital baseline superior.

Phase–fixed phase = +$0.000058/day, 95% CI [−$0.000192,+$0.000291], trainable optical mixing did not help.

Phase–single-arm = +$0.005958/day, 95% CI [+$0.002698,+$0.009660]; the noninvariant ablation is less costly.

**The primary superiority and physical-mechanism gates FAILED.** Do not claim superiority or global priority. Phase architecture is computational and has a mathematically equivalent digital implementation; no chip results exist.

## Disclosed execution deviation
The full monolithic frozen runner exceeded individual tool execution time. We used the additional `complete_locked_eval.py` execution-only resumptions, loading previously saved weights and training remaining seeds with **unchanged source training functions and hyperparameters**. This helper script was authored after test access; the limitation is documented instead of describing the full run as an unmodified pristine executable. Frozen original `residual_study.py` source SHA256: `4870103fb4778bceaa0e5d335f884a054295e5a6dfc2309da3c2476629b1c6ae`. No test-informed coefficient or model tuning was made.

All 12 seed-level model checkpoints, forecast metrics, predictions, per-home-day ledgers, 3,000-replicate paired bootstrap, source code and report are supplied in the accompanying 5.2MB ZIP downloadable through the conversation. The original Ausgrid archive is not redistributed.

**This validation has consumed the 2012–13 confirmation period. Further modifications to optimize on this test are exploratory only, and require an independently frozen new dataset for renewed confirmation.**