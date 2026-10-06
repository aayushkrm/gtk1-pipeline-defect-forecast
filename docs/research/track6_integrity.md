# TRACK 6 — Pipeline integrity assessment + repair-decision practice

Scope: engineering grounding for GTK1 triage thresholds — B1 100 m ranking,
KBD<0.9 pipe flags, repair recommendations, per-section thresholds.
See `docs/PROBLEM.md`, `docs/TRIAGE_SPEC.md`, `docs/DATA.md`.
We do NOT compute fitness-for-service: no failure-pressure claims, only
prioritization. Integrity methods below are the operator-side consumers of our
ranked segment lists and the precedent for our flag semantics.

Search note: websearch returned HTTP 400 on 2026-10-06, so verification used
OpenAlex API + webfetch (DOIs/years/authors confirmed there); standards and
industry pages cited by URL as fetched or snippet-verified.

## (a) ASME B31G / modified B31G / RSTRENG effective-area method

**[1] Pikas, J. "Evaluation of Metal Loss Corrosion with RSTRENG."
Technical Toolboxes + Advantica-for-PHMSA validation (2008 meeting
presentation, primis-meetings.phmsa.dot.gov).**
Content: Original B31G (Level 1, Battelle NG-18, parabolic area) is deliberately
conservative single-pit screening; modified B31G adds flow stress (SMYS+10 ksi)
and 0.85-area Folias factor; RSTRENG effective-area ("river-bottom") profiles
multi-pit clusters and was validated on 200+ burst tests.
Advantica stats (predicted/actual): B31G 1.35±0.48, modB31G 1.19±0.29,
RSTRENG 1.19±0.17 — RSTRENG least scatter, all conservative on mean.
RELEVANCE: Vendor tail cols (Danger/KBD/Pf) are almost certainly Level-1-class
output — hence conservative and threshold-sensitive; our KBD<0.9 flag inherits
that conservatism. Justifies an independent ERF spot-check (vb64 lib, track3 §8)
on watchlist top-K rather than trusting vendor Pf.
Verdict: **ADAPT** — screening-vs-Level-2 distinction + validation stats as cover for flag wording; never recompute Pf ourselves.

**[2] Li, H. et al. (2022). "Residual Strength Assessment and Residual Life
Prediction of Corroded Pipelines: A Decade Review." *Energies* 15(3):726.
DOI: 10.3390/en15030726 (~27 cites, OpenAlex-verified).**
Content: Decade review spanning B31G, modB31G, RSTRENG 0.85-area, DNV-RP-F101,
PCORRC, plus FEA/ANN burst models; depth is the dominant burst-pressure
parameter; analytical codes are systematically conservative vs FEA on complex
(non-idealized) defects.
RELEVANCE: Confirms depth-driven assessment — supports our Depth≥10% operating
cut as the physically literate threshold, with ≥12%/≥15% sensitivity legs
mirroring code conservatism gradients. Gives the triage report a one-line
"why depth" justification.
Verdict: **USE** — cite as methods-landscape reference in report appendix.

**[3] ROSEN USA. "Assessments That Work for You" — Plausible Profiles (P2)
fitness-for-purpose method (rosen-group.com case study; Kariyawasam et al.
2019 Psqr report; Kiefner peer review).**
Content: Detailed RSTRENG takes one deepest-to-deepest river-bottom profile
(over-conservative on circumferentially elongated clusters); P2 generates
hundreds of plausible profiles from ILI box data + tool tolerance and takes
the 5th percentile burst pressure at a target date. Case study: 13 clusters
with pre-2025 repair dates all extended, some 3+ years.
RELEVANCE: Shows deterministic flags over-call on clusters — our segment rank
should up-weight clustered/anomaly-count features (P2 count model) exactly
where single-defect KBD flags are noisiest. Also models how to report
uncertainty bands honestly on the heatmap.
Verdict: **ADAPT** — cluster-aware reasoning + percentile reporting pattern; P2 itself out of scope.

## (b) DNV-RP-F101 capacity equations + failure probability

**[4] Bjørnøy, O.H. et al. (1999). "Introduction and background to DNV
RP-F101 Corroded Pipelines." OMAE (DNV/BG/Shell authors, OpenAlex-verified);
capacity equation §8.2 per pipenostics `dnvpf` docs (omega1x.github.io;
Timashev & Bushinskaya 2016 allow UTS↔SMTS).**
Content: RP gives single-defect capacity from geometry (D, t, defect
length × depth) with a bulging factor Q = √(1+0.31·(l/√(Dt))²),
characterized by SMTS (not SMYS) — i.e. a less conservative, UTS-anchored
alternative to B31G; valid only for isolated corrosion under internal pressure.
RELEVANCE: If a partner ever asks "why not DNV?", the answer is ready:
single-defect scope + needs SMTS-grade data our pipes table only partly has —
while B1 ranking stays method-agnostic. UTS↔SMTS interchange note matters when
auditing vendor Pf provenance.
Verdict: **ADAPT** — reference equation for ERF cross-checks; **REJECT** as triage input.

