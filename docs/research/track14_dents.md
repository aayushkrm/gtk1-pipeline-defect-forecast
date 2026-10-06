# Track 14 — dent and geometric-anomaly assessment

Tooling: websearch worked intermittently (HTTP-400 on ~half the queries); gaps filled via OpenAlex API + webfetch (noted per item). PDFs (PDAM, PHMSA reports, NDT.net, PRCI) are not fetchable with this tool catalog — content taken from websearch snippets and full-text secondary summaries (flagged where primary was unread).
GTK1 context: ON 2025 anomaly table carries 321 DENT rows; Depth is N/A for dents (no %OD recorded) and Location is N/A, so depth-based rules cannot be applied directly and strain must be proxied. DENT/WRIN/OVAL rows are currently EXCLUDED from the corrosion target — this track decides what to do with them instead. Non-duplication: Zhao 2022 dent-standards review lives in track12 §S12 (referenced, not repeated); caliper/MFL tool physics lives in track5 (referenced, not repeated).

## (a) Dent characterization in ILI

### S1 — Haley & Spring 2024, E2G "Are dents really a problem?" (practitioner review, full text fetched)
https://e2g.com/industry-insights-ar/are-dents-really-a-problem/
- Content: Plain smooth single-peak dents characterized by depth + curvature radii in both principal directions; caliper-pig profiles must be filtered/smoothed to get usable base-of-dent radii (API RP 1183 Fig. 4 example). Kinked/constrained (rock) dents, multi-peak dents, and dents at discontinuities need Level-3 FEA or repair — closed-form methods do not apply.
- RELEVANCE: Gives the exact taxonomy to code DENT rows into (plain vs kinked vs constrained vs multi-peak from comments/shape fields). Depth-N/A means our tables cannot even enter the Level-1 procedures — curvature proxy or count-only treatment is forced.
- Verdict: USE (dent triage taxonomy + smoothing caveat for limitations §).

### S2 — NDT.net paper, pipeline dent strain assessment using ASME B31.8 (abstract via websearch; PDF unfetchable)
https://www.ndt.net/article/ndtnet/papers/Pipeline_Dent_Strain_Assessment_Using_ASME_B31.8.pdf
- Content: B31.8-2018 Appendix R assesses dent strain from measured surface curvature, not depth; method hinges on accurate circumferential + longitudinal profiles. Strain, not %OD, is the acceptance variable once profiles exist.
- RELEVANCE: Formal backing for a strain-proxy feature (length/width/aspect + clock position) computed from the geometry columns we DO have, instead of the depth column we lack. Also bounds claims: no profiles → no strain number.
- Verdict: ADAPT (curvature-from-L/W proxy idea; no direct strain computation without profiles).

### S3 — Torres / Fowler / Stenerson 2016, Enbridge complex-dent ILI vs field (IPC2016-64136)
https://doi.org/10.1115/ipc2016-64136
- Content: Operator study on ILI performance and field-measurement interpretation for complex (multi-peak/interacting) dents — caliper sizing degrades exactly where assessment matters most. Field verification remains the arbiter for non-plain dents.
- RELEVANCE: Precedent for treating plain vs complex dents as different data-quality regimes in features: plain-dent proxies are model-usable, complex-dent rows should carry an uncertainty flag (mirrors our match-uncertainty flag convention).
- Verdict: USE (complex-dent uncertainty-flag precedent).

## (b) Strain-based assessment (B31.8 / EPRG)

### S4 — Noronha et al. 2010, procedures for strain-based assessment of pipeline dents (Petrobras)
https://doi.org/10.1016/j.ijpvp.2010.02.004 (abstract + snippet; publisher page bot-walled)
- Content: Industry codes call plain dents injurious past 6% OD, but the strain route (B31.8 App. R lineage: Fowler/Chubb curvature equations) accepts any-depth dents under 6% strain (4% at welds). Depth is a screen; strain is the test.
- RELEVANCE: Justifies keeping depth-N/A dents in a mechanical-proxy feature rather than dropping the rows: depth alone was never the acceptance variable. The 6%/4% pair maps onto our weld-proximity flag (dents at girth/spiral welds = stricter class).
- Verdict: USE (depth-screen vs strain-test distinction for label-design rationale).

### S5 — API RP 1183 (2020 + 2021 errata + 2024 addendum) + PDAM Ed. 2.1 (2024), via S1 full-text summary (primaries paywalled/unfetchable)
Refs: API RP 1183; PDAM Ed. 2.1 Penspen Aug 2024; API 579-1 Part 12; ASME B31.8-2022 App. R
- Content: Closed-form strain from base-of-dent radii vs limits: 40% of MTR elongation / 50% of specified minimum elongation / 6% default / 4% at welds; Level-1 needs R/t > 5 at dent base. PDAM 2.1 cut the dent-at-weld depth limit 4%→2% OD on new rupture tests — API 579 Part 12 (4%) is now non-conservative vs PDAM.
- RELEVANCE: Two actionable items: (i) dent-at-weld rows (esp. PK1 spiral seam, PK2 ERW-era seam) inherit the strictest prior — candidate blocklist for corrosion-label leakage review; (ii) PDAM-vs-579 version drift is a cautionary tale for pinning any threshold to a dated vendor table.
- Verdict: USE (weld-interaction strictness + version-drift caution).

