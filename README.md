# GTK1 — Forecasting defects on main gas pipelines

Private R&D repo. Raw VTD data is **never committed** (see `.gitignore`).
Data lives outside this repo at `../Данные для предварительного изучения/`.

## Problem (short)
Predict where / which defects appear or grow on pipeline sections,
from past ILI anomalies + pipe/weld logs. Target: ≥80% reliability
for a chosen, honestly validated task.

Primary tasks (from data study):
1. `1km-binary`: new corrosion ≥10% in 4–5y (PR-AUC, recall@P=0.7).
2. `1km-count`: new-anomaly count /5y (Poisson/NB, MAE, Spearman).
3. Pipe high-risk, 4. matched Δdepth, 5. regime-change detection.

## Layout
- `src/etl/` — salvage-tolerant parsers, threshold normalization, pipe join
- `src/features/` — pipe-level + 100m/1km aggregates
- `src/models/` — baselines (persistence, Poisson, HGB) → GBM
- `src/validation/` — longitudinal hold-out (train past → test future), group-by-section
- `configs/` — dataset + model configs
- `docs/` — PROBLEM, DATA, VALIDATION, LIMITS
- `experiments/` — dated cheap diagnostics, never tuned on test

## Reproduce
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.etl.build_dataset --config configs/base.yaml
python -m src.models.baseline --config configs/base.yaml
```

## Rules
- No raw `.xls/.xlsx/.csv` in git. Only derived, de-identified aggregates <1MB.
- No test tuning, no cherry-picking, report negatives.
- See `PROGRESS.md` for audit log.
