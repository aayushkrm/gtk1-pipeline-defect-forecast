# Track 11 — corrosion science for feature engineering (what drives external corrosion where)

Scope: external corrosion ≈90% of GTK1 defects (EXT location). No soil, coating-age, or CP data in ILI tables. Goal: justified proxy features for 100 m cells + partner requests. Websearch worked for this track (no API fallback needed).

## (a) Soil aggressiveness — what matters, what classifications exist

**S1 — AWWA C105 point system + resistivity classes (USE)**
https://rosap.ntl.bts.gov/view/dot/34648/dot_34648_DS1.pdf (GTI/PHMSA-256 review, Tables 10–13, pp. 55–57); https://nvlpubs.nist.gov/nistpubs/jres/69c/jresv69cn1p71_a1b.pdf (Schwerdtfeger/NBS)
Content: (1) AWWA C105 scores 5 parameters (resistivity, pH, redox, sulfides, moisture/drainage); total ≥10 = corrosive, trigger for protection. (2) Steel-pipe resistivity classes: <1,000 ohm-cm very severely corrosive; 1–2k severe; 2–5k moderate; 5–10k mild; >10k very mild. (3) ASME B31.8S maps resistivity to rate bins (≈3/6/12 mpy tiers).
RELEVANCE: No soil columns exist, so resistivity itself cannot be a feature; use terrain proxies per 100 m cell — river/wetland crossing flag, topographic wetness/lowland flag, odometer co-location with past external-corrosion clusters. Request from partner: soil survey / resistivity strip charts, backfill type, drainage notes per section.
Verdict: USE (as proxy specification, not as measured feature).

**S2 — NBS/NIST long-burial programme + modern reanalysis (USE)**
https://doi.org/10.6028/NBS.CIRC.579 (Romanoff 1957, Circ. 579); https://nvlpubs.nist.gov/nistpubs/ir/2007/NIST.IR.7415.pdf (Ricker NISTIR 7415); https://doi.org/10.1080/1478422X.2017.1417072 (Melchers & Petersen 2018)
Content: (1) ~4,500 bare-steel specimens, 86 sites, up to 17 y; mass loss + max pit depth recorded per soil. (2) Ricker re-digitised distributions: log-normal mass-loss and penetration rates, pitting ratios; soil chemistry alone explains little variance. (3) Melchers–Petersen: backfill compaction, air voids at steel interface, and moisture above water-holding capacity dominate; clay soils corrode fastest early, then rate declines (bi-modal, not linear).
RELEVANCE: Justifies two features: (i) construction-era/backfill disturbance proxy (pipe install year + crossing/roads work zones), (ii) time-since-install with decaying-rate functional form, not linear age. Request: construction year per pipe, backfill/bedding records, re-excavation history.
Verdict: USE (rate-decay shape + backfill > chemistry prior).

## (b) Coating degradation over decades

**S3 — CP shielding: FBE permeable vs PE-tape shielding (USE)**
https://doi.org/10.1016/j.corsci.2015.07.030 (Kuang & Cheng 2015); https://doi.org/10.1007/s11998-023-00850-y (J. Coat. Technol. Res. 2023 review; full text https://www.diva-portal.org/smash/get/diva2:1825443/FULLTEXT01.pdf)
Content: (1) HDPE/PE tape blocks CP current under disbondment; FBE absorbs water and passes CP (time- and potential-dependent). (2) Up to ~85% of external corrosion sits under disbonded shielding coatings. (3) Trapped-solution renewal (fluctuating water table) drives severe local attack under 3LPE.
RELEVANCE: Pipe `insulation`/coating column exists in weld logs — encode coating family × age interaction per 100 m cell; PE-tape + old + wet-location = highest prior. Request: coating type/rehab history per joint, field-joint coating records, disbondment dig reports.
Verdict: USE.

