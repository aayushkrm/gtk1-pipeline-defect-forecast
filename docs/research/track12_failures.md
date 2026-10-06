# Track 12 — failure analyses: when inspection and prediction MISS

Adversarial evidence for the limitations section. Framing per GUARDRAILS/SUPERVISOR_BRIEF:
"newly-reported ≥10%", 60%/39% vanished-frac, no-80%-claim, repair-priority (triage) use-case.
Tooling note: websearch worked this track; webfetch cannot parse PDFs, so NTSB reports are
cited via their public HTML secondaries + full-text Federal Register advisory (fetched OK).

## (a) PHMSA root-cause statistics

### S1 — AMPP U.S. Pipeline Industry 2026 (PHMSA data analysis)
https://pgjonline.com/news/2026/march/ampp-report-finds-corrosion-behind-growing-share-of-us-pipeline-incidents
- Content: 600–700 PHMSA incidents/yr; corrosion historically ~18% of all incidents, >25% in 2024.
First AMPP energy-industry report; attributes rise to aging infrastructure + workforce shifts.
Sponsored by Sherwin-Williams; analysis of public PHMSA data + specialist interviews.
- RELEVANCE: Quantifies the threat our triage targets (corrosion = largest single preventable cause
and growing). Rising share also warns that past→future stationarity (R3 screen) can break.
- Verdict: USE (headline corrosion-share numbers for limitations §1).

### S2 — Pipeline Safety Trust corrosion primer (citing PHMSA)
https://pstrust.org/what-is-corrosion-and-how-can-it-affect-pipelines
- Content: Internal corrosion ≈60% of all corrosion-caused incidents and ≈12% of GT/gathering/HL
incidents; external corrosion ≈8% of GT/gathering/HL incidents. Transmission lines at higher
corrosion-accident risk than distribution (plastic pipe, lower pressure).
- RELEVANCE: Splits our ≥10% metal-loss label by mechanism — internal vs external need different
assessment methods (ICDA vs ECDA), which our ID-less tables cannot distinguish.
- Verdict: USE (internal/external split evidences label coarseness).

### S3 — Shen et al. 2024, PHMSA vs Canadian CER comparison (ScienceDirect)
https://www.sciencedirect.com/science/article/pii/S1874548224000209
- Content: Material/weld/equipment failure is the leading failure cause in both US and Canadian
datasets (not corrosion alone). External-corrosion rupture rate ≈1.0×10⁻⁵ per km-year — twice the
third-party-excavation or material-failure rupture rates (2002–2013 onshore GT).
- RELEVANCE: Baselines for any severity model: per-km-year rupture rates are ~10⁻⁵, so even a good
ranker has a tiny positive class — precision will always look poor in absolute terms.
- Verdict: USE (base-rate numbers for the repair-priority math preamble).

## (b) Named cases where assessment missed the defect

### S4 — NTSB PAR-11/01, San Bruno CA 2010 (via PHMSA/VNF summaries)
https://www.phmsa.dot.gov/safety-awareness/pipeline/pacific-gas-electric-pipeline-rupture-san-bruno-ca
- Content: 30-in Line 132 (1956 install) ruptured on a substandard weld with a visible seam flaw
that grew to critical size; 8 killed, 38 homes destroyed. PG&E's IM program used ECDA-type
assessment on a seam-weld threat and never detected or repaired the defective pipe.
- RELEVANCE: Canonical wrong-method miss: assessment ran, threat existed, method couldn't see it.
Direct precedent for our "survey-conditional reporting ≠ physical state" disclaimer.
- Verdict: USE (lead case study for ILI/assessment over-reliance).

