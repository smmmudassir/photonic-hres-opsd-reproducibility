# Frozen FR–ES evaluation protocol: coherent two-delay readout (CDIR)

Lock date: 2026-11-01 (source commit precedes the first FR/ES 2019 test execution). The uploaded official OPSD `time_series_60min_singleindex.csv` is used with SHA256 `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`.

## Prior exposure and limits of novelty
FR and ES were **not** among the DE/GB/DK/BE model evaluation countries used in the earlier discussion. This is a new country-specific 2019 *historical* holdout from the **same existing OPSD dataset**, not an independent data-collection source or future physical deployment. Photonic delay feedback and coherent readout have earlier publications; this work tests a **specific passive two-delay + ADC + detector-noise virtual optical field model** as a residual expert in forecasting-assisted battery optimization. It must not be represented as novel hardware or the first delay reservoir.

## Preregistered architecture and experiments
- Target: normalized 1-hour-ahead microgrid net demand using France/Spain national actual load/PV/wind profiles scaled from training years only. These are **regional proxy mixtures** for a hypothetical 1.2 MW load, 0.75 MW PV, and 0.75 MW wind, NOT local plant recordings or actual dispatch.
- Training: 2015–2017. Residual calibration: Jan–Jun 2018; shrinkage selection: Jul–Dec 2018. **Locked evaluation: calendar 2019**. Report valid rows and missingness; no filtering based on model error. Causal lags 0,1,2,24,48,168. No future meteorological data.
- Digital baseline: histogram gradient boosting (180 iterations, 23 leaves, rate .06), LightGBM (260 trees, 22 leaves), persistence (1-hour and seasonal 24-hour).
- Optical virtual device: 48 channels, complex coherent field with amplitude returns from i−1 (0.35, phase 0.37) and i−24 (0.18, phase −0.71), injected fraction 0.47; balanced homodyne real-valued difference; fixed Gaussian phase encoder; independent detector noise std .004 in normalized balanced signal and 8-bit ADC clipping on [−4,4]. State is passive/bounded for unit-amplitude optical injection. The virtual input clock maps successive hourly samples to recurrence steps; it is *not* an actual one-hour optical delay. No device calibration, optical component energy, power consumption, laser noise, or measured latency can be inferred.
- Readout: ridge residual fit on Jan–Jun 2018 using regularization 250; scale from [0,.1,.25,.5,.75,1] minimized on Jul–Dec 2018. Same fitting and tuning for double-delay, no-delay coherent, ideal-noiseless, and matched digital Fourier features. All results—including null effects—reported.
- Fair model comparison: same country labels, feature lags and test timestamps; 2019 net-load RMSE and MAE. 168-hour paired moving-block bootstrap of squared-error differences (1,600 draws). No tuning on 2019.
- Controller: common fixed 1.8 MWh battery model, [0.3,1.8] MWh SOC, 0.75 MW power, 95% efficiencies, synthetic USD/MWh tariff 110/180/300 and 55 export credit, 15 USD/MWh battery-throughput charge, same initial and terminal 1.0 MWh per day. Compare seasonal-day LP, HGB every-6h LP and coherent-forecast every-6h LP. 7-day moving-block bootstrap of paired daily costs; exact hourly ledger, balance audit and unit tests. No physical plant claims.

## Predeclared primary hypothesis and success criterion
**Forecast primary**: two-delay noisy coherent residual is better than HGB on **both FR and ES**, with the 95% moving-block-bootstrap upper CI of the *MSE difference* below zero in each, AND beats matched digital Fourier and no-delay coherent features. Other baselines (LightGBM/persistence) must be reported, even if stronger.

**Control co-primary**: coherent forecast 6h dispatch costs less than matched HGB 6h dispatch with upper 95% CI below zero in **both countries**. Seasonal LP is secondary. Success is **not** established merely by a point improvement or improving in one region. No post-2019 modification will be presented as the same locked test.

**Physical feasibility gate**: field amplitude bound and detector quantization must hold. A positive simulation does *not* demonstrate hardware acceleration, photonic energy/latency advantage, or optical device feasibility absent realistic calibration and measurement.

## Analytic caveats
- Synthetic tariffs and arbitrary national-to-1MW normalization limit external validity.
- Training/calibration dates fixed before test, but the researcher's prior use of the same OPSD *data product* in different countries reduces genuine independence; we explicitly disclose this.
- The 2019 target was not inspected before code and protocol commit. A broken executable may be repaired solely with recorded code diff; any changes after test exposure require labelling exploratory.
- A selected favorable gain cannot establish globally new algorithms. Novelty requires comparison against delay reservoirs and task-aware MPC literature, plus hardware experiments for physical claims.