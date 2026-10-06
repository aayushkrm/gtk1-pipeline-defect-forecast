# TRACK 8 — ILI data engineering at scale (practical ETL relevance)

Context: GTK1 VTD anomaly tables (44/45-col, R4 headers, `.xls`/`.xlsx` salvage, Pipe-No joins, odometer+marker refs, 0% GIS coords). See `docs/DATA.md`, `src/gtk1/io.py` (tolerant-xlrd salvage + `normalize()`).

## (a) Run-to-run alignment / box-to-box matching in production

**S1. OneBridge/CIM ingestion + alignment** — https://irthsolutions.com/blog/back-to-the-future-with-cim-2
Classifiers trained on 5,000+ ILI reports / 40M+ anomalies map any vendor wording into a standard taxonomy with 100s of DQ checks.
Girth welds aligned by minimizing joint-length difference (tolerates odometer error, repairs, re-routes, flow reversal); each joint gets a master joint number. Anomaly boxes matched with 1-to-1 / 1-to-many / many-to-1 overlap logic.
RELEVANCE: Direct template for our salvage parsers (meaning-based class map ARTD→GOUG etc.) + pipe-join master (weld-log as master joint table) + matching windows that allow splits/merges.
Verdict: ADAPT — copy taxonomy-map + master-joint + multi-match design.

**S2. Cenosco IMS PLSS ILI Comparison (GW matching)** — https://ims-handbook.cenosco.com/docs/pl-ili-comparison-girth-weld-matching-data
Odometer drift ±1% of travelled distance (±100 m per 10 km); even with AGMs every ~2 km, defect accuracy is insufficient for matching without weld anchoring.
Auto-match spools when joint-length difference < OTA (default 5%, not 1%, because a 5 mm error on a 0.5 m spool is already 1%); skip-and-resume + manual override + GW-offset QC plot before defect matching.
RELEVANCE: Justifies our ±2 m / ±0.5 m / ±1 h windows as post-weld-correction tolerances, and a GW-offset diagnostic plot as a mandatory ETL gate.
Verdict: USE — adopt OTA-style weld match + offset-plot sign-off.

**S3. Scudder/OneBridge normalized-odometer + active-corrosion score (PGJ Nov 2023)** — https://read.nxtbook.com/gulf_energy_information/pipeline_and_gas_journal/november_2023/risk_assessment_scudder_onebr.html
All runs interpolated into one normalized odometer space keyed on a reference run; same pipe unambiguously traced via aligned weld/joint patterns across history.
Complements pit-to-pit CGRs with a population growth score (mean×sd×skew of local CGR bins) over matched *and* unmatched anomalies.
RELEVANCE: Gives us a principled way to keep unmatched/new/vanished calls informative (our 124 blanks, GWAN campaigns) instead of dropping them.
Verdict: ADAPT — reference-run odometer space + bin-level growth score.

**S4. Open ILI-alignment pipelines (reference implementations)** — https://github.com/rutul831/ili-alignment-pipeline ; https://devpost.com/software/pipe-align
Canonical-schema normalize → reference-match (monotonic nearest-neighbour) → piecewise-linear drift correction → multi-gate candidate + weighted score → greedy/Hungarian 1-to-1 → new/missing/uncertain exceptions.
PipeAlign adds the key guardrail: if the two best scores are within ε, mark Ambiguous rather than forcing continuity in dense clusters.
RELEVANCE: Mirrors our `normalize()` and should shape its next iteration (config-driven column maps, per-pair score breakdown, ambiguity flag).
Verdict: USE — copy pipeline stages + ambiguity rule.

## (b) Odometer calibration, AGM/marker correction, chainage vs GIS

**S5. POF 100 §6–7 (vendor spec language)** — https://pipescanintegrity.com/assets/docs/POF%20100%20Specifications%20and%20requirements%20for%20ILI%20-%20Nov%202021.pdf
Defines "processed raw data" as explicitly corrected for odometer slippage; requires AGM statistics, positively-identified markers in the pipe tally, and tool-viewer software enabling run-to-run comparison.
Distinguishes chainage/odometer measure from GIS coordinates; markers are the bridge between them.
RELEVANCE: Our markers/offsets columns are the AGM bridge — ETL must treat them as first-class correction inputs, and lat/lon emptiness (0%) is normal, not a bug.
Verdict: USE — require marker accounting + slippage-correction metadata per survey.

