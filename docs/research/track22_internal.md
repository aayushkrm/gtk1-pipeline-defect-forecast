# Track 22 — internal corrosion + flow modeling (gas pipelines)

Tooling disclosure: Exa neural search (all queries) + Exa contents extraction worked; routed webfetch worked for HTML (GATE, DergiPark) but 403 on MDPI and no-PDF support (NDT, PPSA) — covered via Exa contents instead; OpenAlex API worked for citation counts/model lineage. No Firecrawl/TinyFish needed. Does NOT duplicate tracks 1–20 (track 11 = external corrosion/CP/coatings; this file = INTERNAL mechanisms only).

Scope note: our INT rows are 3–7% of anomalies, but partner scope may include internal corrosion — this file pre-positions flow-proxy features and partner-request wording.

## (a) Water holdup / critical velocity

**S1. Ma et al. 2022, critical liquid-carrying gas velocity model (high gas-to-liquid gathering lines).** https://doi.org/10.1016/j.jpse.2022.100093 (OpenAlex W4308788874, 6 cites). Updates Turner-type droplet-reversal criterion for high-GLR lines. Content: new correlation for minimum gas velocity that keeps liquids entrained; below it water drops out → BOLC sites.
RELEVANCE: the physical basis for a "flow-proxy" feature (velocity/deficit vs critical) if flow data ever arrives; explains why low spots/low-flow segments concentrate INT rows.
USE (as design reference for flow-proxy features, gated on flow data arrival). No INT forecast from it alone — REJECT as standalone predictor.

**S2. CAPP BMP 431990 (Aug 2025), Mitigation of Internal Corrosion in Carbon Steel Gas Pipeline Systems.** https://www.capp.ca/wp-content/uploads/2025/09/CAPP_EDMS-431990-v3-Draft_CAPP_Mitigation_of_Internal_Corrosion_in_Carbon_Steel_Gas_Pipeline_Systems-August-2025.pdf (full text verified via Exa extraction: pitting mechanisms, mitigation practice). Content: industry BMP covering corrosion forms, monitoring, mitigation in gas systems.
RELEVANCE: citable operator-consensus wording for partner requests (pigging, dehydration, monitoring); frames INT rows as flow-regime-driven, not random.
USE as partner-request/mitigation wording reference.

## (b) CO2/H2S rate models

**S3. GATE Energy TOLC Part 1 (2018, practitioner summary of IFE / NORSOK / de Waard practice).** https://www.gate.energy/viking/insights/gat2004-gkp-2018-05/top-of-line-corrosion-part-1 (full text verified). Content: IFE TOLC model (rate limited by condensation rate × Fe solubility); modified NORSOK M506 for BOLC (pH via ScaleChem, inputs pCO2/T/shear); de Waard 0.1 BOLC→TOLC factor above critical condensation 0.25 ml/m²s; TOLC models invalid with H2S (FeS vs FeCO3 films).
RELEVANCE: gives exact mechanistic features (condensation rate, pCO2, shear, H2S flag) and the 0.1×/0.25-rate heuristics; H2S caveat directly bounds any INT model.
ADAPT the feature list + heuristics as priors; REJECT direct rate transfer (needs flow/chemistry inputs we lack).

**S4. Doğan & Altınten 2023, NORSOK M-506 vs Nešić experiments.** https://doi.org/10.17798/bitlisfen.1191507 (full text verified). Content: NORSOK M-506 predicted ~6× higher than Nešić/Solvi/Enerhaug 1995 loop data.
RELEVANCE: cautions against quoting NORSOK as calibrated truth — conservative by design; supports our no-absolute-rate-claim stance for INT rows.
USE as conservatism evidence.

**S5. de Waard–Milliams lineage (original 1991; improvements paper 2002, 129 cites).** https://doi.org/10.5006/c2002-02235 (OpenAlex W1488800721; full text NOT verified — NACE paywall, cited via secondary/GATE summary). Content: seminal CO2 nomogram/correl; 2002 update adds glycol, pH stabilization, shear effects.
RELEVANCE: the most-cited INT-rate ancestor; documents which corrections (glycol, pH) any flow-proxy model must include.
ADAPT as lineage citation only.

**S6. Zheng/Sonke/Bos 2021, new TOLC model for sweet wet gas (Shell/GATE).** https://doi.org/10.5006/c2021-16812 (OpenAlex W3179286753, 6 cites; full text NOT verified — conference paper). Content: updated sweet-system TOLC model building on IFE/Singer-Nesić experimental base.
RELEVANCE: shows TOLC modeling is still active/sweet-only; sour gap (S3) remains open — justifies flagging H2S segments as out-of-model.
USE as state-of-art pointer.

## (c) Bacteria / sour-service SCC

**S7. Kannan et al. 2018, MIC characterization review (Texas A&M).** https://doi.org/10.1021/acs.iecr.8b02211 (abstract + TOC verified; full text NOT verified — ACS paywall). Content: surveys MIC detection/quantification tools (coupons, probes, molecular, electrochemical) and their limits.
RELEVANCE: MIC explains clustered INT pits in stagnant/low-flow zones; tool limits justify requesting monitoring data rather than inferring MIC from ILI alone.
USE for monitoring-request wording; REJECT MIC-from-ILI-shape inference.

**S8. Sour service: NACE MR0175/ISO 15156 + Nippon Steel sour-resistant line pipe report.** https://files.engineering.com/files/f2ab27f0-ab58-4288-a5fa-97cc4db8a4e3/NACE%5FMR0175%5FISO%5F15156%5F2%5F2020.pdf and https://www.nipponsteel.com/common/secure/en/tech/report/pdf/132-06.pdf (standard full text NOT verified — purchase/login-walled; vendor report via Exa). Content: H2S cracking regimes (SSC/HIC/SOHIC), hardness/microstructure controls, hard-zone prevention in line pipe.
RELEVANCE: internal SCC in sour segments is a material/environment interaction, not a growth-rate problem — our row-count forecaster must exclude sour-cracking claims; partner wording should request H2S service designation.
USE as scope-exclusion + request-list support.

