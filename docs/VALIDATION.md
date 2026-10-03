# VALIDATION — no leakage, no cherry-picking

1. Longitudinal hold-out: train on (2016→2021), test on (2021→2025). Never tune on test.
   Reference: ON 392–526. Replicate on SRTO-1608, PK2 (threshold-corrected).
2. Group-by-section: leave-one-section-out for generalization claim.
3. Baselines first: segment persistence (past density), global rate (Poisson), pipe persistence.
   Claim only if beating all baselines on PR-AUC + recall@P=0.7.
4. Metrics: P1 PR-AUC / F1 / recall@P=0.7; P2 MAE/RMSE/Spearman (zero-inflated);
   never headline accuracy. Calibrate (Platt/isotonic on train only), report calibration.
5. Ablations: without contractor/year covariate (method-effect check), without weld features,
   100m vs 1km. Report negatives. Seed-fixed, config-logged, de-identified aggregates only.