**S6. AGM practice + error physics** — https://www.ndt.net/article/wcndt2012/papers/271_wcndtfinal00271.pdf ; https://www.jstage.jst.go.jp/article/jpi/49/1/49_1_38/_pdf/-char/ja ; https://www.mdpi.com/1424-8220/19/17/3740
AGMs every 1–2 km bound drift to ~1–2 m segments (correction `L = Li + (t−ti)·ΔL`); raw odometer error ~1 m/km accumulates, and weld-bump jumps add 1–10% error depending on speed/fluid/spring force.
Production fusion is IMU+odometer+AGM in an EKF; girth welds detected by wavelet transform validate segment lengths; LSTM compensation cut centerline error 8.75→2.02 m in field tests.
RELEVANCE: Explains our NN ±2 m stability and ~100 m/132 km odometer stability; weld-log pipe lengths are the independent check on odometer slip.
Verdict: ADAPT — AGM-interval correction model + weld-length cross-check as QC rule.

## (c) Girth-weld matching and pipe-tally reconciliation

Covered jointly by S2 + S5, plus:
**S7. Cenosco FFS chain (tally reconciliation pattern)** — https://cenosco.com/insights/pipeline-fitness-for-service-software-ili-repair-plans
Every tally/dig-up import reconciles wall thickness section-by-section against file before any calculation; Condition History must be approved before use; corrections propagate automatically.
RELEVANCE: Our weld-log master needs the same gate — thickness/type mismatch (e.g. PK1 spiral vs straight, SMYS→Sy renames) blocks the join rather than silently passing.
Verdict: USE — wall-thickness reconciliation gate in the pipe join.

## (d) Open data standards: PODS / UPDM / OGC / PODS-ABA

**S8. PODS 7 conceptual model + ILI module (7.0.2)** — https://pods.org/data-models/ ; https://pods.org/wp-content/uploads/2024/06/PODS7-Poster.pdf
`ILI_INSPECTION` (vendor, tool, tolerance, run direction, start/end odometer) → `ILI_DATA` anomaly rows keyed by `ODOMETER + US/DS_GIRTH_WELD_NUMBER + DISTANCE_TO_US/DS_GW + US/DS_MARKER_STATION + JOINT_NUMBER/VENDOR_JOINT_NUMBER`, with depth/length/width/orientation, B31G fields, `POINT_X/Y/Z`.
Designed for 500k+ records/run and 200+ runs/year re-issues; run-to-run analysis across vendors is the explicit goal.
RELEVANCE: Our 44-col tables map ~1-to-1 onto `ILI_DATA` (Distance→ODOMETER, weld offsets→DISTANCE_TO_US/DS_GW, markers→MARKER_STATION, Pipe No→JOINT_NUMBER); adopting these names makes exports PODS-loadable.
Verdict: ADAPT — rename canonical ETL schema to PODS ILI_DATA fields.

**S9. Esri UPDM 2020 + PODS-on-UPDM modules (2026)** — https://pods.org/esri-and-pods-association-launch-first-three-pods-modules-on-updm/ ; https://community.esri.com/t5/blogs/blogarticleprintpage/blog-id/gas-and-pipeline-blog/article-id/31
First three PODS-on-UPDM modules: ILI (millions of points, cross-vendor run-to-run), Integrity-Regulatory, SCADA-link; UPDM adds attribute rules/contingent domains (e.g. material constrained by asset type) and linear-referenced events.
RELEVANCE: Path to GIS-ifying our 0%-coord data later: keep chainage master now, emit UPDM/PODS events when coords arrive; use domains for class-map and unit enforcement.
Verdict: ADAPT — domains + event model; defer full GIS migration.

**S10. OGC PipelineML 1.0 + Observations & Measurements** — https://www.ogc.org/standards/pipelineml/ ; https://docs.ogc.org/is/18-073r2/18-073r2.html
Core covers as-built/rehabilitation components; `PMLAnomaly` (location, % wall loss, orientation, weld proximity, temporal change) is an explicitly reserved *future* class — i.e. no stable open anomaly schema exists in OGC today.
RELEVANCE: Do not target PipelineML for anomaly exchange now; PODS ILI_DATA is the stable target. Revisit if `PMLAnomaly` is ever published.
Verdict: REJECT (for anomaly ETL) — monitor only.

