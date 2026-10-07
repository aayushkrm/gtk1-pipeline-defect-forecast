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

## 2026-10-03 — Reviewer round 3 + E06 shrinkage + E05b lift CI + guardrails
- Round-3 verdict: E04b PARTIAL PASS for task, NO-GO E05-features stands (vanished-row depth audit
  + repair exclusion still open); E05 "hypothesis, not finding" until one number: 95% CI lower bound
  on test lift; operational framing CONDITIONALLY acceptable with 3 mandatory guardrails;
  small feature ablation CONDITIONAL GO with 3 controls (train-only, beat-B1+shuffle, CIs+sensitivity).
- E06 (executed, verified): C1 tuned Poisson still explodes (21.27); C2 log-Ridge MAE 6.48 / RMSE 12.85 /
  spear 0.772 BEATS HGB-poisson 8.52/16.05/0.735; C3 calibrated-B1 8.87 (≈HGB, residual -0.36);
  C4 shuffle 11.5–12.9 ≈ mean (pipeline sane, features carry signal). Conclusion: best count model
  is log-linear, not HGB — E03 HGB quarantined per docs/GUARDRAILS.md, parsimony wins.
- E05b (executed, verified): SRTO test lift 0.216 CI95 [0.130,0.333], lower>0; train 0.429 [0.338,0.525].
  Reviewer's criterion MET → replication of ranking confirmed (absolute AP still section-conditional).
- Added docs/GUARDRAILS.md: newly-reported naming, per-page disclaimer, per-section thresholds,
  quarantine rules. Adopted going forward (old filenames kept for provenance, noted here).
- Next: small ablation (5–8 pre-registered features, ON, SRTO held out) with reviewer's 3 controls;
  vanished-row depth audit + repair exclusion in parallel.

## 2026-10-03 — E07 relaunched (background) + E08 vanished audit done
- E07 run was interrupted twice in foreground; script intact (untracked), no partial results.
  Relaunched in background (sh_10480db7f001B9kFXaBWHioz5n); recording on completion notification.
- E08 (executed, verified, reverse greedy match, cut>=10, corr-only):
  train vanished_frac 0.369, test 0.114 (past-side; forward-side 0.596/0.388 from E02 — asymmetry
  expected: future sets are larger). Matched vs vanished medians IDENTICAL (12/12 train, 13/13 test):
  vanished are NOT shallower — misses look depth-random (re-detection jitter), not threshold dropout.
  Deep-vanished tail30: train 0.028 vs matched 0.004 (small repair-suspect excess), test 0.016 vs 0.037
  (no excess). Repair logs absent from VTD package — exclusion pending partner data (dependency logged).
- Next: commit E08; on E07 completion notification → record + push; reviewer round 4 over E06/E07/E08.

## 2026-10-03 — E07 ablation done (first significant Δ vs B1, with caveats)
- Background run completed; artifacts verified (results_e07.json: features+3 cuts+repro).
  cut>=10%: LR 0.676 vs B1 0.644, Δ=+0.032 CI [+0.011,+0.053] (lower>0); HGB 0.652 Δ=+0.008 [-0.017,+0.033] (tie).
  cut>=12%: LR 0.586 Δ=+0.040 [+0.014,+0.063] (replicates); HGB Δ=+0.034 [-0.003,+0.069] (borderline).
  cut>=15%: LR 0.340 vs B1 0.364, Δ=-0.024 (negative; sparse, prev_te 0.083) — features fail where
  positives are few. F1@train-thr 0.638/0.590/0.440; Brier 0.138/0.106/0.074.
- ANOMALY (not hidden): shuffle-control AP 0.336/0.289/0.136 sits ABOVE base (0.268/0.181/0.083).
  Near-constant predictor should score ≈base; +0.07 excess unexplained (chance transfer from
  1331×7 noise fit, or intercept/threshold artifact). LR lift (+0.032) therefore treated as
  provisional — small effect + shuffle excess = caution, not a win claim.
- Ablation "weakest-dropped" output ambiguous (dropped-subset deltas vs B1, not vs full) — schema
  to be fixed in E07b if rerun; strongest-driver question still open.
- Next: reviewer round 4 (E06/E07/E08) — questions: (a) is +0.032 with shuffle excess publishable
  internally as signal? (b) E05-features gate status? (c) deliverable framing for December?

## 2026-10-03 — Reviewer round 4: lift downgraded, gate shut, deliverable spec set
- (a) +0.032 NOT publishable: shuffle−base excess (+0.068/+0.108/+0.053) exceeds the lift at every cut —
  null uncalibrated, CIs uninterpretable; one permutation is not a null. Deciding controls mandated:
  constant-predictor check (must equal base ±0.005), N≥100 shuffle null, paired CI of Δ vs
  mean(shuffle) with C frozen by train-CV. C-selection confirmed train-only (StratifiedKFold on
  train in e07_ablation.py — suspicion rebutted, frozen-C rule adopted regardless).
- (b) E05-features (≤12) still NO-GO: E04b conditional-pass stands, E05 licenses task not features,
  E08 helps framing but repair exclusion open, E07 beat-shuffle FAIL + sensitivity partial-FAIL +
  ablation schema broken. Permitted: E07b at frozen ≤7 with all fixes + SRTO holdout of LR lift.
- (c) Honest December deliverable: calibrated triage tool (rank 100m segments, heatmap + uncertainty
  + audit columns, per-section thresholds, GUARDRAILS disclaimer on page); ON AP ~0.65±0.05 (~2.4× base);
  count MAE ~6.5 log-linear; NO red/green badges, NO ≥80% meter. This is what the evidence supports.
- Next: E07b (constant-check + 100-shuffle null + ablation-vs-full + SRTO holdout), then re-apply for gate.

## 2026-10-03 — Reviewer round 5 (SPLIT verdict) + E09 killer control launched
- (1) Calibrated null rehabilitates pipeline-sanity only, NOT the +0.03 value-add (Δ-vs-null is the
  wrong comparison; B1 already beats base +0.38). +0.032 stays "real-but-tiny-and-local".
