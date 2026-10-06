# TRACK 4 — Dataset shift, metrics & calibration under drift

Context: contractor/threshold drift inflates counts 2.5–5×; year/contractor is a covariate, never pooled.
PR-AUC primary; accuracy banned; R@P0.7 retired as vacuous; per-section recalibration required.
"New" = newly-reported ≥10% under pipe+2m/0.5m/1h match (includes re-detection). See `docs/GUARDRAILS.md`, `docs/VALIDATION.md`.

## (a) Shift formalism — sensors/vendors as shift

**[1] Quiñonero-Candela et al. (2009). *Dataset Shift in Machine Learning.* MIT Press.**
Method: Taxonomy of shift as factorisation change in p(x,y): covariate shift (p(x) changes, p(y|x) fixed),
prior-probability shift (p(y) changes, p(x|y) fixed), concept shift, sample-selection bias; importance-weighting cures for covariate case.
Relevance: Contractor change is NOT pure covariate shift — finer tool changes both p(x) (signal resolution) and the
label-generating process (what counts as ≥10%). Forcing one label = concept/prior shift on top of covariate shift.
Verdict: **USE** — adopt vocabulary; classify ON→SRTO/PK drift per factorisation before choosing a fix.

**[2] Moreno-Torres et al. (2012). A unifying view on dataset shift in classification. *Pattern Recognit.* 45:521–530.**
Method: Simplifies [1] into three testable cases (covariate / prior / concept) with a decision flowchart from
comparing p(x), p(y), p(y|x) across train/test; surveys which remedies are valid per case.
Relevance: Gives the screen behind our R3 stationarity gate (future/past ratio ∈ [0.5,2.0]): ratio outside band ⇒
prior-shift regime where pooled thresholds are invalid and per-section recalibration is mandatory, not optional.
Verdict: **USE** — cite for R3 gate rationale and for refusing pooled ON+SRTO thresholds.

## (b) Prior-probability shift — per-section recalibration

**[3] Saerens, Latinne & Decaestecker (2002). Adjusting the outputs of a classifier to new a priori probabilities. *Neural Comput.* 14:21–41.**
Method: EM loop: estimate new priors on unlabelled target data from current posteriors, then re-weight posteriors
by prior ratio p_t(y)/p_s(y); iterates to a fixed point without target labels.
Relevance: Exact template for per-section recalibration: keep discriminative model fixed, re-estimate section prevalence
from the target section's own score distribution, adjust intercept only. Fails if p(x|y) also shifted (our case) — so pair with cut-sensitivity column.
Verdict: **ADAPT** — implement EM prior update per section as the recalibration baseline; report with and without.

**[4] Lipton, Wang & Smola (2018). Detecting and correcting for label shift with black-box predictors (BBSE). *ICML*.**
Method: Estimates target p(y) by solving μ̂ = C·w (observed prediction frequencies = confusion matrix × target weights);
consistent even with biased/uncalibrated black boxes if C invertible; plus a BBSD hypothesis test for shift presence.
Relevance: BBSD gives a principled replacement candidate for the ad-hoc R3 ratio gate; BBSE weights give per-section
prevalence correction using only the frozen classifier's outputs — no relabelling of old surveys needed.
Verdict: **ADAPT** — trial BBSD alongside R3; USE BBSE weights as second recalibration comparator vs SLD-EM [3].

**[5] Garg et al. (2020). A unified view of label shift estimation. *NeurIPS* 33.**
Method: Shows BBSE [4] ≈ MLLS (EM maximum-likelihood label shift) under a weak confusion-matrix calibration;
MLLS wins empirically only when paired with a good post-hoc calibrator (Bias-Corrected Temperature Scaling).
Relevance: Decisive for our pipeline order: calibrate FIRST on source section (Platt/isotonic, train-only), THEN run
EM/BBSE on target section. Uncalibrated EM inherits source bias — which is exactly what contractor drift exploits.
Verdict: **USE** — mandates calibrate-then-reweight order; BCTS as candidate calibrator alongside Platt/isotonic.

## (c) Metrics under imbalance — PR-AUC primary

**[6] Davis & Goadrich (2006). The relationship between precision–recall and ROC curves. *ICML*.**
Method: Proves ROC↔PR point correspondence with non-linear interpolation in PR space; a curve dominating in ROC
dominates in PR but PR magnifies early-retrieval differences; linear interpolation in PR is invalid (overstates AUC).
Relevance: Justifies PR-AUC as primary on rare ≥10% cells AND forbids naive trapezoidal PR-AUC code — use Davis–Goadrich
non-linear interpolation (or average-precision) so sparse-positive sections are not overstated.
Verdict: **USE** — normative basis for PR-AUC primary + correct-curve-computation rule.

**[7] Saito & Rehmsmeier (2015). The precision–recall plot is more informative than the ROC plot … on imbalanced datasets. *PLOS ONE* 10:e0118432.**
Method: Demonstrates ROC-AUC invariant while PR-AUC collapses (0.74→0.23) as negatives grow 1k→10k at fixed TPR;
same ROC point = 10× more false positives under imbalance; accuracy/ROC hide what precision reveals.
Relevance: Our 0.27→0.08 cut-driven prevalence swing IS their experiment in the wild: ROC/accuracy would certify a
contractor artefact as skill. Direct licence for banning accuracy and retiring any fixed-recall headline without precision.
Verdict: **USE** — cite for accuracy ban, PR-AUC primary, and cut-sensitivity reporting (≥10%/≥12%/≥15%).

## (d) Calibration — and its collapse under shift

