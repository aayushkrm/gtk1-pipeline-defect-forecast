# Track 17 — primary-source deep extraction (API 1163 / PRCI / POF / NACE SP0102)

Tooling disclosure: websearch HTTP-400 on every query (all phrasings); MDPI + IOP + Techstreet bot-walled (403/Access Denied); PRCI report pages login-walled; Current Science PDF truncated after ladder. Worked: webfetch on HTML pages, OpenAlex API, direct PDF/DOCX download via curl + local pypdf/python-docx extraction. Paywalled full texts (API 1163 3rd ed., PRCI reports) cited via secondary + marked "full text not verified" per PROTOCOL hard boundaries. No commits.

## P1. POF 100 (Nov 2021, 62 pp, primary PDF — read in full)
- Link: https://pipelineoperators.org/media/2225 (mirror used: pipescanintegrity.com PDF)
- Content (actionable): §4 — POD(a) with **a90/50 vs a90/95 distinguished; specify POD90/95 recommended**. Typical high-res MFL floors @POD90: **general corrosion 10%t, pitting 15%t; UT 1–1.5 mm**. Sizing: **depth 10–15%t, length/width 10–20 mm, typical certainty 90%**. Location: **±0.25% of distance to marker, ±0.15 m to weld**. Geometry: dents depth ±1% ID, L ±10–20 mm, W ±20–30 mm, ovality ±1% ID (all @90%). POI rule (Table A4-1): **"Yes" = POI>90%, "No" = POI<50%**. App.4 vendor tables A4-2…A4-9 per anomaly class; A4-4 per-wall-thickness alternative; bend-radius tables.
- Relevance: normative taxonomy + threshold floors for our per-survey POD model; A4-4 justifies per-thickness (not fixed-%t) floors.
- Verdict: USE as spec-number source.

## P2. Filled vendor POF Table A4-2 via NTSB docket (primary example values)
- Link: https://data.ntsb.gov/Docket/Document/docBLOB?FileExtension=.PDF&FileName=IMP%20-%20PII%20POD-POI%20ILI%20tools%20capabilities%2004-13-2012-Master.PDF&ID=40367766
- Content: min depth @90% POD — body **8/10/10/8%t** (general/pitting/axial-groove/circ-groove), weld-HAZ **12/14/14/12%t**. Depth sizing body **±10%t@80% / ±15%@90%** (grooving asymmetric, e.g. −15/+10); HAZ ±15/±20. Width **±20/±25 mm** (HAZ ±25/±30). Length: pitting ±10/±15, general ±15/±20, grooving ±20/±25 (HAZ +5 mm each). Reference diameters **4t general / 2t pitting**. MFL depth rule-of-thumb **±10%t @ 80%**.
- Relevance: exact numbers behind track5's summary; 10–15%t sits in the POD ramp — quantifies drift mechanism.
- Verdict: USE as threshold table.

## P3. POF 330 tool testing (Jan 2026, 14 pp, primary)
- Link: https://pipelineoperators.org/media/2941
- Content: qualification routes per API 1163 = **(a) verified historical data, (b) full-scale real/artificial-anomaly tests, (c) small-scale/modeling**. Tests may be **blind / open / partially blind** (truth-sample sharing improves performance). MFL pull-test velocities **0.5, 1.5, 2.5, 3.5, 5 m/s + one above max spec**. §8: **POD/POI per API 1163 from truth data; unity plots per anomaly class** for sizing assessment.
- Relevance: justifies our matched-pair + unity-plot validation design; velocity ladder = run-quality covariate.
- Verdict: USE.

## P4. POF 310 field verification (Dec 2023, 34 pp, primary) + POF 311 form (Dec 2023 DOCX, primary, parsed locally)
- Links: https://pipelineoperators.org/media/2613 ; https://pipelineoperators.org/media/2612
- Content: Table 1 method-per-type (ext. corrosion: **depth micrometer + laser scan**; cracks: PAUT/ToFD/shear-wave; dents: laser + micrometer). Table 2 NDE tolerances ±mm: **tape 1–2; depth micrometer 0.05–0.15; laser 0.1; UT-0° 0.1–0.25; manual angle-beam 0.5–3; PAUT 0.5–1.5; FMC/ToFD 0.3–1; ACFM +5/−1; tangential ECA 0.3–0.5**. Rules: **window ≥0.3 m beyond anomaly; NDE personnel Level 2**; field tolerance must be small vs ILI error or Level 2/3 verdicts are meaningless (combined-tolerance inflates false passes). POF 311 schema (paired columns ×3 anomalies): header (pipe/odometer/GPS/markers/tech qualifications) + per-anomaly **type, dist-to-up/downstream girth weld, local WT, depth, remaining WT, length, width, o'clock, int/ext, seam orientation, joint length — each ILI-reported AND field-measured**.
- Relevance: 311 = ready schema for any future dig records; Table 2 = metrology error budget.
- Verdict: USE (schema + tolerances); ADAPT 0.3 m window to archive matching.

