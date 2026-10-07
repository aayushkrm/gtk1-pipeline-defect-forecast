# GTK1: where will pipeline defects appear next?

[Читать на русском](README_RU.md)

## The task

Gazprom transgaz Tomsk inspects main gas pipelines with in-line diagnostic tools. Each survey
produces tables of metal defects. We use past surveys to predict which 100-meter segments will
show new defects in the next survey. Engineers can then inspect and repair those places first.

## The data: 6 sections, 32 files

Each survey brings an anomaly table (defect position, size, depth, type) plus a weld or pipe log.
Files live outside this repo in `../Данные для предварительного изучения/`, one folder per section.

| Section | Surveys (files per year) | Anomaly rows | Status |
|---|---|---|---|
| Omsk–Novosibirsk 392–526 | 2016, 2021, 2025 (anomalies + welds each) | 1,907 / 4,455 / 6,598 | Valid pairs 2016→2021, 2021→2025 |
| Parabel–Kuzbass-1 572–714 | 2019, 2022, 2025 (anomalies + welds each) | — / 10,739 / 21,763 (2019: 2,859 clean rows, tail absent) | Valid pair 2022→2025 |
| Parabel–Kuzbass-2 0–110 | 2015 (defect table + pipe journal), 2020, 2025 (anomalies + pipe CSV) | 18,337 / 1,026 / — (2025 file corrupt) | No valid pair (schema + sensitivity break, see below) |
| SRTO–Omsk 1608–1717 | 2016, 2021, 2024 (anomalies + welds each) | 577 / 3,168 / 2,344 | Valid pairs 2016→2021, 2021→2024 |
| SRTO–Omsk 1717–1759 | 2016 (8-sheet station file), 2021, 2024 (anomalies + welds each) | — / 1,451 / 1,220 (2016 mixed file, 2024 repaired copy) | Valid pair 2016→2021 |
| Yurga–Novosibirsk 0–154 | 2020 (anomalies + welds), 2023 (11-sheet report) | 2,621 salvaged / 4,400 salvaged (both truncated) | No valid pair yet (salvage validation pending) |

## What defects were found

Corrosion dominates early surveys everywhere, then weld anomalies surge as tools get more sensitive:

- Omsk: corrosion 82% → 66% → 59%; girth-weld anomalies 128 → 590 → 1,506. Dents appear from 2021 (340, 321).
- Parabel–Kuzbass-1: 2022 is 65% corrosion; by 2025 weld anomalies (10,933) pass corrosion (9,126).
- Parabel–Kuzbass-2: 2015 is 97% corrosion (17,770 of 18,337, median depth 5%); 2020 is mixed (55% corrosion, 16% mechanical, 11% technological).
- SRTO-1608: corrosion 78% → 47% → 30%; weld anomalies rise 13% → 41% → 53%. Totals fall 2021→2024 (3,168 → 2,344) while sensitivity rises, a methodology artifact, not healing.
- SRTO-1717-2021: 37% of rows have empty type; weld anomalies lead (496 + 245), corrosion only 73.
- Yurga–Novosibirsk 2020 (salvaged): corrosion 839, weld 752, mill defects 352. 2023 journal mixes in 1,181 pipe-separator rows among corrosion (871), corrosion clusters (839), and tech defects (735).

Two warnings run through all of it. Counts jump 2–5× between surveys because tools get more sensitive, not because pipes rot faster. And about half of old defects fail to re-match in the next survey, so "new" means newly reported, not necessarily newly grown.

## What we did

Same three steps for every section.

1. Cleaned the tables. Unified columns, fixed decimal commas, one depth scale, kept defects at depth ≥ 10%.
2. Linked defects across surveys. Same pipe plus nearby distance means the same defect seen again. The rest count as newly reported. This step uses past-survey data only.
3. Ranked every 100 m segment by past defect density. Dense places rank high. Checked against the later survey, which the model never saw.

Fancier models (gradient boosting, logistic regression) never beat the simple density ranking convincingly, so the simple one ships. Failed attempts are documented, not hidden.

## What came out

Top-20 ranked segments that truly showed new defects: 20 of 20 on Omsk, 20 of 20 on Parabel–Kuzbass-1 (49 of top 50), 9 of 20 on SRTO-1608 (sparse ground, wide bands). Overall ranking quality (AP, higher is better): 0.644 Omsk (base 0.268), 0.779 PK1 (base 0.401), 0.277 SRTO-1608 (base 0.061), 0.181 SRTO-1717 (base 0.031, 13 cases).

Plain meaning: the ranking puts risky segments on top far better than chance, on four independent sections. Not meaning: physical corrosion forecast, and no 80% guarantee. Every demo number ships with its caveats printed next to it.

Demo pages with ranked lists, pipeline heatmaps, and audit columns: `triage/triage_demo.html` (Omsk), `triage/triage_pk1.html` (Parabel–Kuzbass-1), `triage/triage_srto.html` (SRTO-1608).

## How to reproduce

```bash
pip install -r requirements.txt
bash run_tests.sh
python3 triage/prospective.py --section on --survey 2021 --check
```

Raw data files never enter git. One committer. Method details: `docs/`. Full history: `PROGRESS.md`.

## What is next

We wait on the partner: repair logs, 5 file re-exports, pipe ages, per-survey thresholds. When the next survey arrives, we calibrate per-section alert thresholds and validate the live watchlists (`triage/prospective.py`, `configs/thresholds.yaml` still placeholder).
