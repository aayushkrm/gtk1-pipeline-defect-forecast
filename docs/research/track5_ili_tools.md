# Track 5 — ILI tool physics + performance specs (threshold-drift drivers)

Context: GTK1 VTD tables show 2.5–5x anomaly-count jumps between surveys; Depth≥10% normalization mandatory; tools СО/ПМО/ДМТ per passports. Question: how much of the jump is tool/threshold change vs real growth.

## (a) Technology physics: MFL vs UT vs EMAT vs caliper

### S1. MFL vs UT vs EMAT selection guide (API-compliance framing)
- Link: https://eureka.patsnap.com/article/the-ili-tool-selection-dilemma-mfl-vs-ut-vs-emat-for-api-compliant-assessments
- Content: MFL magnetizes wall, senses flux leakage from metal loss; best for general corrosion/pitting in gas lines, no couplant, fast. UT uses pulse-echo, direct wall-thickness + cracks/laminations, needs liquid couplant, slower. EMAT generates ultrasound electromagnetically, no couplant, surface+subsurface cracks, newer/costlier.
- Relevance: Our lines are gas (Д1220/1020/720) → almost certainly MFL-family (СО/ПМО/ДМТ); UT-only effects (couplant, cleanliness) do NOT explain our drift. Any vendor switch MFL→EMAT/UT changes crack vs metal-loss sensitivity and thresholds.
- Verdict: USE — technology prior for tool-type covariate.

### S2. UT+MFL comparison white paper (NDT Global)
- Link: https://www.ndt-global.com/resources/white-paper/ut-and-mfl-inspection-comparison-for-pipeline-integrity-enhancement/
- Content: MFL is indirect (signal amplitude ∝ depth but confounded by shape/orientation/lift-off); UT/ART is direct thickness measurement, wall-independent accuracy, sees laminations/CRA/under-support corrosion MFL misses. MFL POD/sizing tolerances scale with % wall thickness; UT tolerances are absolute (mm).
- Relevance: Depth in %t must be converted with per-joint nominal thickness (pipe sheet cols); wall-variety across sections (spiral vs straight-seam) shifts absolute detection floor even at fixed 10%t. Use off-cycle different-physics tool for re-inspection to break confounding.
- Verdict: USE — justifies per-pipe thickness normalization + ILI-to-ILI cross-check.

### S3. NTSB docket: POD/POI/sizing explainer + POF metal-loss spec example
- Link: https://data.ntsb.gov/Docket/Document/docBLOB?FileExtension=.PDF&FileName=IMP%20-%20PII%20POD-POI%20ILI%20tools%20capabilities%2004-13-2012-Master.PDF&ID=40367766
- Content: POD at minimum reportable defect size (physics + pipe params); POI = correct classification once detected; sizing = tolerance + certainty, e.g. MFL depth ±10%t @80%. Example MFL POF table: general metal loss POD90 at 12%t body / 18% near weld; pitting 15%/24%; width ±20/25 mm, length ±15/20 mm @80/90%.
- Relevance: Gives concrete numbers to test our Depth≥10% cut: features 10–15% sit exactly in POD ramp where counts explode with small threshold/sensitivity change; weld-zone thresholds are ~1.5x worse → seam-type covariate needed.
- Verdict: USE — reference numbers for per-survey threshold model.

## (b) Generations / resolution → count jumps

### S4. ENTEGRA UHR + ROSEN MFL-A Plus (vendor specs)
- Links: https://entegrasolutions.com/solutions/uhr-ili-technology/why-uhr/ ; https://contenthub.rosen-group.com/api/public/content/ROSEN-Group_Serviceflyer_RoCorr_MFL-A-plus.pdf?v=aba56804
- Content: UHR = 2x sensor density + 2x sampling (Quadra up to 8x/16x) → consistent repeatable data. MFL-A Plus adds ML sizing, pinhole + axial-slotting specs covering all POF classes, reduced human-factor variance. Example specs: 360 tri-axial MFL sensors, 1 mm axial sampling, 1.32 mm circumferential spacing; metal-loss minimum 10%t, ±10%t depth @80%/95%.
- Relevance: Direct mechanism for 2.5–5x jumps: denser sensors + lower reporting floor (pinhole/pit classes newly reported) inflate small-anomaly counts without any growth. Must log vendor+generation+sensor count per survey.
- Verdict: USE — core drift hypothesis; encode tool-generation covariate.

