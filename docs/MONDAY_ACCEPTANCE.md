# MONDAY ACCEPTANCE: checklist for the partner package (due Monday 19.10)

Vlad, project chat: Tuesday drop delayed (colleague overload, part of staff away).
New date Monday. Requested and confirmed in flight: tool types, pipe characteristics,
additional sections. Work continues on current data until then.

## Status 2026-10-24

- Re-issued Wednesday 21.10.2026 17:50 in the project chat as "Датасет НПК.rar" (70.3 MB).
  Vlad: the 15.10 archive was partly damaged when saved from RedOS, integrity re-checked
  before re-export, all earlier data to be deleted. Supersedes "Датасет ВТД.rar".
- Not yet in the workspace, so steps 1-7 are still open. Save the file first.
- Vlad, Tuesday 20.10: one trunk pipeline plus every branch line up to the distribution
  stations; branch diameter and wall thickness differ; coverage 2016-2025 without 2021 and
  2023. Our October tree holds 2021 and 2023 surveys, so read this claim per section at step 1.
- Tool types and pipe characteristics were "still being compiled" on 15.10; not delivered.

## On arrival, verify in this order (report same day in chat)

1. Inventory vs request: pipe characteristics files present? per-section tool lists present?
   Additional section folders present? Name every missing item explicitly.
2. Openability per file: open each new file in LibreOffice AND Excel. Any refusal goes back
   to Vlad the same day with the exact filename ("file broken" + app + version).
3. Pipe-key join: run `python3 experiments/ingest_tuesday.py` against the new files.
   Clean loads must join ≥0.9 of anomaly pipes (proxy-proven); truncated loads route through
   the salvage tier and expect ~0.85 with ~15% unresolvable pipes flagged, not hidden.
4. Tool lines per section: each survey year of each section needs its tool identity.
   Unresolved lines go to `unresolved` bucket for a human look, never silently dropped.
5. Steel grades: confirm the last three sections covered (commitment dated 12.10).
6. Open answers still owed: YN-2023 scope (22,332 vs 4,400), thresholds and methods per survey
   (the 10%-vs-7% verdict), empty-character decode, PK2-2025 viewer on their side, class ruling
   if still ambiguous, dig costs for the economic block.
7. New sections: folder-per-section layout check, survey-year inventory, then full E15-style
   audit (strict rows, coverage spans, salvage only where evidenced) before any modeling use.

## Do not

- Pool new sections with old ones before same-section validation (no-pooling rule).
- Train on re-exports without re-running the frozen provenance (hashes + row counts first).
- Treat Monday files as clean until steps 1–4 pass; RedOS flash corruption is the base rate.
