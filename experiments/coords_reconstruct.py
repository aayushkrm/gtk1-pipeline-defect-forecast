"""Straight-line coordinate reconstruction for the interpolation track (meeting 08.10.2026).

Method (Evgeny proposal): town endpoint coords from a public map source,
odometer chainage laid along the straight line. Documented approximation:
town-proxy straight line, NOT surveyed; pipes bend.

Approximation level of every output: town-proxy straight line, NOT surveyed.
Real pipes bend and leave the straight line, so errors are km-scale. This
geometry must NOT feed 100 m interpolation as surveyed truth.

Corridor model: each named pipeline is one straight town-to-town segment with
km 0 at town A. A section [km_start, km_end] occupies fraction
[km_start / L_full, km_end / L_full] of that segment, where L_full is the
corridor odometer length. L_full is taken as the largest section chainage on
that corridor (documented assumption: the highest-chained section end sits at
town B). Per-100 m cell centroids use linear interpolation in lat/lon degrees.

Sections and km spans come from docs/DATA.md. DATA.md parenthetical lengths
differ slightly from span subtraction; both numbers are recorded, geometry
uses the subtracted span.

Only stdlib is used (math, json). No raw defect data is read or written.
"""
import json
import math
from pathlib import Path

APPROX = "town-proxy straight line, NOT surveyed; pipes bend"

OUT = Path(__file__).resolve().parent / "results_coords.json"
CELL_KM = 0.1
EARTH_R_KM = 6371.0

# Endpoint towns. Coords verified this session via webfetch of English
# Wikipedia infobox coordinates (decimal conversions of the DMS values shown
# on each page). Kuzbass has no single town: Kemerovo (admin center of
# Kemerovo Oblast / Kuzbass) is the documented proxy. SRTO (northern Tyumen
# gas province) has no single town: Novy Urengoy (main field hub city) is
# the documented proxy.
TOWNS = {
    "Omsk": {
        "lat": 54.983, "lon": 73.367,
        "source": "https://en.wikipedia.org/wiki/Omsk",
        "source_detail": "Infobox: 54°59′N 73°22′E = 54.983N 73.367E",
        "approximation": APPROX,
    },
    "Novosibirsk": {
        "lat": 55.050, "lon": 82.950,
        "source": "https://en.wikipedia.org/wiki/Novosibirsk",
        "source_detail": "Infobox: 55°03′N 82°57′E = 55.050N 82.950E",
        "approximation": APPROX,
    },
    "Parabel": {
        "lat": 58.71333, "lon": 81.49917,
        "source": "https://en.wikipedia.org/wiki/Parabel_(rural_locality)",
        "source_detail": "Infobox: 58°42′48″N 81°29′57″E = 58.71333N 81.49917E",
        "approximation": APPROX,
    },
    "Kemerovo": {
        "lat": 55.367, "lon": 86.067,
        "source": "https://en.wikipedia.org/wiki/Kemerovo",
        "source_detail": "Infobox: 55°22′N 86°04′E = 55.367N 86.067E; "
                         "Kuzbass proxy = admin center of Kemerovo Oblast",
        "approximation": APPROX,
    },
    "Yurga": {
        "lat": 55.72306, "lon": 84.88611,
        "source": "https://en.wikipedia.org/wiki/Yurga",
        "source_detail": "Infobox: 55°43′23″N 84°53′10″E = 55.72306N 84.88611E",
        "approximation": APPROX,
    },
    "Novy_Urengoy": {
        "lat": 66.083, "lon": 76.683,
        "source": "https://en.wikipedia.org/wiki/Novy_Urengoy",
        "source_detail": "Infobox: 66°05′N 76°41′E = 66.083N 76.683E; "
                         "SRTO proxy = main Urengoy field hub city",
        "approximation": APPROX,
    },
}

# Corridors: (town_a at km 0, town_b at L_full, L_full odometer km).
CORRIDORS = {
    "ON": ("Omsk", "Novosibirsk", 526.0),
    "PK": ("Parabel", "Kemerovo", 714.0),
    "SRTO": ("Novy_Urengoy", "Omsk", 1759.0),
    "YN": ("Yurga", "Novosibirsk", 154.0),
}

