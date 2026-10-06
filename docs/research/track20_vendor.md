# Track 20 — vendor + operator gray literature 2022–2026

Tooling disclosure: websearch worked throughout (multi-provider, no HTTP-400 this track). Paywalled primaries (PPIM/Clarion proceedings at $/paper, ASME IPC full texts) cited via public abstracts/secondary pages — full text not verified. Negative results: (a) "CorrSight pipeline ML" — no such product exists; hits resolve to a forex-trading app and an FEI light microscope; pipeline-adjacent name in track 3 ("CorroSight") not recoverable as a vendor ML note; (b) Weatherford ILI — no current vendor spec pages found (business exited ILI); covered via TDW/Baker Hughes/ROSEN instead; (c) Transneft/Gazprom quantitative ML metrics — only program-level disclosures found, no precision/recall numbers (recorded as negative below).

## (a) High-resolution MFL / combo tools + sizing ML

1. ROSEN RoCorr MFL-A Plus service flyer (AI data evaluation). https://contenthub.rosen-group.com/api/public/content/ROSEN-Group_Serviceflyer_RoCorr_MFL-A-plus.pdf?v=aba56804
Content: ML-based evaluation "minimizing human factor"; adds POF pinhole + axial-slotting classes. Specs: depth POD90 0.10t (general/pitting/pinhole/axial-grooving), depth ±0.10t at 80% certainty, length ±10–15 mm, width ±12–15 mm depending on class.
RELEVANCE: Gives the exact vendor tolerance numbers to use as sizing-noise priors in threshold calibration. AI-sizing claim shows vendors already re-tune dimension-class distributions — our count-jump analysis must expect class-shift between runs.
Verdict: USE (spec table as noise prior) — discount AI-accuracy marketing; specs, not prose, are the evidence.

2. ROSEN RoCorr MFL-A Ultra (ultra-high-resolution). https://contenthub.rosen-group.com/api/public/content/b8f0a500616a463499c440c2192a5f30?v=92d3b397
Content: UHR MFL + FEM + ML sizing; detects pinholes down to ~1 mm diameter. Specs: depth POD90 0.05t general / 0.08t pitting / 0.10t pinhole; depth ±0.08t at 80% (±0.10t at 90%); length ±4–7 mm at 80%. Separate degraded table near girth welds (±2A zone, depth ±0.17t at 90%).
RELEVANCE: Quantifies the resolution ceiling and the weld-zone penalty — directly supports our per-section/per-weld calibration and the track-5 POD-ramp argument. New-feature floods after tool upgrades (standard→Ultra) are expected, not necessarily real growth.
Verdict: USE — best public numbers for threshold-drift modeling; note weld-zone table when weighting near-weld calls.

3. ROSEN RoCombo MFL-C/XT (axial MFL + eddy-current caliper combo). https://contenthub.rosen-group.com/api/public/content/4f34c472ae3741fb8e93770cc275cac5?v=0c98e53a
Content: Single-run axial metal-loss (SSWC, TOLC, channeling) + geometry/strain mapping; API-1183 Level-3-ready dent+metal-loss output. MFL specs weaker than axial tools: depth POD90 0.15t general, ±0.15–0.19t at 80%.
RELEVANCE: Combo tools trade axial depth accuracy for axial-feature coverage — feature idea: tool-type flag per run as a calibration covariate. Validates our dent×metal-loss colocation features (track 14).
Verdict: ADAPT (tool-type-aware calibration) — combo-run depth numbers are noisier; never pool with axial-MFL runs.

4. Baker Hughes × TC Energy ML tolerance project (World Pipelines, Sep 2023). https://www.worldpipelines.com/special-reports/06092023/advanced-analytics-in-north-america/
Content: "Big data" library of field laser truth data + highest-resolution MFL signals; goal: per-feature predicted tolerance replacing binned ±10% specs. 40,000+ defects over 2 pipelines correlated to laser; inputs: predicted L/W/D, raw triaxial signal parameters, fitting interactions, neighbor-defect interactions.
RELEVANCE: Feature blueprint — signal characteristics + neighbor interactions predict per-anomaly sizing error; mirrors our planned per-section calibrators. Confirms vendor tolerance bins are conservative averages operators want to beat.
Verdict: ADAPT (per-anomaly uncertainty features; replicate with our dig data) — vendor-side study, discount the "step change" framing until peer-reviewed.

