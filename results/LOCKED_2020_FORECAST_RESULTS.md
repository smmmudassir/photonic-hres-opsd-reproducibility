# Locked historical 2020 validation — forecasting results (2026-11-01)

## Provenance and protocol
The preregistration, `locked_validate.py`, requirements and input SHA256 were publicly committed **before the first 2020 evaluation**. The predeclared primary forecasting result did not satisfy the two-country success criterion. No models were retuned on 2020.

- Original data SHA256: `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`
- 2015–2018 train; 2019 calibration; Jan–Sep 2020 locked test.
- 2020 labels first used after the lock. Strictly this is preregistered **retrospective** validation, not live future forecasting.
- The exact predeclared test driver timed out during its computationally demanding hourly dispatch optimization. Forecast results were then generated with a separate `forecast_only.py` evaluation script invoking the *identical frozen forecasting, valid-day and bootstrap functions* from `locked_validate.py`. This is documented as an execution deviation; no parameter was changed. The control endpoint remains **NOT VALIDATED**.

## Frozen forecasting results
| Country | Complete days | Hours | HGB component RMSE | Direct LightGBM RMSE | Global reconcile RMSE | Tariff-regime reconcile RMSE | Day-ahead RMSE |
|---|---:|---:|---:|---:|---:|---:|---:|
| Germany | 274 | 6576 | 0.03504411 | 0.03727864 | **0.03232434** | 0.03232642 | 0.22574678 |
| Great Britain | 273 | 6552 | **0.09043381** | 0.10210596 | 0.09293362 | 0.09135335 | 0.31515076 |

### Locked bootstrap analysis (168-h moving-block, 2000 replicates)
Difference is tariff-regime minus global reconcile **squared error** (negative is favorable):

| Country | Mean difference | 95% confidence interval | 97.5% sensitivity interval |
|---|---:|---|---|
| Germany | +0.00000013453 | [−0.00000051283, +0.00000082884] | [−0.00000058320, +0.00000096290] |
| Great Britain | −0.00029122201 | [−0.00055220345, −0.00010328405] | [−0.00060634258, −0.00008510786] |

**Predeclared success criterion FAILED.** In Germany, the difference is negligible and confidence intervals contain zero. In Great Britain, the regime model improves on global reconciliation, but it still does not beat the individual component HGB model. There is no established cross-country superiority or distinctiveness relative to stronger alternatives.

## Research integrity / remaining tasks
1. The locked control endpoint has not been evaluated because the full hourly optimization exceeds the current execution time limit. It must not be reported as positive, negative or significant.
2. The run used synthetic tariffs and a normalized microgrid representation, not measured hardware economics.
3. The method is digital ensemble reconciliation, not a photonic neural architecture; do not claim measured optical energy or latency.
4. A globally novel contribution has NOT been established against the forecasting and event-triggered MPC literature.
5. The failed predeclared two-country hypothesis must remain visible. Future revisions need a **new dataset and another locked test**, rather than re-labeling 2020 as a fresh holdout.
