# Track 13 — weld-anomaly assessment (girth / longitudinal / spiral)

Context: ON-2025 has 1506 GWAN rows; PK1-2025 is 50% GWAN (edge-offset ×10057 campaign artefact?);
PK2-2025 is 78% GWAN. PK1 pipe is D1020 **spiral** (SWAN/SWCR live there). Tracks 1–12 cover growth,
matching, ILI physics, B31G, failures — this track covers weld-flaw acceptance only.
Tooling: websearch OK this track; paywalled standards (API 1104/BS 7910 full text) via TWI/PRCI summaries.

## (a) Girth-weld defect types in ILI + workmanship acceptance

**S1. MDPI Sensors 2017 review — girth-weld defect ILI (MFL/UT/EMAT/RFEC).**
https://mdpi-res.com/d_attachment/sensors/sensors-17-00050/article_deploy/sensors-17-00050-v2.pdf
Content: Taxonomy planar (incomplete penetration, lack of fusion, crack, undercut) vs volumetric
(porosity, slag) vs irregular (misalignment/hi-lo, bad profile). Domestic/foreign GW cracking accidents
are "mostly crack, incomplete penetration, lack of fusion, sharp undercut". Compares 3-axis MFL,
liquid UT crack tool, EMAT, RFEC signal ID + sizing per technology.
RELEVANCE: Gives our GWAN/LWAN class prior — planar sharp flaws drive rupture, volumetric flaws
mostly do not. Justifies splitting weld-proximity features into sharp-vs-blunt when desc text allows.
Verdict: USE (defect taxonomy + tool-selection table).

**S2. ASCE 2020 — MFL4 girth-weld pull-through + dig validation.**
https://ascelibrary.org/doi/10.1061/%28ASCE%29PS.1949-1204.0000497
Content: MFL4 "generally sensitive to lack of fusion/penetration, deep undercut, local thinning";
NOT sensitive to closed/narrow cracks (<1 mm wide, <2 mm deep). Pull-test + field excavations on
operating lines; detection + int/ext ID + sizing quantified.
RELEVANCE: Our ILI is MFL-family: expect GWAN rows to over-represent LOF/penetration/undercut and
under-report tight cracks. Never treat "no GWAN" as "no crack"; flag vendor/tool per survey (links track 4/5 POD logic).
Verdict: USE (MFL-on-weld POD asymmetry numbers).

**S3. NIST NBSIR 83-1695 — fitness-for-service criteria, TAPS girth welds (public domain).**
https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nbsir83-1695.pdf
Content: Found radiography oversensitive to blunt flaws (porosity/slag/arc burns) yet blind to sharp
planar flaws; blunt flaws "do not decrease weldment strength/fatigue life" in low-cycle tests at −2 °C.
Pushed UT/EMAT sizing for sharp-flaw depth since X-ray densitometry could not size LOF/cracks.
RELEVANCE: Direct precedent for down-weighting volumetric GWAN descriptions vs planar ones in labels;
supports requesting NDE method (RT vs UT) per survey for the threshold covariate file.
Verdict: USE (blunt-vs-sharp evidence base).

## (b) ECA vs workmanship (API 1104 App A / BS 7910 / CSA Z662 K)

**S4. TWI 2009 — API 1104 App A (2007) vs BS 7910 Level 2, full-scale tests.**
https://www.twi-global.com/technical-knowledge/published-papers/comparison-of-api-1104-appendix-a-and-bs-7910-procedures-for-the-assessment-of-girth-weld-flaws-october-2009
Content: Option 1 = graphical (CTOD ≥0.25 / 0.10 mm curves); Option 2 = FAD like BS 7910 L2A;
38 full-scale/wide-plate tests both predict failure with wide scatter, near-identical. API ignores
hi-lo misalignment → non-conservative above ~0.2% strain / 90% yield at 1.5 mm misalignment; BS 7910
handles misalignment + residual stress + Lüders strain explicitly.
RELEVANCE: Our lines see ground-movement strain (cf. track 12): any ECA-style severity proxy must
penalise misalignment-tagged GWAN rows; API-1104-style tables alone are unsafe where hi-lo is reported.
Verdict: USE (core ECA reference; prefer BS 7910 route where misalignment present).

