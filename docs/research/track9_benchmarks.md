# Track 9 — benchmark datasets + evaluation methodology for rare-event degradation forecasting (2026-10-06)

Tooling: websearch (intermittent) + Mendeley public API
(`data.mendeley.com/public-api/datasets/c2h2jf5c54`), OpenAlex,
NASA PCoE pages via webfetch. No overlap with tracks 1–8.

## 1. Mendeley 4-run ILI set — deep dive (the sandbox)

**Link/DOI:** `10.17632/c2h2jf5c54.1` — Yarveisy / Khan / Abbassi, Memorial Univ.,
"Dataset for: Cross-country Pipeline Inspection Data Analysis and Testing of
Probabilistic Degradation Models", v1, 2021-10-04. Companion paper (open access):
`10.1016/j.jpse.2021.09.004` (J. Pipeline Sci. Eng. 1(3):308–320).
**Content (3):** 200+ km line, 4 consecutive ILI runs over 7+ years of
external-corrosion degradation. Files (total **~343 MB**, CC-BY 4.0, direct URLs
in the public-API record): `External Features Year {One,Three,Five,Seven}.xlsx`
(57/71/74/67 MB), `External Anomalies Processed.RData` (73.5 MB), `analysis.R`,
`plots.R`, `README.pdf`. Companion paper adds processing pipeline + stochastic
degradation fits for failure probability / burst pressure.
**Relevance (2):** Only open repeat-run wall-loss time series known — exactly the
matcher/threshold sandbox track 3 nominated. Per-run xlsx split forces the same
match-across-runs problem our pipeline solves (no IDs, threshold drift).
**Verdict: USE — directly downloadable now (CC-BY 4.0, ~343 MB); first action is
README.pdf + row-count/column audit against our field map.**

## 2. NASA C-MAPSS + PHM08 (RUL benchmark family)

**Link/DOI:** Saxena & Goebel (2008), NASA PCoE repository:
`https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip`
(~13 MB); PHM08 challenge set via `https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/`;
mirrors on Kaggle + HuggingFace (`LucasThil/nasa_turbofan_degradation_FD002`).
**Content (3):** Simulated run-to-failure sensor series: 4 FD subsets
(100–249 train / 100–259 test engines; 1–2 fault modes × 1–6 conditions)
plus PHM08 set (218 train / 218 test / 435 blind-validation trajectories, 26 columns).
Reviews: Saxena et al. PHM08 metrics paper; Ramasso & Saxena (2014) benchmarking
survey. N-CMAPSS (2021) adds real flight-condition inputs and 7 failure modes.
**Relevance (2):** De-facto degradation benchmark with 15 years of published
baselines — the template for how we should report (fixed splits, hidden
test, asymmetric cost). Failure physics differs (turbofan ≠ pits) so transfer is
methodological, not parametric.
**Verdict: USE — directly downloadable now (US public domain); FD001 = smoke test
for any sequence/survival head before touching pipeline data.**

## 3. Saxena et al. prognostic-evaluation protocol (PH, α–λ, RA/CRA + PHM08 score)

**Link/DOI:** Saxena et al., "Metrics for Evaluating Performance of Prognostic
Techniques", PHM08, `10.1109/PHM.2008.4711436` (free PDF via NASA DASHlink);
application notes Saxena et al. PHM09 / IJPHM 2010; Sharp (2013) PHM conf.
`phmconf.2013.v5i1.2317` (Weighted Error Bias / Spread / CI Coverage / Convergence
Horizon).
**Content (3):** Hierarchy: Prognostic Horizon (first time predictions stay within
±α of EoL) → α–λ test (stay inside a cone shrinking toward EoL) → Relative
Accuracy / Cumulative RA → Convergence rate. PHM08 competition score is
asymmetric: `Σ(exp(−d/13)−1)` for early (d<0) vs `Σ(exp(d/10)−1)` for late (d≥0)
predictions — late RUL over-estimates penalised ~e-fold harder. Sharp's four
scale-free metrics allow comparing query sets of different sizes/lifetimes.
**Relevance (2):** Direct answer to "how to score censored rare-event forecasts":
adopt PH + α–λ + asymmetric cost for any ≥10 %t lead-time claim, and never report
RMSE alone. Our dig/no-dig decision has the same asymmetry (missed deep defect ≫
false dig), so the PHM08 13-vs-10 constants are a worked precedent for our own
cost ratio.
**Verdict: ADAPT — no download; lift the metric hierarchy + asymmetric-score idea
into our eval plan (Dec scope: report PH-style horizon alongside MAE 6.5 / PR-AUC 0.64).**

