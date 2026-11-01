# CAPRI — frozen previously untested household/quarter confirmation (negative primary outcome)

Pretest preregistration commit: `7fe58bde19738002d4364fc61a58d6b577c1d629`. Source hash commit: `4edb360c05fe6e5c15c90d8e62e1be3938393d27`. Frozen source matches digests in both code and output manifest.

Data: user-supplied original Ausgrid 300-home archive; SHA256 `5a766f52b6c8b3b72730380f4422e478934bc94640a4b089dd0e0e3c055c5d82`. Eight previously untested household IDs 111,113,114,115,116,117,120,121; October–December 2012; **736 household-day cases across 92 dates**. All 48 half-hour values on each valid day were included. Training year 2010–11; validation Feb–Jun 2012. This is a held-aside source cohort, **not an independently collected external dataset**.

## Confirmation, three-seed mean
| Method | RMSE (kW) | Simulated cost ($/home-day) |
|---|---:|---:|
| Strong LightGBM | 0.570190 | **1.356826** |
| CAPRI phase+dual | **0.570104** | 1.357470 |
| Matched digital neural residual+dual | 0.571306 | 1.360357 |
| Frozen phase | 0.570562 | 1.357658 |
| Single arm/no interference | 0.570710 | 1.357960 |
| No-dual-price phase | 0.570262 | 1.357064 |

Seven-calendar-day synchronized-block paired bootstrap; 2,000 replicates. Negative CAPRI differences indicate savings.

| CAPRI minus comparator | Mean difference ($/home-day) | 95% confidence interval |
|---|---:|---|
| LightGBM | +0.000644 | [+0.000229,+0.001015] |
| Matched decision-focused digital | **-0.002887** | **[-0.003431,-0.002365]** |
| Frozen phase | -0.000187 | [-0.000668,+0.000305] |
| Single-arm | -0.000490 | [-0.000933,-0.000043] |
| No-dual phase | +0.000406 | [+0.000106,+0.000722] |

CAPRI was lower cost than the matched digital residual network, but **worse than strong LightGBM and worse than the no-dual ablation**; frozen-phase comparison is not significant. **The strict jointly predeclared superiority hypothesis failed.**

Development-only risk-margin calibration on earlier 2012 data selected alpha=0 for every model (the configured risk margins worsened modeled costs). No 2012Q4 tuning or post-unblinding coefficient change was made. Exact LP battery physical constraints were checked; settlement uses synthetic tariffs, not actual 2012 household bills. The optical phase mechanism is entirely simulated and has a digital equivalent. Global first novelty and optical chip superiority are not established.

The full original code, saved weights, full 11,776-row ledger, bootstrap files and Word report are distributed with the downloadable CAPRI research package from the associated conversation; input original Ausgrid archive is not redistributed. The 2012Q4 holdout is now used and MUST NOT be presented as pristine for further tuning.