- (2) SPLIT gate: B1 primary ACCEPT everywhere; LR-nlag general NO-GO; ON-only experimental
  CONDITIONAL GO (shadow/off-by-default + kill-switch + disclaimer; SRTO dCI includes +0.032 so it
  fails to confirm transfer rather than excluding it — hence default-off mandatory).
- (3) Killer control mandated: spatial-block CV within ON (leave-contiguous-third-out, frozen ≤7/C).
  If nlag Δ collapses ≤0 → proximity/survey-streak leakage, overlay dead even ON-only.
  E09 implemented + launched in background (sh_10489fa9d001bViS3wZUSWZLOd). December builds on B1
  primary regardless; overlay stays non-default until E09 passes.
- (4) TRIAGE_SPEC numbers updated to reviewer's exact qualifier text (B1 0.644 / LR 0.676 ON;
  B1 0.277 / LR 0.281 SRTO; count MAE 6.5 unchanged). No ≥80% claim.

## 2026-10-03 — E09 block-CV done: kill condition NOT met, confirmation weak (heterogeneous)
- Background run completed; artifacts verified. Fold deltas (LR−B1): +0.032 [+0.001,+0.062] (pos=178),
  +0.011 [−0.035,+0.049] (pos=109), +0.005 [−0.055,+0.071] (pos=70). No fold ≤0 → proximity-leakage
  death sentence NOT triggered; but 2/3 CIs cross 0 and effect tracks positivity (denser third holds,
  sparse thirds tie). Fold CIs mutually overlap and overlap global +0.032 — no contradiction, no confirmation.
- Ruling (mine, reviewer re-check invited): overlay stays ON-only experimental / off-by-default;
  B1 primary for December unchanged. The +0.03 is now characterized, not killed and not promoted:
  dense-ground spillover signal, sparse-ground unproven. TRIAGE_SPEC headline (AP ~0.65±0.05 ON) untouched.
- Next: build the triage-tool prototype on B1 primary (ranked 100m list + heatmap + audit columns +
  per-section thresholds + GUARDRAILS disclaimer); overlay branch kept off-by-default with kill-switch.

## 2026-10-03 — Reviewer round 6 (CONDITIONAL GO) + triage prototype v0 launched
- Ship review: methodologically safe under freeze (past-only B1, frozen labels, no re-tuning;
  ranking threshold-free); P@K secondary only with base comparator + bootstrap CI + GUARDRAILS triple
  + "test spent" label; unshippable omission = missing operational definition on-page (banned badges
  already out); BUILD NOW (repair logs block only stronger claims; vanished contamination bounded E08).
- Prototype `triage/build_report.py` implements all conditions: retrospective ON B1 ranking, SVG heatmap,
  top-20 audit table, P@K with bootstrap CI + base, full triple (match-rate, vanished 0.596/0.388,
  cut-sensitivity 0.644/0.546/0.364), git hash in JSON, overlay OFF. Launched in background
  (sh_104905696001ODnSxWUzys2Vwf); outputs recorded on completion only.

## 2026-10-03 — Triage prototype v0 built (B1, deterministic re-run confirmed)
- Background run completed: AP=0.644 live == frozen E04 (deterministic regeneration, no re-tuning).
  P@10=1.000 [1.000,1.000], P@20=1.000 [0.950,1.000], P@50=0.960 [0.900,1.000], base 0.268, match 0.612.
  Artifacts verified: 120KB HTML (heatmap SVG + top-20 audit + P@K + full triple + disclaimer +
  kill-switch note), JSON with git hash 80672f3.
- Status: first end-to-end deliverable increment exists (retrospective demo, ON only). Prospective use
  requires next-survey data + per-section recalibration — stated on page. Overlay still OFF.
- Next: reviewer round 7 (prototype audit: display honesty, P@K framing, ship-readiness);
  PK1/SRTO-1717 scoping for third-section evidence; partner data requests outstanding.

## 2026-10-03 — Round 7 (CONDITIONAL GO, fixes applied) + third-section scoping (no GO w/o repair)
- Prototype audit: frozen re-run PASS, operational definition PASS, no badges PASS; P@K block
  PARTIAL FAIL (match-rate missing on-page — fixed: "Match-rate (test, forward, E02): 0.612" added).
  Required caption inserted verbatim + denominators (10/10, 20/20, 48/50) + K display-chosen note.
  Regenerated deterministically (AP 0.644 identical, git ea7713d); all strings verified on-page.
  K=10/20/50 showcase noted as display-chosen (threshold-free ranking, not label leak).
- Scoping (read-only recon): SRTO-1717 (2016/21/24) CAUTION-best (openable R4 + weld logs all years;
  2024A corrupt-but-salvageable; ~40 pos segs/survey; 2021 covers ~30km); PK2 (2015/20) CAUTION
  (schema break + threshold shift, 2025A dead); PK1 NO-GO as pair (only 2022A opens);
  YN NO-GO (zero usable anomaly surveys). No GO without repair work. Repair queue: PK1-2019A+2025A
  (unlocks best dataset) → SRTO-2024A (salvageable) → PK2-2025A → YN (worst).
- Next: SRTO-1717 2016→2021 replication attempt (sparse, SRTO-1608-like CIs expected);
  repair-attempt spike on PK1-2019A (timeboxed, salvage-parser reuse).

## 2026-10-03 — Repair spike done + E10 third-section replication (3/3 sections replicate ranking)
- Salvage verdict (timeboxed, read-only): PK1-2019A NO-GO (45.8% — rows 2864+ absent, unrecoverable;
  2,859 pristine rows km 0–45 kept as partial supplement); PK1-2025A GO (99.4% via tolerant loader).
  Revised: PK1 2022→2025 pair fully viable (densest, 1093 segs); 2019→2022 partial on 0–45km viable.
