# GTK1: where will pipeline defects appear next?

[Читать на русском](README_RU.md)

## The task

Gazprom transgaz Tomsk inspects main gas pipelines with diagnostic tools that travel inside
the pipe. Each survey produces tables of metal defects. We use past surveys to predict which
100-meter segments will show new defects in the next survey. Engineers can then inspect and
repair those places first.

## The data: 6 sections, 32 files

Each survey brings a defect table (position, size, depth, type) plus a weld or pipe log.
Files live outside this repo in `../Данные для предварительного изучения/`, one folder per section.

| Section | Surveys (files per year) | Defect rows | Status |
|---|---|---|---|
| Omsk–Novosibirsk 392–526 | 2016, 2021, 2025 (defects + welds each) | 1,907 / 4,455 / 6,598 | Good pairs 2016→2021, 2021→2025 |
| Parabel–Kuzbass-1 572–714 | 2019, 2022, 2025 (defects + welds each) | — / 10,739 / 21,763 (2019: 2,859 good rows, rest missing) | Good pair 2022→2025 |
| Parabel–Kuzbass-2 0–110 | 2015 (defect table + pipe journal), 2020, 2025 (defects + pipe CSV) | 18,337 / 1,026 / — (2025 file broken) | No good pair (format and sensitivity changed, see below) |
| SRTO–Omsk 1608–1717 | 2016, 2021, 2024 (defects + welds each) | 577 / 3,168 / 2,344 | Good pairs 2016→2021, 2021→2024 |
| SRTO–Omsk 1717–1759 | 2016 (8-sheet station file), 2021, 2024 (defects + welds each) | — / 1,451 / 1,220 (2016 mixed file, 2024 repaired copy) | Good pair 2016→2021 |
| Yurga–Novosibirsk 0–154 | 2020 (defects + welds), 2023 (11-sheet report) | 2,621 recovered / 4,400 recovered (both cut short) | No good pair yet (recovery check pending) |

## What defects were found

Rust dominates early surveys everywhere. Weld defects grow in later ones because tools turn
more sensitive:

- Omsk: rust 82% → 66% → 59%; ring-weld defects 128 → 590 → 1,506. Dents show up from 2021 (340, 321).
- Parabel–Kuzbass-1: 2022 is 65% rust; by 2025 weld defects (10,933) pass rust (9,126).
- Parabel–Kuzbass-2: 2015 is 97% rust (17,770 of 18,337, typical depth 5%); 2020 is mixed (55% rust, 16% mechanical, 11% shop defects).
- SRTO-1608: rust 78% → 47% → 30%; weld defects climb 13% → 41% → 53%. Totals fall 2021→2024 (3,168 → 2,344) while tools improve. That reflects changed methods, not healing pipes.
- SRTO-1717-2021: 37% of rows have no type filled in; weld defects lead (496 + 245), rust only 73.
- Yurga–Novosibirsk 2020 (recovered): rust 839, weld 752, factory defects 352. The 2023 journal mixes 1,181 pipe-divider rows in with rust (871), rust clusters (839), and shop defects (735).

Two warnings hold for all of it. Counts jump 2–5× between surveys because tools get more sensitive, not because pipes rot faster. And about half of old defects fail to match again in the next survey, so "new" means newly listed, not necessarily newly grown.

## What we did

Same three steps for every section.

1. Cleaned the tables. One column layout, fixed decimal commas, one depth scale, kept defects at depth 10% or more.
2. Linked defects across surveys. Same pipe plus nearby distance means the same defect seen again. The rest count as newly listed. This step uses past-survey data only.
3. Ranked every 100 m segment by past defect density. Dense places rank high. Checked against the later survey, which the model never saw.

More complex models never beat the simple density ranking by a clear margin, so the simple one ships. Failed attempts are on record in the repo.

## What came out

Top-20 ranked segments that truly showed new defects: 20 of 20 on Omsk, 20 of 20 on Parabel–Kuzbass-1 (49 of top 50), 9 of 20 on SRTO-1608 (few cases there, so bands run wide). Whole-list scores, higher is better, chance level in brackets: 0.644 Omsk (chance 0.268), 0.779 PK1 (chance 0.401), 0.277 SRTO-1608 (chance 0.061), 0.181 SRTO-1717 (chance 0.031, 13 cases).

In plain words, the ranking puts risky segments on top far better than chance, on four independent sections. It is not a physical rust forecast, and it carries no 80% guarantee. Every demo number ships with its warnings printed next to it.

Demo pages with ranked lists, pipeline color maps, and check columns: `triage/triage_demo.html` (Omsk), `triage/triage_pk1.html` (Parabel–Kuzbass-1), `triage/triage_srto.html` (SRTO-1608).

## How to reproduce

```bash
pip install -r requirements.txt
bash run_tests.sh
python3 triage/prospective.py --section on --survey 2021 --check
```

Raw data files never enter git. One committer. Method details: `docs/`. Full history: `PROGRESS.md`.

## What is next

We wait on the partner: repair logs, 5 file re-exports, pipe ages, per-survey thresholds. When the next survey arrives, we set alert thresholds per section and validate the live watchlists (`triage/prospective.py`; `configs/thresholds.yaml` still holds temporary defaults).