5. NDT Global Trinity UHR platform + TDW MDS Pro/Flex Ultra Res. https://www.ndt-global.com/uhr-mfl-ili-technologies/trinity/ ; https://www.tdwilliamson.com/mdspro
Content: Trinity: axial MFL + caliper + low-field combo, UHR sensor density claimed since 2015. TDW: Ultra Res axial MFL for pinhole/complex corrosion; SpirALL MFL for axial features/SSWC; ML classifier for gouge-vs-dent validated on real-world features.
RELEVANCE: Second and third independent confirmations that UHR = denser sensors + higher sampling, and that ML is deployed for classification (gouge) not depth regression — bounds what "vendor ML" credibly claims. Run-comparison compatibility (Flex↔Pro) matters for our matched-pair design.
Verdict: USE as existence proof of UHR/ML-classification practice — discount "benchmark" claims without published POD tables.

## (b) Production-ML integrity platforms

6. OneBridge PPIM 2020 dig-to-repair study (1,074 runs, 23,000+ digs). https://onebridgesolutions.com/resources/case-studies-resources/ppim/statistical-analysis-of-dig-operations-leading-to-productive-repairs and https://finance.yahoo.com/news/onesoft-dig-repair-ratio-white-120000537.html
Content: Repair Fraction (productive digs) mostly 40–60%; pit-to-pit growth model correlates repair yield with growth rate while operator half-life model is flat/negative. Claimed 10–20% efficiency gains possible; even 1% matters at $91k/dig scale.
RELEVANCE: Only public at-scale dig-program baseline with N in the tens of thousands — anchors our dig-program design economics and the pit-to-pit > half-life position. Caveat: vendor-authored, single-platform data, no independent replication.
Verdict: USE baseline numbers with vendor-discount — ADAPT pit-to-pit growth prioritization for dig ranking.

7. OneBridge CIM ML ingestion classifier + alignment (now Irth AIP). https://irthsolutions.com/blog/onebridge-solutions-maximizing-pipeline-integrity-with-machine-learning-0 ; https://irthsolutions.com/blog/back-to-the-future-with-cim-2
Content: Bayesian classifiers trained on 5,000–6,000 ILI reports / 40–50M anomalies normalize any vendor format to a standard taxonomy; automated weld + anomaly-box alignment with 1-to-many matching; API-1163 Level 2/3 validation built in.
RELEVANCE: Direct template for our ETL: vendor-agnostic taxonomy + weld-anchored alignment + multi-match handling. No precision/recall published — treat as architecture reference, not accuracy claim.
Verdict: ADAPT architecture — REJECT any implied classification-accuracy transfer; demand our own unity-plot validation.

8. Cenosco IMS + Open AI Energy Initiative (CARMA/AIR). https://cenosco.com/insights/artificial-intelligence-and-asset-integrity-management
Content: Shell/Microsoft/Baker Hughes/Cenosco consortium; CARMA correlates wall-thickness + process data to forecast corrosion rates; AIR drone-imagery ML; Hydrocor physics models for CO₂/H₂S/MIC. No ILI-sizing ML, no precision/recall disclosed — refinery/plant focus, pipeline module is GIS/ILI bookkeeping.
RELEVANCE: Useful as physics-informed rate-model complement (process-condition covariates), not as ILI analytics. Confirms no vendor publishes production precision/recall for pipeline ML — our honesty-first reporting is the norm, not a deficit.
Verdict: ADAPT rate-model covariate idea — REJECT as ILI-ML evidence (wrong asset class, no metrics).

## (c) IPC/PPIM run-comparison + growth ML

9. TC Energy 5-vendor SSWC pull-through test (IPC 2024). https://exa.ai/library/publication/f4vs946twr0
Content: 24-in string with natural + synthetic SSWC/pits/slots/cracks; 12–15 runs per tool at varied speeds; POD/POI/sizing per API 1163. Findings: highest sensor density = most accurate/precise overall; circumferential MFL better precision on narrow seam-weld slots; axial-MFL-with-SSWC-spec better accuracy; one vendor misclassified most seam pits as SSWC.
RELEVANCE: Strongest public evidence that vendor + tool-type effects dominate near-weld sizing — formalizes our never-pool-vendors rule and per-survey POD priors. Misclassification rates justify our two-tier label spec (track 13).
Verdict: USE — operator-run, multi-vendor, API-1163-scored; rare non-marketing ground truth.

10. Petrov/Scudder (OneBridge) six-growth-model comparison, PTC 2023. https://www.pipeline-conference.com/abstracts/comparison-corrosion-growth-models
Content: Six industry growth models scored against field-verified depths; guidance on young single-ILI pipelines and negative-growth handling; short-term dig planning needs instantaneous rate, long-term replacement needs multi-run trend. Full text paywalled — abstract only.
RELEVANCE: Only head-to-head growth-model benchmark found in gray literature; supports our two-horizon design (dig-now vs plan-later rates). Negative-growth handling is directly relevant to our threshold-drift data.
Verdict: ADAPT model-comparison protocol — full text not verified; replicate comparison on Mendeley sandbox.

