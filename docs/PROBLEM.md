# PROBLEM: what is feasible and useful

## Business question
"Where will new / growing defects appear in 4-5y?"
Use the answer for repair + survey prioritization.

## Why not single-crack growth
No persistent defect ID exists.
SSID stays absent/pre-2021 and not inherited.
Coords cover 0%.
Threshold drift spans 2.5-5×.
Class (a) spans 0.1-1.9%.
Individual Δdepth caps at ~R² 0.3-0.5.
Keep honest scope: segment / pipe risk, not crack physics.

## Chosen primary problem
P1. 100-m binary: does ≥1 newly-reported ≥10% row (Depth≥10%, pipe+2m/0.5m/1h greedy matched-new) appear
in segment in next 4-5y?
Train on 2016→2021.
Test on 2021→2025 (ON reference; replicate ON/PK1/SRTO-1608 with AP vs base + lift-CI + R1–R4 gates).
Use AP vs base + lift-CI with R1–R4 gates as primary metric.
recall@precision=0.7 is retired (vacuous operating point).
Make no ≥80% claim.
Keep it recall-oriented.
PK2 is deferred (no good pair).
P2. 1-km count: counts # new anomalies /5y (Poisson/NB, zero-inflated).
Score it with MAE/RMSE and Spearman.
Add secondary: pipe high-risk (KBD<0.9 or a/b), matched Δdepth, burst detection.

## Anti-leakage
Use features from past survey only.
Add Year/contractor/standard as covariate (method effect).
Exclude future depths.
Exclude test-tuned thresholds.
Split group-by-section and keep pure future hold-out.
Never headline accuracy (85-95% pipes defect-free).
Use AP vs base + lift-CI with R1–R4 gates only.
