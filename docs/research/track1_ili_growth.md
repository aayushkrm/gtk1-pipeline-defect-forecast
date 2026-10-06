# TRACK 1 — ILI corrosion growth + measurement-error modeling

Scope: segment/pipe risk forecasting (P1 binary, P2 count) under GTK1 constraints —
no persistent defect IDs, odometer matching ±2 m, reporting-threshold drift 2.5–5×.
See `docs/PROBLEM.md`, `docs/DATA.md`.

Search note: websearch integration returned HTTP 400 on all queries (2026-10-06), so
verification used OpenAlex + arXiv APIs via webfetch (all DOIs/years/authors/citations
below confirmed there). Publisher pages (Hindawi, SpringerOpen) bot-walled; method
summaries cross-checked against OpenAlex abstracts + canonical content.

## (a) Caleyo/Valor group — power-law, Markov chain, Monte Carlo

**[1] Caleyo, F., Velázquez, J.C., Valor, A. & Hallen, J.M. (2009).
"Probability distribution of pitting corrosion depth and rate in underground
pipelines: A Monte Carlo study." *Corrosion Science* 51(9).
DOI: 10.1016/j.corsci.2009.05.019 (~279 cites).**
Method: pit kinetics as power law d = k·(t−t₀)ⁿ fitted per soil class;
extreme-value (Gumbel) distributions for max depth; Monte Carlo propagation of
depth/rate distributions into time-dependent failure probability.
RELEVANCE: power law with n<1 formalizes decelerating growth — supports
short-horizon segment features over linear extrapolation; soil-class conditioning
is the template for our per-section covariates. Needs absolute depths + initiation
times we lack; threshold drift corrupts the distribution's left tail.
Verdict: **ADAPT** — use power-law form as segment growth prior, not per-defect.

**[2] Caleyo, F., Velázquez, J.C., Valor, A. & Hallen, J.M. (2009).
"Markov chain modelling of pitting corrosion in underground pipelines."
*Corrosion Science* 51(9). DOI: 10.1016/j.corsci.2009.06.014 (~170 cites).**
Method: depth discretized into states; non-homogeneous continuous-time pure-birth
chain whose intensities reproduce the power-law mean; closed-form Kolmogorov
forward solution for transition probabilities.
RELEVANCE: yields growth-rate distributions without tracking individuals — matches
the no-ID constraint in principle; but calibration still needs matched defect pairs
with stable reporting thresholds, both violated here.
Verdict: **ADAPT** as population-growth prior at segment level; **REJECT** for
per-defect Δdepth (consistent with the R² 0.3–0.5 ceiling in PROBLEM.md).

**[3] Zhou, W. (2010). "System reliability of corroding pipelines."
*Int. J. Pressure Vessels Piping*. DOI: 10.1016/j.ijpvp.2010.07.011 (~141 cites).**
Method: burst-pressure limit states (B31G-class) + stochastic growth inside a
Monte Carlo system-reliability frame over many defects along a line.
RELEVANCE: the burst-pressure Monte Carlo anchor of this track; shows how growth
samples convert to failure probability — the downstream consumer of any growth
model we fit. Far above our segment-classification scope, but sets the interface:
our P1/P2 outputs should feed, not replace, this kind of assessment.
Verdict: **ADAPT** — keep as reliability-interface reference for KBD<0.9 pipe triage.

## (b) Zhang & Zhou group — hierarchical Bayes + sizing error

**[4] Al-Amin, M., Zhou, W., Zhang, S. & Kariyawasam, S. (2014).
"Hierarchical Bayesian Corrosion Growth Model Based on In-Line Inspection Data."
*J. Pressure Vessel Technol.* 136. DOI: 10.1115/1.4026579 (~23 cites).**
Method: hierarchy defect ⊂ segment ⊂ line; defect growth rates drawn from
hyperdistributions; multiple ILI snapshots; MCMC; separates true growth from
tool effects using operator ILI data.
RELEVANCE: the hierarchy maps exactly onto pipe → 100 m/1 km segment → section;
their tool-effect level is our year/contractor/standard covariate. Requires
box-to-box matched defects, which we only partly have (53–73% NN ±2 m).
Verdict: **ADAPT** — port hierarchy to segment counts/rates (section random
effects in the P2 NB model).

