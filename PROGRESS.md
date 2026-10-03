# PROGRESS.md — audit log (append-only)

## 2026-10-03 — Study complete, build started
- Studied: Project_info.md, 6 images, 1 dashboard video (4 frames), 6 sections / 32 files.
- Key findings: 44/45-col anomaly schema (R4 header), pipes 20→30 cols; threshold drift (PK-2 164→9→55/km); Pipe No join 11788/11858, odometer ±2m match 72.6%/53.4%; no persistent SSID; 0% coords; 5 corrupt/truncated files; TECH/ARTD/GOUG code reuse; 2016 Service-life=100y fictive.
- Decision: unit = pipe (join on Pipe No), aggregates 100m/1km; normalize Depth≥10%; longitudinal pairs ON 2016→2021→2025 (reference).
- Scaffolded `gtk1-forecast/` repo; raw data excluded by `.gitignore`.
- Next: cheap ETL diagnostic (ON reference pair), literature sweep, validation spec. No model claims yet.

## 2026-10-03 — Swarm results + first baselines + repo
- Literature (12 sources): GBM-first (HGB/CatBoost, Poisson/Tweedie, hurdle/ZINB), LGCP spatial benchmark, Hawkes exploratory only; no deep sequence without IDs; PR-AUC + recall@fixed-P per Davis/Saito; contractor-as-covariate + per-survey calibration per shift literature.
- ETL diagnostic (ON, read-only): headers R4; normalized Depth≥10% counts 1649/2583/3751; CORR dominates, NaN-depth = weld classes; pipe-join 100% after key normalization (`75.0`→`75`, `а`-suffixes), 11788 overlap, weld25 truncated to 27km — use weld21 as master + flag; presence saturated, growth is honest target.
- Validation spec frozen: train 2016→2021 / test 2021→2025, match rule pipe+2m+0.5m+1h (no Δdepth tie-break), B1/B2/B3 baselines, AP + R@P0.7 (grouped ties, unattained=0.0), F1 threshold from train-CV only, LOSO extension, stop/pivot gates.
- Ran `experiments/e01_baseline.py` (executed, verified): presence AP 0.968/0.992 (≈base, vacuous); growth AP 0.735→0.872, spear 0.785→0.904; HGB-1feat AP 0.729 ≈ persistence (sanity pass). R@P0.7=1.0 flagged as trivial at 70%+ prevalence — operating point must move to P≥0.85 or count target; not claimed as success.
- Repo: `gtk1-forecast/` git init, single committer aayushkrm, private GitHub `aayushkrm/gtk1-pipeline-defect-forecast`, pushed main 32578f0. Raw data excluded by `.gitignore`, only de-identified aggregates committed.
- Next: E05 full-feature HGB + contractor ablation (E06), 100m-vs-1km ablation, matched-label build (pipe+2m) replacing segment-diff proxy, calibration.
- Next: E05 full-feature HGB + contractor ablation (E06), 100m-vs-1km ablation, matched-label build (pipe+2m) replacing segment-diff proxy, calibration.

## 2026-10-03 — Independent review + E02 matched labels (reviewer must-fix #1-2)
- Reviewer verdict (ses_efc9ae210ffeuGJ9sA6umdvnou): segment-diff label FAIL, R@P0.7 vacuous FAIL,
  leakage conditional-PASS on features / FAIL on test-fit threshold, B2/B3 missing FAIL, no CIs FAIL,
  repro FAIL, GO/NO-GO on growth-AP as signal: NO-GO. Top-3 must-fix accepted as work plan.
- Ran `experiments/e02_matched.py` (executed, verified): greedy per-pipe match
  (same pipe + |dd|<=2m + |doff|<=0.5m + |dh|<=1h, cost dd+2doff+0.5dh, no depth tie-break).
  match_rate tr/te 0.404/0.612, collision 0.320/0.398, vanished-frac 0.596/0.388.
  prev matched-new 0.761/0.746 vs segdiff 0.746/0.716; agreement 0.761/0.896.
- Fixed eval: B1 AP 0.945 [0.910,0.974], B2 0.746 (=base), B3 0.787, HGB 0.946 —
  HGB ties (not beats) B1; R@P0.85 B1 0.910 / HGB 0.92; F1@train-thr 0.888; Brier 0.143.
- Honest negative: matched labels did NOT de-saturate prevalence (75% segments positive);
  segment task still too easy; match gap tr/te + 60% vanished confirm method/threshold drift dominates.
  Decision: pivot target to growth-MAGNITUDE / count (P2) or new-in-clean (rare) — presence retired as headline.
  Repro fixed: relative data path, git hash + versions logged in results_e02.json.
- Next: P2 count baseline (Poisson/NB + MAE/Spearman), new-in-clean rare-target check, 100m-vs-1km ablation,
  contractor/threshold-sensitivity analysis, second-section replication (SRTO-1608).

## 2026-10-03 — E03 count + rare-target + grid ablation (pivot test)
- Ran `experiments/e03_count.py` (executed, verified): matched-new COUNTS per segment (not binary).
  Count stats: mean tr/te 10.51/10.10, max_te 132, zero_frac 0.25.
- P2 results: HGB-poisson MAE 8.52 / RMSE 16.05 / spear 0.735 beats mean-train (11.29/18.41)
  and persistence (12.33/27.77); Poisson-GLM explodes (RMSE 93.67 — overdispersion, unregularized).
  First genuine (if modest) MAE lift with matched counts. Spearman ~0.73–0.76 everywhere = count autocorrelation.