- E10 SRTO-1717 2016→2021 (executed, frozen pipeline): counts d≥10 113/92, match 0.261, prev 0.031
  (13 pos), B1 0.181 vs base 0.031, liftCI [0.024,0.415] lower>0. Caveats: 2021 covers ~30/42km;
  KP-2016 mixed provenance. Ranking replicates 3/3 sections (ON, SRTO-1608, SRTO-1717).
- Next: PK1 2022→2025 replication (tolerant loader, densest test — strongest generalization check yet);

## 2026-10-06 — Research swarm: 4 tracks, 49 sources, all committed
- (INDEX extended with wave 2 below.)

## 2026-10-06 — Research wave 2: 4 tracks, ~50 sources, all committed
- (Wave 3 partial + completion below — 12 tracks total now indexed.)

## 2026-10-06 — Research wave 3 complete: 12 tracks indexed
- Tracks 10/11/12 banked earlier; track 9 (benchmarks) landed on its completion notification and is
  now indexed + committed (Mendeley sandbox URLs, C-MAPSS smoke test, baseline anchors, synthetic stack).

## 2026-10-06 — Research wave 4: 4 tracks banked (16 total); tool question answered honestly
- (Wave 5 below — 20 tracks total now indexed.)

## 2026-10-06 — Research wave 5: providers confirmed keyed, 4 tracks banked (20 total)
- (Wave 6 below — 24 tracks total now indexed.)

## 2026-10-06 — Research wave 6: direct-Exa verified live, 4 tracks banked (24 total)
- (Style audit below — full coverage verified.)

## 2026-10-07 — Style audit: full coverage confirmed, 2 scanner artifacts, 0 real violations
- (Humanizer pass below — both laws now enforced.)

## 2026-10-07 — Humanizer pass: ~100 tells removed, facts intact, tests green
- (Coverage clarification below.)

## 2026-10-07 — Coverage note: 6 studied, 4 validated (README clarified EN+RU)
- (Direct audit below — numbers re-derived by hand, one wording tightened.)

## 2026-10-07 — Direct audit of the 6-section table: all claims verified, 1 precision fix
- (Yu-N salvage counts below.)

## 2026-10-07 — Yu-N salvage: 2023 journals recovered, pair validation queued (E15)
- (User-verified endpoints below.)

## 2026-10-07 — User independently confirmed Yu-N coverage in Numbers
- (Round-14 closure below — re-analysis objective COMPLETE.)

## 2026-10-07 — Round 14: re-analysis objective COMPLETE (GO, residuals named)
- (Yu-N hard check below — 14/14.)

## 2026-10-07 — Yu-N hard check: 14/14 CONFIRMED, zero corrections
- (README rebuild below — full tables from re-derived distributions.)

## 2026-10-07 — READMEs rebuilt: 6-section inventory + defect mix, all numbers re-derived
- (Plain-language pass below for non-technical readers.)

## 2026-10-07 — READMEs simplified for supervisor (humanizer, jargon out)
- Technical terms replaced with plain words (rust for corrosion, chance level for base, color maps
  for heatmaps); scores read as "0.644 vs 0.268 chance". All numbers unchanged and verified.
  Both languages. Tests green.
- `experiments/char_dist.py` measured all 13 readable survey slices fresh (one loader-keyword bug
  found and fixed mid-run; YN slices passed first try). Every share in both READMEs divides out
  from those counts (spot-verified: ON GWAN 128/590/1506, PK1-25 GWAN>corr, SRTO inversion,
  PK2 97%, SRTO-1717 37% empty, YN mixes). Caught one draft error pre-commit (PK1 P@50 49/50).
- `experiments/verify_yn_hard.py` re-derived every Yu-N number: 3 sheets, strict-parse failure,
  2,621 salvaged rows to 37,215.645 m, monotonic, weld log 14,095 rows to 151,492.155 m, 100.0%
  anomaly-to-weld join within 12 m, 11 sheets, pipe log 14,160×10, 4,400 salvaged rows to
  25,655.079 m, out-of-range depths present, 21,015 feature rows. Endpoints match the user's
  Numbers readings to the meter.
- One variance noted honestly: depth garbage max reads 72,259 here vs 137,609 in E15 salvage —
  different column alignment on garbled rows. Both prove out-of-range content; the claim
  "garbage present" is parse-invariant, the exact max is not. Pair verdict unchanged (BLOCKED).
- Ledger: every README/DATA/TRIAGE_SPEC number derived; two stale wordings synced (DATA olefix
  status, E15 tally 24/6/0). YN BLOCKED rests on two readers + re-parse. E14 void stands with
  bit-identical reproducibility. 4/4 tally, R1–R4, 0 DEAD files.
- Residuals (external/prospective only): partner repair logs + re-exports + ages + thresholds;
  next-survey prospective confirmation with per-section recalibration; HGB/LR seed-frozen fits;
  shared-RNG CI order dependence. None blocks COMPLETE — all are named with next checks.
- Supervisor sentence: re-ran every number from raw files, fixed drift/offset/band/tail/denominator/
  equality/tally errors, proved B1 ranking on 4/4 clean pairs with YN blocked for evidenced data
  reasons; only partner re-exports plus next-survey confirmation remain.
- Anomaly end: 37,215 m. Weld-log end: 151,492 m. 2023 journal end: 25,655 m; only 8 rows share
  d=33.3 (no mass fill; earlier suspicion from the screenshot withdrawn).
- All three match salvage exactly. README endpoints updated to exact values in both languages.
  Pair verdict unchanged (E15 validation pending), now co-verified by two independent readers.
- (Triple re-verification below — every repo number rechecked.)

## 2026-10-07 — Triple re-verification: 3 swarms, corrections applied, 1 loss logged
- (Recompute recompute_verify below — NN + AP outputs re-derived.)

## 2026-10-07 — Recompute: NN rates CONFIRMED (raw), E05/E10 AP exact, one false alarm owned
- (E12 independent recompute below — second strict-equality false alarm, tolerance verdict.)

## 2026-10-07 — E12 recompute: CONFIRMED within reporting precision
- (olefix breakthrough below — DEAD verdict overturned.)

