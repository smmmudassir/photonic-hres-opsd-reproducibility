# GAUDL-PQR: frozen independent-year confirmation, 2026-11-01

## Motivation and research status
The first exploratory 2011–12 evaluation showed a phase-feature controller may reduce realized cost against a matched digital residual but does not outperform a strong LightGBM trained on all available past data. The fixed-phase ablation nearly ties the trainable model. **Positive novelty/superiority is not established**. This protocol documents a genuinely untouched *later-year* test before its targets are read.

## Data provenance and protection
- User-supplied original Ausgrid 300-home archive: `Ausgrid_solar_home_data.zip`, SHA-256 `5a766f52b6c8b3b72730380f4422e478934bc94640a4b089dd0e0e3c055c5d82`.
- Only customer IDs 12, 32, 44, 78 and 101, selected using 2010–2012 metadata and absence of a CL meter (GC + GG only). Not a random or nationally representative cohort. Metered GC and GG are kWh per half-hour, multiplied by two to average kW. Solar-home data were measured near Sydney, *not* Hyderabad or Vizag.
- Chronological sources: base LightGBM on July 2010–June 2011; residual conditional-density phase and matched digital learners on July 8, 2011–Feb 29, 2012; Gaussian scale calibration Mar–Apr 2012; controller correction and risk coefficients calibrated only May 1–14, 2012.
- **Final held-out test: July 8–September 30, 2012, same five homes**, without missing-value imputation. The entire 2012–13 file is not parsed until this protocol and source SHA-256 have been committed to public GitHub. This is a calendar shift on the same metered homes, not an independent household cohort.
- The earlier single-home GAUDL preregistration for April–June 2012 is superseded for this **new** model; its prior holdout is treated as explored developmental data, not clean confirmation.

## Frozen model and hypotheses
- Proposed `phase`: trainable 16-channel two-arm relative-phase quotient `cos((a-b)W+b),sin(...)`, Gaussian residual mean/standard deviation over common LightGBM forecast, CRPS + differentiable dispatch-regret proxy + noise-stability penalty.
- `digital`: matched 16-channel, 2-layer residual MLP feature projection, **identical Gaussian and regret learning objective** and controller.
- `fixed`: same phase features with frozen mixing W; `single`: non-invariant single-arm phase control.
- Three seeds **13, 29, 47**, 22 epochs, AdamW lr .002, weight decay .001, 48-width hidden layers, Gaussian scale floor .05, correction bound .55 kW. No checkpoint selection using 2012–13 observations; all seeds must be reported.
- Base LightGBM 250 estimators 15 leaves; independent strong benchmark LightGBM with 350 estimators fitted to July 2010–June 2012. No changes to features, house selection, architecture, seeds, or year after confirmatory inspection.
- Forecast risk calibrated as 90th percentile absolute standardized residual / 1.64485, clipped to [0.25,4], using Mar–Apr 2012 only; controller grid over correction shrink {0,.5,1} and risk margin {0,.5} selected using May 1–14, 2012 realized battery cost per model and seed.
- 48-step day-ahead LP: 6 kWh battery, 2 kW charge/discharge, 0.95 efficiencies, 15–90% SOC, both initial and terminal SOC 50%, synthetic tariff $0.10/$0.20/$0.32 per kWh, export $0.05/kWh, battery wear $0.015/kWh of throughput. No Australian retail-bill claim, no measured chip energy/latency claim. Each policy settles against held-out actual net load under identical LP.
- **Primary confirmatory superiority gate**: proposed phase model has ≥1% lower average daily total operating cost across five homes and three seeds than **both** matched digital and strong refit LightGBM, with household-date paired 7-day-block bootstrap (2,000 reps, seed 90210) 95% CI for the phase minus comparator cost entirely <0. Primary gate fails if either comparator fails.
- **Mechanism gate**: phase also must improve the actual cost over fixed-phase and single-arm ablations, with same block-bootstrap CI <0; otherwise phase learning / gauge invariance is not the reason for observed gain.
- Report RMSE, MAE, 90% conditional Gaussian interval coverage, and CRPS; all metrics in native household kW. Coverage outside 0.85–0.95 is a calibration warning. Report distributional calibration along with cost whether positive or negative.
- Safety gate: no simultaneous charging/discharging; SOC inside limits. Physical optical hardware is not evaluated. A numerically exact digital emulation of the phase model cannot be outperformed on prediction accuracy by the same model evaluated digitally.

## Research-integrity decision
A failed result remains public. Do not optimize or retune on this holdout and call the same period a new independent test. Further tuning after 2012–13 makes it exploratory; new independent homes/years must be reserved before subsequent claims. The method is a **novelty candidate**, not an established first-ever global invention. Prior decision-focused learning, chance constraints and photonic relative-phase embeddings are explicit comparators.

## Source lock SHA-256
- `src/cohort_data.py`: `38625eb8dbd05d45836387da4f3da70065bc49af54221d5e33f001dce2da2ef3`
- `src/experiment.py`: `e46e257d65bb902a9666a9543f46a5f4c4072ee5c98d80f21c940a67f322e5a8`
- `src/residual_study.py`: `4870103fb4778bceaa0e5d335f884a054295e5a6dfc2309da3c2476629b1c6ae`