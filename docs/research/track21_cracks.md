# Track 21 — crack / SCC growth forecasting

Tooling: Exa neural search via `curl` worked throughout; exa.ai library pages rendered abstracts via webfetch. webfetch fails on PDFs/Springer-JS/MDPI-403 — recovered via shell `curl` + `pypdf` extraction (INGAA fatigue, INGAA EMAT, Song/SwRI PHMSA reports, RP-1176 companion) or mirrors (Structurae, OpenAlex). Paywalled primaries cited via abstracts — full text not verified. TDW SSWC whitepaper registration-walled (summary only).

Scope guard: weld taxonomy/X-ray (T13) and tool physics (T5) not duplicated — only GROWTH modeling, repeat-ILI sizing, crack-row treatment.

## (a) Paris-law / fracture mechanics (pressure cycles)

1. BMT/INGAA, "Fatigue Considerations for Natural Gas Transmission Pipelines" (2016, 131 pp, public PDF). https://ingaa.org/wp-content/uploads/2016/07/29846.pdf
Content (verified PDF extraction): HSE/BS-7910/API-579 Paris table for ferritic steels — simplified C=5.21e-13, m=3.0 (mm/cycle, MPa√mm); two-slope constants split at R≤0.5/R>0.5 (mean, mean+2SD). PRCI tests on 12 line-pipe steels (X46–X70, 1930s–2013) plot below BS-7910 means. Rainflow counting mandated (closed hysteresis loops → pressure-range histogram); assess with API-579 parameters until the pipe-specific database grows.
RELEVANCE: The citable source of Paris-law priors and the rainflow requirement for any pressure-cycle-driven crack-growth feature. Directly feeds crack-row growth-rate priors.
Verdict: USE (constants table + rainflow rule as growth priors) — ADAPT pipe-specific PRCI curves only when the expanded database publishes.

2. PRCI PR723-243802-R01, Anderson, "Refitting Paris Fatigue Constants for API 5L Steels and Seam Welds" (2024). https://exa.ai/library/publication/hdjrpy38jtw
Content (abstract via Exa page; full report member-walled, not verified): refit of Paris constants to PRCI IM-3-2 data for a future API RP 1176 edition; original fits contained Simpson's-paradox fallacy; adds Walker-equation fits so operators can account for high- vs low-R-ratio growth differences.
RELEVANCE: Confirms BS-7910/API-579 constants are conservative for line pipe and that R-ratio handling (Walker) is the sanctioned refinement — relevant if pressure telemetry ever yields R-ratio features.
Verdict: ADAPT (watch for RP-1176 2nd-ed constants) — REJECT current use of unpublished numbers; keep API-579 priors.

## (b) SCC colony growth + initiation (high-pH vs near-neutral, dormancy)

