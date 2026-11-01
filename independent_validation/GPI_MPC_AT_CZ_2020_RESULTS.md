# GPI-MPC Austria/Czechia held-out 2020 confirmation (2026-11-01)

Protocol pretest commit: `9dd475b074022e3abd4ac0337b66259ba0c4314d`. Source SHA-256 pretest commit: `eb4632795954f94a3945adfd8ae4f2666a71532d`. Source hash: `6a91aff09d4f6a4770bfcca013d5efc435ac463301517e60f95477d4c88381ac`. Input SHA: `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`.

**Test:** 2020-01-01 through 2020-04-30, 2,904 hours / 121 complete UTC days per nation. Development trained through 2018; validation, residual shrinkage and risk-margin calibration used 2019. Pretest scope is a historical holdout, **not prospective field deployment**.

## Forecasting normalized net-load RMSE

| Model | AT | CZ |
|---|---:|---:|
| Digital LightGBM | 0.089222 | 0.038402 |
| Trainable gauge-invariant dual-reference features | 0.088576 | 0.038386 |
| Frozen-phase ablation | 0.089222 | 0.038394 |
| Noninvariant ablation | **0.088144** | 0.038402 |
| Digital LightGBM with risk buffer | 0.105851 | 0.045942 |
| Phase model with risk buffer | 0.104575 | 0.045919 |
| 24h seasonal persistence | 0.121135 | 0.070637 |

## Simulated battery net costs (USD, illustrative tariff and country-normalized power)

| Controller | AT | CZ |
|---|---:|---:|
| Unbuffered digital LightGBM | 406,862.96 | 440,425.28 |
| Unbuffered phase features | 408,738.87 | 440,360.86 |
| Digital with identical risk buffer | **366,493.35** | 421,199.21 |
| Phase with risk buffer | 367,943.91 | **421,154.78** |

**Matched risk-buffer comparison** (phase minus digital): AT +$1,450.55 total / +$11.99 per day, 95% 7-day-block CI [+4.10,+19.92]/day; CZ −$44.43 total / −$0.37 per day, CI [−5.27,+3.64]/day. **Two-country control superiority criterion failed.** Risk buffering does improve this simulated objective in both countries, but does not establish any added phase-feature control advantage.

## Physical-mechanism test and limitations

Common-phase shift changed invariant model output by at most ~3e-8 in float32. Noninvariant ablation changed by as much as ~0.225. This verifies gauge invariance numerically but not predictive superiority: AT noninvariant is more accurate. The exact phase algorithm can be implemented digitally. No photonic chip experiment, latency, power or energy advantage is measured.

The battery optimizer uses a fixed synthetic tariff, 2 normalized MWh / 0.75 MW storage, 95% efficiency, grid-cap constraint and load shortage penalty. Results are **not real Austrian or Czech electricity bills**, and normalized load is not a physically scaled local microgrid. Complete runnable code, preregistration, hourly audit ledger, daily dispatch, confidence intervals and draft paper are in the accompanying downloadable ZIP; they are not yet all uploaded into this GitHub repository.

**Conclusion:** mathematically valid invariant representation and executable risk-control pipeline; superior novel photonic learning-and-control system NOT demonstrated. Do not claim publication-ready algorithmic or hardware breakthrough. 2020 AT/CZ data are now used and must not be retuned as a fresh holdout.
