# TRACK 2 — Spatial + tabular methods for defect forecasting

Context: P1 = 1-km binary new-corrosion (≥1 new defect ≥10% depth / 4–5y); P2 = 1-km count regression, zero-inflated (85–95% negatives). Metrics: PR-AUC + recall@P=0.7 (P1); MAE/RMSE/Spearman (P2). HGB baselines beat deep models so far. All features past-survey-only; group-by-section + future hold-out (see PROBLEM.md, VALIDATION.md).

## (a) Zero-inflated / hurdle counts

**[S1] Lambert, D. (1992). Zero-Inflated Poisson Regression, with an Application to Defects in Manufacturing. *Technometrics* 34(1):1–14.**
Method: Mixture of a degenerate-zero (structural) process with probability π and a Poisson(λ) count process; EM estimation of both parts.
Covariates enter π and λ separately, so different drivers can govern "any defect" vs "how many".
Originally motivated by manufacturing defects — the closest classical analogue to P2.
Relevance: P2's 85–95% zeros match the ZIP data-generating story (immune segments + sampling zeros). ZIP's π-submodel is structurally a P1 classifier.
But: many zeros alone do not force a ZI model — plain NB often suffices (see S2 caveat).
Verdict: **ADAPT** — fit as P2 diagnostic against plain NB; reuse its binary head as a P1 candidate.

**[S2] Greene, W.H. (1994). Accounting for Excess Zeros and Sample Selection in Poisson and NB Models (NYU WP EC-94-10); Hilbe, J.M. (2007/2014). *Negative Binomial Regression; Modeling Count Data* (CUP). Impl: R `pscl`, `glmmTMB`, `brms`.**
Method: ZINB adds NB dispersion to ZIP (handles overdispersion + excess zeros jointly); Hilbe systematizes NB/ZINB selection (likelihood-ratio/Vuong tests, dispersion diagnostics).
Modern impls add random effects (`glmmTMB`: section-level intercepts) and Bayesian hierarchies (`brms`).
Allison/Statistical-Horizons critique: test NB before ZINB; excess zeros can be pure overdispersion.
Relevance: Gives P2 a principled likelihood ladder: Poisson → NB → ZINB, each strictly generalizing the last, with section random effects matching our group-by-section design. Directly outputs calibrated segment rates for survey prioritization.
Verdict: **USE** — NB as P2 statistical baseline; ZINB only if it beats NB on held-out P2 likelihood/MAE.

**[S3] Hurdle models: Cragg, J.G. (1971). *Econometrica* 39(5); Mullahy, J. (1986). Specification and testing of modified count models. *J. Econometrics* 33(3).**
Method: Two-part model: Bernoulli hurdle P(y=0) + zero-truncated count for y>0; the two parts fit independently (unlike ZIP mixtures).
Handles zero-inflation AND zero-deflation; each part takes its own covariates/link.
Interpretation is cleaner than ZIP: "does anything happen" vs "given action, how much".
Relevance: Maps 1:1 onto our P1+P2 split — hurdle gate ≡ P1 binary task, truncated count ≡ P2-positive. Lets us pair any P1 classifier (HGB) with any count head without joint-likelihood machinery.
Verdict: **USE** — adopt as the P1/P2 architecture: HGB-binary gate × Poisson/NB count head.

## (b) LGCP / INLA for lattice counts

**[S4] Møller, J. et al. (1998). Log Gaussian Cox Processes. *Scand. J. Stat.*; Rue, H., Martino, S., Chopin, N. (2009). Approximate Bayesian Inference for Latent Gaussian Models via INLA. *JRSS-B* 71(2); Diggle, P. et al. (2013). Spatial/Spatiotemporal LGCP review.**
Method: LGCP drives point intensity by exp(Gaussian field) with Matérn covariance; INLA fits latent-Gaussian models deterministically (Laplace + sparse precision), orders of magnitude faster than MCMC.
Lattice extension: segment counts ≈ aggregated LGCP with CAR/ICAR adjacency prior — standard disease-mapping practice.
Uncertainty comes free as posteriors over segment risk.
Relevance: Principled spatial smoother for 1-km lattice counts: borrows strength from neighboring segments, exactly the "hotspot continuity" survey planners want. Fits our small-n regime (hundreds of segments) where MCMC is overkill.
But: needs adjacency design + leakage care (field fit on past only); ranking quality rarely beats GBDT on tabular features.
Verdict: **ADAPT** — use as spatial-smoothing ablation / uncertainty layer over HGB scores, not the primary ranker.

## (c) Self-exciting / Hawkes processes

**[S5] Hawkes, A.G. (1971); Ogata, Y. (ETAS aftershock sequence); Mohler, G. et al. (2011). Self-Exciting Point Process Modeling of Crime. *JASA*; Reinhart, A. (2018). Review of Self-Exciting Spatiotemporal Point Processes. arXiv:1708.02647.**
Method: Conditional intensity λ(s,t) = background μ(s) + Σ triggering kernel g(s−sᵢ, t−tᵢ) over past events; EM/stochastic-declustering attributes each event to background vs triggered.
Crime/earthquake gains come from exact event IDs + timestamps enabling parent–offspring attribution.
Marks (magnitude/depth) modulate offspring productivity.
Relevance: Tempting "corrosion begets corrosion" story, and it conceptually justifies our segment-persistence baseline (past density predicts future density). But GTK1 has no persistent defect IDs (SSID absent/pre-2021, 0% coords) — triggering attribution is unidentifiable from interval-censored 4–5y snapshots.
Verdict: **REJECT** as forecaster (ID requirement unfixable); keep only as narrative justification for past-density features.