## P5. DigIt/CGRealBias unity-plot statistics, Harper et al., JSM 2020 (11 pp, primary)
- Link: https://ww2.amstat.org/meetings/proceedings/2020/data/assets/pdf/1505317.pdf
- Content: per-POF-class unity plots; **paired difference t AND paired ratio t (H0: μ_ratio=1), both 95% two-sided; ratio preferred** (scales with depth), positive-only adjustments for conservatism. API 1163 (2013) sizing test = **Agresti–Coull one-sided upper interval p̂_upper vs stated certainty**; binary test discards information. Demo: **all 3 tool datasets (MFL V1/V2, UT V1) FAILED as-stated spec (±10%WT @ 80%)**; MFL Vendor 2 needed ratio adjustment.
- Relevance: statistical recipe for calibration layer (ratio-bias per class; binomial as compliance check only); expect vendor specs to fail as-run.
- Verdict: USE.

## P6. API 1163 3rd-ed workflow (secondary: Irth/OneBridge 2024 + 2025 change-notes; full text not verified)
- Links: https://irthsolutions.com/blog/validating-ili-performance-with-api-1163-and-prci-research-in-cim-0 ; https://irthsolutions.com/blog/api-1163-3rd-edition-whats-changed
- Content: **Level 1** = accept vendor spec, low-risk / <6 points / extensive experience, no digs (3 options incl. **ILI-to-ILI with p̂=X/n**, combined tolerance = weaker). **Level 2** = two-sided binomial CI vs digs, **4 outcomes (Fig. 8b)**. **Level 3** = as-run bias + tolerance from digs. PRCI spreadsheet minima: **6 pts (L2) / 10 pts (L3)**. New in 3rd ed: **200+ "shall"s; verification (run went to plan, §7.6/7.7 DQA + CEPA 10-pt check) split from validation; §8.2 + Annex C rework; API 1176/1183 hooks**. Field stat: **only 1 of 21 vendors meets ±10% @ 80%**. E2 scope (API public PDF): 79 pp, Apr 2013; E3 + 2nd ed incorporated by reference in **49 CFR 192.493 / 195.591**. Purchase (not bought): API store/Techstreet — user's decision.
- Relevance: adopts Level definitions; our archive supports Level-1-Option-2 (ILI-to-ILI) now, L2/L3 only with digs.
- Verdict: USE (workflow); REJECT any pooled-vendor reading.

## P7. PRCI IM-1-06 Performance Validation Guidelines (report PR-719-223803-R01, Mar/May 2023; full text not verified — login-walled)
- Link: https://www.prci.org/Research/InspectionIntegrity/IIProjects/IM-1-06/236614/260565.aspx (page confirms title, id 260565, "not published" for guests). Addendum: PR719-243812-Z01 crack/dent, doi:10.55274/r0000021 (closed).
- Content (via P6 + §refs): §3.3 depth uncertainty dominates burst pressure; §4.2 field error must be small vs ILI error; §4.3.2 mitigated-significant-anomaly Level-1 rule; §4.3.3 similar-pipeline criteria; §4.7 prior-data use; **Data tab (per-pair ILI vs field) → Calculations tab (CIs, unity plots)**. Exact Data-tab column list NOT recoverable verbatim (screenshot image-only) — partial negative, do not quote.
- Relevance: how-to manual behind P6; POF 311 fields cover the functional column set.
- Verdict: ADAPT (reconstruct sheet from POF 311 + DigIt); flag purchase to user.

## P8. ILI error distributions, Verdín & Liu 2023 (bronze OA, IMP)
- Link: https://doi.org/10.22533/at.ed.3173202307065 (PDF via cdn.atenaeditora.com.br)
- Content: reporting precision **±0.3–0.6 mm UT @95% vs 80% MFL**; K-S over Normal/Lognormal/Gamma/Exponential on 6 datasets: **ILI measurement error ≈ Normal; field pit depth-rate ≈ Lognormal**. Frames validation as NACE **SP0102-2017** regulatory step + API 1163 check.
- Relevance: Normal-error prior for depth calibration; Lognormal prior for pit growth-rate head.
- Verdict: USE.

## P9. UWO thesis — ILI length-error taxonomy (green OA, 139 pp)
- Link: https://uwo.scholaris.ca/bitstreams/acddf8c9-c148-426e-a297-6d8676551e46/download (cites NACE SP0102-2010 §"In-line inspection of pipelines", Item 21094)
- Content: **Type I (no clustering error) vs Type II (with)** defects; ILI-vs-field length correlation poor (Ellinger & Moreno 2016) due to clustering error; burst capacity depends on **depth + length, negligibly width** (Kiefner–Vieth 1989).
- Relevance: length noise >> depth noise — depth-first validation (matches PRCI §3.3); cluster flag as length covariate.
- Verdict: USE.

## P10. Binomial evidence scale (computed, Clopper–Pearson exact)
- 29/29 → lower95 = 0.9019 (the 90/95 POD-demo bar); 28/29 → 0.8466 (one miss fails); 45/46 → 0.9010; 6/6 → 0.607, 10/10 → 0.741 (why L2/L3 minima alone prove little without the interval test). Arithmetic, no citation needed.
- Relevance: gate rule — never pool vendors/surveys for POD claims (track4 compatible).
- Verdict: USE as decision thresholds.

## Negatives + hard-boundary flags
NACE SP0102-2010 full text (AMPP Item, ~$400-class) and API 1163 3rd ed. not purchased — flag both price pages to user. POF 311 parsed fully (above); POF 320 (11 pp, compliance meetings/tables/facility-visit process) and catalog (100/110-UPT/300–303/310/311/320–322/330/510/520, all public at pipelineoperators.org/documents) skimmed only. No RU sources (brief sets none). Word count ~1,450.