## 2026-10-07 — olefix breakthrough: PK1-2025 weld log RECOVERED (DEAD → RECOVERABLE)
- (Queue cleared below — both items landed same turn.)

## 2026-10-07 — Queue cleared: YN E15 PAIR-BLOCKED ( evidenced ), E14 RE-DERIVED bit-identical
- (Supervisor-readable rewrite below.)

## 2026-10-07 — READMEs rewritten for supervisor (plain language, EN+RU)
- Old README relied on jargon. Both versions now read: task, data, 3 steps, concrete outcomes
  (top-20 hits, AP table), plain meaning plus non-meaning, reproduce, next steps. Humanizer applied.
- Caught and fixed my own draft error: PK1 P@50 is 49/50, not 48 (JSON-verified before commit).
- YN validation: salvaged tables saved (2,621 / 21,015 / 4,400 rows in ignored outputs/, verified by
  re-parse). Pair BLOCKED: 2023 depths 28–40% out-of-range (to 137,609); floors 0.1 vs 1.9; EXT/INT
  codes inside depth column; offsets 27–65% empty (frozen ±0.5m term has no input); both sides end at
  corruption edges. Prior 29,234 count corrected (overcounted closings). Clean 2023 re-export + 2020
  tail would unlock the pair with no new method work.
- E14 re-salvage: all 8 metrics bit-identical (diff 0.0 incl. bootstrap). /tmp-loss lesson closed:
  repaired CSV in outputs/ + resalvage_e14.py committed. results_e15.md CRC claim corrected
  (sharedStrings fails; sheets clean). R1–R4 void ruling stands (reproducibility restored, validity unchanged).
- Root cause found: short FAT chain (last ~65KB missing), not corrupt content. Patched xlrd compdoc
  to accept truncated streams + tolerant cells (`experiments/salvage_pk1_weld.py`, reads source
  read-only). Result: 12,927×28 rows, 12,475 numeric distances, max 128.8km (tail ~12km missing),
  12,475 pipes. CSV saved to ignored outputs/ (persists; /tmp lesson applied).
- E15 DEAD verdict overturned: 32-file tally now 24 CLEAN / 6 RECOVERABLE / 0 DEAD / 2 administrative
  PARTIALs. No file defeats all methods anymore. Absent-data list (never-written rows) stands separately.
- (Round-13 stale-verdict cleanup below.)

## 2026-10-07 — Round 13 closure: stale verdicts fixed, split stated, queue narrowed
- results_recompute.json method_note SUPERSEDED (raw-exact finding); results_e12_recompute.json verdict
  SUPERSEDED to tolerance-CONFIRMED. Files now agree with PROGRESS; history preserved in git.
- NN wording split stated: odometer-only NN rates CONFIRMED exact (0.7263/0.5338, raw, pipe-agnostic).
  The older "UNVERIFIED (needs matching rerun)" line meant pipe-AWARE greedy matching, which never ran
  and is not needed (frozen pipeline uses greedy match_win; NN was always a diagnostic, never a claim input).
- Remaining queue before objective closes: (a) YN E15 validation (salvage-parse + schema check),
  (b) olefix attempt for PK1-2025 weld or formal DEAD acceptance, (c) E14 re-salvage or void acceptance.
  Everything else on the ledger is derived, committed, and green.
- Independent src-path rerun: match/prev/B1/base/n_pos identical to 4–5 decimals on both cuts
  (B1 0.57374 vs 0.5737; 0.37499 vs 0.375; n_pos 334/138 exact). My script's == verdict fired only
  on rounding (committed full-precision vs recomputed 4dp) — same error class as the NN denominator
  mistake. Tolerance-based comparison is the rule going forward.
- Bootstrap CIs agree to 3dp at cut12; cut15 lower 0.201 vs 0.208 — Monte Carlo noise from RNG-state
  sequencing (e12 shares one RNG across cuts; recompute reseeds per call). Both lowers stay >0;
  nothing moves. Wart logged: shared-RNG makes CIs order-dependent.
- Ledger closed except: E14 outputs (source lost) and HGB/LR stochastic fits (seeds fixed, scripts
  frozen — reruns prove code path, not new facts).
- NN ±2m recomputed: raw pipe-agnostic 0.7263/0.5338 reproduce 72.6%/53.4% EXACTLY — the original
  numbers were raw-frame rates and my interim d10 run (81.0/69.8) used the wrong denominator, not
  the reports. Correction: my challenge was miscalibrated, not their arithmetic. d10-vs-raw gap is
  itself evidence: filtering inflates apparent persistence (logged in DATA.md).
- E05 train/test + E10 recomputed EXACT (AP/base/match/pos all match committed JSONs to 4 decimals).
  UNRECOMPUTED items closed except E14 (source lost) and E12 cuts (queued).
- ON/YN track: raw-vs-normalized counts exact; weld overlap 11788/11858 exact; salvage counts exact;
  pipe log exact; odometer ranges exact. NN-match rates 72.6%/53.4% UNVERIFIED (needs matching rerun).
- PK track: E11 bit-identical recompute; PK2 medians/shares exact; GWAN shares exact.
  CORRECTED: PK2 drift 55 → 19.1/km (no denominator reproduces 55); edge-offset ×10057 → 10428;
  csv method = UTF-8/errors=replace; PK1-2019 weld tail also absent (14072 dim, 9060 valid to 89.8km).
- SRTO track: E05/E10 inputs exact; 93-vs-92 explained (one depth row lacks Distance); 1608-2024 weld
  stops at 70.5km (new truncation noted); depth/KBD global ranges qualified to typical-clean with
  SRTO-side lows. AP math UNRECOMPUTED by scope (inputs verified, not outputs).
- LOSS logged: /tmp repair_spike purged by the OS — E14 repaired copy gone, re-derivation blocked
  until re-salvage. Committed E14 results stand as run artifacts. Lesson: salvage outputs go to
  ignored outputs/ next time, never /tmp.
- On 100% confidence: unattainable by audit; delivered instead is triple-checked evidence with every
  residual uncertainty named above. That is the honest maximum.
