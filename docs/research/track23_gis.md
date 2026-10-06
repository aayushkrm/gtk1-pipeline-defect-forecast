# TRACK 23 — GIS/spatial covariates for pipeline ML (join methodology for when coordinates arrive)

Scope: our lat/lon is 0% today. This track does NOT re-do track 8 (odometer/AGM run alignment, PODS ETL) or track 11 (soil-corrosivity proxy features) — it specifies exactly which open rasters/layers to sample, how to join them to odometer-referenced ILI rows once a centerline exists, and what to request from the partner now. Tooling: direct Exa API via shell served all 8 discovery searches + 3 Exa-contents pulls; routed webfetch served 9/11 page fetches (gis-lab.info timed out → covered by mapinfo.ru; INGU PDF unsupported type → existence via Exa, flagged). OpenAlex API served abstracts/citation counts (Kim 2021, Edrisi 2026, Ran 2021, Ben Seghier 2020).

## (a) Open soil/geology rasters usable in Siberia

**S1 — SoilGrids v2 (Poggio et al. 2021).** https://soil.copernicus.org/articles/7/217/2021/ ; access https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_02.html ; layers https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html
Content: global 250 m ML predictions (Quantile RF), 6 depth intervals (0–5 … 100–200 cm), per property median + mean + Q05/Q95; properties incl. pH, clay/sand/silt, coarse fragments, bulk density, CEC, SOC, water content at 3 suctions. License CC-BY 4.0 (since 2019). Access: WCS (subset), WebDAV VRT tiles (~5 GB/map), Google Earth Engine, WMS. Native Homolosine/WGS84 (reproject with gdalwarp). Accuracy: 30–70% variance explained; Arctic/Central Asia explicitly low-density input regions.
RELEVANCE: first soil source to sample per 100 m cell (median pH, clay %, coarse fragments at 0–30 cm + IQR width as uncertainty feature). No partner data needed. Verdict: USE.

**S2 — HWSD v2.0 (FAO/IIASA 2023).** https://www.fao.org/land-water/resources/tools/databases/hwsd/en
Content: ~1 km (30 arc-sec) raster + attribute DB, 29,538 mapping units, 7 layers to 2 m (0–20 … 150–200), FAO90+WRB taxonomy, texture/CEC/organic-C/AWC per layer. Free viewer + raster + .mdb downloads on the page. Exact redistribution license not confirmed on page.
RELEVANCE: coarser backup where SoilGrids uncertainty is high (Siberia); categorical WRB unit per cell as fallback feature. Verdict: ADAPT (use where SoilGrids IQR is wide; confirm license before redistributing).

**S3 — NSIDC GGD318 circum-arctic permafrost v2 (Brown et al.).** https://nsidc.org/data/ggd318/versions/2
Content: shapefile + EASE-grid via FTP, DOI 10.7265/skbg-kf16. Permafrost extent classes (90–100/50–90/10–50/<10%/none) + ground-ice volume in top 20 m (>20/10–20/<10/0%) + relict/subsea flags. Coarse (grids 12.5 km/25 km/0.5°).
RELEVANCE: Tomsk is at the southern permafrost margin — even a coarse "sporadic/isolated vs none" flag per section is a legitimate frost-heave/buoyancy covariate. Verdict: ADAPT (section-level flag, never per-cell).

**S4 — Ran et al. 2021, ESSD (1 km MAGT + ALT 2000–2016).** https://doi.org/10.5194/essd-2021-83 (OpenAlex: 19 cites; abstract verified, full text not re-verified)
Content: ensemble statistical learning on 1,002 MAGT boreholes + 452 ALT sites + remote sensing; bias 0.02±0.16 °C, RMSE 1.32 °C; permafrost probability + hydrothermal zonation included. Open-access journal; get raster via paper's data-availability section. Companion: Obu et al. 2019 TTOP 1 km map (https://doi.org/10.1016/j.earscirev.2018.12.001 — existence via Exa/ScienceDirect, full text not verified).
RELEVANCE: sharper than S3 where Tomsk straddles the margin — sample MAGT/ALT + permafrost-probability per cell. Verdict: USE (S4 primary; S3 fallback; Obu flagged).

