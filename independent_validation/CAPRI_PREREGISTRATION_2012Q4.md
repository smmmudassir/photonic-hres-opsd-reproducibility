# CAPRI: frozen, held-aside Ausgrid cohort evaluation — 2026-11-01

## Data provenance and evidence boundary
Input is the *already-known* Ausgrid archive, `Ausgrid_solar_home_data.zip`, SHA-256 `5a766f52b6c8b3b72730380f4422e478934bc94640a4b089dd0e0e3c055c5d82`. The eight customer IDs **111, 113, 114, 115, 116, 117, 120, 121** were selected deterministically using only 2010–11 source metadata (>=360 GC and GG rows, no CL channel, IDs >=110; first eight ascending). They were never among the five previously evaluated GAUDL-PQR customers (12, 32, 44, 78, 101).
- Train: 1 July 2010–30 June 2011; daily samples with complete 48-slot GC/GG labels and causal days -1 and -7; model fit on days with dayofyear divisible by 3 for compute budget.
- Validation: 1 February–30 June 2012 from the 2011–12 file; all rows for early stopping, deterministic every-fourth-day subsample for planning-risk calibration.
- **Confirmation test LOCKED:** 1 October–31 December 2012 from the 2012–13 file, across the same eight households. No 2012–13 test CSV content is read before this lock commit. Missing/invalid days are excluded using the fixed rule (complete, nonnegative GC/GG both current and lagged days; no imputation).
This is a **previously untested household cohort and quarter within the Ausgrid source**, not a new independently collected dataset nor a prospective deployment. Normalized battery tariffs are imposed, not actual historic household billing.

## Hypothesis and mechanism
**CAPRI — Control-Adjoint Phase-Ratio Interference** learns a *relative-phase interferometric readout* from previous-day and previous-week electric measurements, with interference common-phase cancellation. Unlike fixed sinusoidal regression, learning weights for each sample-slot are obtained from the *perfect-information linear-program battery-dispatch equality marginal (dual/shadow price)*, computed on TRAINING targets only. A Gaussian heteroscedastic residual head is fitted using weighted squared error plus likelihood and a simulated phase-perturbation consistency term; the readout augments the same strong LightGBM base model used by all competitors.
The supposed advantage over regular photonic-inspired residual learning is a **decision-dual-guided phase reference**; its uniqueness against published decision-focused learning and photonic models is NOT presumed, and may be falsified by experiments or literature search.
The phase calculations run in software, and have an exact digital representation; no physical optical efficiency/latency/chip claim is made.

## Fixed comparator family
- Strong LightGBM fitted to matched training input with 420 trees, depth 7, leaves 31 and min-child 140.
- Digital residual net with nonlinear embedding and the SAME shadow-price-weighted objective.
- Interferometric CAPRI residual head with trainable optical-inspired relative phase.
- Frozen-phase ablation (same head and dual objective).
- Single-arm/no-interference ablation (same head and dual objective).
- No-dual-price objective ablation (same phase mechanism without learned dual importance).
Training seeds **13, 29, 47**; no test-based seed/model selection. AdamW, learning rate .002, up to eight epochs, early stopping using validation error. Exact code SHA-256 is locked in `CAPRI_FROZEN_SHA256.txt` before the first confirmation run.
The LP has 6-kWh capacity, 2-kW max power, 95% charging/discharging efficiency, 15–90% SOC, terminal 50% SOC, no simultaneous charging/discharging (audited), throughput cost $0.015/kWh. Import tariff: $0.10 off-peak, $0.20 day, $0.32 16:00–21:00; $0.05 export credit. All methods solve the exact same constrained 48-step LP and settle on actual GC-GG net demand.
Uncertainty reserve `alpha ∈ {0, 0.25, 0.5}` is chosen by smallest validation operating cost on the fixed every-fourth-DOY selection; **zero is allowed** and ties select the smaller alpha. Same tuning grid for all models.

## Strict predeclared success
The primary metric is *realized simulated battery operating cost per household-day* over all valid held-out home-days, averaged over the three predeclared CAPRI seeds. Report RMSE as a secondary endpoint. A 2,000-replicate seven-calendar-day moving-block bootstrap resamples synchronized dates across households, averaging the three seeds per home-day before resampling.
Success requires **all**:
1. CAPRI cost improvement >1.0% against strong LightGBM, and paired 95% CI for CAPRI minus LightGBM entirely below zero.
2. CAPRI minus matched decision-focused digital net cost has paired CI entirely below zero.
3. CAPRI minus each frozen-phase, single-arm, and no-dual-price ablation has paired CI entirely below zero.
4. All controllers pass battery power, SOC, and no-simultaneous-charge-discharge numerical checks.
No claim of global algorithmic first, hardware superiority, or generalization to Hyderabad/Visakhapatnam even if these succeed; independent original data and broader evidence would still be required.

## Integrity
All failures, gaps, tuning choices, checksums and any post-lock code changes must be disclosed. No retuning to the held-out quarter. If a bug requires patching, report results as exploratory until confirmation on a new holdout. Test source is accessed only AFTER GitHub preregistration and code SHA lock.
