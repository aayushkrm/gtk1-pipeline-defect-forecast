# Track 15 — ECDA + above-ground survey fusion with ILI (what each survey would add)

Scope: how ECDA/CIPS/DCVG/ACVG/ACCA data fuses with ILI for dig prioritisation and ML features. No soil/CP/coating readings exist in GTK1 tables (DATA.md: lat/lon 0%); this track specifies the FUSION interface, not the science (see track 11 for corrosion mechanisms, track 8 for run alignment/ETL). Websearch worked for this track (no API fallback needed).

## (a) NACE SP0502 ECDA four-step process → dig priorities

**S1 — SP0502 four steps + 49 CFR 192.925 codification (USE)**
https://webstore.ansi.org/preview-pages/NACE/preview_NACE+Standard+SP0502-2008.pdf (flowcharts Figs 1a/1b, §§3–6); https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-D/part-192/subpart-O/section-192.925
Content: (1) Pre-assessment collects pipe/construction/soil/CP/operational history, judges ECDA feasibility, groups ECDA Regions, selects ≥2 complementary indirect tools. (2) Indirect inspection runs the tools over every Region, classifies indications by severity. (3) Direct examination digs prioritised indications (immediate/scheduled/monitor). (4) Post-assessment computes remaining life, sets reassessment intervals, reprioritises.
RELEVANCE: Our 100 m triage score is a pre-assessment/indirect-screening analogue: ECDA severity classes map onto our ranked-cell output as the dig-priority column. Request from partner: ECDA Region boundaries per section + any historic dig-priority sheets (indication → scheduled/monitor class) to validate our ranking against operator practice.
Verdict: USE (process template for dig-priority output format).

**S2 — 10 years of ECDA lessons: regions, clipped gradients, ILI+ECDA prioritisation (USE)**
https://products.corrosionservice.com/ts1547209649/attachments/Page/46/Lessons%20Learned%20during%2010%20Years%20of%20ECDA%20Application.pdf (Corrosion Service, 2014)
Content: (1) Too many/few ECDA Regions destroys reliability — regions must follow corrosion risk, not convenience. (2) DCVG %IR must be read jointly with the CIPS profile: high ON potentials "clip" gradients (severe defects read mild) and tiny on/off shifts deflate %IR. (3) Worked case: 2010 CIPS/DCVG aligned to 2006 ILI on an NPS10 line; pits ≥60% = severe / 45–59% moderate / 25–44% minor prior-corrosion history within 100 m; ECDA-type protocol cut 62 remaining ILI digs to 25 Group-A digs concentrated where potentials ran −450 mV and %IR >60%.
RELEVANCE: Gives the exact fusion recipe — align survey chainage to ILI odometer, classify joint indications, prioritise digs — and the 100 m window precedent matches our cell size. Request: any past CIPS/DCVG-vs-ILI alignment plots or joint-priority dig lists per section, with chainage ties, to replay this protocol on GTK1.
Verdict: USE (reference fusion workflow).

## (b) CIPS / DCVG / ACVG / ACCA — what each measures, resolution vs 100 m cells

**S3 — CIPS + DCVG procedures and %IR severity scale (USE)**
https://mitcorr.com/resources/cips-dcvg-survey.html (Mitcorr MTG-04); https://www.bacgroup.com/media/a3piegmw/pipeline-cips.pdf (BAC method statement)
Content: (1) CIPS walks pipe-to-soil potential at 1–3 m intervals (on + synchronised instant-off), flagging under-protection vs −850 mV/100 mV criteria — a continuous CP-health profile, not a defect list. (2) DCVG measures local voltage gradient over each holiday; severity %IR = ΔV_defect/ΔV_total: <15% minor, 15–35% moderate, 35–60% significant, >60% severe. (3) Combined CIPS+DCVG in one pass is standard practice; each reading GPS-stamped.
RELEVANCE: Future features per 100 m cell: min/mean instant-off potential, count + max-%IR of DCVG indications, metres of sub-criterion pipe — all aggregate cleanly from 1–3 m readings to 100 m. Request: combined CIPS/DCVG exports with GPS + odometer chainage, on/off potentials and %IR per indication.
Verdict: USE (feature specification for cells).

**S4 — ACVG vs DCVG vs ACCA/PCM capabilities and limits (ADAPT)**
https://aucsc.com/downloads/PIM_ECDA%20Indirect%20Inspection%20Tools-DCVG-ACVG%20Current%20Attenuation_2019.pdf (Walton, AUCSC); https://support.radiodetection.com/hc/en-gb/articles/360025245352-Conducting-an-ACCA-survey-and-an-ACVG-Survey (Radiodetection PCMx)
Content: (1) DCVG uses interrupted CP current + half-cell probes, ±4″ pinpointing, and uniquely reports anodic-vs-cathodic (corroding vs protected) state per holiday; needs 400–500 mV shift. (2) ACVG applies low-frequency AC + A-frame, works under paving and in AC corridors, less operator interpretation — but no anodic/cathodic state. (3) ACCA/PCM logs 4 Hz current attenuation at equal intervals: fast screening for coating condition, shorts, and large disbonded areas, but coarse — pinpointing needs a follow-up gradient survey.
RELEVANCE: Survey-type covariate matters (DCVG state flag vs ACVG location-only vs ACCA screening) before any severity is comparable across sections — mirrors our contractor-effect concern. Request: survey method + instrument + probe spacing + applied-signal level recorded per survey run, so indications carry a method tag.
Verdict: ADAPT (method-tagged, never pooled raw).