## 4. Velázquez et al. soil-pitting set (259 rows) + DNN/BNN baselines

**Link/DOI:** Velázquez et al. 2009/2010 (southern-Mexico buried onshore lines, ≤50 yr);
data mirrored with code at `github.com/HMesghali/Predictive-Deep-Learning-for-Pitting-Corrosion`
(`SewagePipe_Data_Complete.csv`, MIT); modelled in Akhlaghi et al. 2023 (PSEP,
DNN, `10.1016/j.psep.2023`) and Cui & Wang 2024 (ensemble BNN + SHAP,
`10.1016/j.psep.2024.05.011`); DataCite record via ResearchGate publication
`318835278`.
**Content (3):** 259 complete rows: 11 inputs (soil chemistry, resistivity,
potentials, coating score, pipe age) → max pitting depth dmax. Small-n,
single-region, cross-sectional (no repeat runs). A 2025 tree-based ILI study on a
different 4-run/3.2M-defect set (JPSE `10.1016/j.jpse.2025.100308`) reports RMSE
0.368 mm, +41.5 % over naïve — shows what "honest win vs naïve" looks like.
**Relevance (2):** Closest open analogue to our per-defect depth problem with
published ML numbers — calibrates expectations for n≈hundreds soil-driven models.
Cross-sectional, so it cannot validate forecasting; useful only as a static-depth
baseline anchor.
**Verdict: ADAPT — downloadable via GitHub mirror (verify against paper tables);
use for static-depth baseline only, never as a forecasting claim.**

## 5. Bastek et al. 2026 cautionary replication (overfitting on the same set)

**Link/DOI:** Bastek / Denecke / Schmidt, "Future directions for data-driven
approaches in pipeline integrity management", Rel. Eng. Syst. Safety 271 (2026),
`10.1016/j.ress.2026.112300` (140-ref review; case study III re-runs a standard ML
fit on the Velázquez data with 10-fold CV).
**Content (3):** Replicates high-accuracy external-corrosion ML claims and finds
severe overfitting once rigorous CV is applied; companion case study shows low
run-to-run replicability of published ILI corrosion counts. Concludes PoF
estimates are insufficiently location-dependent; proposes a GIS-based fix.
**Relevance (2):** The "honest baseline" anchor for our 6.5/0.64: any challenger
model must survive grouped/blocked CV, and inflated single-split R² on 259 rows is
the failure mode to avoid. Independently corroborates our no-pooling / per-survey
POD stance from a second group.
**Verdict: ADAPT — no data; cite as the methodological bar (blocked CV + naïve
benchmark) every P2 experiment must clear.**

## 6. NIST NACE-NIST CORR-DATA (24k lab records) + Coelho meta-database

**Link/DOI:** CORR-DATA, NIST PDR `54AE54FB37AC022DE0531A570681D4291851`,
DOI `10.18434/M3TH4R` (NIST open license, bulk ZIP via `opendata.nist.gov`);
Coelho et al. "Machine learning for corrosion database", Mendeley
`10.17632/jfn8yhrphd.1` (CC-BY 4.0) + notebook `github.com/bcoelho-leonardo/Machine-learning-for-corrosion`.
**Content (3):** CORR-DATA: >24,000 coupon records from >250 documents (1982–1997
NACE-NIST program): alloy × environment × concentration × temperature → observed
rate/mode. Coelho DB: curated literature-level ML-for-corrosion table (features,
targets, critical points per paper). Neither is a pipeline wall-loss series.
**Relevance (2):** Directly downloadable corrosion priors (rate ranges, feature
vocabularies) for sanity-checking our growth priors and feature names. No
repeat-measurement structure, so zero forecasting leverage — prior-only use.
**Verdict: ADAPT (priors/vocab) — both downloadable now; REJECT as forecasting
benchmarks.**