11. Bokhankevich (TDW) kNN run-comparison error compensation, PTC 2024. https://www.pipeline-conference.com/abstracts/towards-accurate-corrosion-growth-rates-addressing-matching-errors-during-run-comparison
Content: kNN-based run-comparison algorithm benchmarked on synthetic matches; quantifies matching-error bias in CGRs; warns manual deep-anomaly samples over-conservatize rates; filtering negative deltas examined. Abstract only.
RELEVANCE: Independent validation of our matcher-first methodology: matching error is a first-order CGR bias, and naive deep-only sampling inflates rates — same mechanism as our vanished-fraction argument.
Verdict: USE conclusion, ADAPT synthetic-benchmark method for our matcher ablation.

## (d) Operator-published analytics + RU disclosures

12. Enbridge Integrated External Corrosion Management (AMPP 2022/2024). https://www.elsyca.com/learn/laying-the-foundation-for-an-engineered-and-integrated-approach-to-pipeline-external-corrosion-prote ; https://www.elsyca.com/learn/cathodic-protection-optimization-using-integrated-external-corrosion-management-ampp-2024
Content: Shift from compliance/time-based to predictive forecasting over 17,000 miles; ILI + CP surveys fused with digital twins; 10-segment case studies with accuracy assessment and cost-benefit. No ML precision/recall published.
RELEVANCE: Operator precedent for ILI×CP fusion and segment-level forecasting — supports our ECDA/CP feature requests (track 15) and per-section modeling. Process template for dig-program design reviews.
Verdict: ADAPT fusion workflow — no accuracy numbers to borrow.

13. Gazprom/VNIIgaz SCC seminar VI (2022) + Ekaterinburg VTD program (2024). https://www.ras.ru/digest/showdnews.aspx?id=1d21e8c8-3081-466c-af02-e789c7ffadb4&print=1 ; https://mysertif.ru/uralskie-gazoviki-pristupili-k-realizacii-programmy-vnutritrubnoj-defektoskopii-2024-goda/
Content: 50+ institutes/operators; topics include intelligent diagnostic-support systems and "machine analysis of VTD data" (Kaverin predictive-modeling lab), auto-analysis of VTD reports, FEM of SCC defects. Ekaterinburg: 2,500 km planned 2024 (2,300 km in 2023) on Orenburg–Samara/Soyuz lines. No quantitative ML metrics disclosed — negative result on numbers.
RELEVANCE: Confirms Russian operators pursue the same ML-on-VTD agenda (validates problem framing for partner); program scale (thousands of km/yr) sets throughput expectations for our pipeline. Cyberleninka Nizhny Novgorod study (2012–2018, 3 contractors) adds: domestic tools miss <20%t SCC, girth-weld slot detection ≤50% — a citable RU-side POD anchor.
Verdict: USE as program context + RU POD anchor — REJECT as ML-evidence (no metrics disclosed).

## (e) Data-delivery formats in practice

14. PODS 7 data model (ILI tables) + API 1163 3rd-ed validation reality. https://pods.org/data-models/ ; https://irthsolutions.com/blog/api-1163-3rd-edition-whats-changed
Content: PODS 7 ILI_INSPECTION/ILI_DATA tables carry odometer, DS/US weld + marker ties, POF class, depth/length/width, tool tolerances, B31G fields — the de facto GIS exchange schema (200+ operators, 39 countries). Irth/PRCI analysis: at ±10%/80% only 1 of 21 vendors meets published spec; API 1163 3rd ed adds 200+ "shalls", Level 1/2/3 validation, PRCI spreadsheet tooling.
RELEVANCE: PODS field list = our ETL target schema; weld/marker ties enable weld-anchored alignment. 1-of-21 finding is the strongest public calibration warning — every run needs its own unity plot, never trust header tolerances.
Verdict: USE both — PODS as schema, 1-of-21 as calibration mandate (vendor-association source, conservatively favorable to operators).

---
Per-file footer: websearch OK all queries (EN+RU); webfetch used on ROSEN/Baker Hughes/PODS pages; OpenAlex/arXiv not needed; PPIM/Clarion + ASME full texts paywalled (abstracts only, marked above); CorrSight-pipeline and Weatherford-ILI recorded as negative; no commits made. Word count ~1,150.