**S5 — PHMSA validation: DCVG/ACVG pinpoint, PCM/C-scan sectionise (USE)**
https://rosap.ntl.bts.gov/view/dot/34535/dot_34535_DS1.pdf (CC Technologies, PHMSA Rept. 80509201)
Content: (1) Head-to-head dig-verified test on 3 pipelines × ≥4 techniques: DCVG and ACVG most accurate with near-identical data; DCVG sized defects better. (2) Gradient surveys pinpoint individual holidays but are slow over long lines; PCM/C-scan bin the line into sections — faster, coarser. (3) PCM suited to large-area disbondment; small deep holidays can hide inside a large neighbour's gradient.
RELEVANCE: Justifies a two-tier feature design: pinpoint densities (DCVG/ACVG counts per 100 m) plus section-grade coating condition (PCM attenuation slope per 100 m). Request: raw station-by-station readings (not just dig sheets), so we control the 100 m aggregation and keep PCM screening separate from gradient pinpoints.
Verdict: USE.

## (c) CP potentials as ML features — published fusion examples

**S6 — 8,338-record field framework: instant-off potential + resistivity dominate (USE)**
https://www.sciencedirect.com/science/article/pii/S2667143326001058 (field-data external-corrosion-rate framework, 2026, open access)
Content: (1) First large field-data ML study fusing CP data with inspection records: 8,338 records from an operating North American buried system (vs prior lab/literature toy sets without CP). (2) Ensemble model with 5-fold + repeated 5×5 CV; feature importance + partial dependence rank instant-off potential and soil resistivity top. (3) Learned instant-off response matches electrochemistry (protection break near −850 mV) — physically consistent, not black-box.
RELEVANCE: Direct precedent for our planned feature set: per-cell instant-off potential is the single highest-value CP column to request; partial-dependence shape gives a prior for encoding it. Request: instant-off (IR-free) potentials at ≤10 m spacing per section, with rectifier on/off state logged, in tabular chainage-referenced form.
Verdict: USE (feature-priority anchor).

**S7 — Interpretable ML: pipe-to-soil potential (pp) top-4 predictor with −850 mV kink (USE)**
https://www.nature.com/articles/s41529-023-00324-x (npj Mater. Degrad. 2023); https://www.sciencedirect.com/science/article/pii/S0957582024005226 (ensemble BNN, R² 0.949, 2024)
Content: (1) On the Velázquez field dataset (Mexican onshore lines, up to 50 y), pp + chloride + pH + age top all importance rankings; ALE curves rise monotonically with pp. (2) Partial dependence jumps past −0.85 V — the SP0169 criterion emerges from data unprompted. (3) Ensemble-BNN gives calibrated uncertainty (MAE 0.33 mm, RMSE 0.449 mm) plus SHAP-ranked drivers, a template for honest intervals.
RELEVANCE: pp threshold behaviour (−850 mV kink, age >20 y acceleration) supplies encoding priors (hinge features, not linear) for when GTK1 CP data arrives; BNN+SHAP is the uncertainty-reporting model to copy. Request: pipe-to-soil potentials co-located with ILI anomaly chainages (the Velázquez schema: pp, pH, resistivity, redox, water content per defect neighbourhood).
Verdict: USE.

## (d) Coating-survey + ILI correlation (disbondment limits)