## (b) Elevation/hydrology as corrosion proxies

**S5 — Copernicus DEM GLO-30.** https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM
Content: global 30 m DSM from TanDEM-X 2011–15; GLO-30/GLO-90 free-and-open license (attribution: © DLR/Airbus, Copernicus/EU/ESA); vertical accuracy <4 m (90%), horizontal <6 m; EGM2008 heights, WGS84; S3 + OData bulk access; quality layers (water mask, height-error mask).
RELEVANCE: derive slope, curvature, TWI and low-point flags per 100 m cell; water-body mask seeds river-crossing buffers. Verdict: USE (primary DEM).

**S6 — SRTM GL1 30 m (NASA/USGS/JPL).** https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003
Content: 1 arc-sec (~30 m) near-global DEM, Feb-2000 shuttle flight; V3 void-filled with ASTER GDEM2/GMTED2010/NED; served on EarthExplorer + Earth Engine (`USGS/SRTMGL1_003`); US-government public data.
RELEVANCE: backup where TanDEM-X has gaps/arctic artefacts; identical 30 m sampling code path. Verdict: ADAPT (fallback DEM).

**S7 — Bretreger, Yeo & Melchers (Sci. Total Environ. 2020–21).** DOI via https://exa.ai/library/publication/bmrp64ysk54 (content verified via Exa; journal full text paywalled — method claims per abstract/summary only)
Content: LiDAR-derived terrain wetness indices reproduce soil moisture above buried pipes and rank corrosion potential for underground infrastructure (Melchers group). Establishes DEM→wetness→corrosion as a published pipeline-relevant chain, not just a GIS exercise.
RELEVANCE: justifies TWI + flow-accumulation + distance-to-water features per cell; river/casing crossings get explicit buffer flags (cf. track 11 wetness proxies). River lines: use open hydro line data at implementation time (HydroRIVERS/OSM — product choice NOT verified this track). Verdict: USE (method); river-line product deferred.

## (c) Class-location / HCA methodology

**S8 — 49 CFR §192.5 + §192.903 (class locations + PIR equation).** https://www.law.cornell.edu/cfr/text/49/192.5 ; https://www.law.cornell.edu/cfr/text/49/192.903
Content: class-location unit = 220 yd (200 m) each side × continuous 1-mile; Class 1 ≤10 / Class 2 11–45 / Class 3 ≥46 buildings; 100-yd rule for 20+-person assembly areas; Class 4 = 4+-story prevalence; cluster extensions 220 yd. PIR: r = 0.69·√(p·d²), r feet, p MAOP psi, d inches (gas factor; B31.8S §3.2 for other gases). HCA Method 1 = Class 3/4 + big-PIR Class 1/2 circles with ≥20 buildings or identified sites; Method 2 = any PIR circle with ≥20 buildings/identified site; HCA extends edge-to-edge of contiguous qualifying circles.
RELEVANCE: exact formulas to reimplement for GTK1 consequence-side screening (Russian regs differ — this is a method template, not a compliance claim). Verdict: ADAPT.

