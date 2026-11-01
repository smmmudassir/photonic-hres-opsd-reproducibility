# GAUDL — Gauge-invariant uncertainty and differentiable dispatch-regret learning

**Research prototype. An independently validated photonic advantage is *not* established.**

GAUDL encodes past household PV/load measurements into 24 trainable complex relative-phase I/Q features, derives Gaussian predictive location and scale from the invariant representation, and optimizes a decision-focused surrogate of constrained battery dispatch regret alongside a proper probabilistic score. The matched digital MLP uses exactly the same training and evaluation objective, with a larger digital projection. Final operating costs are computed by the *same* SciPy linear program for both models.

The novelty *hypothesis* is the specific symmetry-constrained control calibration mechanism; neither interferometric phase differences, neural probabilistic forecasting, decision-focused energy control nor model-predictive scheduling is individually new. There is no optical chip or hardware measurement. A digital processor can implement the entire model exactly.

## Independent Ausgrid source

Original data measured by Ausgrid, reused in Pierre Haessig's [solarhome-control-bench](https://github.com/pierre-haessig/solarhome-control-bench/blob/master/data/README.md) (single household). Download from:
https://raw.githubusercontent.com/pierre-haessig/solarhome-control-bench/master/data/data_2011-2012.csv

The pinned Git blob SHA1 (`1e940b59fb16402d1007541d99fd7dc4f7f78200`) is checked by the runner. Do **not** use the earlier OPSD 2019/2020 holdouts as unseen validation.

```bash
python -m pip install -r requirements.txt
python -m pytest tests -q
python src/run_study.py --smoke --out results/synthetic_smoke
python src/run_study.py --data data_2011-2012.csv --out results/ausgrid_locked
```

Run the real independent command **only after the frozen protocol and source checksums are publicly timestamped**. Never select architectures, seeds, battery sizing, tariff, time horizon or hyperparameters after examining held-out labels. A missing/bad source file produces a hard failure rather than a synthetic fallback.

## What has actually been executed

- Five invariant-gradient/safe-LP/unit tests: PASS.
- Synthetic day-ahead smoke test, **one** seed, **five** simulated dispatch days: PASS; results under `results/smoke_final/`. A favorable synthetic result is **not empirical superiority**.
- Ausgrid measured-data locked experiment: **NOT EXECUTED** in this execution environment, because the external data download was unavailable. It must remain a blank outcome until actually run.

## Scientific cautions

- The proper scoring rule is Gaussian CRPS. The control term is the realized loss of an unrolled, differentiable feasible policy minus a *same-policy-family* oracle, not the true LP regret. The exact LP is used only for evaluation.
- The housing dataset is one selected site, one year, and could have data-quality/seasonal-selection bias. Cross-home or cross-dataset replication will still be necessary even if the locked result is favorable.
- The model uses coherent relative-phase computation only as a mathematical analog. It has no measured physical photonic energy or latency advantage.
- Prices, battery ratings, efficiency and wear are declared simulation assumptions, not reported Australian measurements.
- The source contains privately deidentified household metering data originally published for research; cite Ausgrid and the reuse repository and observe attribution/license terms.

## Reference prior art

- Kim, Das & Wu (2025), *A Neural Optimizer with Decision-Focused Learning for Optimal Energy Storage Operation*, IEEE TII. DOI 10.1109/TII.2025.3597951.
- *Decision-focused end-to-end learning for enhanced building energy flexibility control* (2026), Applied Energy Advances. DOI 10.1016/j.adapen.2026.100280.
- *Decision-Focused Learning Enhanced by Automated Feature Engineering for Energy Storage Optimisation* (2026), ESWA. DOI 10.1016/j.eswa.2025.130554.
- *Adaptive amplitude-phase encoding and physically constrained optimization for high-performance photonic machine learning* (2026), Optik/Optics Communications (metadata requires final bibliographic verification).