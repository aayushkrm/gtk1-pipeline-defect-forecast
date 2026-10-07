# Supervisor brief: GTK1 status (evidence as of E12 + PK1 refresh; src migration proven)

## One-line verdict
Inspection-report triage works. It replicates on 4/4 sections. Physical-corrosion forecasting at ≥80% reliability is not supportable on current data. Survey-conditional reporting predictability differs from physical predictability. See risk below.

## Task mapping (project tasks 1 to 7)
1. Systematized sources. Covered 6 sections × 2 to 3 surveys (2015 to 2025). Included anomaly + weld/pipe logs. Catalogued formats and failures (docs/DATA.md).
2. Completed data QC. Confirmed 44/45-col schema. Confirmed R4 headers. Quantified threshold drift (PK2 164→9→55/km). Found 5 corrupt files. Found code-reuse TECH/ARTD/GOUG. Found 2016 Service-life fictive 100y.
3. Mapped dependencies. Past density → future reporting dominates (Spearman 0.78 to 0.90). Noted pipe type/coating signals. Age is missing (only Y-N 1980).
4. Built dataset. Joined pipes. Built 100m/1km grids. Normalized Depth≥10%. Built matched-new labels (pipe+2m/0.5m/1h). Built longitudinal pairs.
5. Froze models. Set B1/persistence-family as primary (AP 0.64 ON / 0.28 SRTO-1608 / 0.18 SRTO-1717 / 0.78 PK1). Selected log-linear as best count model (MAE 6.5 vs 11.3). Quarantined HGB. Set LR-nlag overlay to ON-only experimental OFF by default.
6. Ran comparison. Ran 12 experiments E01 to E12. Used baselines everywhere. Reported negatives (HGB≈B1, shuffle anomaly, SRTO non-transfer, cut-fragility).
7. Validated historically. Applied train-past→test-future on 4 sections. Added block-CV. Added 100-shuffle null. Added repair-agnostic audit.

## Numbers (section-conditional, operational framing "newly-reported ≥10% @100m")
- ON: B1 0.644/base 0.268; LR 0.676 (+0.032 ON-only). SRTO-1608 test: 0.277/0.061.
- SRTO-1717: 0.181/0.031 (13 pos). PK1: 0.779/0.401 (562 pos, stable methodology).
- Triage pages v0 (ON, PK1) ship ranked lists + heatmaps + audit columns + disclaimers.

## Residual ≥80% risk (one sentence, fourth confirmation)
The "new" label conflates true initiation with re-detected misaligned old defects. It also conflates survey-sensitivity gain (vanished 60%/39%, prevalence 0.27→0.08 across cuts). Any ≥80% reliability framing mistakes survey-conditional reporting predictability for physical corrosion predictability.

## Needed from partner (blockers for stronger claims)
Repair logs; 5 file re-exports; pipe ages; per-survey thresholds/methodology; SRTO-1717-2021 Character decode; 2025 weld-log tail. We continue ranking triage without them.
