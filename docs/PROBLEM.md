# PROBLEM — what is feasible and useful

## Business question
"Where will new / growing defects appear in 4–5y?" for repair + survey prioritization.

## Why not single-crack growth
No persistent defect ID (SSID absent/pre-2021, not inherited), 0% coords,
threshold drift 2.5–5×, class (a) 0.1–1.9%. Individual Δdepth ceiling ~R² 0.3–0.5.
Honest scope: segment / pipe risk, not crack physics.

## Chosen primary problem
**P1 — 1-km binary:** does ≥1 new corrosion defect (Depth≥10%, normalized) appear
in segment in next 4–5y? Train 2016→2021, test 2021→2025 (ON reference).
Metrics: PR-AUC primary, recall@precision=0.7, F1. ≥80% claim only here, recall-oriented.
**P2 — 1-km count:** # new anomalies /5y (Poisson/NB, zero-inflated). MAE/RMSE, Spearman.
Secondary: pipe high-risk (KBD<0.9 or a/b), matched Δdepth, burst detection.

## Anti-leakage
Features from past survey only. Year/contractor/standard as covariate (method effect).
No future depths, no test-tuned thresholds. Group-by-section splits + pure future hold-out.
Accuracy forbidden as headline (85–95% pipes defect-free) — PR-AUC/F-beta only.