### S5. Timashev "Basic performance metrics of ILI tools" (OSTI, proposed API 1163 basis)
- Link: https://www.osti.gov/etdeweb/servlets/purl/20897642
- Content: Full metric set: POD/PTND/false-call/miss + POI + location/sizing errors; bias drifts within a run (sensor wear, velocity excursions, lift-off, debris, channel loss, analyst decisions). Proposes per-tool lifetime "passport" updated after each run + verification digs.
- Relevance: Explains intra- and inter-survey non-stationarity even with same vendor; supports per-survey calibration (not one global correction) and run-quality flags (velocity, cleanliness).
- Verdict: ADAPT — passport idea maps to our year/contractor/standard covariate table.

## (c) API 1163 + PRCI validation

### S6. API 1163 / PRCI IM-1-06 validation explainer (Irth/OneBridge) + PRCI report page
- Links: https://irthsolutions.com/blog/validating-ili-performance-with-api-1163-and-prci-research-in-cim-0 ; https://www.prci.org/Research/InspectionIntegrity/IIProjects/IM-1-06/236614/260565.aspx
- Content: POD (detect ≥ threshold, e.g. 90% ≥10%t), POI (correct type), sizing tolerance+certainty (±10%t @80%). Level 1 = accept vendor spec (low-risk only, no digs); Level 2 = binomial test of spec vs digs (3 outcomes); Level 3 = compute as-run performance from digs, replaces vendor spec. PRCI adds spreadsheet + unity-plot workflow; depth uncertainty dominates burst pressure.
- Relevance: Our repeat-survey archive enables Level-1-adjacent ILI-to-ILI check now, Level 2/3 only where calibration digs exist; depth-first validation matches Pf/Service-tail usage.
- Verdict: USE — adopt Level definitions + unity-plot template for validation module.

### S7. JSM 2020 DigIt/CGRealBias: unity-plot statistics in practice
- Link: https://ww2.amstat.org/meetings/proceedings/2020/data/assets/pdf/1505317.pdf
- Content: ILI depth (x) vs direct depth (y) unity plots filtered by POF class (tool varies by class); three tests: paired-ratio t (preferred — scales with depth), paired-difference t, API 1163 binomial in/out-of-tolerance; binary test discards information. Demo: none of 3 tool datasets (2 MFL, 1 UT) passed API 1163 as-stated; MFL Vendor 2 needed ratio adjustment.
- Relevance: Template for our per-survey bias estimation: fit multiplicative (ratio) bias per POF class, keep binomial as compliance check only; expect vendor specs to fail as-run.
- Verdict: USE — statistical recipe for calibration layer.

## (d) POF specifications

### S8. POF 100 (2021) + POF documents index + POF 330 tool-testing (2026)
- Links: https://pipelineoperators.org/documents ; https://www.pipescanintegrity.com/assets/docs/POF%20100%20Specifications%20and%20requirements%20for%20ILI%20-%20Nov%202021.pdf ; https://pipelineoperators.org/cdn/e8e68dc3-4b02-4429-b046-af3ff64f6ebd/POF%20330%20ILI%20tool%20testing%20-%20Jan%202026.pdf
- Content: POF 100 requires POD/POI/sizing per anomaly class (general/pitting/axial/circ grooving), reporting grid, location accuracy, ERF/Psafe method. POF 310/311 standardize field verification + feedback form. POF 330 (Jan 2026) standardizes blind/open pull-test verification across velocities and defect sizes incl. sub-threshold anomalies.
- Relevance: Use POF 100 class map as our unified taxonomy; POF 311 fields as schema for any future dig records; POF 330 justifies including sub-10% anomalies in POD estimation rather than discarding.
- Verdict: USE — normative schema source.

