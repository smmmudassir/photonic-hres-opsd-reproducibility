# FR–ES 2019 frozen optical-delay evaluation — verified outcomes

Protocol was committed before first inspection of FR/ES 2019 target labels: `fc829c0d5ffe3b19e8eb66ad68b1de21b42074d3`. Code digest was predeclared: `52771902a7afa754be9d6666ca84dbb5738dd8a8e9aac4d98daecf5a70bacf84`. Full code, inputs recipe, predictions and hourly ledgers are available in accompanying ZIP.

## Forecast metrics (8,737 hourly observations / country)
| Model | France RMSE | Spain RMSE |
|---|---:|---:|
| HGB | 0.071637 | 0.032625 |
| LightGBM | 0.073802 | **0.032165** |
| Noisy coherent two-delay virtual reservoir residual | 0.070297 | 0.032542 |
| Noisy coherent no-delay residual | **0.070125** | 0.032498 |
| Digital Fourier residual | 0.071029 | 0.032559 |

For two-delay minus no-delay MSE: 168-hour paired block bootstrap (1,600 resamples) FR mean +0.000024, 95% CI [−0.000005,+0.000057]; ES mean +0.000003, CI [−0.000001,+0.000009]. **Both CIs include zero**; the optical delay mechanism did NOT show a significant benefit. Two-delay beat HGB but not the stronger alternative in all countries.

## Matched simulation control (361 days per country)
| Country | Seasonal-day LP total | Matched HGB 6h LP total | Matched coherent 6h LP total |
|---|---:|---:|---:|
| France | $943,544.72 | $942,600.86 | $942,597.00 |
| Spain | $934,652.28 | $934,700.65 | $934,702.22 |

Mean daily coherent minus HGB cost with 7-day paired block bootstrap: FR −$0.0107, 95% CI [−$0.0700,+$0.0481]; ES +$0.0043, 95% CI [−$0.0008,+$0.0119]. **Neither demonstrates the matched-control superiority condition**.

## Integrity and novelty boundary
- Historic FR and ES traces are unused national regions from the same official OPSD release, not independently collected data and not prospective field data.
- 48 virtual nodes with passive complex recurrence and delayed paths, balanced detection, fixed detector noise and 8-bit quantization. **Software abstraction only. No physical optical component, laser/ADC energy, latency, calibration or measured power advantage.**
- Delayed reservoirs, optical interferometric readout, ridge residuals and constrained battery LP all have prior art. A first-ever novelty claim is not justified.
- Prespecified **joint superiority claim failed**, and the 2019 test must be marked *used* from now on.
- No Hyderabad or Visakhapatnam metered site-level profiles have been acquired; do not claim those localities were validated.

Full source, manifest, numerical result CSVs, all 51,984 hourly controller-ledger rows and technical DOCX report are in the archival ZIP produced for this conversation.
