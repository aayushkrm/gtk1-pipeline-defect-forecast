# Track 7 — Adjacent forecasting paradigms + Russian sources

Context: GTK1 frozen scope is B1 triage — ranked 100 m-segment watchlists for newly-reported ≥10% defects (past→future validated, per-section models, no pooling). P1 = triage ranking; P2 = any future defect-growth forecasting. Russian-data context: 3-survey VTD reports (2016/21/25-style), STO Gazprom norms, Gazprom transgaz Tomsk partnership.

---

## (a) RUL ML for industrial assets — NASA C-MAPSS lessons

**[1] C-MAPSS deep-learning RUL review — Sci. Rep. 2025 (Nature).** https://www.nature.com/articles/s41598-025-09155-z
Content: (1) Surveys LSTM/GRU/attention/CNN RUL models on NASA C-MAPSS turbofan data (FD001–FD004, 1–6 operating conditions, 1–2 fault modes). (2) Standard pipeline: piece-wise-linear RUL labels (flat healthy phase capped ~125 cycles, then linear decay) + NASA asymmetric score penalising late predictions. (3) Best gains come from preprocessing/operating-condition normalisation, not deeper nets; small hybrids often match large models.
Relevance: (1) P1/P2: piece-wise labelling + asymmetric late-prediction penalty is directly reusable if P2 ever scores time-to-defect. (2) Russian-data caveat: C-MAPSS has dense run-to-failure cycles with known EOL; our VTD has 2–3 sparse snapshots per section with no observed "failure" — regression-on-RUL is not estimable here.
Verdict: **ADAPT** (label/penalty design only, not the models).

**[2] NASA C-MAPSS dataset definition.** https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data
Content: (1) Simulated turbofan degradation, engines start with unknown initial wear/manufacturing variation. (2) Multivariate sensor streams per cycle + true RUL vectors for test. (3) Explicit multi-condition/fault-mode splits (FD002/FD004 test generalisation).
Relevance: (1) Transfers: the "unknown initial wear" framing matches our unknown pipe-age/coating-history problem — per-unit baselining matters. (2) Does not transfer: continuous sensor telemetry vs 5-year-gap ILI snapshots; FD-splits assume comparable units, our sections differ by diameter/coating/contractor.
Verdict: **ADAPT** (evaluation-split thinking; reject direct modelling analogy).

---

## (b) Survival analysis for censored time-to-defect

**[3] Gradient-boosted survival models for corrosion risk-based inspection of gas pipelines — Appl. Sci. 2026 (MDPI 16(16):7884).** https://www.researchgate.net/publication/411897315_Gradient-Boosted_Survival_Models_for_Corrosion_Risk-Based_Inspection_of_Gas_Transmission_Pipelines
Content: (1) Predicts time-to-failure of pipeline steels to schedule inspection inside an RBI framework. (2) Compares random survival forest / gradient-boosted survival against Cox baselines on censored corrosion data. (3) Outputs survival curves per segment, not point RUL — inspection priority follows predicted hazard.
Relevance: (1) P1: per-100 m survival curves are the natural upgrade of our watchlist if a second time-point ever supports censoring notation (defect-free at last survey = right-censored). (2) P2/Russian context: handles exactly our data shape — most pipes never defect (censored), surveys are interval-censored; matches STO-style remaining-life language better than regression.
Verdict: **ADAPT** (pilot RSF/Cox on ON 2016→2021→2025 as P2 spike; keep P1 frozen).

**[4] randomForestSRC — Random Survival Forests reference.** https://www.randomforestsrc.org/articles/survival.html
Content: (1) RSF = ensemble of survival trees with log-rank splitting, OOB error via Harrell's C / Brier score / CRPS. (2) Native handling of right-censored data, variable importance under censoring. (3) Mature R implementation with prediction-error curves over time.
Relevance: (1) P2 tooling: fastest route to a survival pilot on pipe-level time-to-≥10% with censoring flags. (2) Caveat: needs honest interval-censoring treatment (defect appeared sometime between surveys) — naive right-censoring biases hazard estimates.
Verdict: **USE** (as P2 prototyping tool, not production).

---

## (c) Multi-task / transfer learning across sections (pooling question)

