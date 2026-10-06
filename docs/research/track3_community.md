# Track 3 — Community / Artifact Sweep (Kaggle, HF, GitHub, PHMSA, practitioners)

Scope: GTK1 VTD triage (44/45-col anomaly tables + weld logs, §DATA.md). Question per item: usable data? reusable code? method idea?
Frozen-scope note: we do **newly-reported ≥10% watchlists**, not physical growth prediction (README/GUARDRAILS).

## (a) Public datasets — Kaggle / HF / open research

### 1. Mendeley: Cross-country pipeline ILI ×4 runs (Yarveisy / Khan / Abbassi, 2021)
- Link: https://data.mendeley.com/datasets/c2h2jf5c54/1 (paper: https://www.sciencedirect.com/science/article/pii/S2667143321000548)
- Content: 4 consecutive ILI sets over ~7 yr, >200 km, external corrosion; anonymized (no coords). The only open true repeat-ILI tabular set found. CC-BY-ish Mendeley Data licence (check v1 page before redistributing).
- Relevance: Closest schema analogue to our 44-col tables (distance/clock/depth/length/width + weld refs). Ideal sandbox for testing greedy-vs-Hungarian matching and past→future validation without touching private VTD.
- Verdict: **USE (method sandbox + benchmark; do not merge into training)** — licence + anonymization OK for local experiments.

### 2. Kaggle: Pipeline Defect Dataset — CCTV/sewer video frames (16 classes)
- Link: https://www.kaggle.com/datasets/manaidu/pipeline-defect-dataset-data (mirror: https://www.kaggle.com/datasets/simplexitypipeline/pipeline-defect-dataset)
- Content: Robot-camera stills labelled broken/deformation/disconnection/misalignment/deposition/obstacle. Image CV task for sewer pipes, no depth/odometer/wall-thickness columns.
- Relevance: Zero overlap with VTD tabular schema; no ILI physics. Useful only if someone later adds photo-of-dig verification, which is out of frozen B1 scope.
- Verdict: **REJECT (data); ADAPT only the YOLOeval harness idea** — check per-dataset Kaggle licence, but do not ingest.

### 3. Kaggle notebooks: predictive-maintenance / thickness-loss (synthetic 1000-row tabular)
- Links: https://www.kaggle.com/code/muhammadwaqas023/predictive-maintenance-of-oil-and-gas-pipelines ; https://www.kaggle.com/code/devraai/pipeline-thickness-loss-predictive-maintenance ; related RUL notebook (Apache-2.0)
- Content: Small synthetic tables (corrosion %, thickness loss, pressure) with RF/GBM failure classifiers. No competition, no winning solution; pedagogical notebooks.
- Relevance: Method pattern only — train/test split by time, P@K-style inspection ranking, HistGradientBoosting baseline. Their "failure" label ≠ our operational ≥10% new-report label.
- Verdict: **ADAPT (notebook pattern; reuse HistGB + time-split discipline)** — Apache-2.0 where stated; treat data as toy.

### 4. HuggingFace: DefectSpectrum + Roboflow in-pipe corrosion images
- Links: https://huggingface.co/datasets/DefectSpectrum/Defect_Spectrum ; https://universe.roboflow.com/piro-jgvtw/in-pipe-corrosion-and-cracks-ntjmq
- Content: Large manufacturing-surface-defect image benchmark (DefectSpectrum) and 693 open-source in-pipe corrosion/crack photos. No odometer/depth/%WT columns.
- Relevance: No fit to 44-col ILI tables. Confirms HF has **no tabular ILI/corrosion-growth dataset** as of Oct 2026 (search returns only CV sets + `transformers` pipelines false positives).
- Verdict: **REJECT (data)** — licences vary (check per-repo); not applicable to VTD triage.

