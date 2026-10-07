# GTK1: where will pipeline defects appear next?

[Читать на русском](README_RU.md)

## The task

Gazprom Tomas Tomsk inspects main gas pipelines with in-line diagnostic tools. Each survey
produces tables of metal defects. We use past surveys to predict which 100-meter segments will
show new defects in the next survey. Engineers can then inspect and repair those places first.

## What data we had

Six pipeline sections, surveyed 2 to 3 times each between 2015 and 2025. Each survey gives an
anomaly table (defect position, size, depth, type) plus a weld and pipe log. Files live outside
this repo in `../Данные для предварительного изучения/`, one folder per section.

Not all data is usable. Five files needed repair parsing. Two sections cannot
form a valid past-to-future pair. Parabel–Kuzbass-2 changed table format and sensitivity between
surveys. Yurga–Novosibirsk files open in Excel and Numbers (those apps repair silently), but they
hold partial data: the 2020 anomalies cover 0–37 km of a 151 km section, and the 2023 journals are
mostly garbled (4,400 clean rows to about 26 km). Recovery continues. Full detail:
`docs/DATA.md`.

## What we did

Three steps, same for every section.

1. Cleaned the tables. Unified columns, fixed decimal commas, converted everything to one depth
   scale, kept only defects at depth ≥ 10%.
2. Linked defects across surveys. Same pipe plus nearby distance means the same defect seen again.
   The rest count as newly reported. This step is strict: it uses only past-survey information.
3. Ranked every 100 m segment by past defect density. Dense places rank high. Checked the ranking
   against the later survey, which the model never saw.

We also tested fancier models (gradient boosting, logistic regression). None beat the simple
density ranking convincingly, so the simple one ships. Failed attempts are documented, not hidden.

## What came out

On the Omsk section, 20 of the top 20 ranked segments truly showed new defects in 2025.
On Parabel–Kuzbass-1, the same: 20 of 20, plus 49 of the top 50. Overall ranking quality
(AP, higher is better): 0.64 on Omsk (base rate 0.27), 0.78 on Parabel–Kuzbass-1 (base 0.40),
0.28 on SRTO–Omsk 1608 (base 0.06), 0.18 on SRTO 1717 (base 0.03, only 13 cases).

What this means in plain words: the ranking puts risky segments at the top far better than
chance, on four independent sections. What it does NOT mean: this is not a physical corrosion
forecast and not an 80% guarantee. Counts jump between surveys because tools get more sensitive,
and about half of old defects fail to re-match. Every number on the demo pages ships with these
caveats printed next to it.

Demo pages with ranked lists, pipeline heatmaps, and audit columns: `triage/triage_demo.html`
(Omsk), `triage/triage_pk1.html` (Parabel–Kuzbass-1), `triage/triage_srto.html` (SRTO-1608).

## How to reproduce

```bash
pip install -r requirements.txt
bash run_tests.sh
python3 triage/prospective.py --section on --survey 2021 --check
```

Raw data files never enter git. One committer. Method details: `docs/`. Full history: `PROGRESS.md`.

## What is next

We wait on the partner: repair logs, 5 file re-exports, pipe ages, per-survey thresholds.
When the next survey arrives, we calibrate per-section alert thresholds and validate the live
watchlists (`triage/prospective.py`, `configs/thresholds.yaml` still placeholder).