**S8 — No above-ground method sees disbondment without a holiday (ADAPT)**
https://rosap.ntl.bts.gov/view/dot/62152/dot_62152_DS1.pdf (PHMSA state-of-art on cathodic-disbondment detection, 2006)
Content: (1) DCVG/ACVG use amplitude only: they detect active holidays, but a disbonded coating with no through-holiday is invisible from above ground — the trapped cell is shielded from both detection and CP. (2) MFL ILI sees resulting wall thinning but not its cause; early-stage disbondment has no thinning to see. (3) ACVG/ACCA may flag large disbondments via capacitance/conductance shifts but cannot size them apart from small holidays.
RELEVANCE: Caps what fusion can claim: survey-quiet ≠ corrosion-free under shielding coatings (GTK1's vintage CTE/tape era — see track 11 S3/S4); disbondment-suspect flag must stay a prior, and ILI-missed-under-disbondment is a known-failure mode for the limitations section. Request: coating family + field-joint coating records + disbondment dig reports per km, to build the shielding-suspect prior per 100 m cell.
Verdict: ADAPT (as uncertainty cap, never as feature).

## (e) Aligning ECDA chainage with ILI odometer (our marker problem, mirrored)

**S9 — AGM/odometer/IMU fusion: accuracy numbers and failure modes (USE)**
https://irthsolutions.com/blog/correcting-imu-data-for-pipeline-movement-analysis-0 (IRTH, 2024); https://www.michigan.gov/-/media/Project/Websites/AG/environment/pipelines/Appendix_13__Enbridge_ILI_Reporting_Profile__West.pdf (Enbridge ILI reporting profile §AGR)
Content: (1) Vendor spec: IMU drift 1:2,000 of distance from nearest control point (≈1.5 m at 3 km spacing); hard points (valves, casings) are permanent, AGMs are temporary stakes prone to loss, mis-staking, missed triggers. (2) Real failure: ignoring post-launcher hard points produced 6-ft systematic offsets; run-to-run 30 m offsets traced to inconsistent secondary (AGM) control. (3) Fix protocol: girth-weld-match a master tally, revise AGM coordinates, have vendor recompute centerline; Enbridge mandates marker-list↔tracking-report correlation with tabulated omission reasons.
RELEVANCE: ECDA chainage and ILI odometer meet at the same weld/AGM control points — our Pipe-No + ±2 m match rule is the no-GPS version of this protocol; weld-anchored alignment (not raw odometer) is the shared fix. Request: AGM/marker lists with GPS + run distances per ILI campaign, and weld-anchored chainage on every future survey export, so ECDA indications land on the same datum as ILI rows.
Verdict: USE (alignment protocol + QC checklist).

## (f) 2022–2026 multi-modal integrity ML (ILI + ECDA + CP + GIS)

**S10 — ROSEN V-ILI: ML over global ILI warehouse feeding ECDA (USE)**
https://contenthub.rosen-group.com/api/public/content/fb75621fb13a4158bc3a7eb0105ea296?v=62f303ef (Barton, Pipeline Technology Journal 4/2023); https://www.rosen-group.com/en/expertise/product-and-service-finder/above-ground-inspection-and-integrity-services-for-unpiggable-pipelines (NIPA)
Content: (1) Virtual-ILI trains on an Integrity Data Warehouse (tens of thousands of inspected lines + rainfall/soil/coating metadata) to predict max-depth class and defect density for unpiggable lines; 7 km gas-line demo fused V-ILI with ECDA surveys to pick 4 digs (found coating flaws, max <11% wt — confirming "good" condition). (2) Value is confidence without extra digs: proving absence of corrosion, the hard case. (3) NIPA productises the same idea above ground: LSM + CP monitoring + construction records + GIS overlaid for hotspot detection.
RELEVANCE: Closest industry analogue of our triage overlay — ILI-history-driven priors fused with local surveys, evaluated by dig outcomes; "confirming absence is harder" directly supports our no-badges/guardrails stance. Request: any operator GIS layers (crossings, casings, rectifier sites) as chainage-referenced tables to prototype the overlay side of V-ILI-style fusion.
Verdict: USE (architecture + evaluation precedent).

**S11 — Production fusion tooling: ILI↔CIS alignment + CP-data ML (ADAPT)**
https://www.newcenturysoftware.com/products/alignment-manager/ (Alignment Manager: ILI+CIS weld-to-weld alignment); https://irthsolutions.com/blog/cis-analysis-within-cims-external-corrosion-module-0 (CIM External Corrosion Module); https://doi.org/10.3390/en14185805 (Rossouw & Doorsamy 2021, ICCP predictive maintenance)
Content: (1) Alignment Manager semi-automates ILI-to-CIS alignment to PODS at weld-to-weld level with tolerance templates — the commercial existence proof of our matcher direction. (2) CIM's ECM ingests CIS + ILI + GIS centerlines, flags sub-−850 mV regions into mitigatable segments, and roadmaps DCVG/ACVG + root-cause ML next. (3) Rossouw 2021 predicts ICCP-unit and downstream test-post potentials with regression/classification + survival analysis for maintenance timing — CP telemetry itself is modellable.
RELEVANCE: Buy-vs-build signal (alignment + CIS ingestion are solved UI problems; our edge is the calibrated triage score on ID-less tables) and a second CP-ML precedent at the rectifier level. Request: PODS/UPDM export of any existing operator GIS + CIS archives, so future fusion starts from aligned tables, not PDFs.
Verdict: ADAPT (interface targets, not methods to copy).

## Partner-request wording to add (continue TRIAGE_SPEC numbering)

6. Combined CIPS/DCVG (or ACVG/ACCA) exports per section with GPS + weld-anchored odometer chainage, on/off potentials, %IR per indication, and method/instrument/probe-spacing tags per run.
7. AGM/marker lists with GPS + run distances per ILI campaign, plus any historic ECDA-Region boundaries and joint ILI↔survey dig-priority sheets.
8. Rectifier locations + outage windows, instant-off potentials at ≤10 m spacing, and CP test-post telemetry where logged.
9. Coating family + field-joint coating + rehab/disbondment dig reports per km (feeds the shielding-suspect prior; survey-quiet ≠ sound).

Note: websearch healthy for this track; no API fallback used. 11 sources, ~1,700 words.
