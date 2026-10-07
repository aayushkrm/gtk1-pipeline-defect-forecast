# VALIDATION: no leakage, no cherry-picking

1. Longitudinal hold-out: train on (2016→2021), test on (2021→2025).
   Never tune on test.
   Use reference: ON 392-526.
   Replicate on SRTO-1608, PK2 (threshold-corrected).
2. Group-by-section: run leave-one-section-out for generalization claim.
3. Baselines first: test segment persistence (past density), global rate (Poisson), pipe persistence.
   Claim only if you beat all baselines on PR-AUC + recall@P=0.7.
4. Metrics: score P1 with PR-AUC / F1 / recall@P=0.7; score P2 with MAE/RMSE/Spearman (zero-inflated).
   Never headline accuracy.
   Calibrate (Platt/isotonic on train only).
   Report calibration.
5. Ablations: drop contractor/year covariate (method-effect check), drop weld features, compare 100m vs 1km.
   Report negatives.
   Keep runs seed-fixed and config-logged.
   Show de-identified aggregates only.