**S5. TWI — ECAs: lifting the lid of the black box (API 1104 A / CSA K / EPRG / DNV).**
https://www.twi-global.com/technical-knowledge/published-papers/ecas-lifting-the-lid-of-the-black-box/
Content: Workmanship limits (API 1104, BS 4515, CSA Z662 Cl.7) = "what a good welder achieves", NOT
fitness-for-service. Compares API 1104-A Opt 1/2, CSA Z662-K, EPRG Tier 1/2/3, DNV-OS-F101: Opt-1/EPRG-Tier-2
usable only if all preconditions met (no fatigue loading); else full BS 7910/API 579. Practical rule:
use Tier 2 / App-A-Opt-1 when eligible, full ECA otherwise.
RELEVANCE: Labels must carry two severities — workmanship-fail (cheap, from desc text) vs ECA-fail
(needs depth/length/CTOD we lack → mark unknown, never impute). Prevents over-claiming GWAN danger.
Verdict: USE (workmanship-vs-ECA separation rule).

**S6. E2G 2025 — CSA Z662 Annex J/K defect assessments explainer.**
https://e2g.com/industry-insights-ar/pipeline-defect-assessments-for-csa-z662-pipelines/
Content: Annex J = ECAs for crack-like flaws in circumferential welds; Annex K Opt 1 (COD curve +
Miller collapse) vs Opt 2 (FAD = API 579 curve, CTOD preferred). Scope: surface-breaking circumferential
flaws ONLY; no residual-stress term; fatigue screened by depth caps (50% gas / 25% liquids).
RELEVANCE: Our GWAN rows fit Annex-K scope (circumferential) but LWAN/SWAN do not — route
longitudinal/spiral flaws to API 579/BS 7910 logic, never Annex K. Depth-cap rule gives a monitor-vs-dig
cut usable with our depth% field.
Verdict: ADAPT (scope gate: GWAN→K-model, LWAN/SWAN→other).

## (c) Spiral-weld specifics (PK1 D1020)

**S7. KOC/TDW 2023 — skelp-end weld cracks in spiral pipe, MDS-ILI trial (PTC).**
https://www.pipeline-conference.com/abstracts/detection-skelp-end-weld-features-spirally-welded-pipe-using-magnetic-ili-technology
Content: 24-in spiral gas lines: cracks along diagonal skelp-end welds (SEW, neither longitudinal nor
circumferential, 1 per 5–7 joints); RT confirmed, joints cut out. TDW multiple-dataset tool run 2023
found SEW features, dig-verified.
RELEVANCE: PK1 spiral pipe likely contains SEWs our tables never name — SWAN rows near unlisted diagonal
features risk mis-assignment to nearest girth weld. Feature: distance-to-nearest-*listed*-weld PLUS
spiral-phase residual (odometer mod helix pitch) to catch SEW-periodic anomalies.
Verdict: USE (SEW threat model for PK1).

**S8. Sonatest — UT of seam/helical butt welds (curved-surface correction).**
https://sonatest.com/blog/ultrasonic-inspection-pipeline-seam-and-helical-butt-welds
Content: Helical welds defeat flat-plate UT: ID curvature refracts each PAUT beam differently → wrong
plotting + lost sensitivity; fix is curved-surface-corrected S-scans; TOFD for through-wall height for
fracture mechanics. RT sees type+length, not height.
RELEVANCE: Explains SWAN sizing noise on PK1 (curvature artefact, not growth) — widen match tolerance
along helix direction and distrust SWAN depth deltas below tool repeatability; request AUT-vs-RT method flag.
Verdict: USE (spiral sizing-uncertainty mechanism).

