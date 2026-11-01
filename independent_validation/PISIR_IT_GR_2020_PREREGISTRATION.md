# PISIR: Phase-Innovation Self-Referenced Interferometric Readout — frozen 2020 validation

**Date frozen:** 2026-11-01, before reading either Italian or Greek **2020** forecast error or target data beyond availability/coverage metadata. **2019 development results were inspected before freezing** and are not confirmatory.

## Scientific question
Does phase-diverse balanced coherent interference between two electronically buffered, phase-encoded versions of the present state and preceding daily state add predictive information that survives matched digital baselines and removal of its physical interaction? This is a simulated physically inspired candidate, not hardware or a demonstration of global novelty.

## Locked dataset and protocol
- Input: OPSD time_series_60min_singleindex.csv v2020-10-06, SHA256 `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`.
- Two previously untested national series: Italy (IT) and Greece (GR).
- Primary target: 1h-ahead **normalized load less normalized solar**, `1.20*load/load_train_median - 0.75*solar/solar_train_p99`. Wind not included, as neither relevant national top-level series contains wind-generation measurements in this release.
- Predictor lags 0, 1, 2, 24, 48, 168 hours, plus causal clock covariates. Drop missing examples. Fit all scaling to 2016–2018 training observations only.
- Training: 2016–2018; ridge residual calibration: Jan-Jun 2019; residual-weight selection: Jul-Dec 2019; **locked confirmation:** 2020-01-01 through 2020-09-30.
- Reference implementation and all tuning settings are frozen in `frozen_experiment.py` (source SHA256 `80d721ec95e66a5f3f70b5aa528661c6bd22c1dd91d748292840ec9e8112a821`). No parameter edits or additional selection after viewing test results.

## Physical mechanism
80 virtual optical phase carriers, two balanced I/Q receiver ports per carrier, and electronic 24h lag storage; synchronous phase modulation produces `Δφ = φ(x_t) − φ(x_{t−24})`, receiver gives `cos(Δφ), sin(Δφ)`. No 24h *optical* delay is asserted. A hardware-plausible 8-bit ADC and zero-mean phase perturbation 0.018 rad are simulated, but never treated as measured optical properties.
A trained ridge residual modifies a fixed hist-gradient-boosting forecast, with residual shrinkage selected exclusively on 2019 H2. Exact digital optical emulation must be bitwise prediction-equivalent (the same mathematics), ruling out unsupported digital-vs-optical accuracy claims.

## Competitive digital baselines and ablations
- Histogram gradient boosting; tuned fixed LightGBM; tuned fixed XGBoost; 1-hour persistence and 24-hour seasonal persistence.
- No coherent contrast, instantaneous phase features (no 24-hour reference), single output quadrature, static sinusoidal/Fourier features at the **same dimensional budget**, exact digital equivalent, 8-bit/noisy hardware-surrogate response.
- Frozen α=350, 80 virtual carriers, seed=731029; shrinkage candidate list predefined in source. The primary endpoint is 2020 one-hour **net-load RMSE** in both countries. Companion MAE, 168h paired moving-block bootstrap CI on MSE differences (1250 replicates).

## Success and falsification gates
A **two-country forecasting superiority claim** is permitted only if the proposed phase-interference model (a) has lower RMSE than HGB, LightGBM, XGBoost, and all non-equivalent ablations in **both IT and GR**; (b) all corresponding predeclared 168-hour paired block-bootstrap 95% intervals for squared-error differences exclude zero below zero; and (c) 8-bit/noisy variant loses <5% in RMSE relative to noiseless. Comparison with the mathematically identical digital emulator is necessarily a tie; optical *hardware* speed/energy gains require separate calibrated chip tests and cannot be claimed from this study.
This is a strict gate, not a guarantee or a requirement to manipulate results. Failures will be published with positive findings. No reruns changing any selection criteria on 2020 will be described as prospective.

## Prior art and physical interpretability
Relevant existing work includes Optical Next Generation Reservoir Computing (Light: Science & Applications 2025; DOI 10.1038/s41377-025-01927-6), topologically reconfigurable optical feedback (Optics Express 2026; DOI 10.1364/OE.606877), and adaptive quantization photonic-aware neural networks (Neural Computing and Applications 2026; DOI 10.1007/s00521-026-11984-6). These prohibit claims that time-delayed nonlinear optics, interferometric detection, low-bit quantization, or phase-aware training are individually unprecedented.