## (d) Inhibitors + monitoring

**S9. Gharbi et al. 2021, inhibitor field test, Algerian gas field (open access).** https://doi.org/10.1007/s13202-021-01287-y (full text verified via Exa). Content: film-forming inhibitor CK981DZ >99% efficiency at low rate (pH + Fe-content evidence); film-forming/neutralizing type raised pH but less effective.
RELEVANCE: field evidence that inhibition changes INT rates by regime — any INT model needs an inhibitor-status covariate; partner-request item.
USE as inhibitor-covariate justification.

**S10. Cortec NACE 2013-2509, volatile inhibitors for TLC.** https://www.cortecvci.com/Publications/Papers/2013-NACE-2509.pdf (verified via Exa). Content: azoles/acetylene alcohols/volatile aldehyde screened at 70 °C pH-4 condensate; TOLC inhibitor effectiveness depends on volatility.
RELEVANCE: TOL segments are inhibitor-starved by physics (S3) — explains persistent TOL INT rows despite BOL inhibition; supports stratified-flow/condensation features.
ADAPT as TOL-persistence mechanism note.

**S11. Powell 2015, coupons + ER probes chapter (5 cites).** https://www.researchgate.net/publication/393076174_Internal_Corrosion_Monitoring_Using_Coupons_and_ER_Probes_A_Practical_Focus_on_the_Most_Commonly_Used_Cost-Effective_Monitoring_Techniques (abstract verified; full text NOT verified). Content: placement (axial + azimuth), coupon/ER vs ILI/radiography sensitivity comparison, fluid-sample cross-check, inhibitor-dosing strategy.
RELEVANCE: monitoring data (coupons/ER) is the ground truth that would calibrate any INT forecaster — top partner-request item; azimuth guidance maps to clock-position features.
USE as monitoring-request authority.

## (e) ILI for internal corrosion

**S12. NDT Global white paper (Munsel/Meinzer): complex internal pitting in 6″ line, UT analysis.** https://assets.ctfassets.net/.../CIM-117_Rev_1.0_White_Paper_Complex_internal_metal_loss_pitting_corrosion__1_.pdf (verified via Exa). Content: detailed UT re-analysis of sub-spec complex internal pitting validated by field digs; shows UT resolves pit morphology where standard evaluation fails.
RELEVANCE: UT is the reference for internal pits; our INT rows likely MFL-derived → sizing bias vs UT; any INT growth claim needs tool-identity/POD gating (links to track 5/17 per-survey POD rule).
USE as UT-as-reference + re-analysis precedent.

**S13. Al Saif/Tehsin (Saudi Aramco), PTC 2025: MFL vs UTML operator comparison.** https://pipeline-conference.com/abstracts/comparative-evaluation-mfl-and-utml-ili-technologies-operators-perspective (abstract verified via Exa). Content: operator-side head-to-head of MFL vs UT metal-loss sizing across damage mechanisms.
RELEVANCE: operator precedent for tool-specific INT performance — reinforces never-pool-vendors (track 4) for INT rows.
USE as operator-precedent citation.

## (f) Internal-corrosion ML predictors

**S14. Liu/Cai/Meng 2025, hybrid ML corrosion-rate predictor (Appl. Sci., open access).** https://doi.org/10.3390/app15042023 (abstract + method verified via Exa). Content: decomposition + PCA + stratified sampling + PSO-BP network beats 8 baselines on western-China gas-line data (R²/MAPE/RMSE panel + PDP/ICE interpretability).
RELEVANCE: closest published analogue of an INT-rate ML forecaster; pipeline (stratified sampling, noise handling, interpretability) is adaptable IF chemistry/flow inputs existed — they don't in our tables.
ADAPT pipeline pattern only; REJECT direct comparison (different inputs).

**S15. Waziri et al. 2025, CFD-informed ML (XGBoost R² 0.95, AKK pipeline).** https://journals.unizik.edu.ng/ujeas/article/view/7322 (abstract verified). Content: ANSYS Fluent features (velocity, pressure, wall shear, turbulence intensity) → XGBoost best; turbulence intensity + velocity dominate; authors flag simulated-data + no-chemistry limits.
RELEVANCE: validates flow-proxy feature ranking (shear/velocity/turbulence) for future use; honesty about simulated-data limits mirrors our no-overclaim rule.
ADAPT feature ranking; REJECT R² as benchmark (simulated data).

## Decisions

1. INT forecaster stays out of December scope: no flow/chemistry/inhibitor inputs → no calibrated INT rate possible; INT rows keep descriptive treatment only.
2. Flow-proxy feature spec (gated): segment velocity vs critical (S1), condensation-rate proxy, pCO2/H2S flags, inhibitor status (S9), clock position (S11) — activate only on data arrival.
3. Partner-request wording: H2S/sour designation (S8), inhibitor program + monitoring exports (S9/S11), ILI tool identity for INT rows (S12/S13).
4. Negative result: no paper forecasts INT rows from ID-less threshold tables (consistent with track 4/18 negatives); TOLC-with-H2S models remain a gap (S3/S6).

Per-file footer: Exa search+contents served S2,S9–S12,S14–S15; webfetch served S3,S4; OpenAlex served S1(deep),S5,S6 lineage/cites; paywalled full texts NOT verified (S5,S6,S7,S8-standard,S11-partial) — cited via abstract/secondary. No commits.