## (e) Data-quality frameworks for ILI

**S11. API 1163 (3rd ed. 2021) validation + PRCI tool** — https://irthsolutions.com/blog/api-1163-3rd-edition-whats-changed ; https://frontlineintegrity.co.uk/how-did-i-do-2/ ; https://frontlineintegrity.co.uk/thumbs-up-or-thumbs-down/
Tiered Levels 1/2/3 (run-to-run unity plots → POD/POI binomial tests → tolerance intervals/bias); run acceptance is the operator's hold-point via a vendor Data-Quality Assessment (missing sensors, speed excursions, degraded sections).
Unity plots with tolerance ellipses separate in-spec vs out-of-spec sizing (typical ±10% WT @ 80%); Level 1 Option 2 is literally previous-vs-current ILI matching.
RELEVANCE: Formalizes our QC: per-survey DQA sheet, unity plots ON 2016→2021→2025 as Level-1 validation, voided/blank rows dispositioned (not silently kept/dropped).
Verdict: USE — DQA gate + unity-plot validation per survey pair.

**S12. Baker Hughes signal-vs-box matching + defect-specific tolerances (PPSA 2025)** — https://www.ppsa-online.com/papers/25-Aberdeen/Paper%207%20BH.pdf
Signal matching (raw MFL alignment) beats box matching on CGR accuracy; ML trained on signal-matched ground truth upgrades box-matched CGRs; cloud Dig Database aligns thousands of runs with laser-scan truth.
Per-defect tolerances (vs static ±10%) cut unnecessary digs up to 62% in operator trials.
RELEVANCE: Our box-only matching inherits box-matching bias — flag CGR uncertainty explicitly and request raw-signal re-analysis only for high-consequence mismatches.
Verdict: ADAPT — uncertainty flags + targeted signal-match requests.

## (f) 2022–2026 tooling: PODS implementations, cloud ILI, ML-ready datasets

**S13. Cloud ILI platforms (AIP/CIM on Azure; ROSEN IDW + Virtual-ILI)** — https://marketplace.microsoft.com/en-us/marketplace/apps/onebridgesolutions.asset-integrity-for-pipelines?tab=overview ; https://contenthub.rosen-group.com/api/public/content/fb75621fb13a4158bc3a7eb0105ea296?v=058539a2
Vendor Portal validates ILI *before* upload against operator rules; IDW (tens of thousands of pipelines, decades) trains Virtual-ILI to predict max-depth/defect-density on unpiggable lines from design+environment covariates.
RELEVANCE: Pattern for our intake (validate-at-ingest with the `io.py` salvage path logged, not hidden) and for forecasting with year/contractor/standard covariates.
Verdict: ADAPT — pre-upload validation + covariate-aware growth models.

**S14. ML-ready ILI analytics (2023–2026)** — https://link.springer.com/content/pdf/10.1186/s43065-023-00081-w.pdf ; https://www.nature.com/articles/s41529-026-00761-4 ; https://github.com/readyforchaos/Predict-external-corrosion-on-oil-and-gas-pipelines
Gumbel (max depth) + Weibull (defect density) stochastic growth on weld-relative positions; Siamese/CNN matchers reaching ~98% pairing accuracy, cutting CGR error 15–20%→~5%; DNV/Azure hackathon pattern: FME ETL → 300→22 features → binned depth classifier (~90% accuracy).
RELEVANCE: Directly consumable once our ETL emits clean PODS-named features: weld-relative position, clock, dimensions, depth% — the exact model inputs these papers use.
Verdict: USE — emit ML-ready feature table in PODS names; pilot Gumbel/Weibull + binned-depth baselines.

## ETL action list (weld-log master focus)
1. Canonical schema renames to PODS `ILI_DATA` fields; meaning-based class map (ARTD→GOUG etc.) versioned per survey.
2. Weld-log master joint table (Pipe No + length + type/thickness); OTA-5%-style auto-match, offset-QC plot gate, manual override list.
3. Post-correction matching windows (±2 m / ±0.5 m / ±1 h) + ambiguity flag + new/vanished/uncertain classes; bin-level growth score over all calls.
4. Per-survey DQA sheet (salvage log, blanks disposition, AGM/marker accounting, thickness reconciliation) + Level-1 unity plots on the ON reference pair.
