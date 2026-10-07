# GTK1 — Inspection-report triage for main gas pipelines (frozen scope: B1 primary)

Private R&D repo. Never commit raw VTD data (see `.gitignore`; verified clean).
Store data outside this repo at `../Данные для предварительного изучения/`.

## What this delivers (honest, evidence-backed)
This repo ranks 100m-segment watchlists for **newly-reported ≥10% defects**.
Read the operational definition in docs/GUARDRAILS.md.
This is NOT physical corrosion prediction.
It validates past→future on 4 sections: ON AP 0.644/base 0.268; SRTO-1608 test 0.277/0.061; SRTO-1717 0.181/0.031; PK1 0.779/0.574/0.375 at ≥10/12/15%.
No ≥80% reliability claim is supportable.
See docs/SUPERVISOR_BRIEF.md.

## Reproduce
```bash
python3 src/tests/test_parity.py            # synthetic parity, no data needed
python3 triage/prospective.py --section on --survey 2025 [--drop-last]
python3 triage/prospective.py --section on --survey 2021 --check   # regression gate
bash run_tests.sh                             # all offline checks
```

## Layout (as-built, not as-planned)
- `src/gtk1/` holds the frozen pipeline.
  It contains io (loaders + tolerant-xlrd + normalize), match (greedy/Hungarian), features (7-feat 100m build), metrics (AP/CI/paired-delta/P@K).
  Both triage paths stay thin consumers.
  Find byte-identical migration proofs in PROGRESS.md.
- `src/tests/` holds parity tests (synthetic).
  It also holds consistency checks (frozen-number tripwire, no data needed).
- `experiments/` holds E01–E12 frozen scripts + result JSONs.
  It serves as audit trail.
  Scripts stay untouched since run.
- `triage/` holds retrospective demo pages (ON, PK1) + prospective harness + forward watchlists.
- `configs/` holds base.yaml (legacy plan) + thresholds.yaml (per-section placeholders, uncalibrated).
- `docs/` holds PROBLEM, DATA, VALIDATION, GUARDRAILS, TRIAGE_SPEC, SUPERVISOR_BRIEF, OVERLAY_STATUS.
- `outputs/` holds ignored full watchlist CSVs.

## Rules (enforced by reviewer rounds 1–10)
- Use past-only features.
- Do not tune on test.
- Report negatives.
- Keep overlay OFF by default (kill-switch).
- Ship every number with match-rate, vanished-frac, cut-sensitivity (docs/GUARDRAILS.md).
- Never commit raw `.xls/.xlsx/.csv/.mp4/.jpg`. Keep single committer.