- new-in-clean NEGATIVE: clean segments n=51/27, prev new 0.53/0.41 — even clean ground gets
  "new" corrosion ~half the time. Not a rare hard target; confirms sensitivity inflation creates
  newcomers everywhere. Retired as headline; kept as diagnostic.
- Grid ablation (raw presence, limitation: not matched-new): 100m AP_B1 0.821 vs base 0.369
  (lift +0.45, n=1331, pos=491) — DO NOT abandon 100m per stop rule (needs >±0.03 to drop);
  1km 0.961 vs 0.858 (+0.10). 100m has more headroom — candidate P1 grid, but must rebuild
  with matched-new labels before claiming.
- Next: matched-new @100m (honest P1 grid), HGB-count seeds s1/s2 full report + calibration,
  contractor/threshold-sensitivity, SRTO-1608 replication. Reviewer re-check before any large campaign.

## 2026-10-03 — E04 honest P1 @100m + cut sensitivity (pre-registered cut>=10%)
- Ran `experiments/e04_100m.py` (executed, verified), greedy match, past-only features.
  cut>=10%: prev tr/te 0.241/0.268 (not saturated); B1 AP 0.644 [0.595,0.690] vs base 0.268
  (lift +0.38); B3 0.499 < B1; HGB 0.651 / F1@train-thr 0.635 / Brier 0.137 — ties B1 (+0.007, in-CI).
  cut>=15%: prev 0.120/0.083, match 0.248/0.701; B1 0.364 vs base 0.083; HGB 0.357 ≈ B1.
- Reading: 100m matched-new is the first REAL task (base 0.27, lift +0.38 over base).
  No feature lift yet (HGB == persistence) — richer features required for E05
  (depth stats, pipe attributes, weld proximity, wider neighbours).
  Cut-fragility proven (prev 0.27→0.08 across cuts; match gaps) — cut>=10% frozen as primary,
  >=15% as sensitivity only. Vanished-frac/match-gap logged, not hidden.
- Next: reviewer re-check (in flight); then E05 feature-rich HGB vs B1 with ablation,
  SRTO-1608 replication, calibration. No ≥80% claim; operating threshold still open.

## 2026-10-03 — Reviewer round 2 verdict (gates E05)
- (1) E04 @100m: non-saturation real, label validity FAIL — 60%/39% vanished, match gap,
  collision 0.32/0.40. "New" = initiation + misaligned-old + sensitivity gain.
  Frame: operational "newly-reported ≥10%", never physical corrosion. (2) Pre-registration PASS
  as containment, not fix; ranking B1>>base survives both cuts (+0.38→+0.28).
  (3) E03 MAE win = shrinkage not signal FAIL — Spearman flat; need tuned-shrinkage control
  (regularised Poisson/NB, residual-after-B1, shuffle control, all seeds).
  (4) Pivots PASS. (5) Next experiment mandated: matcher×cut robustness matrix + vanished audit
  (dd {1,2,5m} × cuts {8,10,12,15%}, greedy-vs-Hungarian, vanished/new depth histograms,
  repair exclusion) BEFORE any E05.
- GO/NO-GO: (a) 100m matched-new as primary eval task — CONDITIONAL GO (operational framing
  with match-gap/vanished/cut-sensitivity reported); (b) feature-rich E05 — NO-GO until gate passes.
- Next: implement robustness matrix (E04b), then SRTO-1608 replication. E05 stays gated.

## 2026-10-03 — E04b gate result (matcher×cut matrix, executed)
- Matrix @100m matched-new: dd {1,2,5}m makes ZERO difference (identical match/prev/B1 in every
  cut) — distance window is not the binding constraint; pipe+offset/orientation decide.
  Cuts drive everything: prev te 0.27→0.27→0.18→0.08; match te 0.64→0.61→0.66→0.70, tr 0.36→0.40→0.35→0.25.
  B1 lift survives all cuts: +0.37/+0.38/+0.37/+0.28 over base (0.640/0.644/0.546/0.364).
- Greedy-vs-Hungarian agree 0.898, same match rate 0.612 — matcher choice not critical (10% disagree logged).
- Depths base10: med matched 12.0 / new-corr 11.0 / past 13.0 — new slightly shallower,
  consistent with initiation + sensitivity gain. Clean vanished-row depth audit still open
  (forward matcher flags future rows only; vanished-frac 0.60/0.39 from E02 stands) — flagged, not hidden.
- Gate ruling: ranking robust across dd and cuts; absolute numbers cut-conditional.
  CONDITIONAL PASS → operational "newly-reported ≥10% @100m" confirmed as primary eval task.
  Next in reviewer order: SRTO-1608 replication (E05 = replication, not feature-rich). E05-features stay gated.

## 2026-10-03 — E05 SRTO-1608 replication (frozen pipeline, external test, executed)
- Counts (Depth>=10): 462/786/1263 — far sparser than ON. .xls read via xlrd, same R4 schema.
  train 2016->2021: match 0.368, prev 0.101 (105 pos), B1 0.530 vs base 0.101 (lift +0.43).
  test 2021->2024: match 0.551, prev 0.061 (63 pos), B1 0.277 vs base 0.061 (lift +0.22). B3 < B1 both pairs.
- Reading: ranking B1>>base REPLICATES on a second section (qualitative PASS), exactly the
  predicted pattern — preserved rank-order with lower absolute AP on sparser ground.
  Per-s Ludwig: recalibrate threshold per section, do not pool. Small-n warning: 63 positives →
  wide CIs (to be added); no success claimed beyond replication of ranking.
- Next: reviewer round 3 (E04b+E05); tuned-shrinkage control for E03 (regularised Poisson/NB +
  residual/shuffle); then small E05-feature ablation ONLY if reviewer releases the gate.