### 5. Velázquez soil-pitting set (241 rows) + NIST soils program (via papers)
- Links: paper https://content.ampp.org/corrosion/article/66/1/016001-1/7386/Technical-Note-Field-Study-Pitting-Corrosion-of ; augmentation study https://www.mdpi.com/1996-1944/17/5/1142
- Content: 241–259 excavation points: dmax, age, coating, pp, pH/resistivity/wc/redox. Small, no repeat ILI, no odometer matching.
- Relevance: Only open source linking environment → pit depth. Could supply an informative prior for segment-level susceptibility overlay (OFF by default per guardrails), never per-defect growth.
- Verdict: **ADAPT (prior/stratification idea only)** — paper data, no clean licence; retype a few summary stats, do not redistribute raw.

## (b) Kaggle competitions / notebooks — corrosion/defect prediction

### 6. No standing Kaggle competition on ILI corrosion growth (gap confirmed)
- Search 2026: only sewer-defect CV sets + toy tabular notebooks (§2–3 above); no "ILI matching / CGR" competition with winning write-ups.
- Content: Best available proxies are the HistGB depth-regression notebook (§6 in GitHub) and RUL-regression notebooks (blending/GBM, Apache-2.0).
- Relevance: Takeaway pattern — winners on adjacent tabular tasks use gradient boosting + time-based folds + calibrated thresholds; directly maps to our per-section ≥10/12/15% cut-sensitivity reporting.
- Verdict: **ADAPT (evaluation discipline, not data)** — nothing to download; cite notebook licences if code is copied.

## (c) GitHub — ILI / corrosion-growth / integrity

### 7. Farhad-Davaripour/AI_Applications_in_Pipeline_Engineering (47 commits, MIT, ★0/⑂2)
- Link: https://github.com/Farhad-Davaripour/AI_Applications_in_Pipeline_Engineering (demo https://ai-applications-in-pipeline-engineering.streamlit.app)
- Content: End-to-end on the Mendeley §1 data: EDA → anomaly mapping across years → aspect-ratio/cyclic-clock features → HistGradientBoosting depth regression + missing-depth imputation + Streamlit visualizer.
- Relevance: Directly reusable matching-feature ideas (aspect ratio, cyclic clock) and the "compare ML vs domain estimate" audit we already do. Matching code is simpler than ours (no Hungarian); good pedagogical contrast.
- Verdict: **USE/ADAPT (features + audit pattern; MIT)** — practical; vendor-neutral.

### 8. vb64/pipeline.integrity (MIT, ★2/⑂2, pip `pipeline-integrity`) + Eduard-Ibr/pipeline-ffs (MIT, Flask, B31G+DNG)
- Links: https://github.com/vb64/pipeline.integrity ; https://github.com/Eduard-Ibr/pipeline-ffs
- Content: Tiny ASME B31G-2012 ERF/safe-pressure calculators (length×depth→ERF, years-to-repair at fixed rate); pipeline-ffs adds DNV-RP-F101 + remaining-life web form.
- Relevance: Our tail cols already carry Danger/KBD/Pf (DATA.md §schemas) — these libs give an independent ERF cross-check for the watchlist top-K without trusting vendor Pf. No matching/growth logic.
- Verdict: **USE (vb64 as offline ERF spot-check; MIT)** / **ADAPT (ffs form ideas only)** — verify units (inches/psi defaults!) before any use.

### 9. Akhila-Susarla/CorroSight (★0, 2 commits; KD-tree + Hungarian + weld alignment)
- Link: https://github.com/Akhila-Susarla/CorroSight
- Content: FastAPI+Angular platform: 3-vendor normalization (15/34/43→20 cols), ~1603 girth-weld piecewise-linear odometer correction, KD-tree candidates + `linear_sum_assignment`, growth regression, B31G interaction + dig list.
- Relevance: Architecture mirror of our frozen `io/match/features` pipeline; validates our Pipe-No + ±2 m + ±0.5 m + ±1 h match recipe and weld-log-as-primary-key choice. Code is greenfield/untested — read, don't depend.
- Verdict: **ADAPT (matching + alignment method notes; licence = check LICENSE file)** — borrow scoring weights/confidence formula, keep our parity-tested matcher.

## (d) PHMSA incident data — usability for segmentation

