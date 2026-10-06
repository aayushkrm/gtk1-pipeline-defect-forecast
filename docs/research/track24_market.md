# Track 24 — commercial landscape of pipeline-AI products 2023–2026

Tooling disclosure: DIRECT Exa (curl, api.exa.ai) served vendor-offering discovery (ROSEN, Baker Hughes, NDT Global, CorrosionRADAR, Transneft-Diaskan, Irth/OneBridge); routed websearch served funding/claim verification (Cenosco Summit round, CorrosionRADAR $14M, Senslytics SBIR, RU digital programs, PODS); webfetch verified NDT Global assessments page, Senslytics SBIR release, Irth acquisition release. One webfetch failed (in-power.ru Transneft-Diaskan AI note — transport error; covered via Exa result + alternate RU press below, marked). OpenAlex/arXiv not needed (commercial track). No commits.
Scope guard: tracks 10 (deployment UX) and 20 (vendor tool specs) already cover ILI physics and triage design; this track covers only packaging, pricing, procurement, and claim language. No per-tool sizing specs repeated.

## (a) ILI vendors' analytics product tiers (public packaging, no prices disclosed)

### 1. ROSEN — tool + analytics + software tiers (Integrity Analytics / IDW, CGA, NIMA, NIPA/R3)
Link: https://www.rosen-group.com/en/technology-and-innovation/research-and-development/r-and-d-capabilities/integrity-analytics · https://www.rosen-group.com/en/expertise/product-and-service-finder/nima · https://www.rosen-group.com/en/expertise/product-and-service-finder/r3-service
Content: ROSEN packages (i) Integrity Analytics screening built on the Integrity Data Warehouse (IDW, decades of ILI runs): external-corrosion prediction for uninspected/unpiggable lines; (ii) Corrosion Growth Assessment consultancy (engineer-led rate credibility review); (iii) NIMA IM software (asset integrity management platform); (iv) service bundles R3 and NIPA (non-intrusive, LSM + CP + GIS + AI-augmented analytics, e.g. 3-yr Amber Grid award Aug 2026). No public price list; enterprise consultative sale.
RELEVANCE: Closest template for December packaging: screening service + engineer review + software, sold as decision support, never as autonomous verdict. Demo script can mirror "screen → targeted study → dig" narrative.
Verdict: ADAPT (tier ladder: triage list = screening tier; analyst pages = assessment tier).

### 2. NDT Global — assessment menu + software via Dynamic Risk
Link: https://www.ndt-global.com/integrity-assessments/ (webfetch-verified) · https://www.ndt-global.com/integrity-management/
Content: Menu pricing-by-scope: Immediate Integrity Assessment (post-report triage), Feature Growth Assessment ("signal-on-signal… most realistic predictions"), Cracks-in-Dents Diagnosis ("industry leading PODd"), FEA, Fitness-for-Purpose, Pipeline Movement, Dent Strain. Software layer via Dynamic Risk (sister company) risk-management platform. Engineers dual-hatted as "certified data analysts."
RELEVANCE: Validates per-threat assessment menu as the industry packaging unit — our watchlist maps to their "Immediate Assessment" tier. Shows how vendors bundle human expertise with analytics to stay credible.
Verdict: ADAPT (menu structure; REJECT "most realistic / industry leading" adjectives as evidence).

### 3. Baker Hughes Cordant APM — modular SaaS, Azure Marketplace, "start small then expand"
Link: https://www.bakerhughes.com/cordant/applications/asset-performance-management (Exa-found) · https://marketplace.microsoft.com/en-us/product/saas/bakerhughesbentlynevadallc1724949197512.bh_cordant_apm_public (listing from $1.00/1-yr entry) · https://antea.tech/company-news/baker-hughes-integrates-antea-mechanical-integrity-into-cordant/ (Antea MI integration, Nov 2025)
Content: Cordant APM = Asset Health + Strategy + Defect Elimination modules on Azure (AI Foundry/Databricks), sold "start with a priority asset set, establish risk/cost baseline, then expand." Antea MI (36-yr RBI know-how, 200+ asset models) folds in Q1 2026. Public proof point framed as risk-avoidance: ENMAX "avoided $13M operational risk; 89% of recommendations accepted" (2026 solution brief).
RELEVANCE: Playbook for Gazprom handover: pilot on one section (GTK1), baseline precision@K, expand per-section. Marketplace listing shows even giants use land-and-expand SaaS, not big-bang licenses.
Verdict: ADAPT (pilot framing + module split; treat $13M/89% as vendor-reported, not transferable).

