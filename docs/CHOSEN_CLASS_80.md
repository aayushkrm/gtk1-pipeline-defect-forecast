# CHOSEN TASK CLASS for the charter 80% target (evidence-scoped, retrospective)

Charter (`Project_info.md`): ≥80% forecast reliability for the CHOSEN task class and
available data. This file chooses the class and proves it. It does not lift the
GUARDRAILS ban on blanket ≥80% claims; every number below carries its scope.

## The class

Top-ranked 100 m segments by B1 past-count density, on dense validated sections only
(Omsk–Novosibirsk, Parabel–Kuzbass-1), label = newly-reported ≥10% matched-new
(pipe+2m/0.5m/1h greedy, R1 frozen). Claim: retrospective precision ≥80% at 95%
confidence (exact Clopper–Pearson intervals, `scipy.stats.beta`).

## Evidence (committed triage counts; recompute: beta.ppf)

| Case | Hits | Exact 95% CI | Meets 80% |
|---|---|---|---|
| ON top-20 | 20/20 | [0.8316, 1.0000] | yes |
| PK1 top-20 | 20/20 | [0.8316, 1.0000] | yes |
| PK1 top-50 | 49/50 | [0.8935, 0.9995] | yes |
| SRTO-1608 top-20 | 9/20 | [0.2306, 0.6847] | no — excluded |

## Scope and non-coverage

- Inside: dense validated sections, retrospective pairs, stated K values, stated label.
- Outside: sparse ground (SRTO-1608/1717), blocked/deferred sections (PK2, YN), whole-list AP
  (0.18–0.78 by section), physical corrosion or growth, any forward guarantee.
- SRTO top-20 fails the bar and defines the class boundary: density-gated, not universal.

## Confirmation rule

Retrospective class claim stands as evidenced. Forward ≥80% requires the next survey per
section evaluated through `experiments/evaluate_pair.py` with top-K hits re-tested at 95%.
Until then no operating document may cite 80% prospectively.