**S9. Eddyfi — spiral-pipe MFL + PAUT combo; ±100 mm weld dead zone.**
https://blog.eddyfi.com/en/how-to-inspect-spiral-welded-pipelines-better
Content: Pipescan-HD MFL screens at ~1 m/s to 30% wall-loss threshold, LYNCS-CM PAUT sizes; ~100 mm each
side of spiral weld unscannable by either → manual 7.5 MHz/64-el PAUT. MFL = volume, not depth.
RELEVANCE: Gives a concrete weld-proximity band: anomalies within ~0.1 m of a spiral seam live in the
dead zone → tag `near_weld_deadzone` and suppress growth claims there; MFL-depth ≠ PAUT-depth across surveys.
Verdict: ADAPT (100 mm band + manual-PAUT follow-up rule transposed to our dig list).

## (d) Operator disposition (excavate vs monitor; corrosion-at-weld)

**S10. Baker Hughes — ILI-based girth-weld threat assessment (MagneScan + caliper + IMU).**
https://dam.bakerhughes.com/asset/c241e50a-3180-4a22-ba97-196af07164ee/PPS-ILI-based-girth-weld-assess-integrity-services-fact-sheet-25005.pdf
Content: Prioritises by COINCIDENCE, not single flags: weld crack/anomaly + wall transition/tie-in +
dent/wrinkle/ovality at weld + circumferential corrosion growth + IMU/AXISS bending strain. Strain demand
vs capacity framing; single indicators rarely actionable alone.
RELEVANCE: Blueprint for our triage score: GWAN row severity = base class × coincidence multipliers
(IMU strain, dent-at-weld, corrosion-at-weld growth). Single GWAN with no covariates → monitor, not dig.
Verdict: USE (coincident-indicator triage = our weld-risk feature spec).

**S11. PHMSA 49 CFR §§192.712/714/933 — crack + weld response criteria (law).**
https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-D/part-192/subpart-M/section-192.712
Content: Crack depth+ML >50% WT or >tool max = immediate; FPR<1.1 immediate, <1.39/1.50 one-year by class;
dent >2% diameter affecting girth/longitudinal/spiral curvature = 1-yr unless ECA clears; in-situ PAUT/IWEX
required on crack digs; conservative toughness defaults (4 ft-lb weld LOF) when records missing.
RELEVANCE: Ready-made dig-vs-monitor thresholds mappable to our fields (depth%, ERF/FPR, dent-groove at
weld). Adopt FPR + 50%-depth rules as label tiers; cite for the December triage page.
Verdict: USE (regulatory response table).

**S12. PRCI PR328-163605 (2019) — seam-anomaly management with ILI+NDE+lab.**
https://exa.ai/library/publication/d9gxpnknkvl
Content: ILI cannot discriminate seam crack vs hook crack vs notch-LOF vs inclusion → operators must
assume crack + most conservative assessment → excess digs of benign features. Builds a staged process
(ILI → NDE sizing → lab-calibrated re-class) to cut unnecessary excavations on gas + liquid lines.
RELEVANCE: Authorises our "assume-crack pending NDE" labelling for LWAN/SWAN linear indications, with an
explicit downgrade path on dig feedback — and warns our GWAN counts overstate crack prevalence.
Verdict: USE (assume-crack-then-downgrade protocol).

## (e) Failure cases + weld-proximity POD

**S13. NTSB PIR-22/01 Enbridge Hillsboro (2020) + PHMSA Gulf South 2023 — missed-weld ruptures.**
https://www.ntsb.gov/investigations/AccidentReports/Reports/PIR2201.pdf ;
https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/2024-06/20230212-Gulf-South-Jackson-MS-Final2-May-2024.pdf
Content: Hillsboro: 30-in girth weld with 7-in × 0.13-in IP/LOF defects failed at 1.3–2% strain capacity
under landslide loading operator under-predicted 3×. Gulf South: 26-in IP zone at 48% WT failed under
0.2% bending strain; 2017 + 2021 ILI (incl. circumferential MFL-A) reported ZERO girth anomalies.
RELEVANCE: Two field proofs that (i) long shallow weld flaws + modest ground strain = rupture, and
(ii) ILI weld POD is far from 1 — our model must include an IMU-strain × weld-flaw interaction term and
a survey-specific weld-POD prior, never raw GWAN counts as hazard rates.
Verdict: USE (case-law anchors for strain×flaw term + POD<1).