### 4. OneBridge CIM → Irth AIP — SaaS integrity suite acquired by Blackstone-backed Irth
Link: https://irthsolutions.com/blog/irth-solutions-acquires-onebridge-solutions-inc.-an-industry-leading-saas-company-for-pipeline-integrity-management (webfetch-verified, Nov 2024 close) · https://marketplace.microsoft.com/en-us/product/saas/onebridgesolutions.asset-integrity-for-pipelines (AIP listing)
Content: CIM (ingestion/alignment, compliance analysis, dig management, vendor portal, corrosion/crack/risk/geohazard modules; 180k miles, 500+ users per 2022 deck) becomes Irth "Asset Integrity for Pipelines," bundled with Irth geospatial + 811 damage-prevention platform. Acquirer rationale: "unified platform… extending asset lifespan." No public per-mile pricing; 100% SaaS recurring, SOC 2 Type 2, Microsoft co-sell.
RELEVANCE: Direct comp for our December narrative: ingest → align → rank → dig-manage is the expected module order; acquirers pay for installed operator data integrations, not algorithms. Confidentiality boundary lesson: CIM never publishes customer raw ILI — only aggregates (1,074 runs / 23k digs repair-fraction study).
Verdict: USE (module order + acquisition logic; REJECT any implied valuation of our code — value is in integration + audit trail).

## (b) Startup landscape 2024–2026

### 5. Cenosco — Shell-born IMS, Summit growth equity Mar 2025
Link: https://cenosco.com/insights/cenosco-growth-investment-led-by-summit-partners (Mar 2025) · https://uk.finance.yahoo.com/news/cenosco-acquires-shell-integrity-management-130000461.html (Jan 2024 Shell IMS IP acquisition)
Content: Acquired full Shell IMS IP (20-yr co-development), then Summit Partners + Fortino growth round; 11,000+ users, 200+ assets, 40+ countries; claims "up to 20% inspection-cost reduction, 15% less downtime" (customer-reported). RBI + probabilistic modeling, refinery-first, pipeline module is GIS/ILI bookkeeping.
RELEVANCE: Model for university→operator handover: IP assignment + long co-development history is what makes enterprise buyers trust the tool. Our December package should document provenance the same way (whose data, whose labels, whose sign-off).
Verdict: ADAPT (IP-story + "customer-reported" labeling convention).

### 6. CorrosionRADAR (Cambridge) — $14M total, Aramco/Dow strategic money
Link: https://corrosionradar.com/resources/news/corrosionradar-secures-new-investment-for-growth-from-aramco-ventures-dow-kanoo-ventures-and-mercia-ventures-bringing-total-funding-to-14-million (Jul 2024)
Content: Predictive CUI monitoring (sensors + analytics); £5M Series B led by Aramco Ventures/Dow/Kanoo, total $14M; customers named as Dow and Aramco pilots. Sells hardware + monitoring subscription, not pure software.
RELEVANCE: Shows strategic-corporate VC (operator as investor-customer) is the viable path for niche corrosion tech — relevant if Gazprom entities later fund continuation. Note: sensor company, not ILI analytics; do not compare accuracy.
Verdict: USE (funding-route precedent only).

### 7. Senslytics (Oklahoma) — DOT SBIR Phase I + $500k OCAST, "causal AI, no big data needed"
Link: https://senslytics.com/senslytics-awarded-phase-1-sbir-grant-from-dot-to-develop-an-ai-solution-for-internal-corrosion/ (webfetch-verified, Jun 2024)
Content: CausX "causation-based AI" for internal corrosion simulation; 7 patents claimed; team includes Texas A&M corrosion lab; pitch: expert knowledge + small data beats big-data ML. Grant-funded (SBIR + state), pre-commercial.
RELEVANCE: Closest startup analogue to our position (small-data, expert-guided, grant-funded pilot). Their framing — simulation to choose chemicals, reduce unnecessary digs — is an honest-claim model. Also a procurement lesson: US operators buy via SBIR-validated pilots.
Verdict: ADAPT (small-data + expert-first positioning; discount "causal" until peer-reviewed).

## (c) How operators procure ML pilots

### 8. ENMAX × Cordant + TC Energy × Baker Hughes — two public POC shapes
Links: https://dam.bakerhughes.com/asset/1d5fa9e9-eb10-4c34-8ef8-3c6efa07db92/Cordant-Microsoft-Partnership-APM-_Solution-Brief.pdf (ENMAX $13M/89%) · https://www.worldpipelines.com/special-reports/06092023/advanced-analytics-in-north-america/ (TC Energy 40k-defect laser-truth library)
Content: Shape A (ENMAX): priority-asset pilot → baseline risk/cost → acceptance-rate + risk-avoidance success criteria. Shape B (TC Energy): joint data library (operator field truth + vendor signals) → per-feature tolerance model; success = tighter-than-spec tolerances on blind holds, not a single accuracy %.
RELEVANCE: December handover should propose both: (i) GTK1 pilot with pre-registered precision@K-at-dig-budget criteria; (ii) joint truth library (vendor ILI + Gazprom dig sheets) with blind-hold evaluation. Data-sharing stays inside operator systems — no raw export.
Verdict: USE (copy both POC structures into handover demo script + runbook §pilot).

## (d) Open-source vs proprietary positioning

