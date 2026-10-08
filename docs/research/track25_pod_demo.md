# Track 25 — POD demonstration methods for in-line inspection (wave 7)

Tooling disclosure: websearch worked this session (4 query rounds, no HTTP 400). webfetch verified 12 pages in full. OpenAlex API verified 6 records (metadata + abstracts). arXiv API returned only off-topic probability-theory hits (recorded as negative below). Exa key absent, Exa SKIP per protocol (no Exa client in agent env). No commits made.

Context: track4 scopes MIL-HDBK-1823A and API-1163 per-survey POD framing plus the no-pooling rule. Track5 scopes per-tool sensitivity jumps and the 10 to 15% POD ramp numbers. This file does not repeat them. It adds demonstration designs that work with 3 to 4 repeat ILI runs, and it quantifies what a 10% to 7% registration threshold shift does to a demonstrated POD90 claim.

## (a) Hit/miss demonstration design with 3 to 4 repeat runs

Use binary outcomes only. Each anomaly site in each run scores 1 (reported at or above the stated depth cut) or 0 (absent or below cut). Fit a generalized linear model (logit or probit link) of hit probability on size. Read a90/95 straight from the confidence bound on the fitted curve [S3].

Minimum sample guidance from the handbook tradition: at least 60 flawed sites with sizes spread across the transition zone [S6, S13]. With 3 to 4 repeat runs over the same line, treat run as a grouping factor, not as independent evidence. Repeated inspections of the same sites do not multiply POD as 1-(1-p)^n. Independence fails across runs of the same pipe. Repeats characterize the inspection process itself [S4].

Practical recipe for our archive: build the site list from the union of all runs at the LOWER cut (7%). Score each run 0/1 at the common cut. Fit one GLM per survey pair with run indicators. Report a90/95 per run. Compare runs at matched POD, never at matched raw counts.

## (b) Signal-vs-size (ahat-vs-a) regression design

Use reported depth as the continuous response where the archive carries it. Regress reported depth on reference size with censored regression. Censoring matters because sub-threshold sites record no signal value. Dropping them biases the fit [S2]. Derive POD(a) as P(signal > decision threshold | size a) from the fitted mean line and residual spread [S7].

This design needs a reference size per site. Without digs, use the maximum reported depth across runs as a proxy reference, or use one run as reference and fit the other against it (ILI-to-ILI analogue of the unity-plot approach in track5 S7). Flag the result as relative POD, not absolute POD. Absolute POD needs field truth [S9, S10].

Threshold enters this design explicitly. POD(a) = 1 - CDF(threshold) at size a. Lowering the decision threshold from 10% to 7% shifts every POD(a) value up and moves a90 down. The fitted regression line does not change. Only the threshold cut through it changes [S7].

## (c) MAPOD with random effects

Model-assisted POD replaces part of the physical test matrix with simulation. The CNDE program states the two aims: quantify what a limited sample set can still support, and validate the simulation against measured points [S8]. The PNNL literature review maps the same structure: model calibration, uncertainty propagation, limited-set transfer [S14].

Random effects enter as hierarchical terms: run, tool, analyst, and site-group intercepts (and slopes where data suffice). They separate repeatable bias from noise. The SHM literature shows the repeated-measures version of this comparison directly: multiple inspections per flaw, method differences quantified per flaw [S15]. For ILI, the natural grouping is survey (tool plus crew plus software) with section nested inside.

Minimum honest MAPOD for our case: one calibrated sizing-error model per survey (slope plus intercept per POF class, per track5 S7/S9), a noise model from unmatched sub-threshold calls, and a transfer check where the two surveys overlap. No transfer check means no MAPOD claim. Record the check or drop the claim.

## (d) What a 10% to 7% threshold shift does to demonstrated POD90

A POD claim always pairs a size with a threshold. "POD90 at 10%" means 90% of flaws at 10% depth get reported. "POD90 at 7%" is a stronger claim. It asserts detection of smaller flaws. The same tool earns a lower a90 under the lower threshold, but it also pays with more false calls. Threshold moves trade sensitivity against specificity along a fixed ROC curve [S5].

Consequences for our matched-pair labels:

