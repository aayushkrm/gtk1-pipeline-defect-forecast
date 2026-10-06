# Research index — literature + community sweep (2026-10-06, while awaiting partner data)

Tooling note: websearch returned HTTP 400 all day, so tracks verified via OpenAlex/arXiv
APIs + webfetch; some publisher pages bot-walled (noted per-track). No extra research plugins
exist in the tool catalog and no API keys are available — built-ins only. No Exa/Firecrawl/
TinyFish keys exist here; nothing was skipped for lack of them (public APIs covered the need).

## Track files (5,643 words, 49 sources/items)
- `track1_ili_growth.md` — ILI growth + sizing-error models (14 sources). Core finding: NO paper
  forecasts from ID-less threshold-drifting tables; Dann–Maes + Voronoi matching + operator vetting
  is the methodology core; stochastic processes contribute priors only.
- `track2_spatial_tabular.md` — spatial + tabular methods (10 sources). USE hurdle architecture
  (binary gate × Poisson-Tweedie head), NB ladder, GBDT-first, TreeSHAP; REJECT Hawkes as forecaster
  (no IDs — unfixable); ADAPT LGCP/INLA smoother, ZIP.
- `track3_community.md` — Kaggle/HF/GitHub/PHMSA (12 items). Only usable open sandbox: Mendeley
  4-run ILI set (repeat-ILI method testing). Kaggle/HF tabular ILI: none (image-CV only). vb64 B31G
  lib USE (MIT) for ERF spot-checks; Farhad/CorroSight matching + PRCI/C-FER + OneBridge = ADAPT notes.
- `track4_shift_metrics.md` — shift + metrics + calibration (13 sources). Mandates: calibrate→
  reweight order (Saerens EM/BBSE/Garg), PR-AUC+cut-sensitivity panel, per-section calibration,
  R3+BBSD screen; MIL-HDBK-1823A/API-1163: per-survey POD, never pool vendors; no vendor-neutral
  harmonization standard exists (negative result, Hoening IPC2024).

## Cross-track decisions (all provisional, reviewer-gated, none change December scope)
1. Matcher upgrade candidate: Voronoi matching (Amaya-Gómez 2022) vs current greedy/Hungarian —
   cheap ablation if budget allows; must pass R1–R4 + block-CV to displace.
2. P2 architecture candidate: hurdle (HGB gate × Poisson-Tweedie/NB head) + LGCP-smoothed density
   feature — first model that could beat log-linear MAE 6.5 honestly.
3. Mendeley 4-run set: sandbox for matcher/threshold experiments WITHOUT touching spent test pairs.
4. Calibration order: calibrate-then-reweight per section (BBSE); Ovadia 2019 forbids carrying
   calibrators across contractors — formalizes our no-pooling rule.
5. Negative results kept: no ID-less forecasting paper exists; no harmonization standard exists;
   Hawkes rejected; Kaggle/HF have no fit tabular data. These close avenues, which is progress.

## Wave 2 (2026-10-06, 4 tracks, ~50 sources; websearch flaky — worked for some tracks, HTTP-400 for others with API fallbacks noted per-file)
- `track5_ili_tools.md` — MFL/UT/EMAT physics, UHR resolution, API-1163 L1/2/3 + PRCI unity plots, POF
  specs, calibration digs. KEY MECHANISM: 10–15%t sits in the POD ramp (POD90 12–15% body, 18–24%
  near weld) — small threshold changes explain our 2.5–5× count jumps; real growth credible only on
  matched pairs above BOTH surveys' POD90.
- `track6_integrity.md` — B31G/RSTRENG, DNV-RP-F101, B31.8S taxonomy, RBI dig programs, Pd/MAOP/KBD
  semantics. Position: triage outputs are PoF-side screening feeding dig workflows; KBD<0.9 is a
  conservative Level-1-family flag; cut-sensitivity + per-section thresholds have direct precedent.
- `track7_rul_russian.md` — C-MAPSS lessons, survival/RSF, transfer learning, 4 Russian-language sources
  (cyberleninka TIU/Gorny/VNIIGAZ, STO summaries, TIU/Gubkin schools). CITABLE BASELINE: Gaznadzor-
  coauthored 2019 paper reports VTD-based repair-planning accuracy only ~36–56%, 52–54% of SCC pipes
  invisible to ILI — supports the no-80%-claim position. Deep sequence models rejected (3 snapshots).
- `track8_data_eng.md` — run alignment, odometer/AGM correction, tally reconciliation, PODS 7/UPDM
  schemas (ADAPT), API-1163 DQA gates, 4-step weld-log-master action list for our ETL.
- Gated follow-ups (none change December scope): POD90-aware matched analysis (growth credible only
  above both POD90s); hurdle-P2 + RSF-survival experiment order (RSF → per-medium CatBoost → one gated
  transfer test); Mendeley sandbox + PODS field map for ETL hardening.

## Wave 3 (2026-10-06 — deployment, corrosion science, failure analyses; benchmarks pending)
- `track10_deployment.md` — triage UX (ranked pull lists + override logging, never badges), CORP plots
  for analysts only, MLOps recalibration decision table mapping to PHMSA §192.947, four evidence lines
  backing the no-badges rule. Directly supports triage pages + runbook wording.
- `track11_corrosion.md` — soil-resistivity proxies, NBS rate-decay prior, FBE-vs-tape shielding ×
  25–30y life, CP criteria request list, stray-current/MIC flags, ERW-vs-spiral spectra, NACE 0.4 mm/y
  upper-bound prior. Feature-request list for partner data; no model change.
- `track12_failures.md` — PHMSA/NTSB miss cases (San Bruno, Marshall $800M+, Bellingham, Carlsbad),
  $91k/dig vs 10³–10⁴× failure economics (repair-priority math), Danville 441-vs-16 re-analysis as
  field-scale twin of our vanished-frac argument, 192.939 half-life + 7-yr cap horizon justification.
  Strengthens limitations section with named evidence.
- Track 9 (benchmarks/datasets) still in progress — indexed on its completion notification, not here.

## Wave 3 completion (2026-10-06 — track 9 benchmarks landed)
- `track9_benchmarks.md` (11 items): Mendeley 4-run ILI set deep-dive (343 MB, CC-BY 4.0, direct URLs —
  USE as matcher sandbox); C-MAPSS/PHM08 (USE FD001 smoke test); Saxena metrics + PHM08 asymmetric
  score + time-dependent PR (ADAPT into eval); Velázquez-259 + Bastek-2026 + JPSE-2025 RMSE 0.368 mm
  (honest-baseline anchors, blocked CV); NIST CORR-DATA + PHMSA incidents (public domain); SKAB
  protocol-only; in-house synthetic stack (GRF + clustered points + POD layer); 6/11 downloadable.
- EGIG confirmed members-only (rejected in-file). Mendeley row counts need post-download audit.
- December-scope actions recorded in-file; none change frozen scope.