### S5 — NTSB PAR-12/01, Marshall MI Line 6B 2010 (via InsideClimate News)
https://insideclimatenews.org/news/10072012/national-transportation-safety-board-ntsb-kalamazoo-enbridge-6b-pipeline-marshall-michigan
- Content: 2005 ILI detected the very cracks that ruptured; misinterpreted as minor, unrepaired for
5 years until a 6.5-ft gash spilled >1M gal dilbit. Control room missed it 17 hrs, twice re-pumping
oil into the leak. NTSB: "complete breakdown of safety"; cleanup >$800M.
- RELEVANCE: Strongest adversarial exhibit: detection ≠ prevention (sizing/interpretation +
human factors failed). Supports triage design where ranked lists must carry audit columns and
explicit uncertainty, not bare scores.
- Verdict: USE (centerpiece "ILI found it and still failed" case).

### S6 — NTSB PAR-02/02, Bellingham WA Olympic 1999 (via PST summary)
https://pstrust.org/olympic-pipeline-disaster/the-cause
- Content: 1994 excavation dent went uninspected; later "inaccurate evaluation of in-line inspection
results led to the company's decision not to" excavate the damage site; 1999 rupture killed 3 youths
(237k gal gasoline). Probable cause explicitly names the ILI mis-evaluation.
- RELEVANCE: Miss by mis-sizing/dismissal rather than by no-inspection — mirrors our threshold-drift
worry (a ≥10% call that vanishes or is dismissed at the next survey is a Bellingham-type error).
- Verdict: USE (second "ILI ran, defect dismissed" case).

### S7 — NTSB PAR-03/01, Carlsbad NM El Paso 2000 (via EHS Today/NTSB)
https://www.ehstoday.com/archive/article/21907202/ntsb-fatal-nm-pipeline-rupture-caused-by-corrosion
- Content: Severe internal corrosion thinned a 1950s 30-in line until it burst; 12 campers killed
(deadliest US gas-transmission blast). No adequate internal-corrosion program; segment geometry
(pig receiver/drip layout) made the rupture section uncleanable/unpiggable.
- RELEVANCE: Unpiggable-segment blind spot + internal-corrosion mechanism our tables cannot isolate;
justifies per-section "inspectability" flags in triage pages.
- Verdict: USE (unpiggable + internal-corrosion case).

## (c) False-negative economics (missed defect vs dig)

### S8 — Operator excavation cost ≈$91k (PHMSA-2025-0019 docket attachment)
https://downloads.regulations.gov/PHMSA-2025-0019-0027/attachment_1.pdf
- Content: Industry survey mean excavation/verification cost $90,057 (≈$91k after outlier removal),
used to price "unnecessary excavations" (predicted FPR>1.25×MOP). PHMSA's 2025 repair-criteria
modernization targets ~$390M/yr savings by risk-prioritizing rather than prescriptive digs.
- RELEVANCE: The cost side of repair-priority math: each false-positive dig burns ~$91k, so ranking
quality (AP at top-k) converts directly to dollars — the honest utility metric for our triage pages.
- Verdict: USE ($91k/dig as the unit cost in triage value framing).

### S9 — Failure-side costs: Marshall, San Bruno-scale, El Paso penalties
https://insideclimatenews.org/news/10072012/national-transportation-safety-board-ntsb-kalamazoo-enbridge-6b-pipeline-marshall-michigan
- Content: Marshall cleanup >$800M; PHMSA proposed a then-record $3.7M civil penalty (22 violations);
EPA Clean Water Act exposure $1,100–$4,300/bbl. El Paso (Carlsbad) paid $15.5M penalty + system-wide
reforms (per NACE/DOJ summaries). Single ruptures cost 10³–10⁴× one dig.
- RELEVANCE: Asymmetry (10⁴:1) is why repair-priority triage is the defensible use-case: we rank
where $91k digs buy the most expected risk reduction, without claiming ≥80% physical reliability.
- Verdict: USE (failure-vs-dig asymmetry numbers).

## (d) NTSB/PHMSA on ILI over-reliance + intervals

