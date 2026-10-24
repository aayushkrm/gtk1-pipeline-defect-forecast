# CHARTER_ASSESSMENT_NPK: the 80% target on the October 2026 archive

## The target and the rule

The charter asks for at least 80% forecast reliability for the chosen task class on the
available data. The repo reads this as a scoped, retrospective precision claim at top-K
(`docs/CHOSEN_CLASS_80.md`), not as a blanket or forward guarantee. A positive claim needs
all four gates from `docs/GUARDRAILS.md`: R1 frozen pipeline, R2 source-grade input, R3
stationarity screen, and R4 lift-CI lower above zero with at least 30 positives.

## What the new archive adds

`Датасет НПК.rar` is the authoritative re-export of the Parabel–Kuzbass corridor. It holds
18 anomaly files across 2016–2025, with 2021 and 2023 absent. It adds trunk sections at
0–110, 111.2–242, 242–404, and 406–572 km, and branch lines at 0–14, 0–36.6, 0–71, 14–22,
0–10, 0–3.8, 0–21.7, 3.8–5.4, and 0–91 km. The 572–714 km section is the same section as
the old PK1 card.

Five candidate pairs exist. One passes R1–R4. The rest fail the join gate or R3. The
dataset card records the full inventory (`docs/DATASET_NPK.md`).

## The clean pair

`main572_2022_2025`: 572–714 km, 2022 survey → 2025 survey. Past and future frames use
the frozen R1 pipeline: depth ≥10%, pipe+2 m/0.5 m/1 h greedy match, 100 m cells, B1
past-count score.

| Cut | Positives | Prevalence | AP | Base | Lift 95% CI | Match | P@20 | P@50 |
|---:|---:|---:|---:|---:|---|---:|---:|---:|
| ≥10% (primary) | 558 | 0.3960 | 0.7778 | 0.3960 | +0.3517…+0.4109 | 0.725 | 20/20 | 48/50 |
| ≥12% | 333 | 0.2363 | 0.5710 | 0.2363 | +0.2901…+0.3855 | 0.728 | 17/20 | 41/50 |
| ≥15% | 135 | 0.0958 | 0.3551 | 0.0958 | +0.1869…+0.3366 | 0.705 | 12/20 | 26/50 |

Exact Clopper–Pearson 95% intervals:

| Cut | P@20 | Exact 95% CI | P@50 | Exact 95% CI |
|---:|---:|---|---:|---|
| ≥10% | 20/20 | [0.8316, 1.0000] | 48/50 | [0.8629, 0.9951] |
| ≥12% | 17/20 | [0.6211, 0.9679] | 41/50 | [0.6856, 0.9142] |
| ≥15% | 12/20 | [0.3605, 0.8088] | 26/50 | [0.3742, 0.6634] |

At the primary cut, both top-20 and top-50 meet the 80% bar at 95% confidence. At ≥12% and
≥15%, the top-20 and top-50 lower bounds fall below 0.80. The 80% claim is therefore
specific to the primary cut.

The corrosion-only variant at cut ≥10% gives AP 0.7792, P@20 20/20, P@50 48/50, and lift
CI +0.3510…+0.4103. The boundary-cell exclusion leaves AP 0.7778 and the same top-K
counts. The result is not driven by non-corrosion rows or by the last cell.

## Replication of the old PK1 result

The old PK1 2022→2025 pair reported 562 positives, prevalence 0.4011, AP 0.7795, top-20
20/20, and top-50 49/50. The new archive gives 558 positives, prevalence 0.3960, AP
0.7778, top-20 20/20, and top-50 48/50. The difference is four cells and −0.0017 AP.

This is a source re-export of the same section and the same survey pair. It is a
replication of the frozen result on the authoritative file, not an independent sample.
It confirms the old number. It does not widen the evidence base.

## What does not count

- `branch720_2016_2024`: 720 mm branch, 2016 → 2024. AP 0.6930, base 0.4978, lift CI
  +0.1629…+0.2304, P@20 18/20, P@50 46/50. R4 passes. R3 fails: the future survey is
  4.57× denser (1,431 → 6,542 frame ≥10 rows) and the match rate is 0.170, below the 0.20
  screen. The top-20 exact CI is [0.6830, 0.9877], so the lower bound is below 0.80 even
  without R3. This pair is suggestive only. It is not replication evidence.
- `branch720_2022_2024`: 0–21.7 km → 0–91 km. The extents differ, the pipe index shifts,
  and the match rate is 0.000. The density ratio is 5.314 and AP is 0.5705. The pair is
  void.
- `main242_2017_2020`: PK2 242–404. Only 8.9% of past pipes appear in the future file,
  the match rate is 0.000, the density ratio is 4.03, and the lift CI crosses zero
  (−0.0014…+0.0085). The pair is void. PK2 stays deferred.
- `main110_2019_2020`: 0–110 km. Only 3.4% of past pipes appear in the future file, the
  match rate is 0.000, the density ratio is 2.51, and the lift CI crosses zero
  (−0.0024…+0.0200). The pair is void.

The branch pair's corrosion-only sensitivity raises the match rate to 0.367 and keeps AP
0.6923 with lift CI +0.1602…+0.2269. That is evidence that the branch corrosion signal is
coherent. It does not change the R3 verdict, because R3 is defined on the frozen
full-frame pipeline.

## Verdict

The charter target is met in the scoped, retrospective sense defined in
`docs/CHOSEN_CLASS_80.md`:

- Section: Parabel–Kuzbass-1, 572–714 km.
- Pair: 2022 → 2025.
- Label: newly-reported ≥10% matched-new, pipe+2 m/0.5 m/1 h greedy.
- Claim: retrospective top-20 precision 20/20 (95% CI lower 0.8316) and top-50 precision
  48/50 (95% CI lower 0.8629).

The target is not met as a blanket claim, not forward, not at cut ≥12% or ≥15% for top-20
or top-50, not on the 720 mm branch, and not on PK2. The new archive confirms the old PK1
result but adds no second clean section. The scoped class in `docs/CHOSEN_CLASS_80.md`
remains the correct reading of the charter.

## What would change the verdict

- A clean pair on PK2 or on a branch line that passes R3 and R4.
- A forward survey for 572–714 km evaluated through the same frozen pair evaluation
  (`experiments/npk_pairs.py` for this archive; `experiments/evaluate_pair.py` for the old
  tree) with exact top-K intervals.
- Stable pipe numbering across the 2017→2020 or 2019→2020 surveys, which would reopen
  those pairs for a join-gate retest.

Until then, no operating document may cite 80% prospectively, and no page may drop the
scope line.

## Disclaimer

> "New = unmatched future ≥10% row under pipe+2m/0.5m/1h match; includes re-detection.
> Absolute AP is cut- and survey-conditional."

For the clean pair: match-rate 0.725; vanished-frac (non-match share) 0.275; cut
sensitivity ≥10% / ≥12% / ≥15% as in the table above. The vanished-frac here is the share
of past ≥10% rows with no future ≥10% match under the frozen greedy past→future matcher.
It is not the E08 reverse-greedy corr-only audit.