- (E15 full audit below — user-challenged re-verification of all 32 files.)

## 2026-10-07 — E15 audit: user more right than the old table; 3 corrections logged
- 24 CLEAN / 5 RECOVERABLE / 1 DEAD / 2 PARTIAL (both partials are strictness artifacts, corrected
  to RECOVERABLE with known methods). Full per-file table in results_e15.json.
- Corrections: SRTO-1717-2024A "corrupt" was wrong (1,220 rows strict-clean; broken dimension tag
  only); PK2-2025A recoverable via proven salvage (2,162 rows); PK2 csv via encoding flag.
  PK1-2025 weld DEAD under both xlrd paths, olefix queued, not final.
- Absent-at-any-cost list: PK1-2019 rows 2864+, ON/PK1-2025 weld tails, YN-2023 garbled majority.
  Pair verdicts stand (PK2 comparability, Yu-N E15 validation, E14 void). No pair was ever lost to
  strict-parser failure alone.
- Background counter finished: sheet3 (особенностей) 25.84MB → 29,234/29,497 well-formed (99.1%);
  sheet4 (аномалий) 23.73MB → 4,405/28,717 well-formed (15.3%, duplication-garble pattern like PK1-2019).
  Row-start count ≈ summary-stats magnitude, so most markers are repeats, not records.
- Status change: Yu-N moves from "blocked" to "salvageable, pair TBD". Pair still unclaimed:
  needs salvage-parse + Distance/column validation + schema check (2020 is 45-col SSID format vs 2023
  new-format journals — possible PK2-class comparability break). Queued as E15 validation experiment.
- README Yu-N rows corrected in both languages (counts stated, no pair claimed). Re-export request stands
  as the clean fix regardless.
- Re-ran everything personally against raw files (no subagent): 6 folders, 39 files (32 data + 7
  .DS_Store). PK2-2015: 23 cols, n=18,337, med 5.0, 5.8% ≥10. PK2-2020: n=1,026, med 11.0, 96.1% of
  measured depths (76.2% of rows). PK2-2025A corrupt (ParseError). YN-2020A corrupt; YN-2023 journals
  corrupt on full read (3-row probe passed — method lesson: always full-read); pipe log 14,160 rows.
  ON-2016 and PK1-2022: 44 cols, readable.
- Fix: README "6% vs 96%" mixed denominators (all-rows vs measured-only). Now states both precisely.
  Conclusion stands (threshold regime break). No other changes.
- Supervisor question answered: all six folders studied (schemas in DATA.md, scoping recon, salvage
  spikes). PK2 deferred (schema + threshold break, rounds 10–11); Yu-N blocked (zero readable anomaly
  surveys, re-export requested). README tables now read "4 of 6 studied sections" with reasons.
- (Supervisor-facing rewrite below.)

## 2026-10-07 — SUPERVISOR_BRIEF removed; README rewritten EN+RU
- Deleted docs/SUPERVISOR_BRIEF.md via git rm (no test or code dependency; history keeps the record).
  Remaining references live only in frozen files (PROGRESS history, track evidence) — left intact.
- README.md rewritten: status, built artifacts with evidence table, data layout, pipeline, reproduce,
  progress vs pending, map, rules. README_RU.md mirrors it in Russian (decimal commas, same numbers,
  same commands/paths). Cross-linked both ways. Verified number parity EN↔RU + tests green.
- Three agents applied the humanizer skill over the 11 styled docs (dashes→periods/colons,
  bold decoration out except mandated warnings, shout-caps lowered, triads/openers/closers cut,
  corrective contrasts kept where they fix a real misreading). Exempt classes untouched again.
- Verified: net ~100+/101- prose-only diff; range hyphens unambiguous in context; run_tests.sh green;
  frozen numbers + disclaimer strings intact. Committed below.
- Question: is every doc rewritten under the AGENTS.md rule? Answer: yes, except the classes the
  rule itself exempts (frozen track evidence, frozen result outputs, PROGRESS history, verbatim
  triage captions). `/Users/akm/Tsu Project/AGENTS.md` exists and is byte-IDENTICAL to the repo copy.
- Automated scan of all 11 restyled docs: avg 6.6–12.6 words/sentence, filler ≤3 per file.
  All >25w hits inspected: output-field tables, schema column enumerations, and spec lines with exact
  numbers — all protected by the rule's own exceptions (identifiers/quantities stay exact).
  Two apparent long sentences re-checked in place: already short sentences separated by markdown
  structure (scanner artifact). No fixes required; nothing changed.

- (Style pass below.)

## 2026-10-07 — Repo polished for supervisor review under new writing law
- Saved user instruction as `AGENTS.md` (project law: STE-flavored prose, exceptions for
  identifiers/numbers, format ladder, repo bindings for verbatim captions and frozen evidence).
- Three rewrite agents restyled README + 10 docs (PROBLEM, VALIDATION, DATA, GUARDRAILS, TRIAGE_SPEC,
  SUPERVISOR_BRIEF, RUNBOOK, OVERLAY, research INDEX + PROTOCOL). Track files untouched (frozen).
- Verified: run_tests.sh green (frozen numbers + disclaimer strings intact); invariant grep passes;
  diff is prose-only (no code/command/number changes). Committed below.
- (Quad-provider client layer below.)

## 2026-10-06 — Quad-provider search layer built; 1 of 4 keys reachable (ball in user court)
- `src/research_tools/`: per-provider clients (schemas verified vs official docs) + quad.py concurrent
  fan-out + self-test. Live self-test: exa OK (3 hits), firecrawl/parallel/tinyfish SKIP (keys absent
  from agent env — they sit in the user keyring only). Architecture for "all four in parallel" is
  DONE and proven; only key custody blocks full activation.
- PROTOCOL tooling section updated. Subagent briefs now mandate dual-channel use (direct clients +
  routed search) with per-file channel disclosure.
