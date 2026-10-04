# GTK1 — Inspection-report triage for main gas pipelines (frozen scope: B1 primary)

Private R&D repo. Raw VTD data is **never committed** (see `.gitignore`; verified clean).
Data lives outside this repo at `../Данные для предварительного изучения/`.

## What this delivers (honest, evidence-backed)
Ranked 100m-segment watchlists for **newly-reported ≥10% defects** (operational definition in
docs/GUARDRAILS.md — NOT physical corrosion prediction). Validated past→future on 4 sections:
ON AP 0.644/base 0.268; SRTO-1608 test 0.277/0.061; SRTO-1717 0.181/0.031; PK1 0.779/0.574/0.375
at ≥10/12/15%. No ≥80% reliability claim is supportable — see docs/SUPERVISOR_BRIEF.md.

## Reproduce
```bash
python3 src/tests/test_parity.py            # synthetic parity, no data needed
python3 triage/prospective.py --section on --survey 2025 [--drop-last]
python3 triage/prospective.py --section on --survey 2021 --check   # regression gate
bash run_tests.sh                             # all offline checks
```

## Layout (as-built, not as-planned)
- `src/gtk1/` — frozen pipeline: io (loaders + tolerant-xlrd + normalize), match (greedy/Hungarian),
  features (7-feat 100m build), metrics (AP/CI/paired-delta/P@K). Both triage paths are thin consumers
  (byte-identical migration proofs in PROGRESS.md).
- `src/tests/` — parity (synthetic) + consistency (frozen-number tripwire, no data needed).
- `experiments/` — E01–E12 frozen scripts + result JSONs (audit trail; scripts untouched since run).
- `triage/` — retrospective demo pages (ON, PK1) + prospective harness + forward watchlists.
- `configs/` — base.yaml (legacy plan) + thresholds.yaml (per-section placeholders, uncalibrated).
- `docs/` — PROBLEM, DATA, VALIDATION, GUARDRAILS, TRIAGE_SPEC, SUPERVISOR_BRIEF, OVERLAY_STATUS.
- `outputs/` — ignored full watchlist CSVs.

## Rules (enforced by reviewer rounds 1–10)
- Past-only features; no test tuning; negatives reported; overlay OFF by default (kill-switch).
- Every number ships with match-rate, vanished-frac, cut-sensitivity (docs/GUARDRAILS.md).
- Raw `.xls/.xlsx/.csv/.mp4/.jpg` never committed. Single committer.