## 7. PHMSA incident + annual-report data (US, public domain)

**Link/DOI:** No DOI; `phmsa.dot.gov/data-and-statistics/pipeline/source-data` —
flagged incident ZIP (`PHMSA_Pipeline_Safety_Flagged_Incidents.zip`, monthly
updates, USA public-domain license) + per-system annual-report mileages; 20-year
trend definitions (serious/significant/fire-first flags).
**Content (3):** All US reportable gas + hazardous-liquid incidents since 1970
(thousands of rows: date, location, injuries, commodity released, cause/subcause,
cost in current + 1984 dollars). Annual reports give mileage denominators. Cause
taxonomy harmonised across the 20-yr window.
**Relevance (2):** Only open event-rate ground truth at national scale — usable to
calibrate base rates / priors for rare ≥10 %t occurrence per mile-year, and as the
downstream "did incidents fall?" check. Too coarse (no defect-level depths, no
repeat runs) for model training.
**Verdict: ADAPT — downloadable now; use for base-rate calibration + context,
never for training. (EGIG European incident data is members-only: REJECT.)**

## 8. SKAB (Skoltech Anomaly Benchmark) — eval-protocol template

**Link/DOI:** `github.com/waico/SKAB` (GPL-3.0) + Kaggle mirror
`10.34740/KAGGLE/DSV/1693952` (Katser & Kozitsin 2020); companion discussion of
TranAD/TSS protocol in `arXiv:2601.19022`.
**Content (3):** 34 multivariate sensor series from a water-circulation testbed, one
labelled anomaly each, with DUAL markup (point-outlier vs collective/changepoint)
+ reference leaderboard (T², PCA, Isolation Forest, LSTM, autoencoder,
MSCRED) and standardised scoring modules.
**Relevance (2):** The dual-markup + fixed-leaderboard pattern is exactly what our
matcher sandbox needs: score point-defect matches and segment-level degraded
intervals separately, publish frozen baselines. GPL-3.0 copyleft — keep at arm's
length (protocol inspiration + temporary harness, no vendored code).
**Verdict: ADAPT (protocol + harness idea) — downloadable now; do not merge
GPL code into our repo.**

## 9. Rare-event / censored-data eval methodology cluster

**Link/DOI:** (i) Rare-event prediction survey `arXiv:2309.11356` (ACM Comp. Surv.
2024); (ii) time-dependent precision–recall under censoring, Biometrical J.
`10.1002/bimj.202300135`; (iii) "provisional evaluation" of censored time-to-event
forecasts `arXiv:2603.14835` (2026).
**Content (3):** Survey: honest rare-event practice = PR-AUC over ROC,
cost-aware thresholds, event-grouped CV, CIs on every metric — but almost no
rare-event-specific eval exists for numeric forecasting (gap we sit in).
(ii) extends PR curves to censored outcomes; (iii) proves threshold-weighted
CRPS/log-score stay strictly proper under right-censoring while the *mean*
forecast is NOT elicitable — evaluate quantile/interval forecasts.
**Relevance (2):** Theoretical backing for our panel (PR-AUC + cut-sensitivity +
per-section calibration from track 4): report AUPRC at multiple operating cuts with
bootstrap CIs, and frame ≥10 %t forecasts as censored quantile problems. Directly
warns against our MAE-6.5-style point-metric-only reporting.
**Verdict: ADAPT — papers only; adopt AUPRC-at-cuts + censored-quantile framing
in the eval plan.**

## 10. Synthetic corrosion generators (stress-test the matcher)

