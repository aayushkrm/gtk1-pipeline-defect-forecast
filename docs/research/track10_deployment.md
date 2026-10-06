# Track 10 — deploying inspection-triage ML into operations

Scope: productization of the December triage deliverable (B1 ranked watchlists, heatmaps,
audit columns, no badges, per-section thresholds, disclaimers). See TRIAGE_SPEC.md, GUARDRAILS.md.
No overlap with tracks 1–8. Websearch worked for this track; two vendor pages webfetch-verified.
12 sources, ~1,650 words.

## (a) Human-in-the-loop ranking / triage UX

### S1. R4VR framework — safe human-in-the-loop visual inspection (2025)
Link: https://opus.hs-furtwangen.de/frontdoor/deliver/index/docId/12532/file/processes-13-04086.pdf
Content: Steel-surface inspection framework balancing automation with human oversight by risk tier.
Operators see uncertainty + explanations per prediction; high-uncertainty/disagreement cases route
to manual review; routine spot-checks (e.g. once per shift) catch drift; all predictions, warnings,
corrections versioned for EU AI Act auditability.
RELEVANCE: Direct template for our triage pages — ranked list + uncertainty flags + operator
override column, with audit columns as the log. Supports per-section review cadence in the runbook.
Verdict: ADAPT (role/queue pattern, not the vision models).

### S2. Cost-optimal human-inspection boundaries for one-class inspection models (2023)
Link: https://www.degruyterbrill.com/document/doi/10.1515/teme-2023-0010/html
Content: Formal cost model splitting outlier scores into auto-accept / human-inspect / auto-reject
bands; human-review interval [bl, bu] solved from false-negative vs labour costs. Reports ~57%
mean cost improvement over F1-optimal cutoffs across cost parameters on MVTec data.
RELEVANCE: Justifies our per-section operating thresholds as cost-driven, not accuracy-driven.
Harness could log implied cost of top-K review vs blind digs; runbook frames thresholds this way.
Verdict: ADAPT (two-boundary logic; recalibrate costs per section, never pool).

### S3. Radiology worklist triage via calibrated risk + queue simulation (Baruah & Rathore 2026)
Link: https://proceedings.mlr.press/v317/baruah26a.html
Content: Calibrated ICH probabilities reprioritize head-CT reading queues; discrete-event simulator
converts AUC into operational minutes-saved (median time-to-read for positives), conditioned on load,
staffing, prevalence, calibration. Ships a reproducible config-driven pipeline for pre-deployment eval.
RELEVANCE: Closest analogue to "B1 score → dig-queue order": measure triage value as time/cost saved
at fixed review budget (precision@K), not AUC alone. Harness should add a queue-sim metric.
Verdict: USE (evaluation pattern; adapt simulator to dig budgets per section).

### S4. Alert fatigue: drivers and mitigations (JMIR 2026; ICU meta-analysis 2026; DAVs study)
Links: https://www.jmir.org/2026/1/e78676/PDF · https://link.springer.com/article/10.1186/s12912-026-05328-x · https://journals.sagepub.com/doi/10.1177/0018720815585666
Content: Fatigue is contextual, not just volume: pooled ICU severity ~52/100 (I²≈100%);
triggers are false/non-actionable alerts, identical-looking alerts, jargon, workflow interruption.
Non-interrupting annotated visualizations cut inappropriate orders 34%→18% vs pop-up alerts (p<.001);
structured alarm-management education reduces fatigue in RCTs.
RELEVANCE: Triage pages must be pull-based ranked lists with reasons (match/vanished flags), never
interruptive pass/fail pop-ups. Cap default watchlist length; require override reasons (forces
accountability, per JMIR). Runbook needs a fatigue section.
Verdict: USE (design constraints: ranked pull list, short labels, audit-logged overrides).

## (b) Calibration / uncertainty display practice

