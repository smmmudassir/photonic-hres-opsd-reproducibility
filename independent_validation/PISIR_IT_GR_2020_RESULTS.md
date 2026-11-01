# PISIR IT/GR 2020 — locked confirmation outcomes

**Preregistration before 2020 evaluation:** commit `87897ad49e625a5ba179f45762358f13cd91181e`. **Code+input SHA precommitted:** `f1536f5d2e79926a9eded787ed3092b8609e5e7e`.

## Proposed mechanism
PISIR — Phase-Innovation Self-Referenced Interferometric Readout — digitizes phase differences between current and electronically buffered 24h-prior samples using simulated balanced I/Q ports (80 virtual channels). Ridge residual corrects a histogram-gradient-boosting prediction; parameter selection uses 2019 only. **Software simulator, not actual optical hardware.** Exact digital implementation gives equal predictions.

## Confirmatory 2020 one-hour normalized net-load RMSE
| Model | IT | GR |
|---|---:|---:|
| PISIR | 0.029127 | 0.032591 |
| Histogram boosting | 0.029168 | 0.032591 |
| LightGBM | **0.028714** | 0.032878 |
| XGBoost | 0.029505 | **0.031959** |
| Lag-1 persistence | 0.098759 | 0.086978 |

n=6568 test hours in each country. IT PISIR vs HGB MSE difference -2.367e-6, 168h block-bootstrap 95% CI [-3.910e-6,-0.868e-6]; IT vs LightGBM +2.391e-5, CI [+9.082e-6,+3.770e-5]; GR PISIR vs HGB difference is exactly 0.

## Ablations
- IT PISIR improves on no-coherence and single-quadrature ablations but not on instantaneous-phase features at the prespecified significance level.
- GR's 2019-selected residual weight is **zero**, meaning PISIR and all optical ablations exactly equal HGB. Physical mechanism has no demonstrated effect here.
- 8-bit quantization and simulated phase noise have negligible incremental effect, but cannot prove physical feasibility or power/speed benefits.
- Exact digital equivalent reproduces PISIR; no digital-vs-optical accuracy superiority is claimed.

## Decision
**Predeclared joint two-country superiority gate FAILED.** This does not validate a new superior photonic learning-and-control system. No new battery-control simulation or chip experiment was run. The 2020 holdout is now used. Full frozen executable, prediction rows, exact statistical CSVs and protocol are supplied in the downloadable experimental archive in the corresponding ChatGPT conversation.