**[5] Bao, J. & Zhou, W. (2021). "Influence of depth thresholds and
interaction rules on the burst capacity evaluation of naturally corroded
pipelines." *J. Pipeline Sci. Eng.* DOI: 10.1016/j.jpse.2021.01.001
(~25 cites, OpenAlex-verified).**
Content: On real (non-machined) corrosion: interaction rules deciding
whether adjacent pits act as one defect move burst capacity as much as the
capacity model choice; shallow-depth screening thresholds change which
defects even enter the assessment.
RELEVANCE: Direct precedent for our cut-sensitivity triple (≥10/12/15%):
the reporting threshold IS an assessment parameter, not a neutral filter.
Also warns that our ±2 m/0.5 m/1 h match rule merges/splits clusters the way
interaction rules do — flag cluster-membership uncertainty in audit columns.
Verdict: **USE** — cite for cut-sensitivity + match/interaction uncertainty rationale.

## (c) ASME B31.8S integrity management + threat taxonomy

**[6] ASME B31.8S-2004 "Managing System Integrity of Gas Pipelines"
(public copy law.resource.org); threat table per EIGA DOC235 §7.**
Content: Three threat groups — time-dependent (external/internal corrosion,
SCC; addressable by any of ILI/pressure-test/DA/ECDA), stable/resident
(manufacturing, construction, equipment — pressure-test-centric), and
time-independent (third-party, incorrect operations, weather/outside force).
Stale-data rule: old data stays valid for stable threats but NOT for
time-dependent ones like corrosion.
RELEVANCE: Our corrosion-only P1/P2 scope = time-dependent-threat lane, which
is exactly why the protocol demands recent-survey features and future hold-out
(2016 data cannot assess 2025 corrosion). Stable/third-party threats are out of
scope — say so in GUARDRAILS, since VTD tables mix features (e.g. GWAN arcs).
Verdict: **USE** — taxonomy + stale-data rule as scope/disclaimer backbone.

**[7] INGAA / P-PIC "Anomaly Evaluation, Response, and Repair Summit"
(ingaa.org): industry practice on B31.8S Figure 4 + Table 3 scheduling.**
Content: Operators convert ILI anomalies to failure-pressure ratio
FPR = Pf/predicted-failure ÷ operating pressure via B31G/modB31G (some RSTRENG),
then schedule by B31.8S Figure 4: FPR ≤ 1.1 → immediate; any defect >80% deep
with FPR > 1.1 → near-term leak response; remainder scheduled/monitored with
corrosion-rate-adjusted dates.
RELEVANCE: This is the operator workflow our triage feeds: ranked 100 m
segments → dig shortlist → FPR-dated response. Our repair recommendations must
mirror its language (immediate/near-term/scheduled/monitor, never pass/fail)
and our KBD<0.9 + class-a/b flags positioned as pre-FPR screening, not verdicts.
Verdict: **USE** — adopt response-category vocabulary for recommendation tiers.

## (d) RBI and dig/repair programs

**[8] DNV "What is Risk-Based Inspection (RBI)?" (dnv.com; API RP 580/581
lineage, 1994→2016 3rd ed.); field implementation: ROSEN NIMA RBI case study
(Central Asia, 2021; rosen-group.com).**
Content: Risk = PoF × CoF; inspection does NOT reduce risk, it buys damage
knowledge that lets mitigation act; dates/effectiveness set by projecting the
risk curve to a maximum-tolerable line ("evergreening", revalidated 3–5 y or
when degradation beats prediction ~20%); NIMA shows the PoF/CoF-per-damage-
mechanism + risk-matrix machinery running on real asset data.
RELEVANCE: Formal cover for the whole triage posture: B1 score is a PoF-side
ranking input to a dig program, never a risk verdict (no CoF side modeled).
Evergreening logic justifies per-section recalibration controls and the
"re-rank after each survey" operating rule in TRIAGE_SPEC.
Verdict: **USE** — PoF-side framing + evergreening cadence for ops section.

**[9] Tkalec, D. (2024). "Risk-Based Assessment for Pipeline Corrosion:
A Practical Guide." Cenosco IMS PLSS (cenosco.com).**
Content: Worked pipeline-corrosion RBI arithmetic: Remaining Life =
Remaining Corrosion Tolerance ÷ Future Corrosion Rate, with RCT from nominal
wall − MAOP-derived limiting state − wall loss (defect-free) or ILI-reported
tolerance minus elapsed loss; Next Inspection = Last + RL × Interval Factor,
IF from confidence × criticality matrices; three strategies (design-intent /
extended-life / fit-for-purpose).
RELEVANCE: Closest public template for turning our segment outputs into dated
survey recommendations: P2 counts ≈ tolerance-consumption signal, B1 score ≈
susceptibility side of criticality. IF-table thinking (confidence × criticality)
supports per-section thresholds (ON vs SRTO vs PK1 get different factors).
Verdict: **ADAPT** — RL/IF formulas as recommendation-date scaffolding, fed by P1/P2, not by invented rates.