**[5] Transfer learning for internal-corrosion prediction in pipelines — Politecnico di Milano (J. Pipeline Sci. Eng.).** https://www.researchgate.net/publication/355104456_A_transfer-learning_approach_for_corrosion_prediction_in_pipeline_infrastructures
Content: (1) ML corrosion model trained where labels are abundant, fine-tuned where target-pipeline labels are scarce. (2) Shows positive transfer only when source/target feature distributions overlap; otherwise negative transfer. (3) Explicit small-data regime — the realistic VTD case (one section, few matched defects).
Relevance: (1) Directly tests our no-pooling rule: pooling SRTO+ON+PK sections is multi-task with distribution shift (D720 vs D1220, film vs other coatings, contractor change) — negative transfer is the expected outcome. (2) P2: source→target fine-tune (e.g. ON→PK1) is the only pooling variant worth a gated experiment, with per-section fallback.
Verdict: **ADAPT** (one gated ON→PK1 fine-tune experiment; default stays no-pooling).

**[6] Transfer-learning CNN-LSTM-Transformer for corrosion-rate prediction, small samples — 2025 (PMC).** https://pmc.ncbi.nlm.nih.gov/articles/PMC12530524/
Content: (1) Compares empirical / statistical / ML corrosion predictors; proposes CNN-LSTM-Transformer + gradual fine-tuning for small samples. (2) Reports gains over from-scratch training on limited target data. (3) Code published (github.com/longpujun/Tranfer_Learning).
Relevance: (1) P2 cautionary: architecture is built for dense corrosion-rate time series, not 3-snapshot ILI — expect the gain to vanish on our sampling. (2) Useful only as a negative-control reference if anyone proposes deep sequence models for GTK1.
Verdict: **REJECT** (for our data regime; keep as cited negative control).

---

## (d) Russian VTD literature (cyberleninka / elibrary-adjacent)

**[7] Выдренков/Медведев/Шагбанов/Голик (ТИУ) — прогнозирование остаточного ресурса на базе интеллектуальных методов, 2024.** https://cyberleninka.ru/article/n/prognozirovanie-ostatochnogo-resursa-gazonefteprovodov-na-baze-intellektualnyh-metodov-analiza-dannyh
Content: (1) Compares ОСТ 153-39.4-010-2002 factor-based vs statistical residual-life calculations (~10–14% disagreement on a 15-year gas-transport segment). (2) Trains per-medium (gas vs liquid) gradient-boosting ensembles (CatBoost/XGBoost/GBM + k-means denoising) on ~30 diagnostic/operational variables. (3) Claims ~2% deviation from actual decommissioned-segment life vs ~14.5% for norm methods.
Relevance: (1) Closest Russian analogue to P2: defectoscopy-driven ML residual life, separate gas/liquid models (= our no-pooling instinct). (2) Caveat: single-segment verification, no past→future protocol reported — their 2% is in-sample-adjacent; our bar (prospective validation) is stricter.
Verdict: **ADAPT** (per-medium modelling discipline + CatBoost baseline for P2; discount accuracy claim).

**[8] Любчик/Крапивский/Большунова (Горный университет) — прогнозирование состояния МГ по анализу аварий, 2011.** https://cyberleninka.ru/article/n/prognozirovanie-tehnicheskogo-sostoyaniya-magistralnyh-truboprovodov-na-osnove-analiza-avariynyh-situatsiy
Content: (1) 200+ gas-pipeline accidents: 80% SCC failures at 4–8 o'clock position, 70% within 25 km downstream of compressor stations, 80% on >10-year pipe. (2) 45-factor expert system "Прогноз-2" combining protection potential, soils, insulation state, stress concentrators. (3) Argues probabilistic localisation forecast from distance/geophysical features where ILI is blind.
Relevance: (1) P1 feature ideas: distance-to-KS, clock-position priors, soil/corrosion-activity covariates are cheap past-only features compatible with triage. (2) Validates our guardrail stance: ILI misses shallow SCC (<10–15%), so "newly-reported" ≠ "newly-formed" — report language must stay operational.
Verdict: **USE** (feature priors + blind-spot justification).