## (e) Sizing bias + correction via digs

### S9. Hallen et al., Statistical calibration of ILI data (WCNDT 2004)
- Link: https://www.ndt.net/article/wcndt2004/html/htmltxt/712_hallen.htm
- Content: Comparative-calibration model d_ILI, d_Field = f(d_True) + noise; separates constant (additive) vs non-constant (multiplicative slope β≠1) bias via M-Wald/M-Jaech estimators; field tools also noisy (pit-gage ±0.3–0.5 mm internal/external). Monte Carlo: ~30 verification digs optimal; fewer degrades fast, more adds little.
- Relevance: Formal justification for per-survey slope+intercept correction with ~30 digs/survey-class; without digs, only relative (ILI-to-ILI) calibration is identifiable — matches our no-dig constraint.
- Verdict: USE — calibration math; ADAPT thresholds when n<30.

### S10. ROSEN in-field verification tolerances (Oldfield et al. 2023 summary)
- Link: https://www.rosen-group.com/en/expertise/experience-center/case-studies/improving-confidence-in-ili-data-through-in-field-verification
- Content: Combined ILI+field tolerance governs unity plots. MFL vs laser/micrometer (±0.2 mm): tight, high confidence. Crack tools (UTCD/EMAT) vs shear-wave field sizing (±0.7–3 mm): wide combined window can falsely "pass" a bad tool. Ignoring field tolerance over-rejects; inflating it over-accepts.
- Relevance: Any future GTK1 dig program must use laser-grade metrology for metal loss, else Level 2/3 verdicts are meaningless; until then, flag validation confidence as low.
- Verdict: USE — metrology requirement.

## (f) 2022–2026 advances

### S11. ROSEN MFL-A Plus ML sizing + NETL/PNNL ML diagnostic-prognostic program
- Links: (S4 ROSEN flyer above); https://netl.doe.gov/sites/default/files/netl-file/21CMOG_OG_Denslow.pdf
- Content: ML sizing trained on laser-mapped real-defect library improves dimension classification and pinhole detection, cuts analyst variance. DOE program: CenterNet on 3-component MFL-as-RGB → 81% boundary accuracy, depth binned per 10%; FE-simulated synthetic defects supplement sparse ground truth; prognosis needs defect-matching curation (matched pairs show ± growth noise from thresholds/matching).
- Relevance: Explains vendor-side count inflation post-~2022 (same raw signals, more calls); our forecaster should treat post-ML surveys as different reporting functions; synthetic-data trick reusable for our growth-model testing.
- Verdict: ADAPT — model vendor ML-generation as regime switch; borrow RGB/FE ideas only if raw signal ever available (currently report-level only → REJECT for sizing, USE for regime flag).

### S12. Multi-tech combo tools (TDW/Structural/EnviroCal class)
- Links: https://www.structint.com/wp-content/uploads/2026/01/ILI-Process-and-Differentiators.pdf ; https://aucsc.com/downloads/TT_Common%20PIpeline%20Anomalies_2023_P9.pdf
- Content: Single run combines axial MFL + circumferential/transverse MFL + caliper/geometry + IMU/speed control (e.g. 456 sensors, tri-axial); residual-field + secondary ring resolve mill defects/HAZ/sleeves; caliper separates dent vs metal-loss-with-dent.
- Relevance: If any GTK1 survey used combo (check ДМТ/ПМО passports), its ARTD/GOUG vs CORR split differs systematically from MFL-only years — do not pool feature-type counts naively.
- Verdict: USE — feature-type × tool interaction term.

## Synthesis: what drives our 2.5–5x drift
1. Reporting-floor drop (pinhole/pit classes newly sized by UHR/ML tools) — largest suspect; test via size-histogram comparison at 10–20%t.
2. Vendor/generation switch (sensor density, analysts/algorithms) — test via per-survey count + POF-class mix.
3. Weld-zone sensitivity change — test via seam-proximity share.
4. Real growth — residual after 1–3 are removed; only credible on matched (pipe+distance±2 m+offset±0.5 m+orient±1 h) pairs above POD90 of *both* surveys.