**S9 — 49 CFR §192.905 + PHMSA HCA fact sheet (operator data sources).** https://www.law.cornell.edu/cfr/text/49/192.905 ; https://primis.phmsa.dot.gov/stakeholder-comms/factsheets/fshca/
Content: identified sites from O&M records + public officials (or visible marking / license lists / public maps); gas-HCA population from Census maps; liquid-HCA water/ecology via state heritage data + Nature Conservancy; liquid HCAs pre-mapped on NPMS (https://www.npms.phmsa.dot.gov/); gas operators compute PIR circles themselves along every point of the line.
RELEVANCE: template for our "consequence" layer: building counts from open data (e.g., OSM/Microsoft footprints — product NOT verified this track) inside PIR buffers; NPMS shows the regulator-precompute pattern. Verdict: ADAPT.

**S10 — ENTRUST Gas HCA Tool, Class Location reference (ArcGIS, G2/ENRUST).** https://entrustsol.com/products/gas-hca-tool/gas-hca-tool-reference/gas-hca-master-tools/class-location/
Content: full reproducible recipe — centerline with begin/end measures (linear referencing), 660-ft structure buffers, 300-ft qualifying-area buffers, influence ranges, 5,280-ft sliding-mile generation, cluster methods (arc vs perpendicular/parallel), sliver-dissolve tolerances, scripted arcpy example.
RELEVANCE: copy the pipeline (buffer→influence-range→sliding-window→cluster→dissolve) for both class-location analogues and our PIR/HCA screening; begin/end-measure centerline is exactly the odometer→GIS bridge. Verdict: USE (method; tool itself is licensed/commercial — recipe only).

## (d) CP rectifier/telemetry geospatial integration

**S11 — Mobiltex CorView cloud platform.** https://www.mobiltex.com/solutions/corview-cloud-platform/
Content: cellular/satellite RMUs on rectifiers + test stations; site locations on GPS/Google-Maps engine; GPS-synchronised interruption; open API + CSV/Excel export + automated reports; 3-yr archive; SOC2/AWS. Pattern: every CP reading is a geo-tagged time series joinable to pipe chainage.
RELEVANCE: when partner CP data arrives, require rectifier/test-point coordinates + timestamps in the same schema; join = nearest-chainage + outage-window flags per cell (extends track 15 items 6–9). Verdict: USE (integration pattern + request wording).

## (e) Published GIS→ILI joins (which covariates won)

**S12 — Wang, Sreeharan & Castaneda 2021 (Bayesian ML + soil corrosivity, 110 km pipeline).** https://exa.ai/library/publication/pphvx836w5v (abstract verified via Exa; full text not verified)
Content: soil survey + indirect-inspection + ILI + precipitation/vegetation → spatial corrosivity regions with per-region defect-depth and defect-count statistics; clustering respects spatial variation along the ROW; output feeds dig scheduling.
RELEVANCE: closest published analogue of our future pipeline: zone-then-count modeling with environmental covariates. Verdict: ADAPT.

**S13 — Edrisi & Aghajani 2026 (spatially validated ML surrogates, gas transmission).** https://doi.org/10.1016/j.rineng.2026.112452 (abstract via OpenAlex; full text not verified)
Content: 1,104 obs at 1-km chainage; 9 categorical predictors from CIPS + DCVG + Wenner resistivity + records; 5 contiguous spatial folds with 5-km exclusion buffer + block bootstrap; XGBoost R² 0.925, RMSE 0.0197 mm/yr, MAE 0.0109 mm/yr vs ridge/mean baselines.
RELEVANCE: effect sizes + honest protocol (buffered spatial folds) to copy; resistivity + CP-survey covariates won. Verdict: USE (evaluation protocol + covariate shortlist).

**S14 — ICASP14 2023 (inspection + soil-survey growth model, 112 km).** https://exa.ai/library/publication/x84136vpqk3 (abstract verified via Exa; full text not verified)
Content: power-law growth + soil properties in the formulation + depth/length correlation + Bayesian updating + Poisson initiation; works with matched OR unmatched defects; predicts new-defect counts since last inspection.
RELEVANCE: directly supports our ID-less setting — soil-conditioned growth without requiring matched pairs. Verdict: ADAPT (cite in P2 design; re-derive, don't import).

**S15 — Kim et al. 2021, JPSE review (77 cites).** https://doi.org/10.1016/j.jpse.2021.01.010 (abstract via OpenAlex; full text not verified)
Content: global-vs-local parameter framing: macro spatial distribution controls initiation; local soil/steel interface conditions control propagation; covers deterministic → data-driven models.
RELEVANCE: vocabulary for our two-scale features (section climate/soil zone × cell wetness/CP). Also-noted: Ben Seghier et al. 2020 (EFA, 169 cites, max-pit-depth ML — abstract unavailable, full text not verified, recorded only). Verdict: USE (framing).

## (f) Coordinate-reference pitfalls

**S16 — GOST 32453-2017 parameters (mapinfo.ru, Russian).** https://mapinfo.ru/articles/gost
Content: SK-42→WGS84 ΔX 23.57 / ΔY −140.95 / ΔZ −79.8 m (Krasovsky ellipsoid) vs PZ-90.11→WGS84 at cm level (0.013/−0.106/−0.022 m); SK-42/SK-95 legal use ended 2021-01-01 (Decree 1240 → ГСК-2011/PZ-90.11); sign-flip trap between GOST/Coordinate-Frame (EPSG:1032) and PROJ/Position-Vector (EPSG:1033) rotations; Tomsk Oblast (~77–89°E) spans Gauss-Krüger zones 13–15 (6° rule — computed, verify per sheet).
RELEVANCE: any legacy SK-42 sheet uncorrected = ~100+ m systematic shift = a full 100-m cell error. Verdict: USE (mandatory CRS-declaration + transform gate).

**S17 — Odometer→GPS error budget (Liu/Zheng/Li 2019, Sensors).** https://www.mdpi.com/1424-8220/19/17/3740 (via track 8 S6 + Exa contents verified: IMU+odometer+AGM fusion; LSTM slip compensation cut mean absolute error 8.75→2.02 m)
Content: production chainage↔GPS accuracy is ~2 m only after AGM/IMU fusion; raw odometer drifts ~1 m/km. Noted but not fetched: INGU PTC-2025 odometerless positioning paper and Czyz et al. 2024 inertial-survey re-analysis (existence via Exa only).
RELEVANCE: budget for the join — weld-anchored chainage ±2 m ≪ 100 m cells is safe; uncorrected odometer (±100 m/100 km, track 8) is NOT. Verdict: USE (gate: only AGM/IMU-corrected chainage enters GIS).

## Exact future feature list (per 100 m cell, once centerline exists)
Soil: SoilGrids median pH, clay%, coarse-frag% (0–30 cm) + IQR widths; WRB unit (HWSD fallback); MAGT + permafrost probability (S4/S3). Terrain/hydro: elevation, slope, curvature, TWI, low-point flag (S5/S6); river/wetland buffer flag + crossing distance (S7). CP/infra: distance to nearest rectifier/test point + outage-window flag (S11); road/rail/foreign-crossing count (track 11 S6). Consequence (screening only): PIR from p·d (S8) + building/assembly counts in circle (S9/S10 recipe).
Join method: (1) centerline route with M = corrected odometer (S17 gate); (2) anomalies → route events by M; (3) raster sampling at chainage-interpolated cell centroids; (4) buffer overlays for lines/points; (5) CRS-declaration gate (S16) before any step; (6) Edrisi-style buffered spatial folds for any model using these features (S13).
Partner-request wording: "просим: (i) координаты оси трубы или привязку одометр→GPS (система координат обязательна); (ii) chainage ме́ток/маркеров (AGM) и выверок; (iii) координаты выпрямителей/КИП и журналы отключений; (iv) пересечения рек/дорог по chainage; (v) почвенные разрезы/резистивиметрия по участкам, если есть."

*Footer: Exa direct API served discovery + 3 content pulls; webfetch served 9/11 (gis-lab timeout → mapinfo.ru substitute; INGU PDF type unsupported → existence-only). OpenAlex served 4 abstracts. Paywalled primaries (Obu, S7 journal, S12–S15 full texts, Ben Seghier) cited via abstract/secondary and marked "full text not verified". Negatives: no verified open river-line or building-footprint product for Tomsk this track (deferred to implementation); HWSD redistribution license unconfirmed.*
