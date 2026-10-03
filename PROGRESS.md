# PROGRESS.md — audit log (append-only)

## 2026-10-03 — Study complete, build started
- Studied: Project_info.md, 6 images, 1 dashboard video (4 frames), 6 sections / 32 files.
- Key findings: 44/45-col anomaly schema (R4 header), pipes 20→30 cols; threshold drift (PK-2 164→9→55/km); Pipe No join 11788/11858, odometer ±2m match 72.6%/53.4%; no persistent SSID; 0% coords; 5 corrupt/truncated files; TECH/ARTD/GOUG code reuse; 2016 Service-life=100y fictive.
- Decision: unit = pipe (join on Pipe No), aggregates 100m/1km; normalize Depth≥10%; longitudinal pairs ON 2016→2021→2025 (reference).
- Scaffolded `gtk1-forecast/` repo; raw data excluded by `.gitignore`.
- Next: cheap ETL diagnostic (ON reference pair), literature sweep, validation spec. No model claims yet.

## 2026-10-03 — Swarm results + first baselines + repo
- Literature (12 sources): GBM-first (HGB/CatBoost, Poisson/Tweedie, hurdle/ZINB), LGCP spatial benchmark, Hawkes exploratory only; no deep sequence without IDs; PR-AUC + recall@fixed-P per Davis/Saito; contractor-as-covariate + per-survey calibration per shift literature.
- ETL diagnostic (ON, read-only): headers R4; normalized Depth≥10% counts 1649/2583/3751; CORR dominates, NaN-depth = weld classes; pipe-join 100% after key normalization (`75.0`→`75`, `а`-suffixes), 11788 overlap, weld25 truncated to 27km — use weld21 as master + flag; presence saturated, growth is honest target.
- Validation spec frozen: train 2016→2021 / test 2021→2025, match rule pipe+2m+0.5m+1h (no Δdepth tie-break), B1/B2/B3 baselines, AP + R@P0.7 (grouped ties, unattained=0.0), F1 threshold from train-CV only, LOSO extension, stop/pivot gates.
- Ran `experiments/e01_baseline.py` (executed, verified): presence AP 0.968/0.992 (≈base, vacuous); growth AP 0.735→0.872, spear 0.785→0.904; HGB-1feat AP 0.729 ≈ persistence (sanity pass). R@P0.7=1.0 flagged as trivial at 70%+ prevalence — operating point must move to P≥0.85 or count target; not claimed as success.
- Repo: `gtk1-forecast/` git init, single committer aayushkrm, private GitHub `aayushkrm/gtk1-pipeline-defect-forecast`, pushed main 32578f0. Raw data excluded by `.gitignore`, only de-identified aggregates committed.
- Next: E05 full-feature HGB + contractor ablation (E06), 100m-vs-1km ablation, matched-label build (pipe+2m) replacing segment-diff proxy, calibration.

