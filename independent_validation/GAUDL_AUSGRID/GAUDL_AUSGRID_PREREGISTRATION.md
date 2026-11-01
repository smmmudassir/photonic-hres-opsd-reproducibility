# GAUDL locked independent-data evaluation protocol

**Freeze status:** model, loss, evaluation design and source-code checksums are fixed before access to the April–June 2012 evaluation labels. A successful forecast or control result is NOT assumed.

## Scientific hypothesis
GAUDL (Gauge-invariant, uncertainty-aware differentiable dispatch learning) maps causal previous-day and previous-week solar/load measurements through a trainable relative-phase interferometric feature bank, outputs the **Gaussian conditional distribution of 48 successive half-hour net-load values**, and optimizes the sum of proper CRPS and a differentiable battery-regret *surrogate*. Matched digital MLP receives the same causal measurements, has at least as much representation capacity, and uses the **identical** loss, parameter-selection rules and battery LP at evaluation.

The proposed contribution is the specific symmetry-constrained probabilistic/decision-focused coupling. Photonic hardware, computational speedups, energy savings or global priority are NOT claimed. Exact digital emulation of this model is possible.

## Independent dataset and no-leakage boundary
- Publisher of original measurements: Ausgrid, NSW, Australia (gross PV generation `GG` and general electricity consumption `GC`, half-hourly meters; independent of all earlier OPSD national data).
- Reuse: Pierre Haessig, `solarhome-control-bench`, `data/data_2011-2012.csv`, public source https://github.com/pierre-haessig/solarhome-control-bench/blob/master/data/data_2011-2012.csv.
- Exact Git blob SHA-1: `1e940b59fb16402d1007541d99fd7dc4f7f78200`; executable verifies before opening labels. This is a curated household series and *not* a separate random cohort of 300 customers.
- Training: from July 2011 through **2012-02-29**. Only prior-day and prior-week measured variables, and future-known calendar variables, are predictors.
- Validation and conformal sigma calibration: **2012-03-01 to 2012-03-31**.
- Locked independent test: **2012-04-01 to 2012-06-30**; no testing or hyperparameter tuning against those target values before commit.
- Original GC and GG are 30-minute energy in kWh and multiplied by 2 for average kW. No rescaling the original PV system to a fictitious size. Units and dataset time zone must be explicitly disclosed.
- The source's time-index integrity is checked; any failure to parse or unexpected missing values halts evaluation. There is no unregistered test-data cleanup.

## Fixed model, training and controller
- Three fixed seeds [13,29,47]; 24 trainable relative-phase I/Q channels, 40 hidden units, default 20 training epochs, AdamW LR 0.002 and batch 16. Model selection uses validation CRPS only. Loss = Gaussian CRPS + 0.12 × differentiable dispatch-regret surrogate per 48 slots.
- Matched digital MLP trained end-to-end with the **same** CRPS+surrogate objective and identical optimizer/epochs, and a larger digital projection to avoid giving the photonic-inspired model an artificial parameter-count advantage.
- Other registered ablations: frozen phase mixing (`frozen`), single-arm/noninvariant phase features (`single_arm`), and gauge invariant without dispatch regret (`gauge_no_regret`). No training against test labels.
- 90% Gaussian predictive interval widths are multiplied by a validation-only normalized-residual factor; no claim of distribution-free finite-sample conditional coverage.
- Hourly synthetic 3-tier tariff: [0.10,0.20,0.32] USD/kWh; export credit 0.05 USD/kWh; battery 6 kWh, 2 kW, 95% charge/discharge efficiencies, SOC 15–90%, fixed initial and terminal SOC 50%, wear 0.015 USD/kWh of charge+discharge. These are **illustrative** economic counterfactuals, not Australian electricity bills.
- For every method, risk margin α selected on validation from [0,0.5,1.0], then fixed for test. Evaluation solves identical 48-slot constrained linear programs using SciPy HiGHS. Simultaneous charge/discharge is monitored and reported.
- No model is replaced, and no seed is dropped, based on test outcome.

## Predeclared primary success gate
Mean actual settled **daily battery operating cost** for GAUDL must be **≥1% lower** than the matched digital decision-focused learner, averaging the three seeds on the same test days; paired *seven-day circular block bootstrap* 95% CI (3,000 resamples, seed 90210) for GAUDL−digital cost must lie entirely below zero. The full hourly/test-day loss is reported, whether successful or not.

## Predeclared physical-ablation and forecast gates
- GAUDL should also improve settled cost over **each** of frozen, single-arm and GAUDL-without-regret ablations; otherwise the mechanism-specific benefit is not established.
- Report RMSE, MAE, Gaussian CRPS and 90% coverage for all models; coverage outside [0.85,0.95] or CRPS more than 3% worse than the digital counterpart is a separate model-quality warning.
- The common optical-phase invariance test must pass within float32 tolerance ≤2×10^-6 under a shared shift of 0.1→2.5 radians; this tests mathematical software symmetry, **not** chip robustness.
- Perfect-foresight LP is an unattainable lower-bound comparator, used only in retrospective evaluation; not allowed in training or controller selection.

## Decision rule
If any gate fails, report a **negative, inconclusive or mixed finding** without revising this registration or seeking superiority through test-set retuning. All prior OPSD holdouts are treated as used. Publish exact commit and SHA256, environment, seed scores, CSV ledgers, confidence intervals, and any code/data deviations. New claim of full originality still requires broader prior-art assessment and replication beyond one selected household.

## Source SHA-256 at protocol freeze
- `src/gaudl.py`: `3dbecfa328fdeeb11609a4e2870e51688bccae3163dac787c4e778e9578c884d`
- `src/run_study.py`: `d8f85186c03832503c9a10eb49401c4e7de0b953674203d0eb9f0f5050adb541`
- `requirements.txt`: `7f26bfa0c3e34cbbd2841a67b7c71c741901607e537813d87b050c6fcaa1d077`

**Status at authoring:** independently collected Ausgrid real test series has been identified publicly, but its file has not been downloaded successfully in this runtime. No real test or statistical superiority result exists yet.