**[9] Арабей/Шипилов/Ряховских (Газпром/ВНИИГАЗ/Газнадзор/Трансгаз Югорск) — система прогнозирования стресс-коррозионных участков, 2019.** https://cyberleninka.ru/article/n/informatsionno-analiticheskaya-sistema-prognozirovaniya-avariyno-opasnyh-stresskorrozionnyh-uchastkov-magistralnyh-gazoprovodov-i
Content: (1) 500+ km, 35 450 SCC defects: >90% shallower than 0.1t; 52–54% of SCC pipes invisible to ILI yet cut at overhaul — VTD-based repair planning accuracy only ~36–56%. (2) 100×100 m GIS cells, Shannon-informativity factor weights, pattern-recognition + ANN two-category (dangerous/not) classifier. (3) Ranks segments for overhaul priority incl. sub-threshold defects.
Relevance: (1) Strongest precedent for P1: same 100 m cell, same ranking-for-repair framing, same sub-threshold-blindness problem — and a published Gaznadzor-coauthored accuracy baseline (~36–56%) that justifies our no-80%-claim position. (2) Their geospatial+ANN stack is the P2 design to beat, with past→future discipline added.
Verdict: **USE** (methodological template + baseline numbers for supervisor brief).

---

## (e) STO Gazprom / Gaznadzor methodology summaries

**[10] СТО Газпром 2-2.3-112-2007 + 2-2.3-1050-2016 + Инструкция Газнадзор-2013 (сводка по открытым описаниям).** https://files.stroyinf.ru/Data1/58/58899/index.htm · https://e-idpo.kstu.ru/pluginfile.php/57986/mod_resource/content/2/СТО%20Газпром%202-2.3-1050-2016.pdf
Content: (1) 112-2007: strength assessment of corroded sections — allowable pressure from defect geometry (depth/length vs wall), complex-profile interaction rules. (2) 1050-2016: ILI general requirements — tool admission, defect detection thresholds (cf. ГОСТ Р 55999-2014: SCC threshold ~0.15t), reporting/coordination procedure. (3) Газнадзор-2013 instruction: defect danger ranking + repair deadlines, implemented in ГАЗНАДЗОР-ОД-СР software.
Relevance: (1) Defines the normative meaning of our tail fields (Danger rank, KBD, Pd/Pf/MAOP) — triage watchlists should sort consistently with Gaznadzor danger ranks, not invent parallel severity. (2) Threshold provenance: any ≥10/12/15% cut must cite ГОСТ Р 55999-2014 sensitivity limits, else VTD-blind SCC undermines the cut.
Verdict: **USE** (normative alignment of ranks/thresholds; no modelling content).

---

## (f) Russian pipeline-integrity groups

**[11] ТИУ школа Земенковой — интеллектуальный нейросетевой мониторинг трубопроводов (Записки Горного института, 2022).** https://cyberleninka.ru/article/n/intellektualnyy-monitoring-sostoyaniy-obektov-truboprovodnogo-transporta-uglevodorodov-s-primeneniem-neyrosetevyh-tehnologiy
Content: (1) 8-stage NN modelling pipeline (task→inputs→outputs→training→architecture→verification) for safety-criterion monitoring. (2) Hierarchical safety criteria (mechanical/process/environmental) fused by multilayer perceptron, demo on pump-station regimes (>1000 SCADA cases). (3) Explicit import-substitution framing under national AI/digital-economy programmes.
Relevance: (1) Partner-facing: TIU/Tyumen school is the natural academic counterpart for transgaz Tomsk work — same vocabulary (остаточный ресурс, ВТД, КРН). (2) Methods are SCADA-regime oriented, not ILI-oriented — cite for context/positioning, not for code. (Gubkin side: кафедра сооружения и ремонта ГНП и хранилищ — https://gubkin.ru/faculty/pipeline_network_design/chairs_and_departments/building_and_repair_pipeline_and_storage/ — plus CPIPE tools; no open VTD datasets found at either school.)
Verdict: **ADAPT** (collaboration framing + 8-stage checklist; not ILI methods).

---

## Cross-cutting verdicts for GTK1

1. Keep P1 frozen (per-section triage, no pooling); cite [9] 36–56% baseline against inflated claims.
2. If P2 is funded: order of experiments is RSF survival [3–4] → per-medium CatBoost [7] → one gated transfer test [5]; deep sequence models [6] and C-MAPSS architectures [1–2] stay out.
3. Normative alignment ([10]) and blind-spot language ([8–9]) go into GUARDRAILS/SUPERVISOR_BRIEF, not into models.