### S5. Calibrate: interactive analysis of probabilistic output (Hunter et al. 2022) + CORP triptych
Links: https://ar5iv.labs.arxiv.org/html/2207.13770 · https://ar5iv.labs.arxiv.org/html/2301.10803
Content: Practitioners always pair reliability diagrams with prediction-density histograms — empty
bins have huge CIs, and identical-looking curves can hide very different ECE. CORP (PAV-isotonic)
removes ad-hoc binning, adds consistency/confidence bands, and decomposes Brier into
miscalibration/discrimination/uncertainty components.
RELEVANCE: Our pages must show calibration curves WITH counts + bands, per section; show Brier/ECE
bands as diagnostics for analysts, never as single headline numbers for operators. Formalizes the
no-≥80%-meter rule: report MCB/DSC/UNC triple, not one scalar.
Verdict: USE (CORP plots + bands in harness/analyst pages; keep off operator watchlists).

## (c) MLOps for integrity programs

### S6. Audit-ready MLOps + EU AI Act Art.72 post-market monitoring (2025–2026)
Links: https://consensuslabs.ch/blog/mlops-regulated-industries-audit-ready-pipelines · https://sota.io/blog/eu-ai-act-post-market-monitoring-mlops-implementation-alert-thresholds-2026
Content: Every decision traceable to dataset snapshot, code hash, model version, input hash;
tiered drift alerts (inform → caution → mandatory review → stop-the-line) keyed to decision risk,
not raw metric size; Art.72 requires documented PMS thresholds, drift-event log with closure status,
and a retraining log judging each retrain against the "substantial modification" boundary.
RELEVANCE: Blueprint for our harness: freeze matcher/cut/inputs per run (R1–R2), log R3 stationarity
screen + lift-CI (R4) per prospective pair, tier alerts (recalibrate-per-section vs quarantine), keep
a retraining/void log (E14 as worked example). PHMSA §192.947 record-keeping (below) is the domain hook.
Verdict: ADAPT (port tiers + logs to pipeline-integrity idiom).

### S7. Redeploy / recalibrate / refit trichotomy (insurance-monitoring, Brauer et al. 2025)
Link: https://github.com/burning-cost/insurance-monitoring
Content: Production monitor separating discrimination drift (Gini) from miscalibration (GMCB/LMCB):
nothing→REDEPLOY, calibration-only→RECALIBRATE (intercept fix, hours), discrimination loss→REFIT
(weeks); anytime-valid tests avoid monthly-retest false-alarm inflation (~40%/yr at α=.05).
RELEVANCE: Exact decision logic our runbook needs per survey pair: match/vanished drift with intact
rank-order → per-section recalibration; rank-order collapse → quarantine + remodel; neither → redeploy
frozen. Adopt anytime-valid-style caution against re-testing spent pairs (matches R-gate discipline).
Verdict: ADAPT (decision table + false-alarm math; methods are insurance-domain).

## (d) Operator case studies (ML-assisted dig/prioritization)

### S8. ROSEN V-ILI + ECDA field study (Pipeline Technology Journal 2023) ✓ core case
Link: https://contenthub.rosen-group.com/api/public/content/fb75621fb13a4158bc3a7eb0105ea296?v=058539a2
Content: ML trained on ~1,868 IDW pipelines predicted per-segment corrosion class for an unpiggable
line; 4 targeted excavations chosen from V-ILI + survey overlays; worst find <11% wt vs predicted
25–50% class — authors claim confidence gain, NOT defect sizing. Depth-confidence only 32–39%.
RELEVANCE: Honest precedent for our positioning: screening that focuses digs + reports low confidence
openly. Cite its <11%-vs-25–50% gap in the runbook as why we ship bands + match/vanished flags.
Caveat: vendor paper, no controlled comparison, unpiggable context only.
Verdict: USE (with caveats printed alongside).

### S9. OneBridge/Irth CIM ML classification model (2024, webfetch-verified)
Link: https://irthsolutions.com/blog/onebridge-solutions-maximizing-pipeline-integrity-with-machine-learning-0
Content: Classifiers trained on 6,000+ ILI reports / 50M+ anomalies normalize vendor-specific
descriptions into standard labels so anomalies can be matched across surveys for growth analysis;
also imputes missing risk-assessment fields and flags inconsistencies (e.g. coating vs install date).
No public precision/recall or dig-outcome numbers disclosed.
RELEVANCE: Validates our matcher/normalization-first architecture (standardize → match → rank) and
audit-column practice (sizing tolerances, MAOP surfaced per anomaly). Do not cite as accuracy evidence.
Verdict: ADAPT (ingest/match pattern; REJECT as performance evidence — vendor blog, no metrics).