# Sections: key -> (corridor, km_start, km_end, DATA.md length label).
SECTIONS = {
    "ON_392_526": ("ON", 392.0, 526.0, "132km"),
    "PK1_572_714": ("PK", 572.0, 714.0, "140km"),
    "PK2_0_110": ("PK", 0.0, 110.0, "113km"),
    "SRTO_1608_1717": ("SRTO", 1608.0, 1717.0, "104km"),
    "SRTO_1717_1759": ("SRTO", 1717.0, 1759.0, "42km"),
    "YN_0_154": ("YN", 0.0, 154.0, "151km"),
}


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R_KM * math.asin(math.sqrt(a))


def corridor_point(town_a, town_b, frac):
    a, b = TOWNS[town_a], TOWNS[town_b]
    return (a["lat"] + frac * (b["lat"] - a["lat"]),
            a["lon"] + frac * (b["lon"] - a["lon"]))


def build():
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "passed": bool(ok), "detail": detail})
        return bool(ok)

    corridors = {}
    for name, (ta, tb, L_full) in CORRIDORS.items():
        straight = haversine_km(TOWNS[ta]["lat"], TOWNS[ta]["lon"],
                                TOWNS[tb]["lat"], TOWNS[tb]["lon"])
        bend = L_full / straight
        corridors[name] = {
            "town_a": ta, "town_b": tb,
            "L_full_odometer_km": L_full,
            "straight_line_km": round(straight, 3),
            "bend_factor_nominal_over_straight": round(bend, 4),
            "bend_flag": ("INCONSISTENT: straight line longer than odometer; "
                          "town proxy does not span this section"
                          if bend < 1.0 else "plausible (>=1)"),
            "approximation": APPROX,
        }
        # Sanity 1: corridor endpoints reproduce the declared source coords.
        p0 = corridor_point(ta, tb, 0.0)
        p1 = corridor_point(ta, tb, 1.0)
        check(f"endpoint_A_matches_source:{name}",
              abs(p0[0] - TOWNS[ta]["lat"]) == 0.0 and abs(p0[1] - TOWNS[ta]["lon"]) == 0.0,
              f"t=0 -> {p0} vs {ta} {(TOWNS[ta]['lat'], TOWNS[ta]['lon'])}")
        check(f"endpoint_B_matches_source:{name}",
              abs(p1[0] - TOWNS[tb]["lat"]) == 0.0 and abs(p1[1] - TOWNS[tb]["lon"]) == 0.0,
              f"t=1 -> {p1} vs {tb} {(TOWNS[tb]['lat'], TOWNS[tb]['lon'])}")

    sections = {}
    for key, (corr, km0, km1, label) in SECTIONS.items():
        ta, tb, L_full = CORRIDORS[corr]
        span = km1 - km0
        n = int(round(span / CELL_KM))
        check(f"cell_count_matches_span:{key}", abs(n * CELL_KM - span) < 1e-9,
              f"n={n} cells x 0.1km = {n * CELL_KM} vs span {span}")
        centroids = []
        for i in range(n):
            km = km0 + (i + 0.5) * CELL_KM
            lat, lon = corridor_point(ta, tb, km / L_full)
            centroids.append([round(km, 3), round(lat, 6), round(lon, 6)])
        kms = [c[0] for c in centroids]
        check(f"chainage_monotonic:{key}",
              all(b > a for a, b in zip(kms, kms[1:])),
              f"{len(kms)} centroids strictly increasing "
              f"{kms[0]}..{kms[-1]}" if kms else "empty")
        check(f"chainage_edges_half_cell:{key}",
              abs(kms[0] - (km0 + CELL_KM / 2)) < 1e-9 and abs(kms[-1] - (km1 - CELL_KM / 2)) < 1e-9,
              f"first={kms[0]} last={kms[-1]} vs [{km0},{km1}]")
        lat0, lon0 = corridor_point(ta, tb, km0 / L_full)
        lat1, lon1 = corridor_point(ta, tb, km1 / L_full)
        sub_straight = haversine_km(lat0, lon0, lat1, lon1)
        sec_bend = span / sub_straight if sub_straight > 0 else float("nan")
        lats = [c[1] for c in centroids]
        lons = [c[2] for c in centroids]
        check(f"centroids_inside_corridor_bbox:{key}",
              min(lats) >= min(TOWNS[ta]["lat"], TOWNS[tb]["lat"]) - 1e-9
              and max(lats) <= max(TOWNS[ta]["lat"], TOWNS[tb]["lat"]) + 1e-9
              and min(lons) >= min(TOWNS[ta]["lon"], TOWNS[tb]["lon"]) - 1e-9
              and max(lons) <= max(TOWNS[ta]["lon"], TOWNS[tb]["lon"]) + 1e-9,
              f"lat [{min(lats)},{max(lats)}] lon [{min(lons)},{max(lons)}]")
        sections[key] = {
            "corridor": corr,
            "town_a": ta, "town_b": tb,
            "km_start": km0, "km_end": km1,
            "span_computed_km": span,
            "span_label_DATA_md": label,
            "span_label_matches_computed": label == f"{span:g}km",
            "n_cells_100m": n,
            "cell_km": CELL_KM,
            "straight_subsegment_km": round(sub_straight, 3),
            "section_bend_factor_span_over_subsegment": round(sec_bend, 4),
            "edge_start": {"km": km0, "lat": round(lat0, 6), "lon": round(lon0, 6)},
            "edge_end": {"km": km1, "lat": round(lat1, 6), "lon": round(lon1, 6)},
            "centroids_km_lat_lon": centroids,
            "approximation": APPROX,
        }

    # Sanity: contiguous SRTO subsegments share the km-1717 point exactly.
    e_end = sections["SRTO_1608_1717"]["edge_end"]
    e_start = sections["SRTO_1717_1759"]["edge_start"]
    check("srto_contiguous_at_1717",
          e_end["lat"] == e_start["lat"] and e_end["lon"] == e_start["lon"],
          f"1717 point {e_end} vs {e_start}")

    passed = all(c["passed"] for c in checks)

    verdict = ("FITNESS VERDICT for 100m interpolation use: UNFIT as surveyed "
               "geometry — town-proxy straight-line error is km-scale "
               "(town centers stand in for unknown pipe endpoints; real pipes "
               "bend off the line; ON corridor bend < 1 proves the proxy does "
               "not even span that section). Use odometer chainage only for "
               "along-pipe joins; use these coords solely as coarse map "
               "overlay, never as 100 m cell truth.")
    check("fitness_verdict_recorded", True, verdict)

    return {
        "approximation_level": APPROX,
        "method": {
            "proposal": "Evgeny straight-line reconstruction, meeting 08.10.2026",
            "model": "One straight town-to-town segment per corridor; km 0 at "
                     "town A; section [km_start, km_end] at fraction "
                     "[km_start/L_full, km_end/L_full]; linear in lat/lon degrees; "
                     "cell centroids at km_start + (i+0.5)*0.1.",
            "L_full_rule": "Largest section chainage on the corridor "
                            "(assumes that section end sits at town B).",
            "length_reference": "haversine great-circle km; bend factor = "
                                "nominal odometer km / straight-line km.",
            "limits": "Town centers proxy unknown pipe endpoints; linear "
                      "degrees ignore route bends, river/road crossings, and "
                      "offsets; errors are km-scale vs 0.1 km cells.",
            "dependencies": "stdlib only (math, json, pathlib)",
            "raw_data_touched": "none (aggregates only, no defect data)",
            "approximation": APPROX,
        },
        "endpoints": TOWNS,
        "corridors": corridors,
        "sections": sections,
        "sanity": {"passed": passed, "checks": checks,
                   "approximation": APPROX},
        "fitness_verdict": verdict,
    }


def main():
    result = build()
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")
    for name, c in result["corridors"].items():
        print(f"{name}: {c['town_a']} -> {c['town_b']} "
              f"L_full={c['L_full_odometer_km']}km "
              f"straight={c['straight_line_km']}km "
              f"bend={c['bend_factor_nominal_over_straight']} [{c['bend_flag']}]")
    for key, s in result["sections"].items():
        print(f"{key}: n_cells={s['n_cells_100m']} "
              f"span={s['span_computed_km']}km (DATA.md {s['span_label_DATA_md']}) "
              f"sec_bend={s['section_bend_factor_span_over_subsegment']}")
    print(f"sanity passed: {result['sanity']['passed']} "
          f"({sum(c['passed'] for c in result['sanity']['checks'])}/"
          f"{len(result['sanity']['checks'])} checks)")
    print(result["fitness_verdict"])


if __name__ == "__main__":
    main()
