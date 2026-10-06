# TRACK 16 — Regulatory landscape for forecasting claims

Position (per GUARDRAILS): tool is inspection-report triage ranking
"newly-reported ≥10%" cells per section. No physical-corrosion,
no ≥80%-reliability claim. Absolute AP is cut- and survey-conditional;
every page prints match-rate, vanished-frac, cut-sensitivity column.
Search-API was flaky during this track (several queries returned nothing);
Russian queries listed in the task were run; per-file availability noted below.

## (a) PHMSA integrity-management rules

### 1. 49 CFR Part 192 Subpart O — Gas Transmission IM
Link: https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-D/part-192/subpart-O
Content: (1) §192.917 requires threat identification + data integration/risk
assessment from last assessment results. (2) §192.939 sets reassessment
intervals (max 7-yr base; 10/15/20-yr by stress with confirmatory DA at yr 7).
(3) §192.937/941/943: continual evaluation; extensions/waivers need analysis.
RELEVANCE: Prediction never replaces assessment; analytics may only *prioritise
segments and justify intervals*. Our wording "rank 100-m cells for next-survey
attention" fits; "predict corrosion / extend reassessment" forbidden.
Handover: present triage output as §192.917 data-integration input, not as assessment.
Verdict: USE.

### 2. PHMSA ADB-2026-06 + 2020 Risk Modeling Report (probabilistic models = best practice)
Link: https://www.federalregister.gov/documents/2026/07/13/2026-14071/pipeline-safety-guidance-for-enhancing-the-effectiveness-of-distribution-integrity-management
Content: (1) Probabilistic models (distributions, not point estimates) "considered
a best practice for supporting all decision types". (2) Overriding principle: any
risk model must "support risk management decisions to reduce risks". (3) Guidance
is non-binding; does not create enforceable duties.
RELEVANCE: Permits "probabilistic ranking to support dig/verification decisions";
forbids "model proves safety / replaces survey". Our per-section AP + lift-CI with
n_pos≥30 matches the distributions-not-point-estimates norm.
Verdict: USE.

## (b) API assessment / crack-management framing

### 3. API RP 1183 — Assessment and Management of Dents (1st Ed.)
Link: https://www.api.org/products-and-services/standards/important-standards-announcements/rp1183
Content: (1) Standard methods for dent severity + fatigue-life screening
(e.g. SSI/spectrum methods per PPIM/ASME PVP-2023 literature).
(2) "Predicting fatigue life" means screening-banded estimates with
conservative bounds, feeding reassessment prioritisation. (3) Purchase-only
standard; details via companion papers, e.g. https://asmedigitalcollection.asme.org/PVP/proceedings/PVP2023/87486/V005T06A082/1171521
RELEVANCE: "Prediction" precedent = banded screening + conservatism, never a
point claim. Our cut-sensitivity columns (≥10/12/15%) are the analogue.
Forbids headline single-number reliability.
Verdict: ADAPT (dent-fatigue → corrosion-reporting screening logic).

### 4. API RP 1176 — Assessment and Management of Cracking (+ companion guide)
Link: https://www.api.org/products-and-services/standards/important-standards-announcements/api-rp-1176
Content: (1) Framework to characterise cracks, integrate inspection + operating
data, prioritise repairs, set reassessment. (2) Companion guide:
https://www.energyinfrastructure.org/-/media/energyinfrastructure/images/pipeline/pipeline-safety/2016-252-rp1176-companion-guide-071417.pdf
(3) "Predict and prevent" = program-level threat management, not defect-level prophecy.
RELEVANCE: Permits "crack/corrosion-threat screening and dig prioritisation";
forbids per-defect initiation forecasts. Handover: map our ranked-cell list to
RP-1176-style "scheduled verification" language.
Verdict: USE.

## (c) Probabilistic assessment language

### 5. ISO 19345-1/-2 — Pipeline integrity full-life-cycle management
Link: https://www.iso.org/obp/ui/es/#!iso:std:64659:en and https://www.iso.org/obp/ui/ru/#!iso:std:64660:en
Content: (1) Integrity management across life cycle with threat/risk assessment.
(2) Quantitative assessment must state assumptions, data quality, uncertainty.
(3) Residual-life outputs feed inspection planning, not fitness-for-service verdicts.
RELEVANCE: Permits "probability of newly-reported indication conditional on
survey/methodology"; forbids unconditioned "probability of corrosion".
Our disclaimer + R2/R3 instrument-validity gates implement exactly this.
Verdict: USE.

### 6. DNV-ST-F101 — Submarine pipeline systems (safety philosophy + target probabilities)
Link: https://www.dnv.com/energy/standards-guidelines/dnv-st-f101-submarine-pipeline-systems/
Content: (1) Limit-state (LRFD) framework with calibrated target failure
probabilities per safety class. (2) "Probability" claims allowed only inside
a stated calibration: characteristic values, partial factors, inspection
effectiveness (e.g. AUT POR 85%|95% conventions). (3) Operation/abandonment
phases require re-qualification on new data.
RELEVANCE: Permits calibrated "P(newly-reported ≥10% | section, survey regime)";
forbids transferring ON/PK1 numbers to SRTO or across methodology breaks (our R3 gate).
Handover: quote operating envelope, not a portability claim.
Verdict: ADAPT (offshore limit-state → onshore triage ranking discipline).