**S4 — Useful life 25–30 y; disbondment forensics (USE)**
https://pngrb.gov.in/pdf/press-note/GAIL15062022/PCR.pdf (coating spec/rehab, pp. 9–13: CTE/FBE ≈25–30 y, 3LPE ≈50 y); https://rosap.ntl.bts.gov/view/dot/36467/dot_36467_DS1.pdf (DNV/PHMSA dissecting disbondments, 2010)
Content: (1) Coal-tar enamel and FBE useful life ≈25–30 y before resistivity/CD-current thresholds fail; 3LPE ≈50 y. (2) DNV: cathodically disbonded FBE/CTE zones show low adhesion + pH 10–11 only adjacent to defect, near-neutral centimetres away. (3) Contaminated surface prep pre-disposes large-area low adhesion.
RELEVANCE: GTK1 pipes are multi-decade vintage → assume CTE-era coatings past design life; feature = age − 25 y exceedance × wetness. Request: recoating/rehab dates per km, surface-prep era if known.
Verdict: USE.

## (c) Cathodic protection criteria + failure modes

**S5 — NACE SP0169 criteria −850 mV / 100 mV / −950 mV SRB (ADAPT)**
https://midstreamcalculator.com/engineering/pipeline-ops/cp-survey-fundamentals.html (SP0169 §6.2.2 summary); https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/Corrosion_Enforcement_Guidance_Part195_6_22_2016.pdf (PHMSA enforcement, §195.571)
Content: (1) −850 mV vs Cu/CuSO₄ (IR-free/instant-off) = primary criterion; 100 mV polarisation shift = alternative where −850 unachievable. (2) −950 mV in SRB/anaerobic soils; avoid <−1200 mV (disbondment, hydrogen risk on high-strength steel). (3) ON-potential without IR correction inflates apparent protection — enforcement cases withdrawn over this.
RELEVANCE: No CP potentials in ILI data; use rectifier/drainage-point distance + known outage windows as hotspot features. Request: CIS/DCVG surveys, rectifier locations and outage logs, instant-off reads per km.
Verdict: ADAPT (criteria → data request + distance-to-CPS feature, not a threshold we apply).

**S6 — Stray-current / interference hotspots + magnitude (USE)**
https://pmc.ncbi.nlm.nih.gov/articles/PMC12902980/ (dynamic metro stray-current lab study, 2025); https://www.puc.pa.gov/media/2065/cathodic_protection_requirements090722.pdf (PA PUC interference requirements)
Content: (1) Dynamic DC stray current raised initial pitting rate to 1.283 mm/a unprotected; −1.2 V CP cut general/pitting to ≈0.05 mm/a. (2) 1 A discharging from a 1-inch holiday perforates pipe in ~16 h (EMS/CP course figure). (3) Interference signatures: narrow deep pits (width:depth <3), potential irregularities with intact coating spec.
RELEVANCE: Feature = crossing inventory per 100 m cell (rail, HV line, foreign pipeline/rectifier) + prior-defect morphology (narrow-deep pits flag). Request: AC/DC interference surveys, rail/utility crossing chainages.
Verdict: USE.

## (d) MIC signatures

**S7 — SRB-dominated MIC review + prevalence (ADAPT)**
https://doi.org/10.3390/ma17204996 (Materials 17:4996, 2024 review); https://pmc.ncbi.nlm.nih.gov/articles/PMC9841911/ (global petroliferous MIC metagenomics review)
Content: (1) SRB cause ~70% of MIC cases; anaerobic bottom-of-pipe biofilms reduce sulfate → H₂S, cathodic depolarisation, pitting. (2) MIC ≈10–20% of oil-&-gas corrosion events (NACE 2016 via Machuca); global survey finds sulfidogenic + methanogenic + acid-producing consortia co-correlated. (3) Clusters in stagnant/low-flow, water-accumulating, anaerobic, organic-rich soils — not uniform along line.
RELEVANCE: MIC cannot be diagnosed from ILI tables; use low-point/water-accumulation proxy + clustered deep-pit colonies with clean-steel surroundings as MIC-suspect flag. Request: dig-verified MIC cases, soil-sampling SRB counts, low-point elevation profile.
Verdict: ADAPT (suspect-flag + request, never a label).

## (e) Pipe manufacturing / vintage effects