### S6 — Suvarnalatha et al. 2024, EPRG vs fracture-mechanics on third-party damage (Penspen, IPC2024-133950)
https://doi.org/10.1115/ipc2024-133950
- Content: Compares the semi-empirical EPRG/British-Gas dent-gouge fracture model (burst pressure from dent depth + gouge length/depth + toughness) against modern fracture-mechanics routes; pipe toughness dominates consequences. Confirms EPRG model still the industry workhorse for combined dent-gouge.
- RELEVANCE: No gouge dimensions exist in our tables, so the EPRG model itself is not computable — but its input list (dent depth + co-located metal loss + toughness) defines exactly which co-location feature to build: dent↔metal-loss proximity join within the ±2 m match window.
- Verdict: ADAPT (EPRG input list → dent–metal-loss co-location feature spec).

## (c) Dent + corrosion/gouge/SCC interaction — when a dent becomes a dig

### S7 — 49 CFR 192.933, response rules (primary source, eCFR fetched 2026-10-06)
https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-D/part-192/subpart-O/section-192.933
- Content: Immediate repair: top-2/3 dent WITH metal loss/cracking/stress riser (unless §192.712(c) strain analysis clears it); 1-year: smooth top-2/3 dent >6% OD, any dent >2% OD affecting girth/seam-weld curvature, bottom-1/3 dent with metal loss/cracking. Bottom-1/3 plain dents >6% OD with cleared strain = monitor. Clock position + interaction, not depth alone, set the clock.
- RELEVANCE: Direct template for a rule-based dent flag from our columns: clock (upper-2/3 vs lower-1/3 — we HAVE orientation) × weld-proximity × co-located ≥10% metal loss. Depth-N/A rows default to the interaction/weld branches, which need no depth. 192.933 contains NO ovality criterion (negative result, verified in full text).
- Verdict: USE (clock×weld×colocation flag logic for dent-feature design).

### S8 — He & Zhou 2021, fatigue reliability of dented pipelines (cited 28×)
https://doi.org/10.1016/j.jpse.2021.08.004
- Content: Probabilistic fatigue-life framework for dented pipes under cyclic pressure; dent severity + pressure spectrum drive failure probability, with reliability-index outputs suitable for dig scheduling. Gas lines see fewer cycles than liquids, but compressors-station-adjacent segments still accumulate them.
- RELEVANCE: Supports a segment-level dent-count × pressure-cycling exposure prior (proximity to compressor stations/pump points as request-list item) rather than any per-dent life claim. Also reinforces: dents are a fatigue threat, not a corrosion-growth threat — keep them out of the corrosion target.
- Verdict: ADAPT (dent-count × cycling-exposure prior; no per-dent prediction).

### S9 — PHMSA TTO dent study final report 2004 (snippet via websearch; PDF unfetchable)
https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/technical-resources/pipeline/gas-transmission-integrity-management/65291/tto10dentstudyfinalreportnov2004.pdf
- Content: Codifies the pre-192.933 consensus adopted into regulation: plain dents injurious past 6% OD (any depth OK if strain <6%); dents at girth/seam welds injurious past 2% OD (strain <4% exception). Comparative 192-vs-195 table included.
- RELEVANCE: Historical anchor showing the 6%/2% + strain-exception structure predates and survives into current regulation — our flag logic inherits a 20-year-stable threshold family, not a vendor whim. Same depth-N/A caveat as S7 applies.
- Verdict: USE (threshold-family stability argument, cited once).

## (d) Wrinkles / wrinklebends and ovality

### S10 — Holliday et al. 2018, strain- and stress-based assessment of wrinkles reported by ILI (ROSEN, IPC2018-78488)
https://doi.org/10.1115/ipc2018-78488
- Content: Wrinkles (field-bend/settlement buckles) reported by geometry ILI need combined strain + stress assessment distinct from dent rules; wrinkle apex cracking under cyclic load is the governing threat, evaluated by FEA-backed screening, not depth limits.
- RELEVANCE: WRIN rows must not be scored by any dent-depth logic — separate rare-class flag with its own (monitor-only) handling. Any wrinklebend near a weld or with co-located loss inherits the S7 interaction escalation.
- Verdict: USE (wrinkles ≠ dents separation rule).