### 10. PHMSA GT/GD/HL incident ZIPs (operator-reported, public domain, 1984/1985→present) + flagged 20-yr trends
- Links: https://www.phmsa.dot.gov/data-and-statistics/pipeline/distribution-transmission-gathering-lng-and-liquid-accident-and-incident-data ; trends https://www.phmsa.dot.gov/data-and-statistics/pipeline/pipeline-incident-20-year-trends ; portal https://pipeincident.azurewebsites.net (403 on direct fetch 2026-10-06 — use landing page + ZIP downloads)
- Content: Per-incident rows: date/location/operator, deaths/injuries, commodity released, cause, property damage; field-definition file in each ZIP. US only, event-level (no ILI depths, no odometer).
- Relevance: Cannot train or validate 100 m VTD watchlists (no defect linkage, different population). Usable only as segment-context overlay: national cause mix (corrosion ≈ ~23% of significant per Fessler 2008, https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/technical-resources/pipeline/gas-transmission-integrity-management/65341/finalreportpipelinecorrosion.pdf) to sanity-check that corrosion-priority segments are plausible.
- Verdict: **ADAPT (context/overlay only; US public-domain data)** — never as labels; note reporting-threshold breaks in trend lines.

## (e) Practitioner blogs / forums — VTD threshold, POD, vendor differences

### 11. Irth/OneBridge active-vs-passive corrosion models + Cenosco ILI-comparison + Frontline POD note
- Links: https://irthsolutions.com/blog/using-data-science-to-determine-active-internal-corrosion-0 ; https://ims-handbook.cenosco.com/docs/pl-ili-comparison-match-defects-and-corrosion-rates-tables ; https://frontlineintegrity.co.uk/how-did-i-do-2 ; related https://www.mistrasgroup.com/resources/newsroom/2021/06/01/signal-to-signal-corrosion-growth-matching-services-for-pipeline-integrity
- Content: OneBridge: pit-to-pit CGR is noisy → bin anomalies (50+/≤400 ft) and score populations by mean×sd×skewness; new-pipe-as-coupon trick; validated on ~500 pipelines. Cenosco: default match threshold 0.3 m. Frontline: vendor POD typically quoted 90% (9/10 detection).
- Relevance: Direct support for our guardrails: report match-rate/vanished-frac/cut-sensitivity; distrust single-pit deltas; keep per-survey contractor covariate; treat vendor threshold/POD as calibration input (our requested "per-survey thresholds" in DATA.md §Reference pair).
- Verdict: **ADAPT (method + QC discipline; vendor blogs, no code licence needed)** — cite, don't copy; signal-to-signal monograph is vendor service pitch.

### 12. PRCI/C-FER repeat-ILI growth-rate method (Nessim et al., IPC 2008) + PRCI PR-186 generic CGR distributions
- Links: https://www.cfertech.com/insights/obtaining-corrosion-growth-rates-from-repeat-in-line-inspection-runs-and-dealing-with-the-measurement-uncertainties ; http://prci.org/report/pr-186-213600-r01-generic-external-corrosion-growth-rate-distributions-for-buried-pipelines ; webinar https://prci.org/webinar/pr-186-213600-w01-ili-based-generic-external-corrosion-growth-rate-for-buried-pipelines
- Content: Formal treatment: CGR distribution as function of (observed growth ÷ sizing error); when ratio is small, uncertainty swamps inference. PR-186 gives empirical generic external-CGR priors from ILI + NDE.
- Relevance: The principled backing for our "no ≥80% claim" stance and our uncertainty-flagged new/vanished logic. Generic CGRs could seed a future (non-frozen) remaining-life overlay; today they justify conservative watchlist language.
- Verdict: **USE (method reference + uncertainty framing; PRCI reports are member/paid — use public abstracts + C-FER summary)** — do not redistribute.

## Bottom line for GTK1
- Download now: Mendeley 4-run ILI set (sandbox), vb64 B31G lib (ERF check), PHMSA ZIPs (context). Read-only: Farhad + CorroSight matching code, OneBridge/C-FER/PRCI method notes.
- Nothing found replaces VTD tables or weld logs; nothing on Kaggle/HF matches the 44-col schema. No git commits made by this sweep.