## (d) GBDT count losses + monotonic constraints

**[S6] Ke, G. et al. (2017). LightGBM. *NeurIPS* (LightGBM docs: `objective ∈ {poisson, tweedie, gamma}`, `monotone_constraints`, `monotone_constraints_method`); Prokhorenkova et al. (2018). CatBoost. *NeurIPS* (ordered boosting, Poisson loss, monotone constraints); sklearn HGB (`loss='poisson'`).**
Method: Native Poisson/Tweedie log-link objectives optimize count likelihood directly (variance ∝ mean^p), no log(1+y) hacks; Tweedie p∈(1,2) interpolates Poisson–Gamma for zero-mass + heavy-tail counts.
Monotone constraints force selected features (past max depth, defect density, age) to be non-decreasing in risk — physics/audit guardrail.
Histogram binning + native categoricals keep training fast on segment tables.
Relevance: Direct P2 upgrade path from HGB-regression: same pipeline, proper count likelihood, calibrated rates for ranking; monotone constraints convert engineering priors into testable ablations and block embarrassing reversals (e.g. deeper past → lower risk). Pair with P1 binary HGB = S3 hurdle.
Verdict: **USE** — LightGBM/HGB Poisson-Tweedie + monotone constraints as primary P2 heads; ablate constraints on/off per VALIDATION.md.

## (e) Trees vs deep on tabular

**[S7] Grinsztajn, L., Oyallon, E., Varoquaux, G. (2022). Why do Tree-Based Models Still Outperform Deep Learning on Typical Tabular Data? *NeurIPS* 2022 (45 datasets, ~20k compute-hours HPO).**
Method: Controlled benchmark of XGBoost/RF vs ResNet/FT-Transformer/TabNet with equal HPO budgets on medium tabular data (~10k rows).
Trees win SOTA; gap traced to inductive biases: irregular target functions, uninformative features, rotation-sensitive (meaningful-axis) features.
Gap narrows only at large n or with heavy tuning — neither our regime.
Relevance: Independently predicts our observed HGB>deep result: segment tables are small-n, heterogeneous, irregular — exactly tree-favorable. Sets the burden of proof: any deep model must beat tuned HGB on PR-AUC/recall@P=0.7 to justify its cost.
Verdict: **USE** as policy — GBDT-first, deep-only-with-ablation; cite in methods to pre-empt "why no transformers".

## (f) SHAP auditability

**[S8] Lundberg, S.M., Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS* 2017 (SHAP; TreeSHAP exact for GBDT).**
Method: Shapley additive attributions: unique locally-accurate/consistent per-prediction feature credits; TreeSHAP computes them exactly and fast for tree ensembles.
Global (mean |SHAP|, dependence plots) + local (per-segment) explanations from one fitted model.
Interfaces to monotonicity checks: dependence plots must show the enforced direction.
Relevance: Engineering auditability requirement: every flagged 1-km segment needs a reason (past density? max depth? contractor/method covariate?). SHAP also operationalizes the VALIDATION.md method-effect ablation — contractor/year SHAP mass quantifies threshold-drift confounding.
Verdict: **USE** — TreeSHAP on all HGB/LGBM models; per-segment top-features ship with every risk list.

## (g) Applied pipeline/corrosion forecasting 2022–2026

**[S9] Chen, X. et al. (2023). Analysis and Prediction of Pipeline Corrosion Defects Based on Data Analytics of In-Line Inspection. *J. Infrastruct. Preserv. Resilience* 4:14.**
Method: ILI-driven corrosion analytics: defect sizing/growth statistics across repeat inspections, ML classifiers for defect occurrence/severity on segment features.
Explicitly wrestles with tool/threshold comparability across runs — same drift problem as our 2.5–5× threshold change.
Validation is retrospective hindcast, not prospective hold-out.
Relevance: Closest applied template: segment-level ILI features → corrosion risk. Adopt their feature engineering (density, size distribution, growth proxies); reject their validation — ours must stay prospective (2016→2021 train, 2021→2025 test) per VALIDATION.md.
Verdict: **ADAPT** — borrow features, not evaluation design.

**[S10] Tree-ensemble ILI studies: Alshaye, E. (KFUPM thesis). Supervised ML for Max Depth of Corrosion Defects from historical ILI; Ammi et al. (2023). ML-Based Classification for Pipeline Corrosion. *Energies* 16(8); Appl. Sci. (2025). Corrosion-rate prediction for gas pipelines (tree/GBM leads).**
Method: RF/XGBoost/GBM on ILI + pipe attributes for depth classification and corrosion-rate regression; consistent finding: tree ensembles top single-model leaderboards on ILI tables.
Depths predicted at defect level where IDs match; segment aggregation secondary.
Interpretability via importance/SHAP increasingly standard for operator acceptance.
Relevance: Convergent evidence for S7 in our domain: on ILI-style tabular data, tuned trees are the bar. Supports HGB-first P1/P2 and SHAP reporting (S8). None solve our harder task (prospective new-defect forecasting under ID loss) — that gap is our contribution.
Verdict: **ADAPT** — treat as domain baselines to beat; differentiate on prospective protocol + zero-inflated evaluation.

## Track verdict

Primary: hurdle architecture (S3) = HGB-binary P1 gate × LightGBM/HGB Poisson-Tweedie P2 head (S6) with monotone constraints; NB/ZINB ladder (S2) as statistical check; LGCP/INLA (S4) as spatial-smoothing ablation; TreeSHAP (S8) on everything; Grinsztajn (S7) + applied studies (S9–S10) as baselines-to-beat. Hawkes (S5) rejected — no IDs, no attribution.