- Fixed the tool question properly: $EXA_API_KEY present in agent shell, curl-verified working
  (Zhang&Zhou hit); Firecrawl/Parallel/TinyFish reachable only via user-side routed failover
  (absent from agent env). Briefs now mandate dual-channel use + per-file channel disclosure.
- T21 cracks (Paris/SCC/EMAT/SSWC/ECA), T22 internal corrosion (de Waard/NORSOK/TOLC/UT-reference),
  T23 GIS covariates (SoilGrids/DEM/HCA join method + SK-42 trap), T24 market packaging (tiers,
  POC shapes, on-premise constraint, honest-claim templates). ~38.5k words total.

- Corrected the record: OpenChamber panel shows Exa/Firecrawl/Parallel/TinyFish keyed + auto-failover
  (Tavily empty); briefs told agents to exploit per-provider strengths + retry. INDEX tooling note fixed.
- T17 primaries with extracted values (POF tables, API-1163 workflow, binomial gates); T18 academic deep
  search + citation graph + 2 recorded negatives; T19 Russian primary texts (FNiP/GOST/STO numbers,
  3 new VTD papers); T20 vendor gray literature (exact POD/tolerance numbers, disclosed negatives).

- (Skip-audit + PROTOCOL below.)

## 2026-10-06 — No-skip protocol codified + 16-track skip audit passed
- `docs/research/PROTOCOL.md`: fallback ladder (search→fetch→OpenAlex→arXiv→mirrors→secondaries→
  recorded negative), per-file disclosure, minimums, HARD boundaries (no paywall purchases, no
  logins, no credential use). All future research briefs cite it first.
- Skip audit over all 16 tracks (grep for could-not/unable/failed/skipped/paywalled): hits are
  domain language or already-handled fallbacks (secondaries, mirrors, API verification, all noted
  per-file). Only residual: paywalled-standard full texts via summaries — allowed boundary, flagged
  per item, purchase decision left to user. No cleanup wave needed.

- T13 welds, T14 dents, T15 ECDA fusion (+partner items 6–9), T16 regulatory (allowed/forbidden claim
  rule; RU = инструмент планирования, не ЭПБ). All committed.
- Exa/Firecrawl/Parallel/TinyFish: NOT connected here — no integrations, no API keys, no catalog
  entries. Offered: paste keys and I wire them same-turn; otherwise built-ins + public APIs stand.

- Tracks 10/11/12 banked earlier; track 9 (benchmarks) landed on its completion notification and is
  now indexed + committed (Mendeley sandbox URLs, C-MAPSS smoke test, baseline anchors, synthetic stack).

- Parallel subagents: T5 ILI tool physics + POD (12 src; KEY: 10–15%t in POD ramp explains 2.5–5×
  jumps; growth credible only above both surveys' POD90), T6 integrity practice (12 src; triage =
  PoF-side screening; KBD<0.9 conservative flag), T7 RUL + Russian sources (11 src, 4 Russian;
  Gaznadzor-2019 baseline 36–56% accuracy supports no-80% position), T8 data engineering (14 src;
  PODS schemas, weld-master action list). websearch flaky across tracks (fallbacks noted per-file).
- No extra plugins installable (catalog + keys) — built-ins + public APIs sufficed, stated in INDEX.

- Parallel subagents: T1 ILI growth + sizing error (14 src), T2 spatial/tabular (10),
  T3 community Kaggle/HF/GitHub/PHMSA (12 items), T4 shift/metrics/calibration (13).
  websearch was HTTP-400 — verified via OpenAlex/arXiv APIs + webfetch instead (noted per-track).
  No research plugins exist in catalog and no API keys available — built-ins sufficed.
- Gated decisions (none change December scope): Voronoi-matcher ablation candidate; hurdle P2
  architecture candidate; Mendeley 4-run sandbox for method tests; calibrate→reweight order;
  negatives kept (no ID-less paper, no harmonization standard, Hawkes rejected, no fit open data).

## 2026-10-03 — E14 second 1717 pair: ranking survives, methodology break flagged (weak replication)
- Executed (frozen, repaired 2024A, 5 placeholders dropped): d≥10 92 vs 440 (4.8× jump — sensitivity/
  methodology break between 2021→2024, or repair-side effect; cannot separate without source re-export).
  Match 0.134 (lowest ever; E10 pair had 0.261), prev 0.100 (42 pos), B1 0.201 vs base 0.100,
  liftCI [0.019,0.212] lower>0 — ranking replicates a 5th time, but barely and dirtily.
  CORRECTION (reviewer round 12): honest tally stays 4/4 clean — E14 is VOID as replication evidence
  (fails R2 source-grade + R3 stationarity: ratio 4.78, match 0.134 vs 0.261 prior; R4 pass with a
  changed instrument is uninterpretable). E14 kept as methodology-break evidence only.
- Decision: NO 1717-2024 triage page (thresholds on a methodology-break pair would be meaningless);
  pair kept as drift evidence only. Repaired-copy results are internal, never handover-grade.
  Reinforces PK2-deferral and the per-survey-threshold rule.

## 2026-10-03 — Round 11 + SRTO-2024A salvage GO + test coverage closed
- Round 11: no scoring breach; priority ranking hold>(c)doc>(a)salvage>(b)PK2. Forced choice taken
  (freeze December scope). Two buildable gaps closed this turn: SRTO frozen-number + disclaimer +
  src-only-import assertions in test_consistency.py; runbook SRTO retrospective-only sentence.
- Salvage spike: SRTO-2024A GO qualified (99.6% Pipe+Distance keys; 5 placeholder-pipe rows;
  repaired copy in /tmp repair_spike, repo untouched; depth empty-by-design per class).
  Unlocks SRTO-1717 2021→2024 second pair — queued (cheap, small section), not run yet.
- run_tests.sh now covers all 6 consistency tests; full runner green.

## 2026-10-03 — Swarm: SRTO-1608 triage page + partner runbook (both verified, committed)
- `triage/build_srto.py` (src-only imports, zero experiment references) reproduced E05 exactly:
  AP 0.2767/base 0.0605/match 0.5511; P@10 0.400 [0.100,0.800], P@20 0.450, P@50 0.420 (sparse-ground
  wide CIs, reported not hidden). All display conditions verified on-page. Third shipped page.