**Link/DOI:** (i) Zhang et al., pit-growth random-field + copula + Monte Carlo,
ASCE J. Eng. Mech. `10.1061/(ASCE)EM.1943-7889.0001957` (2022); (ii) GRF depth-
increment model with Gaussian/exponential semivariograms, RESS 2026
`10.1016/S0951832026003352`; (iii) latent-GRF metal-loss field with intermittency
threshold, `10.1016/S0167473021000205`; (iv) Valor et al. Markov-chain extreme-pit
model (2010) + stochastic power-law pit growth (WJAETS-2026-0382 MATLAB model);
(v) Kroese & Botev `arXiv:1308.0399` — MATLAB recipes for GRF/MRF/point-process/
Lévy-field synthesis; (vi) pit-pattern scale analysis justifying clustered
synthesis, PMC `7659981` (Ripley's-L multiscale, `spatstat`).
**Content (3):** Recipe stack: GRF/Matérn field for background depth +
clustered point process (Thomas/Matérn-cluster per PMC scale findings) for pit
centres + Markov/power-law growth in time + POD-threshold observation layer to
mimic the 10–15 %t detection ramp. All open-form methods with reference code.
**Relevance (2):** Generates unlimited matched-pair ground truth with known
growth; degrade it (drop IDs, jitter odometry, apply POD ramp) to measure matcher
recovery vs greedy/Hungarian — the ablation track 1 asked for, without spending
real test pairs. Also yields the clustered textures our hurdle head must handle.
**Verdict: USE — build a small in-house generator (numpy/scipy, our license);
papers give parameters, not code to vendor.**

## 11. NBS/NIST underground-corrosion re-analysis (negative result)

**Link/DOI:** Ricker, NISTIR 7415 (2007), `nvlpubs.nist.gov/nistpubs/ir/2007/NIST.IR.7415.pdf`;
data paper PMC `4548875` (1922–1940 bare-steel coupon burials across US soil types).
**Content (3):** Decades-long coupon mass-loss/pit data with contemporary soil
surveys; re-analysis concludes damage equations are possible but with irreducibly
large uncertainty (seasonal/positional scatter, <50 % sites with full soil data).
No repeat in-situ wall-loss series.
**Relevance (2):** Bounds what soil-only forecasting can ever achieve — supports
keeping soil features as weak priors, not primary predictors, and explains why our
model must lean on repeat-ILI signal. Historical interest only beyond that.
**Verdict: REJECT as benchmark; keep one-line citation for the "soil alone is not
enough" position.**

---

### (b) Downloadable-now summary

| # | Set | License | Size / rows | Access |
|---|---|---|---|---|
| 1 | Mendeley 4-run ILI `c2h2jf5c54` | CC-BY 4.0 | ~343 MB; 4 xlsx + RData | direct file URLs (API record) |
| 2 | C-MAPSS + PHM08 | US public domain | ~13 MB; 100–435 engines/set | NASA S3 ZIP + Kaggle/HF mirrors |
| 4 | Velázquez-259 mirror | MIT (mirror) | 259 rows CSV | GitHub raw |
| 6 | NIST CORR-DATA / Coelho DB | NIST-open / CC-BY 4.0 | 24k records / lit-table | direct ZIP / Mendeley |
| 7 | PHMSA flagged incidents | US public domain | 1000s rows, monthly | direct ZIP |
| 8 | SKAB v0.9 | GPL-3.0 (arm's length) | 34 CSV series | GitHub/Kaggle |

### (d) Published baseline anchors (honest-reporting references)

- PHM08 board: winner **score 437** on test (#5T); published tables add
MSE/MAE/MAPE/FPR/FNR per entry — report the full panel, not one number.
- C-MAPSS FD001 RUL: plain 2-layer LSTM **RMSE ≈ 16.8 / MAE ≈ 13.1 / PHM-score
≈ 380** (public repo, matched-param); recent hybrid/state-of-art **RMSE ≈ 15.5**;
classical RF/LASSO/SVM worse — sequence structure buys ~5–30 %.
- PHM21 (N-CMAPSS) winning blend **score 3.0** (0.5·RMSE + 0.5·asymmetric-s) —
precedent for a composite metric like ours.
- ILI depth on real data: tree models **RMSE 0.368 mm, +41.5 % over naïve**
(JPSE 2025) — the "beat naïve by a stated margin" reporting bar; Bastek-2026
shows single-split wins on 259 rows evaporate under 10-fold CV.

### December-scope actions (no scope change)

1. Download item 1 (README + row/col audit) and item 2 (FD001 smoke test).
2. Freeze eval panel: PR-AUC-at-cuts + MAE + PH-style horizon + asymmetric cost;
blocked CV mandatory (items 3, 5, 9).
3. Build item-10 mini-generator for matcher ablation; PHMSA base rates (7)
as priors only.