## (f) 2022–2026 advances (AUT/PAUT + ML on radiography — links to our X-ray images)

**S14. JAI 2024 — YOLOv8 on real AUT B-scans: LOF F1 0.814 (359 images, J-bevel).**
https://www.mdpi.com/2813-477X/2/2/7
Content: First SOTA benchmark on industrial (not lab) girth-weld AUT B-scans; zone-discrimination
(cap/body/root) strip charts; YOLOv8n beats DETR variants without augmentation; confidence-threshold
sweep reported for precision/recall trade.
RELEVANCE: Direct pipeline from our X-ray image archive: same LOF target, same zone logic. Reuse their
threshold-sweep + zone-stratified eval protocol; YOLOv8n as baseline before custom work.
Verdict: ADAPT (eval protocol + baseline; retrain on our images, no weight import).

**S15. Heliyon 2024 (ResNet50: RIAWELC 98.75%, GDXray 90.3%, field archive 75.8%) + Sensors 2023
(6-class X-ray CNN 92%, 4479 images: cavity/crack/slag/LOF/shape/normal).**
https://www.cell.com/heliyon/fulltext/S2405-8440(24)06621-0 ;
https://www.mdpi.com/1424-8220/23/14/6422
Content: RIAWELC public set (24,407 images: crack/pore/LOP/no-defect) + transfer learning generalises to
GDXray but drops to 75.8% on low-contrast field scans; augmentation (rotate/shear/zoom/brightness/flip)
recovers much of it. Six-class CNN covers exactly our GWAN vocabulary gap (LOF vs slag vs shape).
RELEVANCE: Our X-ray images ARE the low-quality third dataset — expect ~75% out-of-box, plan
augmentation + zone-crop pipeline; adopt their 4/6-class label schema for image→table joins.
Verdict: ADAPT (RIAWELC/GDXray pretrain → fine-tune on ours; label schema USE).

## Implications for our labels/features (weld-proximity design)

1. Two-tier label: `workmanship_fail` (text-derived, cheap) vs `eca_concern` (needs depth+length+strain;
   unknown by default). Never promote GWAN counts to hazard rates (S5, S12, S13).
2. Weld-proximity features: `d_girth` (m), `d_seam_helix` (m, PK1), `in_deadzone_0.1m` (S9),
   `hi_lo_reported` (misalignment penalty, S4), `coincidence_count` (dent/oval/ML/strain at same weld, S10),
   `strain_x_flaw` (IMU bending × flaw length, S13), `sew_phase_residual` (S7).
3. Survey covariate: NDE method (RT vs UT/AUT vs MFL-only) + per-survey weld POD prior (S2: LOF seen,
   tight cracks missed; S13: POD<1 proven). Growth credible only on matched pairs above both surveys'
   POD90 (cf. track 5). Spiral SWAN depths get ×wider tolerance (S8).
4. Dig rule starter (triage page): immediate = crack depth+ML>50% WT or FPR<1.1; 1-yr = dent>2% at
   girth/spiral or FPR<1.39/1.5; else monitor + PAUT/IWEX on dig (S11). Linear seam indications assumed
   cracks pending NDE (S12).
5. X-ray ML path: RIAWELC/GDXray pretrain → fine-tune on our scans with augmentation; YOLOv8n baseline
   F1≈0.8 target on LOF; zone-stratified eval (S14, S15). No December-scope change.

Word count: ~1450. No git commits.