3. Song/Lu/Gao/Elboujdaini (SwRI/Blade/CANMET for PHMSA), "Development of a Commercial Model to Predict SCC Growth Rates in Operating Pipelines" (2011). https://rosap.ntl.bts.gov/view/dot/36473
Content (verified PDF, 93 pp): high-pH CGR from first principles (film rupture + dissolution, Faraday's law) reduced to a commercial tool; NN-pH model empirical. Constant-rate/linear-extrapolation practice is "fraught with uncertainties" — real growth is nonlinear. Appendices: Newton + least-squares inversion of growth parameters from 2, 3, N repeat-ILI depth pairs.
RELEVANCE: Mechanism-embedded alternative to linear extrapolation for SCC rows; multi-run ILI inversion math templates growth-from-repeat-crack-ILI. High-pH vs NN-pH split justifies separate growth priors per SCC subtype.
Verdict: USE (model structure + ILI-inversion appendices) — numbers need recalibration to modern EMAT data.

4. SwRI PHMSA Final Report Project 14080 (2011, companion deep report). https://primis.phmsa.dot.gov/rd/FileGet/6900/Final_Report_SwRI_Project14080_DOT_062011.pdf
Content (verified PDF): KISCC ≈ 20–21 MPa√m threshold; ILI-detectable cracks are already past it, so "when ILI tools detect a crack, the crack would be considered to be growing without dormancy." NN-pH SCC is hydrogen-assisted cracking under cyclic load — constant load causes dormancy (Chen–Sutherby restart on cycling); anodic dissolution's role unclear.
RELEVANCE: Dormancy rule for crack-row treatment — detected cracks grow (no dormancy credit); sub-detection colonies may be dormant. Pressure-cycling history, not just age, drives NN-pH growth.
Verdict: USE (KISCC/dormancy rules as modeling assumptions).

5. Yu et al., "A review of crack growth models for near-neutral pH SCC on oil and gas pipelines" (J. Infrastruct. Preserv. Resilience, 2021, cited 16). https://doi.org/10.1186/s43065-021-00042-1
Content (OpenAlex abstract verified; Springer page JS-walled, full text not verified): review of NN-pH growth-model families (hydrogen-assisted, dissolution, combined) and their field-applicability gaps.
RELEVANCE: Points to which NN-pH model family to borrow growth-rate priors from; confirms no consensus field model (supports conservative priors).
Verdict: ADAPT (model-family map) — full text not verified, do not quote numbers.

## (c) EMAT / crack-ILI sizing + growth from repeat crack ILI

6. ADV Integrity for INGAA Foundation, "Technical Guidance: Integrity Assessment for SCC Using EMAT ILI" (May 2023, 81 pp, public PDF). https://ingaa.org/wp-content/uploads/2023/11/Integrity_Assessment_for_SCC_using_EMAT_Final.pdf
Content (verified PDF): end-to-end EMAT workflow — essential variables, reporting vs detection thresholds, Likely/Possible/Unlikely classification per RP 1176, FAD sentencing, outlier management, dig iteration, reassessment from conservative CGR, API-1163 Level 1/2/3 validation (Level 2 = comparison against other ILI runs).
RELEVANCE: EMAT outlook for crack rows — reporting-vs-detection-threshold split mirrors our threshold-drift problem; likelihood tiers map to two-tier crack labels; Level-2 repeat-run comparison sanctions matched-pair growth analysis.
Verdict: USE (workflow + classification tiers as design template).

7. Palmer/Davies/Ginten/Palmer-Jones, "Detection of Crack Initiation Based on Repeat In-Line Inspection" (2016, cited 4). https://exa.ai/library/publication/tnl8q607sbs
Content (abstract verified via Exa page; full text not verified): repeat-EMAT comparison identifies newly detectable cracks (initiation) via feature matching + raw-signal comparison; raw-signal growth confirmation "still in its infancy" — unlike MFL corrosion-growth signal comparison, EMAT cannot yet confirm/discount growth run-to-run.
RELEVANCE: Direct precedent and honesty anchor: repeat-crack-ILI supports initiation detection, NOT quantitative growth — caps what our crack-row growth estimates may claim.
Verdict: USE (initiation-method + stated growth-confirmation limit).

## (d) SSWC / slanted-flaw assessment

8. TDW, "It's What You Don't See That Matters: Identifying SSWC" (Jul 2024). https://www.tdwilliamson.com/resources/papers/identifying-selective-seam-weld-corrosion-sswc
Content (verified page): SSWC attacks ERW bond line preferentially; NTSB demanded better SSWC data after 8-in gasoline-line failure near Minneapolis; detection needs MFL+SMFL bond-line-groove discrimination.
RELEVANCE: Mechanism note for seam-weld crack/corrosion rows — SSWC is a distinct slanted/bond-line morphology, not general corrosion crossing the seam.
Verdict: USE (mechanism + NTSB precedent).

9. PRCI PR350-233804-R01, Wang & Wang, "Comprehensive Review of SSWC Assessment" (Apr 2025, 35 pp). https://www.prci.org/Research/InspectionIntegrity/IIProjects/IM-3-03/253467/312802.aspx
Content (public abstract verified; full report members-only, not verified): SSWC threatens pre-1970 ERW/flash-weld pipe, caused multiple failures; current burst-pressure models evaluated against 12 SSWC failures; "reasonably accurate burst prediction remains a challenge."
RELEVANCE: Justifies conservative consequence weighting on vintage-seam rows and no burst-pressure claims from our side.
Verdict: ADAPT (failure-set benchmark design) — full text not verified.

10. TDW SSWC classifier whitepaper via World Pipelines (May 2023, 10 pp). https://www.worldpipelines.com/whitepapers/td-williamson/validating-selective-seam-weld-corrosion-classification-using-ili-technology/
Content (public summary verified; PDF registration-walled — negative, not downloaded): MDS-platform classifier (SMFL+MFL+IDOD+LFM+GEO+XYZ) validated on 700 SSWC calls / 75 runs / 8 yr, 201 digs; PHMSA requires evaluation/remediation of seam-weld corrosion within 180 days regardless of threat. Note: T20's TC-Energy pull-through found one vendor misclassifying most seam pits as SSWC.
RELEVANCE: Only public SSWC classifier validation scale; 180-day rule sets response-time context for seam-row triage.
Verdict: ADAPT (validation protocol) — vendor-authored, discount accuracy framing.

11. NDT Global × Phillips 66, "Complex cracking in LF-ERW pipelines — Phase II" (PPSA Newsletter Oct 2025). https://ppsa-online.com/newsletter/2025-10/6_From-data-to-decisions-Leveraging-destructive-testing-to-unlock-the-truth-about-complex-cracking-in-LF-ERW-pipelines-Phase-II
Content (verified full text): 1951 LF-ERW line; CW/CCW asymmetry + alternating reflections flag tilted hook cracks; destructive testing of 9 anomalies: 6 bond-line LOF, 3 surface laps, ZERO in-service growth; ILI met spec (±35 mils @80%, API-1163 validated) — apparent under-sizing was NDE error; refined rules cut 3,000 sub-threshold candidates to <20.
RELEVANCE: Slanted-flaw ground truth — tilt/skew defeats NDE sizing, destructive testing is the only sizing truth, sub-threshold triage by refined patterns is field-proven. Supports our threshold/destructive-validation stance.
Verdict: USE (pattern-refinement + NDE-distrust precedent).

12. Cosham/Macdonald/Hadley/Moore (TWI), "ECAs: Lifting the Lid of the Black Box" (OMAE2017). https://www.twi-global.com/technical-knowledge/published-papers/ecas-lifting-the-lid-of-the-black-box
Content (verified full text): API 579-1 vs BS 7910 FAD comparison for circumferential girth-weld flaws (Level 2/3A ≈ Option 1; 3B ≈ Option 2); workmanship limits (API 1104/CSA Z662/EPRG Tier 1) are NOT fitness-for-service limits (Tier 2/3); misalignment, residual stress, constraint assumptions dominate results.
RELEVANCE: ECA option/level map for crack-row consequence screening; workmanship-vs-FSS split mirrors our screening-vs-certification boundary.
Verdict: USE (FAD-level map; no ECA numbers of our own).

## (e) Probabilistic crack management (API 1176 / PRCI)

13. API RP 1176 (2nd ed. published; full text purchase-only — NOT verified) via Companion Guide (AOPL/API, 2016, public PDF) + API announcement. https://www.energyinfrastructure.org/-/media/energyinfrastructure/images/pipeline/pipeline-safety/2016-252-rp1176-companion-guide-071417.pdf ; https://www.api.org/products-and-services/standards/important-standards-announcements/api-rp-1176
Content (companion verified via PDF; standard itself via announcement only): PDCA crack-management programs; likelihood classification, response timing, reassessment intervals, program-effectiveness review. PRCI reliability-threshold / circumferential-POF / crack-response projects (NDE-4-24, NDE-4-20) are members-only — recorded, not used.
RELEVANCE: The regulatory home for our crack-row outputs: ranked likelihood + response timing + reassessment interval, never a fitness certificate. Matches T16 allowed/forbidden framing.
Verdict: USE (program structure) — REJECT any claim our model satisfies RP 1176 assessment requirements.

14. Salemi & Wang, "Fatigue life prediction of pipeline with EIFS using Bayesian inference" (JIPR, 2020, cited 14, open access). https://link.springer.com/article/10.1186/s43065-020-00005-y
Content (verified full text): hierarchical Bayes infers EIFS distribution (mean error 2%, SD 4.6% vs >90% for direct MLE) then cycles-to-failure PDF; FE + polynomial/GP SIF surrogates on 34-in, 7.1-mm pipe, 42 crack geometries; builds on Xie et al. 2018 ILI prognostics.
RELEVANCE: Probabilistic crack-life template compatible with sparse ILI snapshots — EIFS absorbs initiation uncertainty our data cannot resolve; GP-surrogate caution (overfit, no extrapolation) noted.
Verdict: ADAPT (EIFS-Bayes framing for crack-row uncertainty) — synthetic-data demo, not field-validated.

## (f) 2022–2026 crack-growth ML

15. Choi & Lee, "Probabilistic Fatigue Crack Growth Prediction for Pipelines with Initial Flaws" (Buildings, 2024). https://www.mdpi.com/2075-5309/14/6/1775 (MDPI 403-walled; abstract verified via Structurae mirror, CC-BY)
Content: particle-filter Bayes updating of Paris-law crack growth (depth + length, 1-D/2-D), 90% CI remaining life, Paris-parameter negative correlation across diameters/aspect ratios/materials.
RELEVANCE: Closest recent analogue of honest probabilistic crack forecasting — particle filtering handles sequential ILI updates the way our repeat-survey pairs arrive.
Verdict: ADAPT (particle-filter update scheme) — full text not verified.

16. Sherbakov et al., "ML-based approach for predicting fatigue crack growth in steel pipe under pure bending" (Eng. Res. Express, 2025, open access). https://doi.org/10.1088/2631-8695/adc541
Content (verified full text): TP316L pipe, 4-point bending; RF best for da/dN with ΔK/a/N inputs (R² best with crack length a as input); ridge regression fails on da/dN; polynomial conservative; leak-before-break radial model, constant amplitude, lab air — no corrosion, no variable amplitude.
RELEVANCE: ML-on-Paris-variables benchmark with a useful negative: linear models cannot learn da/dN; crack size dominates ΔK as a predictor. Lab-only — no transfer to field SCC rows.
Verdict: ADAPT (RF-over-linear + a-dominance lesson) — REJECT any field-growth transfer.

17. Yu et al., "ConvLSTM-based prediction of fatigue crack propagation path of surface cracks in pipelines" (Int. J. Pressure Vessels Piping, 2024, cited 4). https://doi.org/10.1016/j.ijpvp.2024.105420
Content (meta verified via Exa/OpenAlex; paywalled, full text not verified): ConvLSTM predicts spatial propagation path of surface cracks.
RELEVANCE: Only spatiotemporal path-prediction entry — path, not rate; confirms no 2022–26 paper forecasts growth from ID-less tables (extends T1/T18 negatives into crack ML).
Verdict: REJECT as forecaster (needs tracked geometry we lack) — keep as negative-result marker.

18. Feng et al., "Development of a NN-pH SCC Growth Model Using ML" (IPC2022-87207, CanmetMATERIALS). https://doi.org/10.1115/ipc2022-87207
Content (OpenAlex abstract verified; proceedings paywalled, not verified): RF/Extra-Trees/GB/XGBoost estimate da/dN from geometry + pressure + environment on full-scale cyclic-pressure pipe tests; k-fold-tuned, independent test set.
RELEVANCE: Only ML SCC-growth model trained on full-scale pipe tests with pressure/environment covariates — feature-set blueprint (geometry × pressure × environment) for any future crack-growth head.
Verdict: ADAPT (feature blueprint + tree-ensemble choice) — full text not verified, no metric transfer.

19. "Review of Prediction of SCC in Gas Pipelines Using ML" (Machines, 2024, cited 60). https://doi.org/10.3390/machines12010042 + "DL-enabled FEA for SCC prediction" review (2024, cited 30). https://doi.org/10.1080/19942060.2024.2302906
Content (OpenAlex abstracts verified; full texts not verified): Machines review finds NO published work demonstrating real field SCC detection/prediction ability — lab-only models don't transfer; DL+FEA review finds DL strong on accuracy/cost but literature "scarce," no comprehensive field validation.
RELEVANCE: Two high-citation reviews jointly certify the no-field-ML-SCC-growth position — our honesty-first stance is the literature consensus, not a deficit.
Verdict: USE as consensus evidence (both) — no method transfer.

## Crack-row treatment (provisional, reviewer-gated, December-safe)

Growth priors: Paris/API-579 constants (a) for fatigue-driven rows; Song high-pH / empirical NN-pH (b) for SCC rows, with KISCC/dormancy rule (detected = growing). EMAT outlook (c): likelihood tiers + repeat-run initiation detection only — no run-to-run growth claims. Slanted/seam flaws (d): vintage-seam rows get conservative consequence weight; sizing truth = destructive only. Management (e): RP-1176 PDCA framing, EIFS-Bayes uncertainty. ML (f): tree ensembles + particle filtering as future heads; no field transfer today. Negative results kept: no ID-less crack-growth forecaster exists; RP-1176/PRCI full texts purchase/member-walled; TDW SSWC whitepaper registration-walled.