**S8 — ERW seam threat spectrum; spiral vs longitudinal context (USE)**
https://downloads.regulations.gov/PHMSA-2011-0023-0680/attachment_25.pdf (PHMSA ERW study review, Battelle/Kiefner/DNV); https://bymmt.com/wp-content/uploads/2023/08/PPIM-2023_NDE-Toughness-Submitted-Rev-3.pdf (PPIM 2023: vintage ERW seam vs body toughness)
Content: (1) Vintage low-frequency ERW: cold welds, hook cracks, selective seam corrosion, pressure-cycle fatigue enlargement; seam CVN ≈1–30 ft-lb vs body 5–30 ft-lb (lower shelf). (2) Seam failures concentrate on bond-line/HAZ with unrecognisable origins; pre-1970s welds most suspect. (3) Spiral (SAW-helical, large-D) vs longitudinal (ERW/LSAW): spiral distributes stress helically, larger-D from narrow strip; longitudinal straight seam = burst-strength-critical line.
RELEVANCE: `pipe Type` + weld columns already encode spiral vs single/double-seam — build seam-type × vintage interaction per 100 m cell; expect seam-adjacent defect spectra to differ (ERW-selective vs spiral long-helix). Request: mill/manufacture year + process per joint, hydrotest history.
Verdict: USE (directly matches our Type field; X-70 vs 17G1S-U strength split adds hydrogen/SCC caution per S5).

## (f) Published corrosion-rate numbers (priors for depth reasoning)

**S9 — NACE/ECDA default + EPRI compiled distribution (USE)**
https://restservice.epri.com/publicdownload/000000000001025256/0/Product (EPRI soil-side rate literature review, 2012, §§2–3,7–8)
Content: (1) NACE SP0502 default pitting rate 0.4 mm/y (16 mpy) = upper-80th percentile of bare-coupon maxima (348 datasets: NBS C-450/C-579, PRCI Barlo, ASTM); max in set 2.0 mm/y (cinders). (2) Mean ≈0.2 mm/y (7.9 mpy), σ ≈9.1 mpy. (3) 0.4 mm/y deemed conservative for coated + CP transmission pipe; not valid under MIC/stray-DC/galvanic coupling (raise to ≥0.5 mm/y near copper grounding).
RELEVANCE: Prior for matched-Δdepth sanity checks: sustained >0.4 mm/y on coated/CP pipe = suspect sizing/threshold artefact or MIC/stray event, not background. Request: operator's assumed rate for re-inspection intervals.
Verdict: USE (upper-bound prior, not a growth model).

**S10 — Pitting-rate probabilistic models (ADAPT)**
https://www.researchgate.net/publication/223383957_Probability_distribution_of_pitting_corrosion_depth_and_rate_in_underground_pipelines_A_Monte_Carlo_Study (Caleyo et al., Corros. Sci. 2009); https://www.sciencedirect.com/science/article/pii/S0010938X12004350 (Valor et al. reliability review)
Content: (1) External pit depth/rate best fit by extreme-value (Gumbel/Weibull-family) distributions via Monte Carlo over soil/age covariates — tail, not mean, drives leaks. (2) Single-value NACE rate under-states early-life variance; time-dependent and Markov-chain growth models compared for reliability. (3) Practical upshot: model P(new deep pit) per segment, not mean wall loss.
RELEVANCE: Supports P1-binary + P2-count hurdle framing (Problem.md): predict ≥1 new defect and tail counts per km, never segment mean depth. No new feature; shapes loss/metric choice.
Verdict: ADAPT (method prior; REJECT as direct rate plug-in — needs soil covariates we lack).

## Consolidated proxy-feature shortlist (100 m cells; past-survey only)
1. Wetness: river/wetland crossing + lowland flag. 2. Coating family × max(0, age−25). 3. Seam-type × vintage (spiral vs ERW/LSAW; X-70 vs 17G1S-U). 4. Rectifier/interference-crossing distance. 5. Prior external-corrosion density (LGCP-smoothed) + narrow-deep-pit flag. 6. Install-year + backfill-disturbance zone.
Partner requests: soil/resistivity strips, coating+rehab per joint, CIS/DCVG + rectifier outages, crossing chainages, MIC dig confirmations, mill year/process.