1. Re-cut both surveys at one common threshold before any matching. A pair built from a 10% run and a 7% run mixes two reporting functions. It is not a growth signal.
2. Rebuild the match table at 7%, at 10%, and at least one higher cut (12 or 15%). Keep the cut-sensitivity column from track4. The 7% column will show inflated "new" counts. That inflation is threshold mechanics, not corrosion.
3. Recompute match-rate and vanished fraction per cut. Expect vanished fraction to fall at 7% (fewer old calls disappear) and "new" share to rise (more small calls appear). If the pattern reverses, suspect a tool change on top of the threshold change.
4. Restrict growth claims to pairs above both surveys' a90/95. At 7% to 10% depths the pair sits inside the POD ramp where detection is chance-dominated. Growth computed there measures threshold luck.
5. Re-state every POD-adjacent number with its threshold. "POD90 = 12%" is meaningless. "POD90 at 7% reporting threshold" is a claim.

Positive predictive value falls as the threshold drops and prevalence of small indications rises. Most new 7% calls will be shallow or noise. This follows directly from the sensitivity versus PPV distinction [S5]. Plan analyst review capacity for the 7% column accordingly.

## (e) Per-survey POD requirement tie-in (API 1163, no duplication)

API 1163 3rd edition keeps POD plus POI plus sizing tolerance per anomaly type, and it now separates verification (did the run go to plan) from validation (are the results within spec) [S9, S10]. Level 1 accepts vendor spec for low-risk populations. Level 2 tests the spec with a binomial interval. Level 3 computes as-run performance. Our repeat-run designs above slot into Level 1 Option 2 (ILI-to-ILI comparison on unity plots) today, and into Level 2 or 3 only where dig measurements exist.

The 3rd edition also documents the field result that motivates this whole track: with tolerance +/-10% and certainty 80%, only 1 of 21 ILI providers met spec as-run [S10]. Expect vendor POD specs to fail as-run. Demonstrate per survey instead.

## (f) Negative results (kept explicitly)

1. No ready-made 10%-to-7% POD90 conversion factor for MFL exists in the sources found. Searched EN plus RU phrasings ("MFL POD90 reporting threshold percent wall", "POF detection threshold POD"). Result: only the mechanism (threshold moves along POD(a)) is documented. The numeric shift must be computed from our own matched data.
2. No random-effects MAPOD paper specific to ILI pipeline inspection was found. Closest verified items: the SHM repeated-measures POD comparison [S15] and the MAPOD review plus PNNL review [S13, S14]. ILI-specific hierarchical POD remains a gap.
3. arXiv API returned only generic probability-theory preprints for POD queries. No ILI-relevant POD preprint found there this session.
4. GIE run-to-run matching page timed out on fetch. Cited from search snippet only. Marked below.
5. ASNT MAPOD review page returned HTTP 403 (bot wall). Cited via OpenAlex metadata record only. Marked below.
6. NASA LS-POD guidebook and Trueflaw practical-POD PDFs use content types the fetcher cannot read. Cited from search snippets only. Marked below.
7. Springer hit/miss-versus-ahat comparison article is paywalled. Cited from abstract plus snippet. Marked below.
8. Exa unavailable (no key in agent env). Quad-provider self-test from INDEX.md still stands: Exa OK for lead, others SKIP.

## Sources (14 items; verification status per item)

### S1. Annis, mh1823 algorithms page (MIL-HDBK-1823A overview)
- Link: https://statistical-engineering.com/mh1823-algorithms/
- Content: Handbook scope (plan experiment, build specimens, collect data, fit POD(a) with 95% bounds, noise analysis, tradeoff curves). Hard limits: inputs must reduce to signal or hit/miss; specimens need measurable targets (amorphous corrosion excluded unless parameterized); software assumes true sizes and responses; POD model pinned to 0 left and 1 right (floor/ceiling needs workshop build).
- Relevance: Defines which of our archive columns qualify as POD inputs (binary call columns yes; raw report tables need preprocessing). The measurable-target limit is why depth in %t is our size variable.
- Verdict: USE as method authority.
- Verification: full page fetched this session.

### S2. Annis, how ahat-vs-a works
- Link: https://statistical-engineering.com/how-a-hat-works/
- Content: Animated demo: 30 (a, ahat) pairs per sample, censored regression fit (blue) against constructed truth (black), confidence versus prediction bounds. Ten resamples show how far one sample's fit can sit from truth. a90 covered by its confidence bound in 95 of 100 repeats.
- Relevance: Visual proof that one survey pair gives one noisy POD realization. Justifies per-survey fits plus bounds, never point estimates.
- Verdict: USE for analyst-facing explanation of a90/95 uncertainty.
- Verification: full page fetched this session.

