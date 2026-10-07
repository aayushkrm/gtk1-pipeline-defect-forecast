# VALIDATION: no leakage, no cherry-picking

1. Longitudinal hold-out: train on (2016→2021), test on (2021→2025).
   Never tune on test.
   Use reference: ON 392-526.
   Replicate on SRTO-1608 and PK1 (@100m matched-new cells, AP vs base + lift-CI + R1–R4 gates).
   PK2 deferred (no good pair).
2. Group-by-section: run leave-one-section-out for generalization claim.
3. Baselines first: test segment persistence (past density), global rate (Poisson), pipe persistence.
   Claim only if you beat all baselines on AP vs base with lift-CI lower>0 + R1–R4 gates.
   recall@P=0.7 is retired.
4. Metrics: score P1 @100m matched-new cells with AP vs base + lift-CI + R1–R4 gates; score P2 with MAE/RMSE/Spearman (zero-inflated).
   Never headline accuracy.
   Calibrate (Platt/isotonic on train only).
   Report calibration.
5. Ablations: drop contractor/year covariate (method-effect check), drop weld features, compare 100m vs 1km.
   Report negatives.
   Keep runs seed-fixed and config-logged.
   Show de-identified aggregates only.