### S10. Cenosco IMS refinery business case: $95M / 52 leaks prevented (2025, webfetch-verified)
Link: https://cenosco.com/insights/leading-middle-east-refiner-cuts-costs-with-ims
Content: RBI rollout (66% risk-based strategy mix) + CUI campaign over 3,200 assets: projected 80%
Tier-3 LOPC reduction, 52 potential leaks prevented, ~$95M safeguarded revenue/downtime avoidance.
Vendor business case; savings are projected/avoided-cost, not audited; refinery RBI, not pipeline ILI.
RELEVANCE: Usable only as "risk-ranked inspection planning pays" existence proof for stakeholders;
never as a transferable effect size. Harness must report realized precision@K instead of avoided-cost
projections. Pair with Shell predictive-maintenance caveat (11,000 models, 15M predictions/day claimed
via secondary LinkedIn summary — unverified, REJECT as citable numbers).
Verdict: ADAPT (narrative only, with "projected, vendor-reported" label mandatory).

### S11. PHMSA record-keeping + data-integration mandates (§192.947; 2022 RIN2 final rule)
Links: https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/technical-resources/pipeline/gas-transmission-integrity-management/60761/finalruleamendedgas071707.pdf · https://downloads.regulations.gov/PHMSA-2011-0023-0634/content.htm
Content: Operators must retain for pipeline life all records supporting threat/risk/dig decisions
(§192.947); 2022 rule forces verified, validated data integration (named attributes, SME-bias
controls) feeding risk assessment, plus analysis of interacting threats. GAO (2006) found operators'
weakest point was documenting decisions, not conducting assessments.
RELEVANCE: Regulatory grounding for audit columns: every ranked segment must carry its provenance
(survey pair, matcher version, cut, match-rate/vanished-frac). Runbook's per-page disclaimer +
R-gate log directly answer the GAO documentation gap.
Verdict: USE (compliance anchor for the whole December package).

## (e) Dashboard anti-patterns

### S12. Evidence that badges/meters mislead (BMJ Q&S; risk-matrix color; forest plots; dark-is-more)
Links: https://qualitysafety.bmj.com/content/26/1/81 · https://exa.ai/library/publication/d8n82w3dx69 · https://exa.ai/library/publication/1gbb35mzt77 · https://www.clicdata.com/blog/preventing-dashboard-misreads/
Content: RAG coloring of point values vs targets hides common-vs-special-cause variation and
provokes harmful on/off actions (BMJ: "at best useless, at worst harmful" — use control charts).
Colored risk matrices induce boundary-crossing bias (paying to cross a color line, not to reduce
risk), strongest in numerate users. Color-coded forest plots make users ignore estimate precision
and decide on significance color; dark-is-more bias overrides legend numbers on hazard maps.
RELEVANCE: Empirical backbone of our no-badges / no-single-meter rules: a red/green segment badge
or one "reliability %" invites exactly these biases (threshold artifacts, precision neglect, color
override of numbers). Keep heatmap sequential-intensity + numeric P with bands; add control-chart
view of AP over surveys rather than RAG status per survey.
Verdict: USE (cite in GUARDRAILS rationale; design heatmaps sequential, never traffic-light).

## Cross-track implications (provisional, reviewer-gated)
1. Harness: add precision@K-at-dig-budget + queue-sim minutes-saved metric (S3); CORP plots with
counts+bands per section (S5); redeploy/recalibrate/refit decision table per pair (S7).
2. Pages: ranked pull lists with reason flags + override-reason logging (S1/S2/S4); sequential
heatmap + numeric P with bands (S12); disclaimer + provenance on every page (S11).
3. Runbook: cost-framed per-section thresholds (S2); fatigue section (S4); vendor-case citation
policy — ROSEN citable with caveats, OneBridge/Cenosco narrative-only with labels (S8–S10).