### S3. Annis, how hit/miss models work
- Link: https://statistical-engineering.com/how-hit-miss-models-work/
- Content: Binning hits by size interval wastes data (size resolution versus POD resolution tradeoff). Better: posit a bounded continuous POD function, estimate by maximum likelihood (GLM). a90/95 reads directly off the confidence bound, unlike ahat-vs-a where it takes an extra step. Demo uses n=60 with resampling variability.
- Relevance: Primary recipe for section (a). n=60 sets the sample-size bar for our per-run hit/miss fits.
- Verdict: USE as hit/miss design basis.
- Verification: full page fetched this session.

### S4. Annis, repeated inspections
- Link: https://statistical-engineering.com/repeated-inspections/
- Content: The 0.9-to-0.99 double-inspection arithmetic assumes independence, which repeat looks at the same object violate. Apple-barrel parable: re-examining one apple teaches nothing new about the barrel mix, but disagreement teaches about inspection repeatability.
- Relevance: Blocks the most likely misuse of our 3 to 4 runs (claiming 1-(1-p)^n gains). Redirects repeats to repeatability estimation and run-effect modeling.
- Verdict: USE as constraint on section (a) and (c).
- Verification: full page fetched this session.

### S5. Annis, false positives (POD versus PPV, ROC)
- Link: https://statistical-engineering.com/false-positives/
- Content: Sensitivity (POD|a) and specificity are test properties. PPV and NPV mix test with population prevalence. Worked tables: a 90%/90% test at 0.3% prevalence gives PPV under 3%. Moving the decision threshold trades sensitivity against false calls (ROC). ROC ignores prevalence, so it misleads at low defect rates.
- Relevance: Core mechanism for section (d). Lowering 10% to 7% raises sensitivity, cuts specificity, and floods the call list where prevalence of shallow indications is high. PPV framing predicts the analyst-load cost.
- Verdict: USE as threshold-shift authority.
- Verification: full page fetched this session.

### S6. NDE-ed.org, introduction to POD
- Link: https://www.nde-ed.org/NDEEngineering/POD/introPOD.xhtml
- Content: POD study outputs (mean curve plus confidence bound; false-call rate as second output). Two study types: signal-reporting (ahat-vs-a) versus detection-only (hit/miss); signal data can be thresholded down to hit/miss at the cost of information. Hit/miss needs logistic regression.
- Relevance: Taxonomy for sections (a) versus (b). Licenses converting our depth columns to 0/1 at a stated cut while noting the information loss.
- Verdict: USE.
- Verification: full page fetched this session.

### S7. NDE-ed.org, background theory (POD math)
- Link: https://www.nde-ed.org/NDEEngineering/POD/backgroundTheory.xhtml
- Content: POD(a) = P(ahat > decision threshold) = 1 - CDF(threshold) given the signal distribution at size a. POD studies must vary instruments, inspectors, geometries, materials across the fleet. Worked Gaussian signal model with fitted intercept and slope.
- Relevance: Exact formula behind the threshold-shift claim in (d): same regression, new cut, new POD(a). Fleet-variability list maps to our survey-as-random-effect design in (c).
- Verdict: USE.
- Verification: full page fetched this session.

### S8. CNDE, MAPOD initiative page
- Link: https://www.cnde.iastate.edu/research/research-project-archive/model-assisted-probability-of-detection-mapod-initiative/
- Content: Program objective: full MAPOD methodology with reduced empirical testing. Aim 1: simulation plus statistics to support limited-sample POD. Aim 2: transfer-function cases with flaw-by-geometry interactions. Model validation required before limited-set or transfer claims.
- Relevance: Gate for section (c): simulation may shrink the dig matrix, but the transfer check on overlapping surveys is mandatory.
- Verdict: USE as MAPOD scope gate.
- Verification: full page fetched this session.

### S9. Irth/OneBridge, validating ILI performance with API 1163 and PRCI
- Link: https://irthsolutions.com/blog/validating-ili-performance-with-api-1163-and-prci-research-in-cim-0
- Content: POD = stated detection threshold plus probability per anomaly type (example: extended metal loss, 10%t threshold, POD 90%). POI defined separately with its own threshold. Sizing as tolerance plus certainty. Three validation levels (accept spec / binomial test / as-run). Burst capacity most sensitive to depth uncertainty. Field error must stay small relative to ILI error.
- Relevance: Industry wording for POD-plus-threshold pairing used in (d) and (e). Unity-plot workflow matches our ILI-to-ILI relative-POD design.
- Verdict: USE.
- Verification: full page fetched this session.