### S10 — NTSB P-22-003 → PHMSA Advisory ADB-2024-01 (hard spots; ILI data limits)
https://www.federalregister.gov/documents/2024/11/18/2024-26725/pipeline-safety-identification-and-evaluation-of-potential-hard-spots-in-line-inspection-tools-and
- Content: NTSB asked PHMSA to warn operators of "data limitations associated with hard-spot MFL ILI
tools and analyses." Danville KY 2019 rupture: 2011 ILI analysis found 16 hard spots; 2019 re-analysis
of the SAME 2011 data found 441. Five HIC hard-spot ruptures 2013–2023; susceptibility widened beyond
A.O. Smith to 8+ makers, all pre-1970 pipe.
- RELEVANCE: Re-analysis sensitivity gain (16→441) is the field-scale twin of our 60%/39%
vanished-frac + cut-driven prevalence (0.27→0.08): "new"/"absent" is analysis-conditional.
- Verdict: USE (strongest external support for the survey-conditional disclaimer).

### S11 — Kowalewski/PST program evaluation of IM (2013) + Jones Day rule summary
https://pstrust.org/wp-content/uploads/2015/10/Kowalewski-IM-PE_Report.pdf
- Content: IM rules assumed (i) assessment technology detects/characterizes defects accurately and
(ii) 5/7-yr reassessment catches deterioration pre-failure; evaluation flags both as unproven,
plus repair-criteria safety-factor erosion. Jones Day (2016 PHMSA proposal): ILI/pressure-test give
"a higher level of assurance (though still not 100%)" vs sampling methods like DA.
- RELEVANCE: Authoritative "not 100%" framing + challenged interval assumptions — exactly the
regulator-side humility our no-80%-claim position mirrors.
- Verdict: USE (over-reliance caution, quoted sparingly).

## (e) Academic ILI blind spots

### S12 — Zhao et al. 2022, dent assessment standards review (cited 50×)
https://www.sciencedirect.com/science/article/pii/S1995822222002552
- Content: Plain dents are manageable, but dents + fatigue, dents + corrosion/SCC, and dents with
gouges are major threats; standards (ASME B31.8, API 1160/579, PDAM/Cosham) treat interacting
threats with separate, conservative models. Complements PRCI NDE 4-12/4-13 (crack/SSWC detection
still improving) and axial-MFL seam-parallel blindness (Entegra).
- RELEVANCE: Interacting threats (dent+gouge, SCC+corrosion) are precisely the defects single-mode
MFL tables under-report — our ≥10% depth rows carry no interaction features, bounding what any
tabular model can learn.
- Verdict: USE (interacting-threat blind spot for limitations §2).

## (f) Reassessment-interval practice (forecast-horizon justification)

### S13 — 49 CFR 192 Subpart O + B31.8S: half-life rule, 7-yr cap, Fig. 4/80% limit
https://www.enersyscorp.com/assessment-intervals-regulations-and-challenges
- Content: Gas-T IM caps reassessment at 7 yrs (liquids 5); ICDA/SCCDA intervals = HALF the time for
the largest remaining defect to grow to critical size at the applicable rate (192.939). B31.8S Fig. 4
schedules corrosion responses by FPR with an 80%-depth application limit (INGAA/PHMSA-2008-0255
docket: Kiefner — practical limit, not accuracy limit).
- RELEVANCE: Industry's own horizon logic is half-remaining-life with conservative rates — our
survey-to-survey forecast horizon (years, not decades) and per-section thresholds sit comfortably
inside this practice; the 80%-depth note parallels our ≥10%-with-sensitivities reporting.
- Verdict: USE (horizon justification; cite 192.939 half-life rule + 7-yr cap).

## Cross-track verdicts
USE all 13 (S1–S13). No ADAPT/REJECT: every item directly evidences a limitation claim
(survey-conditional labels, dismissed/mis-sized calls, unpiggable gaps, interaction blindness,
10⁴:1 cost asymmetry) or justifies a triage-design choice (ranked dig lists, audit columns,
per-section thresholds, survey-horizon forecasts).
