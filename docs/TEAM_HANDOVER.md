# TEAM_HANDOVER: committed record of track memos (chat drafts live here as evidence)

Each section below is the memo its owner received in chat, with the committed artifact
that backs every number. Status: handed over, consumption by track owners untracked.

## Aleksei Alekseev — paired time extrapolation (different methods)

My lane: B1 past-count ranking, verified (Omsk AP 0.644, PK1 0.779 vs chance; see
`triage/triage_demo.json`, `triage/triage_pk1.json`). Proposed split: Aleksei takes a
different family (CatBoost or Random Forest variant) on the same 7 past-only features
(`src/gtk1/features.py` FEATS). Shared scoring only: `src/gtk1/metrics.py` AP vs base +
paired-delta CI per `docs/EVAL_SPEC.md`, identical labels, fixed seeds. Keep one
tried-versus-untried log between the pair; E17 (`experiments/results_e17.json`) is the
worked example (HGB/RF tie B1 on both sections).

## Fyodor Voznesensky — repair-schedule reconstruction

First schedule with uncertainty flags: `experiments/results_repair.json` (ON persistent
406/1568 past, SRTO-1608 121/453; reappeared controls 163/51 excluded as misalignment).
Cell maps: `triage/repair_cells_on.json` (76 cells), `triage/repair_cells_srto.json`
(62 cells), each with reappeared-control overlay. Rule: gone across two later surveys =
candidate; reappeared later = misalignment, never repair. Danger skew backs it (persistent
holds all (a) rows: 1 ON, 3 SRTO; reappeared all (c)).

## Leonid Irintseev — formula-drift evidence

`experiments/results_danger.json`: ab-shares spike around 2021/2022 then collapse on all
full-data sections (ON 0.21→2.29→0.67%, SRTO-1608 0.69→5.78→0.55%, PK1 6.38→2.14%) while
row counts rise monotonically: rule-driven, supports the ~2022 requirement lowering.
`experiments/results_e16.json`: future ab rows rematch past rows (4/0/0 new positives),
i.e. the program flags known defects under monitoring. `a_by_character` per file exposes
the weld concentration of critical flags.

## Victoria Engelke + Dmitry Bityukov — interpolation geometry

`experiments/results_coords.json`: town-proxy straight-line geometry with recorded UNFIT
verdict (ON corridor bend 0.8616 < 1 proves proxies cannot span that section). Odometer
chainage stays the join key; these coords serve coarse map overlay only, never 100 m truth.
Real endpoint coordinates remain a partner request.

## Natalia Mandzhieva — merge support

Loaders: `src/gtk1/io.py` (`load_anomalies` stock → tolerant-xlrd → truncated-OLE salvage;
`normalize` with explicit column errors). Evgeny NULL rules apply (separate category for
categorical gaps, median for scalars). Schema notes: `docs/DATA.md`. Tuesday stub
`experiments/ingest_tuesday.py` accepts a union table and reports pipe-key join coverage
(self-test: 1.0 clean, 0.846 truncated).