### 9. PODS open data model + Open AI Energy Initiative vs proprietary analytics
Links: https://pods.org/data-models/pods-data-models/ · https://cenosco.com/insights/artificial-intelligence-and-asset-integrity-management (OAI/CARMA)
Content: PODS (25+ yr, 200+ operators, 38 countries, PHMSA-aligned) is fully open and vendor-neutral — yet vendors (ROSEN, OneBridge, Cenosco) keep analytics proprietary and compete on top of it. Shell/Cenosco opened IMS-adjacent physics models (CARMA/AIR) via OAI consortium while keeping the IMS product closed.
RELEVANCE: Confidentiality boundary for our repo: safe to show PODS-schema ETL, matcher logic, calibration plots, and harness methodology (methods layer); keep Gazprom ILI rows, dig outcomes, and tuned weights private (data/parameters layer). Consortium framing (university + operator) mirrors OAI precedent.
Verdict: USE (two-layer open/closed rule — write into handover README).

## (e) Russian market specifics

### 10. Transneft-Diaskan — domestic ILI stack + in-house AI analysis (import-substitution proof)
Links: https://www.in-power.ru/news/neftigaz/49903-ao-transneft-diaskan-pristupilo-k-ispolzovaniyu-informacionnoi-sistemy-s-primeneniem-.html (Exa-found; direct fetch failed — full text not verified, via secondary) · https://www.ndtspace.ru/novosti/152 (combined MFL+UT defectoscope, CIPPE 2024)
Content: Diaskan (90+ tools, 55,000+ km/yr) builds combined magnetic-ultrasonic pigs in Lukhovitsy and now runs an AI-assisted diagnostic-data analysis information system (neural nets/computer vision per iadevon.ru 2022 coverage). Fully domestic chain: tools + software + analysis.
RELEVANCE: Sets the bar for our handover: domestic tools + on-premise analysis is the norm, not a limitation. Positions our triage tool as the same category (отечественная аналитика поверх отечественных приборов).
Verdict: USE (program context; no accuracy numbers disclosed — record as negative on metrics).

### 11. Gazprom transgaz Tomsk × NOTA (T1) + import-substitution constraints
Links: https://ict2go.ru/news/54026 (Tomsk + NOTA strategic cooperation, Sep 2026) · https://korusconsulting.ru/industries/avtomatizatsiya-neftegazovoy-otrasli (only 65% of digital solutions mature enough to replace foreign systems) · https://www.cnews.ru/articles/2026-05-19_kirill_veselyjgazprom_transgaz (Gazprom transgaz Saratov: Directum AI, 7.5× document processing — shows approved AI surface is back-office first)
Content: Tomsk entity signed domestic-PO cooperation (1C templates, tech sovereignty framing) with T1's NOTA. Industry-wide constraint: foreign cloud ML (Azure/M365) is off-table for operational data; approved stack is on-premise + Russian registry software (TESSA/Directum precedents), AI admitted first in documents, not in safety decisions.
RELEVANCE: Hard packaging constraint: December delivery must run offline/on-premise, no foreign-cloud dependency, no data leaving operator контур. Demo script must say this explicitly — it is the import-substitution answer.
Verdict: USE (deployment constraint; cite in handover cover note).

## (f) Honest-ML-claim playbook (verbatim-style, adapt wording, keep hedges)

### 12. Three vendor phrasings worth copying
- ROSEN Integrity Analytics (screening, not sizing): "rapid, reliable screening of onshore pipeline networks, enabling **targeted detailed studies** and inspection… **particularly effective for unpigged or unpiggable pipelines**" + "meticulous approach to model training, testing, and validation ensures… **realistic and reliable** predictions" — note: "reliable screening," never "accurate sizing." https://www.rosen-group.com/en/technology-and-innovation/research-and-development/r-and-d-capabilities/integrity-analytics
- NDT Global (expert-in-loop): "team of pipeline integrity engineers **are also certified data analysts**, making them uniquely qualified to produce **actionable insights**" — claim attaches to people + process, not to a model %. FEA is "the **closest thing to** actually observing defect behaviors" — simile, not equality. https://www.ndt-global.com/integrity-assessments/
- Baker Hughes/ENMAX (accepted-recommendations, not accuracy): "**89% of Cordant APM recommendations were accepted**, helping to achieve the $13M in risk avoidance, reflecting **organizational alignment and confidence**" — metric is adoption + avoided-risk estimate, labeled as program outcome. Solution brief (link §8).
RELEVANCE: Our December pages should speak exactly this way: "screening to focus digs," "engineer-reviewed ranking," "X% of top-K reviewed / precision@K on blind holds" — never a bare accuracy %.
Verdict: ADAPT all three phrasings (with our own numbers + "vendor-reported" labels where borrowed).

---
Per-file footer: Exa-direct OK (6 queries); websearch OK (EN+RU); webfetch OK on 3/4 (in-power.ru failed, covered via Exa + alternates); OpenAlex/arXiv unused; paywalled IPC/PPIM papers not needed; negative results: no public per-product prices found for any ILI analytics suite (all consultative/SaaS-undisclosed — recorded, not omitted); no RU quantitative ML metrics disclosed; no "CorroSight" pipeline product exists (cf. track 20). ~1,750 words. No commits.