## (d) Russian side

### 7. ФНиП «Правила безопасности для ОПО магистральных трубопроводов» (Приказ РТН №517 от 11.12.2020)
Link: https://docs.cntd.ru/document/573174913 (mirror text: https://meganorm.ru/Data2/1/4293775/4293775515.htm)
Content: (1) Technical diagnostics (техническое диагностирование) mandatory to
establish condition and safe-operation limits. (2) Repair/planning decisions rest
on diagnostics + ЭПБ conclusions, design/operations docs. (3) Analytical tools are
secondary — admissible only as planning support inside the diagnostics regime.
RELEVANCE: Permits "вспомогательный инструмент планирования ВТД/проверок";
forbids "прогноз заменяет диагностику/ЭПБ". Handover (Gazprom transgaz Tomsk):
position tool as triage for verification digs, with methodology-change log.
Verdict: USE.

### 8. ГОСТ Р 51164-98 — Steel trunk pipelines: general corrosion-protection requirements
Link: https://docs.cntd.ru/document/1200001879 (also https://base.garant.ru/12137483/)
Content: (1) Comprehensive protection (coatings + ЭХЗ) mandatory for all buried
pipe; cathodic polarisation continuous over whole length. (2) Periodic control +
complex surveys by licensed orgs; protection effectiveness judged by extent and
time; failure analysis feeds corrosion-state forecast "по НД".
(3) Protection/control docs retained for whole service life.
RELEVANCE: Only compliant-adjacent "forecast" in Russian norms is the ЭХЗ/corrosion-state
прогноз по НД after survey + failure analysis. Our tool must cite survey regime
per section; never claim cathodic-protection effectiveness.
Handover: attach per-survey threshold/methodology sheet (the missing-data request).
Verdict: USE.

### 9. ЭПБ трубопроводов — consultant подборка + практика (Ростехнадзор lens)
Link: https://www.consultant.ru/law/podborki/jekspertiza_promyshlennoj_bezopasnosti_truboprovodov/ and https://www.ruspromexpert.ru/uslugi/ekspertiza_gazoprovoda/
Content: (1) ЭПБ establishes conformity of condition + operating conditions to
ФНиП; conclusion owned by licensed expert org. (2) Forecast/ranking software is
not an ЭПБ subject — it cannot certify fitness. (3) Pages fetched OK; docs.cntd
fetch timed out once (noted per-file flakiness, content via Garant/meganorm mirrors).
RELEVANCE: Permits "материал для ЭПБ/планирования"; forbids any "экспертное
заключение о пригодности" wording. Russian handover must state tool ≠ ЭПБ.
Verdict: USE.

## (e) ECA acceptance as precedent for model-assisted decisions

### 10. ECA in codes (BS 7910 / API 579-1/ASME FFS-1 via TWI route)
Link: https://theweldinginstitute.com/event-4767804
Content: (1) Fracture-mechanics ECA derives flaw acceptance criteria from
material, stress, NDT capability. (2) Accepted because inputs, NDT POD, and
safety factors are explicit and auditable. (3) Outcome is accept/monitor/repair
bands, not "will/won't fail" dates.
RELEVANCE: Precedent permitting our ranked-list + audit-column format ("verify
first / routine") while forbidding per-cell failure-date claims.
Matches quarantine discipline (E03 HGB stays comparator until controls pass).
Verdict: ADAPT.

## (f) Honest vendor/analyst wording examples

### 11. Probabilistic ILI-based integrity literature (OGJ + SPE)
Links: https://www.ogj.com/pipelines-transportation/pipelines/article/17240376/pipeline-inspection1-reliability-based-method-assesses-corroding-pipelines and https://jpt.spe.org/pipeline-integrity-assessment-using-probabilistic-transformation-method-and-corrosion-growth-modelin
Content: (1) Reliability-based assessment reports per-defect failure probability
with ILI sizing uncertainty + corrosion-growth distributions. (2) Outputs quoted
with POD/PFA and tool tolerance, methodology-conditional. (3) Growth rates
inferred only where repeat high-quality ILI exists.
RELEVANCE: Template for compliant claims: "AP 0.64 newly-reported ≥10% @100 m,
ON section, 2015→2021 survey pair; match-rate X, vanished-frac Y" — never "64%
of corrosion predicted". Vendor-style point-accuracy without conditioning = REJECT.
Verdict: USE (wording template).

## Claim-wording rule for our triage tool
Allowed: "ranks 100-m cells by P(newly-reported ≥10%) for section S under stated
survey pair; supports verification prioritisation alongside diagnostics/ЭПБ."
Forbidden: "predicts corrosion / initiation / growth", "≥80% reliable",
"extends reassessment", "certifies fitness", any pooled ON+SRTO number,
any E14-derived number. Russian handover adds: инструмент планирования, не ЭПБ.
