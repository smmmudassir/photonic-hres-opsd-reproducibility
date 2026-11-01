# GAUDL-PQR/CAPRI independent *saved-output* reproducibility audit (2026-11-01)

This audit does NOT assert positive photonic superiority or new independent test data. It verifies previously saved model outputs for two Ausgrid household cohorts; no model retraining or holdout-informed retuning was performed.

**Original source:** Ausgrid solar-home archive, SHA256 `5a766f52b6c8b3b72730380f4422e478934bc94640a4b089dd0e0e3c055c5d82`; raw data are not redistributed.

## Confirmed by a separate read-only Python auditor
- GAUDL-PQR: 5 homes, 85 valid July–September 2012 calendar days, 425 home-days. Phase cost **$1.553485** vs separately refitted strong LightGBM **$1.500651**; +3.52%, phase worse.
- CAPRI: 8 previously unused homes, 92 October–December 2012 days, 736 home-days. Phase cost **$1.357470** vs strong LightGBM **$1.356826**; +0.047%, phase worse.
- CAPRI vs matched digital neural residual: −$0.002887/home-day, 95% seven-day block CI [−$0.003431,−$0.002365].
- CAPRI vs no-dual ablation: +$0.000406/home-day, 95% CI [+0.000106,+0.000722]; the ablation wins.
- Original GAUDL 3000-iteration and CAPRI 2000-iteration paired seven-day block bootstraps reproduced exactly from frozen ledgers, including original RNG evolution.
- Frozen source SHA-256 and 3-seed aggregation verified. CAPRI risk-buffer alpha = 0 for every model in the saved confirmation ledger.
- A 20-case synthetic LP sanity test supports the bound `regret <= 2 Delta sum_t p_t |y_t-yhat_t|` under the original common-feasible-set and price assumptions. This is not an original general optimization theorem.

## Essential scientific limitations
1. This is an *archive-output audit*, not independent deep model training or a new historically unseen test. Both 2012 cohorts were already evaluated.
2. Phase features are digital sine/cosine implementations, not a measured photonic circuit.
3. The refitted GAUDL strong LightGBM used additional development history compared with the residual heads; it is a practically strong comparator, **not an equal-training-data architecture control**.
4. Both overall predeclared superiority gates FAILED. There is no established globally novel or superior photonic learning-and-control system.
5. The audited full source/checkpoints and independent executable audit form a downloadable research archive; the full archive **has not been published as a GitHub release or DOI-bearing deposit**. Authors must publish and link it before claiming full public reproducibility.

**New manuscript contribution:** sharpened originality boundary, verifiable comparator definitions, a specialized regret bound, and a documented independent replay of frozen result arithmetic and statistical tests. New household/month stratifications are expressly post-hoc descriptive—not new confirmations.

**Original registered negative result records:**
- [GAUDL-PQR](https://github.com/smmmudassir/photonic-hres-opsd-reproducibility/blob/main/independent_validation/GAUDL_PQR_AUSGRID_2012_2013_RESULTS.md)
- [CAPRI](https://github.com/smmmudassir/photonic-hres-opsd-reproducibility/blob/main/independent_validation/CAPRI_2012Q4_RESULTS.md)

The two reports must remain visible and not be replaced by a favorable-only summary.
