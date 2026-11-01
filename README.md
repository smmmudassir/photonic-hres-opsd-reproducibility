# Preregistered 2020 cross-national forecast–dispatch validation

**Study status:** prospective relative to this run, not a previously unseen external prospective deployment. Test labels are historical 2020 observations, but no 2020 outcomes were evaluated before the preregistration commit.

This research combines component forecasting, a direct net-load expert, a three-regime, ridge-shrunk convex reconciler, and a constrained day-by-day 24-hour battery linear program. The method is called **Tariff-Regime Shrunk Reconciliation with Budgeted Replanning (TRSR-BR)**. We do not claim this combination was the world's first, or that it implements optical hardware. Related literature on decision-focused learning and event-triggered MPC is acknowledged in the manuscript.

The preregistration and executable code are committed before the 2020 test evaluation. Frozen parameters and tests are described in `PREREGISTRATION.md`. The full OPSD dataset is obtained from the original source; derived data are intentionally not embedded in the repository.

Run locally with `python -m pip install -r requirements.txt` then `python locked_validate.py --input time_series_60min_singleindex.csv --out results_2020`. Validation explicitly checks the dataset SHA256 before running. All output files should be committed with a clear post-lock timestamp and attached to the preregistered commit.

Do not treat this as a photonic neural demonstration: the methods are digital learning and LP optimization.