- `docs/PROSPECTIVE_RUNBOOK.md`: partner procedure (prereqs, --check gate, --drop-last default,
  recalibration rule, outputs, limitations, troubleshooting). Three-section demo set (ON/PK1/SRTO-1608).

## 2026-10-03 — Handover hygiene: README as-built, run_tests.sh green, overlay archived
- README rewritten (was aspirational scaffold; now frozen deliverable + reproduce + rules).
- `run_tests.sh`: parity + consistency + binary-hygiene in one verified-green run (pytest absent noted).
- docs/OVERLAY_STATUS.md: LR-nlag archived OFF with promotion rule (prospective dense-ground
  confirmation + null re-pass + reviewer round). Ship B1-only.

## 2026-10-03 — Reviewer round 10: no scoring breach; tests hardened; PK2 deprioritized; scope freeze
- Audit: NO new scoring breach (migrations hold, prospective IDENTICAL, E13 isolates artifact).
  One claim rebutted with evidence: thresholds.yaml EXISTS on disk + tracked (reviewer's ls miss).
  Doc-sync lag fixed (TRIAGE_SPEC header, GUARDRAILS edge-cell rule).
- Tautology `or True` removed; real CI check in its place. New `test_consistency.py`: frozen-number
  tripwire (ON/PK1 AP+base+match, all lift-CI lowers>0, disclaimer strings on pages) — passes, no raw
  data needed. pytest absent on this machine; tests run as scripts (documented limitation, CI TODO).
- PK2 2015→2020 correctly deprioritized (schema + threshold break = weeks for a 5th replication that
  cannot change the primary or support ≥80%). Forced choice taken: FREEZE December scope to B1-only
  ON+PK1 triage, drop-last default, placeholder thresholds; PK2/overlay-promotion/calibration post-December.

## 2026-10-03 — Prospective harness built: regression IDENTICAL, forward watchlists out, edge artifact flagged
- `triage/prospective.py` (past-only B1, per-section thresholds.yaml placeholder, full CSV to ignored
  outputs/): --check vs shipped pages IDENTICAL both sections (ON-2021, PK1-2022 top-20 cells+scores exact).
  Forward watchlists: ON-2025 (nonzero 491/1331, top cell 173), PK1-2025 (nonzero 830/1401, top cell 1400).
- FLAG (not hidden): PK1-2025 #1 cell 1400 has 211 counts vs #2 114 — boundary accumulation
  (known 140782–140830m overrun rows fall in last cell). Edge-cell guard queued as E13 (pre-registered:
  exclude boundary cell, recompute top-20); no scoring change until then. ON-2025 top cell 173 unremarkable.

## 2026-10-03 — E13 edge guard done: artifact isolated to itself, ranking stable
- `--drop-last` implemented (boundary cell excluded, scores renormalized, dropped cell logged).
  PK1-2025 noedge top-20 overlaps guarded run 19/20 — only cell 1400 leaves; new top1 = cell 438 (114).
  New top-3: 438/480/1366. Guard adopted as DEFAULT for prospective watchlists (edge cells collect
  overrun rows by construction); retrospective pages unchanged (frozen evidence).

## 2026-10-03 — PK1 path migrated: src-built outputs byte-identical (both paths proven)
- `triage/build_pk1.py` now imports only `gtk1.{io,features}` (+sklearn); rerun reproduced AP=0.779,
  base=0.401, match=0.715, P@K exactly. `git diff`: triage_pk1.html UNCHANGED, JSON hash-field-only
  (fd4cad4→0538414). Both triage paths are thin verified consumers; round-9 migration proof complete.
- Docs refreshed (TRIAGE_SPEC evidence as of E12+refresh with PK1 triple; BRIEF header current).

## 2026-10-03 — Reviewer round 9 + src migration proof in flight
- Round 9: src = shelfware until consumer migrates (parity test insufficient: synthetic-only, tautology
  `or True`, no normalize/R4/tolerant coverage, no consumer). Migration proof required: thin-wrapper
  triage builder + byte-comparable outputs + real-data fixture hashes in CI.
- December readiness: tasks 1–7 DONE (deps with age caveat; overlay partial). Docs stale (TRIAGE_SPEC "as of
  E08", BRIEF "E12 running") — refresh queued. Prospective-run harness (ingest + recalibration) not built.
- Overlay ruling: archive as experimental/lr-nlag-ON-only, OFF + kill-switch, no tuning, no delete
  (provenance). Ship B1-only paths. "Dead unless prospective dense-ground confirms."
- No new expensive campaigns: remaining budget → migration proof, docs refresh, prospective readiness,
  partner requests. Cheap frozen reruns only.
- Migration: `triage/build_report.py` now imports only `gtk1.{io,features}` (+sklearn); experiment
  fallback import removed (was a live ImportError risk). Re-run launched background (sh_...Vyr4);
  proof = AP 0.644 identical + HTML byte-comparable modulo git-hash. Recorded on notification only.

## 2026-10-03 — Migration proof PASS: src-built outputs byte-identical
- Rerun on `src/gtk1` imports: AP=0.644, base=0.268, match=0.612, P@K identical.
  `git diff`: triage_demo.html UNCHANGED (byte-identical), triage_demo.json differs ONLY in git-hash
  field (ea7713d→2be3a6d). Reviewer's exact migration check satisfied for the ON path.
  src/gtk1 graduates from shelfware to verified consumer-backed package (PK1 path migration queued).

## 2026-10-03 — src/gtk1/ package + parity tests (reproducible-software track)
- Consolidated frozen pipeline into importable `src/gtk1/`: io (loaders + tolerant-xlrd + normalize),
  match (greedy/Hungarian), features (7-feat cell build), metrics (AP/CI/paired-delta/P@K/R@P).
  Experiments keep frozen copies for provenance (no script edits).
- `src/tests/test_parity.py` passes (executed): match flags identical 60/62, build labels+features
  identical, metrics == sklearn on synthetic frames (no raw data in tests).
  repair queue updated (SRTO-2024A salvageable → PK2-2025A → YN).

## 2026-10-03 — E11 PK1 done: 4/4 sections replicate, methodologically cleanest pair
- Background run completed (tolerant loader worked; put_cell chatter is xlrd debug noise, harmless).
  Counts d≥10: 8982 vs 8989 — nearly identical across surveys (stable methodology, unlike ON inflation).
  Match 0.715 (highest yet), prev 0.401 (562/1401), B1 0.779 vs base 0.401, liftCI [0.348,0.409].
- Ranking now replicates 4/4 sections (ON 0.644, SRTO-1608 test 0.277, SRTO-1717 0.181, PK1 0.779),
  with PK1 the tightest CI and cleanest methodology. B1>>base is a cross-section empirical regularity
  for newly-reported ≥10% @100m — still operational framing (vanished/cut caveats stand), still no ≥80% claim.
- Next: reviewer round 8 (4-section synthesis + December build approval); PK1 triage page (same v0 template,
  per-section thresholds); repair queue as before.

## 2026-10-03 — Round 8 (B1 freeze YES, December CONDITIONAL GO) + PK1 page/E12 launched
- (1) B1 freeze as December primary: YES — 4/4 lift-CIs lower>0; SRTO-1717 weak only for its own
  thresholds, not the freeze. AP spread (0.18–0.78) mandates per-section recalibration, no pooling.
- (2) PK1 page with cut-sensitivity pending: SPLIT — structure-only internal demo OK; quantitative
  headline HOLD until E12 (cheap frozen rerun). E12 (cuts ≥12/≥15) written + launched background
  (sh_...OIxI, 120s stagger); PK1 page build launched background (sh_...U5PB). Numbers on notification only.

## 2026-10-03 — PK1 triage page v0 built (E12 still running)

## 2026-10-03 — E12 done: PK1 triple complete, quantitative headline UNBLOCKED
- cut≥12%: match 0.715, prev 0.238 (334 pos), B1 0.574 vs base 0.238, liftCI [0.289,0.387].
  cut≥15%: match 0.690, prev 0.099 (138 pos), B1 0.375 vs base 0.099, liftCI [0.208,0.354].
  PK1 triple: 0.779 / 0.574 / 0.375 — ranking survives all cuts with lower>0 (unlike ON's 15% fade).
  Match-rate cut-invariant (0.715/0.715/0.690) — further evidence of stable PK1 methodology.
- Round-8 HOLD released for PK1 thresholds. Refreshing triage_pk1.html triple (pending-flag →
  completed numbers) via background regen; page + results committed on its notification.

## 2026-10-03 — PK1 page refreshed: triple completed, pending-flag gone
- Regen completed: AP=0.779 identical (deterministic, git fd4cad4). Page carries completed triple
  "0.779 / 0.574 / 0.375", zero PENDING strings; JSON cut_sensitivity dict {10:0.779,12:0.574,15:0.375}.
- PK1 evidence package closed: page + E11 + E12 all committed. Two-section triage demo set (ON + PK1)
  with per-section thresholds and full disclaimers.
- Background run completed: AP=0.779 live == frozen E11 (deterministic). P@10=1.000, P@20=1.000, P@50=0.980.
  All round-7 display conditions verified on-page (disclaimer, pending-flag "cut≥10% only — ≥12/≥15 PENDING E12",
  caption, denominators, ON→PK1 per-section wording). 138KB HTML + JSON (git e4155d6).
- E12 (PK1 cut-sensitivity) still running in background — quantitative PK1 headline stays HOLD until it lands.
- (3) December build: CONDITIONAL GO — multi-section B1 triage + per-section thresholds + overlay OFF
  + disclaimer triple + no badges/meters. HOLDs only: PK1 thresholds till E12; physics language till
  repair logs. (4) Residual ≥80% risk (for supervisor): "new" conflates initiation + re-detection +
  sensitivity gain — survey-conditional reporting predictability ≠ physical corrosion predictability.

## 2026-10-03 — E11 PK1 2022→2025 launched (background, densest test)
- Tolerant-xlrd patches vendored into `experiments/e11_pk1.py` (attributed to prior salvage work;
  read-only use; stock xlrd tried first). Frozen pipeline: Depth≥10%, pipe+2m/0.5m/1h greedy,
  100m matched-new KMAX=1400, B1/B2 + 2000-bootstrap lift CI. ~21k×11k-row match — backgrounded
  (sh_105855277001RqlcBW1wtjvrAp); numbers recorded on completion only.

## 2026-10-03 — E07b done: null calibrated, driver found, SRTO holdout fails feature lift
- Background run completed; artifacts verified. Constant-check PASS (const=base exactly, gap +0.0000) —
  AP path sane; E07 single-shuffle excess was chance (null−base CI [−0.066,+0.275] / [−0.058,+0.314] includes 0).
  Δ LR vs null-mean +0.311 [+0.263,+0.354] / +0.297 [+0.238,+0.363] — LR beats calibrated null decisively.
- Ablation-vs-full (driver answered): dropping nlag costs −0.039/−0.036 (dominant); npipes −0.008/−0.002;
  n_past only −0.002/+0.002 (collinear with lags); maxd/meand/gwan/mech ≈ noise (±0.006).
  The +0.03 lift is spatial spillover (neighbor counts), still autocorrelation-family — explains fragility.
- SRTO holdout of LR lift: LR 0.281 vs B1 0.277, dCI [−0.032,+0.039] — feature lift does NOT transfer;
  LR==B1 off-site. B1 ranking itself replicated earlier (E05b lift CI lower>0); only the +0.03 overlay is ON-only.
- Net: task framing stands everywhere; feature overlay provisional ON-only. Shipped-model implication:
  B1/persistence-family ranker as primary (transfers), LR-nlag overlay experimental (ON-only flag).
  Re-applying to reviewer for gate ruling (round 5).

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