**[5] Zhang, S., Zhou, W. & Qin, H. (2013). "Inverse Gaussian process-based
corrosion growth model for energy pipelines considering the sizing error in
inspection data." *Corrosion Science* 74. DOI: 10.1016/j.corsci.2013.04.020
(~89 cites).**
Method: IG process for depth growth + measurement equation (reported = true +
tool bias + scatter); bias estimated jointly; shows ignoring sizing error biases
growth rates.
RELEVANCE: statistical twin of our threshold-drift problem; justifies the
Depth≥10% normalization + campaign covariate, and skepticism toward raw Δdepth.
Needs repeated matched depths — ON 2016→2021→2025 only.
Verdict: **ADAPT** — adopt bias-per-campaign + scatter structure inside the
matched-Δdepth secondary analysis.

**[6] Zhang, S. & Zhou, W. (2014). "Bayesian dynamic linear model for growth of
corrosion defects on energy pipelines." *Reliab. Eng. Syst. Saf.*
DOI: 10.1016/j.ress.2014.04.001 (~54 cites).**
Method: state-space (dynamic linear) growth with Kalman-type updating as new ILI
arrives; pools information across defects while allowing individual trajectories.
RELEVANCE: sequential-updating logic fits our train-2016→2021 / test-2021→2025
protocol; pooling is what makes sparse matched data usable. Same matched-data
prerequisite as [4]–[5].
Verdict: **ADAPT** — updating/pooling pattern for the matched subset; not the
main P1/P2 engine.

## (c) Gamma-process foundation

**[7] van Noortwijk, J.M. (2009). "A survey of the application of gamma processes
in maintenance." *Reliab. Eng. Syst. Saf.* 94(2). DOI: 10.1016/j.ress.2007.03.019
(~1365 cites).**
Method: review of the monotone gamma Lévy process: shape/scale functions,
closed-form hitting-time (first-passage) distributions, estimation, inspection
updating, maintenance optimization.
RELEVANCE: monotone growth fits corrosion; hitting-time math underpins a
"time-to-first-Defect≥10%" framing of P1. Assumes repeated perfect observation
of the same unit — broken by unmatched defects + drifting thresholds.
Verdict: **ADAPT** — hitting-time logic for P1 survival framing; **REJECT**
per-defect gamma fitting on VTD tables.

## (d) Matching + growth-rate vetting without IDs

**[8] Amaya-Gómez, R. et al. (2022). "Matching of corroded defects in onshore
pipelines based on In-Line Inspections and Voronoi partitions."
*Reliab. Eng. Syst. Saf.* 224. DOI: 10.1016/j.ress.2022.108520 (~21 cites).**
Method: cross-run defect matching via Voronoi partitions over longitudinal +
circumferential distance; probabilistic (not deterministic) matches; validated on
Colombian onshore lines; feeds growth estimation.
RELEVANCE: direct template for our same-pipe + distance ±2 m + offset ±0.5 m +
orient ±1 h rule; justifies match-probability + new/vanished uncertainty flags
instead of hard links.
Verdict: **USE** — adopt as matching-methodology reference.

**[9] Dann, M.R. & Maes, M.A. (2015). "Population-based approach to estimate
corrosion growth in pipelines." ICASP12, Vancouver. hdl.handle.net/2429/53254.**
Method: growth-rate distribution deconvolved from two ILI population depth
histograms — no defect-to-defect matching; physical-bound vetting of rates.
RELEVANCE: built for exactly our no-ID case; works under threshold drift if
left-truncation is modeled; backs P2 count modeling + vetting of matched Δdepth.
Verdict: **USE** — primary statistical cover for unmatched growth estimation.