### S11 — Bakhtyar 2014, low-cycle-fatigue tool for wrinkled pipelines (thesis) + Papadaki et al. 2018, buckling of pressurized spiral-welded pipe (cited 19×)
https://doi.org/10.1016/j.ijpvp.2018.07.006 (Papadaki; thesis record via OpenAlex)
- Content: Wrinkled-pipe life is governed by low-cycle fatigue at the wrinkle ridge; spiral-weld pipe (our PK1/PK2 construction) shows distinct buckling/bending capacity vs straight-seam pipe. Construction type conditions geometric-threat severity.
- RELEVANCE: Justifies a pipe-type × geometry-threat interaction feature (spiral-weld sections + WRIN/OVAL counts carry higher prior). Also relevant to PK1 spiral-seam dent-at-weld strictness in S5.
- Verdict: ADAPT (construction-conditioned geometric prior; note spiral-weld relevance to PK1/PK2).

### S12 — Ovality: negative result (verified against S7 full text + B31.8S scope)
- Content: No in-service ovality repair threshold exists in 192.933 (full-text check — dents only); ovality limits live in construction codes (pipe-mill/field-bend tolerances), not in integrity-response regulation. Geometry-ILI ovality is therefore a construction/condition record, not a dig trigger.
- RELEVANCE: OVAL rows → segment-level ovality-rate covariate only; never a label, never a dig proxy. One-line justification, no further literature needed.
- Verdict: USE (as documented negative result bounding OVAL handling).

## (e) Operator dent-management programs

### S13 — API RP 1183 dent-assessment-and-management framework (via S1; E2G confirms May-2024 addendum current)
Ref: API RP 1183 Nov 2020 + Jan 2021 errata + May 2024 addendum (summarized in S1)
- Content: Operator program = caliper/geometry ILI → dent ranking (depth × strain × interaction × weld × pressure history) → Level-1/2/3 assessment ladder → dig-or-monitor disposition with re-inspection intervals; Level-1/2 fatigue screening needs ≥1 yr of location-specific pressure data. Cyclic-service (liquids) dents get fatigue ranking; gas lines mostly screen out at 150-cycle API 579 Part-14 gate.
- RELEVANCE: Our gas-transmission setting means most dents land in monitor/rank bins — consistent with excluding them from the corrosion target while retaining dent-count as a third-party-activity proxy. The ≥1-yr pressure-history requirement goes on the partner-data request list (we have no pressure data).
- Verdict: USE (program structure → our monitor-mostly posture + pressure-data request).

## (f) 2022–2026 work: high-resolution geometry + ML strain

### S14 — Xu et al. 2024, DNV 3D profile-matching for dent FEA (IPC2024-133117)
https://doi.org/10.1115/ipc2024-133117
- Content: Automated matching of high-resolution 3D dent profiles to FEA assessment models — removes manual profile-picking bottleneck in Level-3 dent analysis. Direction: dense geometry + automated strain, not better depth cutoffs.
- RELEVANCE: Confirms the industry trajectory (profiles→strain automation) that our depth-N/A tables cannot join — strengthens the case for count/proximity features now + a profile-data request for future campaigns. No method to borrow without 3D data.
- Verdict: ADAPT (request-list justification: ask vendors for raw geometry profiles, not just anomaly tables).

### S15 — Liu et al. 2022, ILI bending-strain feature ID via optimized deep-belief network (Energies, cited 10×)
https://doi.org/10.3390/en15041586
- Content: ML (optimized DBN) classifies bending-strain features from ILI signals on an operating gas network (PipeChina coauthor) — demonstrates learned models extracting strain-relevant features from inspection signals where closed-form curvature fails.
- RELEVANCE: Only ML-on-ILI-geometry precedent close to our strain-proxy idea — but it trains on raw ILI signals, which we do not have. Cite as feasibility direction, explicitly out of December scope.
- Verdict: ADAPT (feasibility citation only; blocked on signal access).

### S16 — IPC2024-133905, improvements to B31.8 dent-strain estimation (snippet via websearch; proceedings paywalled)
https://asmedigitalcollection.asme.org/IPC/proceedings-pdf/IPC2024/88551/7415945/v02bt03a013-ipc2024-133905.pdf
- Content: Local plastic-strain estimation from dent-profile curvature remains B31.8's core, with ongoing work on curvature-calculation accuracy; PRCI notes the 6% limit itself is conservative for modern steels (S1: "further work required on critical strain values").
- RELEVANCE: Even the strain numbers are in flux — another reason to keep our dent handling to ordinal flags (plain / weld-affected / interacting) rather than pseudo-strain values with false precision.
- Verdict: USE (ordinal-not-cardinal dent encoding rule).

## Label/feature decisions for GTK1 (provisional, reviewer-gated)
1. DENT/WRIN/OVAL stay OUT of the corrosion target (fatigue/geometric threats, S8/S10; no depth data, S1/S2).
2. Build per-segment mechanical-proxy features: dent count, clock-split counts (upper-2/3 vs lower-1/3, S7), weld-proximate dent count (S4/S5), dent↔metal-loss co-location count within match window (S6/S7), WRIN/OVAL rare-class flags (S10–S12).
3. Ordinal dent encoding only — no pseudo-strain values (S16); complex/kinked dents carry uncertainty flags (S3).
4. Partner-data requests: raw caliper/geometry profiles (S14), ≥1-yr location pressure history (S13), per-survey geometry-tool specs (track5 extension).
