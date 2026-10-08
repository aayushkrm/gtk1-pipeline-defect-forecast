# EVAL_SPEC: how the team compares models (answers Evgeny's testing ask, 08.10.2026)

One scoring standard for all paired workers (Ayush+Aleksei, Victoria+Dmitry) and all
reviewer gates. Implementations live in `src/gtk1/metrics.py`; this file fixes their USE.
Gates R1–R4 themselves stay defined in `docs/GUARDRAILS.md` (referenced, not repeated).

## Which metric for which task

- Binary newly-reported ≥10% @100m (Task A core): AP vs base prevalence + 2000-cell lift CI
  (`ap_lift_ci`). Win iff lift-CI lower above 0 with n_pos≥30 on the SAME frozen labels.
- Paired-model comparison (two workers, one task): `paired_delta_ci` on identical labels and seed.
  Report Δ with CI; CIs crossing zero mean tie, not loss. Never compare APs from different label builds.
- Per-cell counts (P2): MAE vs mean baseline + Spearman. Quarantine stands for HGB until residual and
  shuffle controls pass (GUARDRAILS model quarantine). No P2 functions in metrics.py yet — add them
  before citing this line as code-backed.
- ABC display colors: no metric. Colors are present labels (`triage/abc_*.json`), not predictions.
- Recall@P retired as vacuous (round 4). Accuracy never headlined (defect-free majority).

## Reporting rules

- Every AP ships with cut, survey pair, match-rate, vanished share, and prevalence. Bare numbers rejected.
- Sensitivity cuts ≥12%/≥15% accompany every ≥10% primary. No pooling across sections.
- Null and negative results committed with the same fields (see E16: n_pos 4/0/0 closed a track).
- Seeds fixed and logged; git hash in `repro` of every result JSON. Package versions belong here
  too once a freeze file exists (requirements.txt is pinned but not yet recorded per-run).
- Empty-bootstrap intervals return NaN with warning; NaN never enters a committed JSON (null instead).

## Worker protocol (paired tracks)

- Agree the method split in writing before running (CatBoost vs Random Forest or equivalent).
- Share tried-versus-untried lists; no duplicate runs across the pair.
- Both workers score through this file's metrics on identical labels. Disagreements go to the 1:1,
  not into competing metric definitions.