**[10] Kariyawasam, S. & Wang, H. (2011). "Learning from Multiple Corrosion Growth
Rate (Run-Comparison) Studies." NACE CORROSION 2011, C2011-11303; and (2012).
"Useful Trends for Predicting Corrosion Growth." IPC2012-90539.**
Method: operator (TransCanada/TC Energy) lessons across many run comparisons:
apparent negative growth = measurement noise; growth-rate vetting rules;
active-vs-dormant population trends.
RELEVANCE: industry precedent for quarantining implausible rates and flagging
new/vanished defects with uncertainty — validates treating negatives as noise.
Verdict: **USE** — adopt vetting rules in ETL.

## (e) Vendor sizing bias + POD

**[11] Caleyo, F. et al. (2007). "Criteria for performance assessment and
calibration of in-line inspections of oil and gas pipelines."
*Meas. Sci. Technol.* 18(7). DOI: 10.1088/0957-0233/18/7/001 (~59 cites).**
Method: bias (systematic) vs scatter (random) sizing error vs excavations;
calibration factors; POD-style reasoning per size class.
RELEVANCE: the bias/scatter vocabulary for our vendor/campaign covariate;
excavation-verified error magnitudes justify distrusting raw Δdepth.
Verdict: **USE** — cite for ETL normalization rationale; request vendor spec
sheets alongside the 5 planned re-exports. (Also note API RP 1163, ILI Systems
Qualification, as the industry POD/verification standard.)

**[12] Siraj, T. (2018). "Quantification of Uncertainties in Inline Inspection
Data for Metal-loss Corrosion … and Implications for Reliability Analysis."
PhD thesis, Western Univ. (Zhou group). OA via Scholarship@Western.**
Method: full ILI uncertainty budget — tool bias, scatter, depth-dependent POD,
spatial correlation — propagated into reliability; dig-verification datasets.
RELEVANCE: POD-vs-depth curves explain threshold drift as missing-small-defects,
not absent defects — critical for the P1 label (Depth≥10% + campaign covariate).
Verdict: **ADAPT** — lift POD/threshold reasoning into P1/P2 label design.

## (f) ML corrosion forecasting 2022–2026

**[13] Cui, B. & Wang, H. (2023). "Analysis and prediction of pipeline corrosion
defects based on data analytics of in-line inspection."
*J. Infrastruct. Preserv. Resilience*. DOI: 10.1186/s43065-023-00081-w (~24 cites).**
Method: statistical + ML analysis of real multi-run ILI: clustering features,
growth-rate distributions, future-defect prediction.
RELEVANCE: closest published analog to P1/P2 — segment-scale forecasting from ILI
history rather than crack physics.
Verdict: **USE** — benchmark feature set for segment models.

**[14] Song, Y. et al. (2023). "Interpretable machine learning for maximum
corrosion depth and influence factor analysis." *npj Mater. Degrad.*
DOI: 10.1038/s41529-023-00324-x (~61 cites).**
Method: gradient boosting + SHAP: max depth from geometry/soil/operational
factors with influence ranking.
RELEVANCE: SHAP-style influence analysis suits repair/survey prioritization; but
point-prediction accuracy won't transfer to unmatched, drift-affected VTD data.
Verdict: **ADAPT** — interpretable-ML + SHAP pattern for section ranking, not
depth regression. (Complements: Alshaye et al. 2025 tree-based max-depth from
historical ILI, *J. Pipeline Sci. Eng.* DOI: 10.1016/j.jpse.2025.100308 —
same verdict; Ben Seghier et al. 2026 generative augmentation for rare deep pits,
*PSEP* DOI: 10.1016/j.psep.2026.109627 — consider augmentation for the P1
minority class only, under strict future hold-out.)

## Takeaways for GTK1

1. No paper forecasts from ID-less, threshold-drifting VTD tables — the
   Dann–Maes population route [9] + Voronoi matching [8] + operator vetting [10]
   is our methodology core.
2. Every growth paper assumes stable, matched depths; our campaign-covariate +
   Depth≥10% design [4][5][11][12] is the honest substitute.
3. Stochastic-process literature [1][2][5][7] contributes priors and P1
   survival framing — never per-defect predictors.
4. ML literature [13][14] supports segment-scale classification with
   interpretability, matching the P1 ≥80%-recall scope; per-defect Δdepth stays
   secondary (R² ceiling stands).