## (e) Safety factors / allowable pressures (Pd/MAOP/Psw/Pf semantics)

**[10] Burst/MAOP semantics: Barlow P = 2·S·t/D instrument (e.g.
eureka.patsnap.com burst-pressure explainer); PHMSA/FPR practice per [7];
repo tail columns Danger/KBD/Pd/MAOP/Psw/Pf (docs/DATA.md).**
Content: Standard chain: Pf (burst/failure pressure from a capacity model) →
allowable/safe pressure = Pf ÷ safety factor (ERF/FPR form) → MAOP must sit
below it (Barlow with allowable stress for the intact-pipe anchor); KBD reads
as the vendor's strength-margin factor in the same family (flag at KBD<0.9 ≈
margin consumed toward the FPR ≤ 1.1 immediate band, exact mapping unverified).
RELEVANCE: Lets us document Pd/MAOP/Psw/Pf column semantics and the KBD<0.9
convention honestly: working interpretation, pending partner confirmation
(TRIAGE_SPEC blocker logic). Independent ERF check via vb64
`pipeline.integrity` B31G calculator (track3 §8, MIT) validates vendor Pf on
top-K before any recommendation leans on it.
Verdict: **ADAPT** — semantics table + unverified-mapping caveat in report; **REJECT** any re-derivation of MAOP.

## (f) Reliability-based corrosion management 2022–2026

**[11] Stephens, M., Nessim, M. & van Roodselaar, A. (2010). "Reliability-Based
Corrosion Management…" IPC2010 (cfertech.com) — industry process foundation.**
Content: Combines failure-prediction models + ILI data + pipe characteristics
+ growth projections in a probabilistic frame to get failure probability vs
time; quantifies benefit of selective/staged remediation and picks the
cost-optimal feature count + time-to-next-inspection.
RELEVANCE: The end-state our triage plugs into: today's ranked segments become
tomorrow's staged-dig optimization once growth data exists. Cite to show the
December deliverable is step one of an accepted industry path, not ad hoc ML.
Verdict: **USE** — roadmap positioning; full probabilistic frame out of scope.

**[12] Recent reliability front (all OpenAlex-verified): Kere, K. et al.
(2025). Probabilistic interaction rule + burst model for corrosion colonies,
*J. Pipeline Syst. Eng.* DOI: 10.1061/jpsea2.pseng-1714; Li, A. et al. (2024).
Reliability assessment with detection cycles, *Energies* 17:3366.
DOI: 10.3390/en17143366; Meneses-Gelves, J. et al. (2026). Spatial
variability via random fields, *Reliab. Eng. Syst. Saf.*
DOI: 10.1016/j.ress.2026.112519.**
Content: Colony interaction treated probabilistically (not deterministic
spacing rules); detection/inspection cycles modeled explicitly inside
reliability (imperfect, thresholded ILI like ours); spatial random fields
capture along-line correlation of degradation — the segment, not the pit, as
modeling unit.
RELEVANCE: Three direct upgrades-in-waiting for GTK1: (i) probabilistic
interaction justifies soft cluster features over hard defect merging;
(ii) detection-cycle modeling is the reliability-grade version of our campaign
covariate; (iii) random-field correlation is the formal basis for 100 m/1 km
segment risk (neighbors inform each other) and per-section thresholds.
Verdict: **ADAPT** — design pointers for phase 2 (spatial segment model + campaign-aware reliability); **REJECT** for December scope.

## Takeaways for GTK1

1. Triage outputs are PoF-side screening ([8]) feeding the Figure-4 dig workflow
   ([7]): rank + uncertainty + audit columns, recommendation tiers in
   immediate/near-term/scheduled language — no pass/fail badges, no MAOP claims.
2. KBD<0.9 stays a conservative Level-1-family flag ([1]); cross-check top-K
   with independent ERF ([10]/track3) and document the unverified KBD↔FPR
   mapping next to the flag, per-section.
3. Cut-sensitivity triple (≥10/12/15%) is assessment practice, not hedging
   ([5]); per-section Interval-Factor-style thresholds ([9]) handle the
   ON/PK1/SRTO prevalence spread honestly.
4. Corrosion is a time-dependent threat: only recent surveys assess it ([6]);
   matched-Δdepth stays secondary while P1/P2 segment statistics carry the
   program — with the [11]–[12] reliability path as the documented next step.