### S10. Irth, API 1163 3rd edition changes
- Link: https://irthsolutions.com/blog/api-1163-3rd-edition-whats-changed?hsLang=en
- Content: 200+ shall statements; verification versus validation split; Level 1 expanded (low risk, too few anomalies for sampling, similar-line experience); Level 1 Option 2 is ILI-to-ILI depth comparison on unity plots with combined tolerance flagged as weaker; Level 2 uses two-sided binomial intervals; PRCI spreadsheet sets 6 points (L2) and 10 points (L3) minima. Field finding: 1 of 21 providers met +/-10%@80% as-run.
- Relevance: Slots our repeat-run work at Level 1 Option 2 now, Levels 2/3 gated on digs. The 1-of-21 result warns against trusting vendor POD specs.
- Verdict: USE.
- Verification: full page fetched this session.

### S11. C-FER, corrosion growth rates from repeat ILI runs
- Link: https://www.cfertech.com/insights/obtaining-corrosion-growth-rates-from-repeat-in-line-inspection-runs-and-dealing-with-the-measurement-uncertainties/
- Content: PRCI-sponsored method: growth-rate distribution as a function of observed-growth-to-measurement-error ratio. Small ratio means uncertainty swamps the growth estimate and no probabilistic inference is meaningful. Defect-to-defect and population-comparison variants with worked repeat-run examples.
- Relevance: Companion gate for section (d) item 4: pairs inside the POD ramp have low growth-to-error ratios, so growth rates there are not meaningful even before threshold effects.
- Verdict: USE alongside track1 growth papers.
- Verification: full page fetched this session.

### S12. POF documents index (POF 100/300/310/311/330 availability)
- Link: https://pipelineoperators.org/documents
- Content: Public index confirms POF 100 (Nov 2021), POF 300 series (June 2026), POF 310/311 field verification (Dec 2023), POF 330 tool testing (Jan 2026) as downloadable documents.
- Relevance: Normative schema home for POD/POI/sizing tables per anomaly class (track5 S8 dependency). Confirms POF 330 exists for sub-threshold anomaly handling in future POD work.
- Verdict: USE as pointer; full POF 100/330 text still to mine in a later wave.
- Verification: full page fetched this session.

### S13. MAPOD review, ASNT Research Symposium 2024 (OpenAlex W4404140581)
- Link: https://doi.org/10.32548/rs.2024.002
- Content: Review of MAPOD evaluation methods with emphasis on reduced empirical testing (title/abstract via OpenAlex; proceedings article, closed access).
- Relevance: Secondary anchor for section (c) method survey.
- Verdict: ADAPT via secondary citation.
- Verification: metadata via OpenAlex API this session; full text not verified (closed access, ASNT page 403).

### S14. Meyer et al. 2014, Review of Literature for MAPOD (PNNL, OpenAlex W2296425144, 21 citations)
- Link: https://doi.org/10.2172/1183633
- Content: PNNL literature review structuring the MAPOD field (calibration, uncertainty, transfer).
- Relevance: Structure source for section (c) three-part minimum (sizing model, noise model, transfer check).
- Verdict: ADAPT via secondary citation.
- Verification: metadata via OpenAlex API this session; full text not verified.

Supporting (cited, secondary status): Generazio 2014 NASA/TM-2014-218183 on ROC/binomial/logit/Bayes POD interrelations (OpenAlex W576434265, OA via NTRS, metadata verified); Tai et al. 2024 POD review for phased-array corrosion mapping (OpenAlex W4401590471); Kim et al. 2025 MAPOD for wall-thinning defects (OpenAlex W4416253497); O'Connor 2019 thesis on method differences in POD prediction for SHM repeated-measure settings (OpenAlex W2972632246); Wang et al. 2019 J NDE hit/miss-versus-ahat comparison (https://link.springer.com/article/10.1007/s10921-019-0628-z, paywalled, abstract plus snippet only); NASA LS-POD guidebook 2021 (https://ntrs.nasa.gov/api/citations/20210018515/downloads/20210018515_corrected.pdf, PDF unreadable by fetcher, snippet only); Trueflaw 2016 practical POD paper (snippet only); GIE run-to-run matching note (page timed out, snippet only).

## Design implications (what track 25 mandates)

1. Fit per-survey POD now with hit/miss GLMs at a common cut (section a). Minimum 60 flawed sites across the transition zone per fit.
2. Run the ahat-vs-a relative fit where depth columns exist (section b). Report threshold explicitly with every POD number.
3. Treat survey as a random effect in any pooled model (section c). No transfer check means no MAPOD claim.
4. On the 10% to 7% question: re-cut, re-match, re-tabulates at 7/10/12%+, growth only above both a90/95s (section d).
5. File POD claims at API 1163 Level 1 Option 2 (ILI-to-ILI) until digs exist (section e).