**[8] Niculescu-Mizil & Caruana (2005). Predicting good probabilities with supervised learning. *ICML*.**
Method: Benchmark of Platt (2-param sigmoid, data-frugal) vs isotonic (non-parametric stepwise, needs ≈1000+ calibration
points, overfits below); boosted trees/SVM need calibration, bagged trees/RF less so.
Relevance: Per-section calibration sets are small ⇒ Platt default, isotonic only where n suffices; fit on train fold only
(VALIDATION.md §4). Sigmoid-shape assumption breaks under contractor shift — hence per-section refit, never carry-over.
Verdict: **USE** — Platt-default/isotonic-if-n≥1000 rule, train-only fitting.

**[9] Van Calster et al. (2016). A calibration hierarchy for risk models. *J. Clin. Epidemiol.* 74:167–176; + Guo et al. (2017). On calibration of modern neural networks. *ICML* (ECE/reliability diagrams).**
Method: Four levels — mean (calibration-in-the-large: mean p̂ = prevalence), weak (intercept 0 + slope 1), moderate
(p̂ correct conditional on p̂; = ECE≈0/reliability-diagonal), strong (unattainable). ECE = binned |accuracy − confidence|.
Relevance: Minimum shippable claim per section is MEAN calibration (predicted rate = observed newly-reported rate at stated cut);
report intercept/slope + ECE + reliability diagram per section. A model can rank well (PR-AUC) yet be catastrophically miscalibrated across contractors.
Verdict: **USE** — mean calibration mandatory per section/cut; ECE + slope/intercept as standard panel.

**[10] Ovadia et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. *NeurIPS*.**
Method: Large-scale result: accuracy AND calibration degrade with shift severity; temperature scaling (in-distribution fit)
goes ineffective OOD; ensembles degrade slowest.
Relevance: Kills "calibrate once on ON, deploy on SRTO/PK": ID calibration does not transfer across contractor shift.
Requires per-section recalibration + reporting ECE on the TARGET section, and favours simple/ensembled heads for robustness.
Verdict: **USE** — cite against cross-section calibration carry-over; motivates per-section refit + ensemble comparator.

## (e) POD / detection-curve normalisation (NDT/ILI)

**[11] Berens (1988, POD methodology) → MIL-HDBK-1823A (2009) â-vs-a; ASTM E3023/E2862. DoD NDE reliability handbook + standards.**
Method: â-vs-a: regress continuous signal â on flaw size a (censored regression), derive POD(a) curve with confidence bound;
a90/95 = smallest flaw detected w.p. 0.9 at 95% confidence. Hit/miss (logistic) alternative for binary calls. Threshold â_dec trades POD vs false-call rate explicitly.
Relevance: This is the correct normalisation for contractor drift: each survey gets its own POD(a)/threshold curve; cross-survey
comparison happens at matched POD (e.g. a90/95), not matched raw counts. Our cut-sensitivity column (≥10/12/15%) is a coarse
â_dec sweep — POD says make it explicit: report operating threshold per survey and align surveys at equal detection probability.
Verdict: **ADAPT** — adopt POD framing + per-survey â_dec reporting; full â-vs-a fit is future work (needs signal-level archives we lack).

**[12] API Standard 1163, 3rd ed. (2021). In-line Inspection Systems Qualification (+ NACE SP0102 / ASNT ILI-PQ).**
Method: Umbrella qualification: every ILI *system* (tool+people+software) states POD, probability of identification (POI),
and sizing tolerance at stated certainty (e.g. ±10% wall at 80%) per anomaly type; 3 validation levels (system/manufacturer/operator dig verification).
Relevance: Industry already encodes our guardrail: performance claims are SYSTEM-conditional, never pooled across vendors —
exactly "absolute AP is cut- and survey-conditional." Per-section operating thresholds + dig-verified match-rate/vanished-frac are our API-1163-analogue validation levels.
Verdict: **USE** — cite as domain authority for never pooling ON vs SRTO and for POD/POI/tolerance triple per survey.

## (f) 2022–2026 threshold harmonisation across vendors

**[13] Hoening (2024). Technical ILI system — verification vs validation. *IPC2024* V02BT03A008; Penspen ILI benchmarking (PTC 2021, Charlton); operator practice (resolution normalisation pre-matching).**
Method: No published 2022–2026 standard harmonises thresholds across ILI vendors. State of practice: (i) API-1163 validation
per system; (ii) run-to-run anomaly matching with resolution normalisation (sensor interval, minimum detectable size, depth
uncertainty) BEFORE growth analysis; (iii) low-confidence pairs to manual review, never force-matched.
Relevance: Confirms our design is the honest one: no universal vendor-neutral threshold exists, so harmonisation = per-section
thresholds + resolution-aware matching (our pipe+2m/0.5m/1h greedy match + boundary-cell exclusion) + per-section recalibration.
Force-pooling vendors is the known source of spurious growth rates — our E14 void (ratio 4.78) is that error caught.
Verdict: **ADAPT practice, REJECT pooling** — mirror the match-then-normalise pipeline; record negative result (no harmonisation standard found).

## Design implications (what Track 4 mandates)

1. Order: fit ranker → calibrate on source (Platt default) → re-estimate prevalence on target (SLD-EM [3] vs BBSE [4]) → report at matched POD [11–12].
2. Metrics: PR-AUC (Davis–Goadrich interpolation) primary [6–7]; accuracy banned; every AP printed with match-rate, vanished-frac, cut-sensitivity column.
3. Calibration panel per section×cut: mean (mandatory), slope/intercept, ECE + reliability diagram [8–10]; never carry calibration across contractors [10].
4. Shift screen: keep R3 gate now; trial BBSD [4] as principled successor; classify each break per [1–2] before choosing covariate (reweight) vs prior (recalibrate) remedy.
