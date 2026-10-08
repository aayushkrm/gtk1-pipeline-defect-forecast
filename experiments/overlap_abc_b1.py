"""Overlap of B1 top-ranked cells with ABC red/orange cells.

Reads only committed artifacts. No raw data access.
No new dependencies. Standard library only.
"""
import json
import math
import statistics
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRI = REPO / "triage"

WATCHLISTS = [
    "triage/watchlist_on_2021.json",
    "triage/watchlist_pk1_2022.json",
    "triage/watchlist_on_2025.json",
    "triage/watchlist_pk1_2025_noedge.json",
]

ABCS = [
    "triage/abc_on_2025.json",
    "triage/abc_pk1_2025.json",
    "triage/abc_srto_2024.json",
    "triage/abc_srto1717_2021.json",
]

KS = [20, 50, 100, 200]


def clean(o):
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def git_hash():
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]
        ).decode().strip()
    except Exception:
        return "unknown"


def load(rel):
    with open(REPO / rel) as f:
        return json.load(f)


def extract_ranking(w):
    """Inspect keys first. Use whatever top-K list fields exist."""
    found = {}
    for k, v in w.items():
        if k.startswith("top") and isinstance(v, list):
            found[k] = v
    cell_to_rank = {}
    for key, rows in found.items():
        for e in rows:
            if isinstance(e, dict) and "cell" in e and "rank" in e:
                c, r = int(e["cell"]), int(e["rank"])
                if c not in cell_to_rank:
                    cell_to_rank[c] = r
            elif isinstance(e, (list, tuple)) and len(e) >= 2:
                # triage top20 row form: [rank, cell, ...]
                try:
                    r, c = int(e[0]), int(e[1])
                    if c not in cell_to_rank:
                        cell_to_rank[c] = r
                except Exception:
                    continue
    max_k = max(cell_to_rank.values()) if cell_to_rank else 0
    return found, cell_to_rank, max_k


def extract_worst(a):
    worst = a.get("worst", [])
    red = [i for i, v in enumerate(worst) if v == 2]
    orange = [i for i, v in enumerate(worst) if v == 1]
    return worst, red, orange


def overlap_stats(cell_to_rank, max_k, red, orange):
    """Cell index equals worst-list index. worst len equals n_cells."""
    out = {}
    red_ranks = sorted(cell_to_rank[c] for c in red if c in cell_to_rank)
    for k in KS:
        if k <= max_k:
            topk = {c for c, r in cell_to_rank.items() if r <= k}
            out[f"red_in_top{k}"] = sum(1 for c in red if c in topk)
            out[f"red_frac_top{k}"] = (
                sum(1 for c in red if c in topk) / len(red) if red else None
            )
            out[f"orange_in_top{k}"] = sum(1 for c in orange if c in topk)
            out[f"orange_frac_top{k}"] = (
                sum(1 for c in orange if c in topk) / len(orange)
                if orange
                else None
            )
        else:
            out[f"red_in_top{k}"] = None
            out[f"red_frac_top{k}"] = None
            out[f"orange_in_top{k}"] = None
            out[f"orange_frac_top{k}"] = None
    median_rank = statistics.median(red_ranks) if red_ranks else None
    return out, red_ranks, median_rank


def full_ranking_supplement(watch_rel, red, orange):
    """Local-only supplement: full B1 order from gitignored outputs/ CSVs.
    Never committed as ground truth; committed top-20 stats above stand alone.
    Returns dict or None when the CSV is absent."""
    import csv

    csv_path = REPO / "outputs" / (Path(watch_rel).stem + ".csv")
    if not csv_path.exists():
        return None
    order = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            order.append(int(row["cell"]))
    rank_of = {c: r + 1 for r, c in enumerate(order)}
    red_ranks = sorted(rank_of[c] for c in red if c in rank_of)
    out = {}
    for k in (50, 100, 200):
        topk = set(order[:k])
        out[f"red_in_top{k}"] = sum(1 for c in red if c in topk)
        out[f"red_frac_top{k}"] = (sum(1 for c in red if c in topk) / len(red) if red else None)
        out[f"orange_in_top{k}"] = sum(1 for c in orange if c in topk)
        out[f"orange_frac_top{k}"] = (sum(1 for c in orange if c in topk) / len(orange)
                                      if orange else None)
    import statistics as _st

    out["median_b1_rank_red_full"] = _st.median(red_ranks) if red_ranks else None
    out["red_ranks_full"] = red_ranks
    out["source"] = ("UNCOMMITTED local outputs/ CSV (same run that wrote the committed "
                      "watchlist JSON); supplement only, not ground truth.")
    return out


def analyze_pair(watch_rel, abc_rel):
    w = load(watch_rel)
    a = load(abc_rel)
    found, cell_to_rank, max_k = extract_ranking(w)
    worst, red, orange = extract_worst(a)
    stats, red_ranks, median_rank = overlap_stats(cell_to_rank, max_k, red, orange)
    same_year = w.get("survey") == a.get("survey")
    same_cells = w.get("n_cells") == len(worst)
    topk_avail = sorted(found.keys())
    rec = {
        "watchlist": watch_rel,
        "watch_section": w.get("section"),
        "watch_survey": w.get("survey"),
        "abc": abc_rel,
        "abc_section": a.get("section"),
        "abc_survey": a.get("survey"),
        "same_survey_year": same_year,
        "same_ground_truth": bool(same_year and same_cells),
        "n_cells_watchlist": w.get("n_cells"),
        "n_cells_abc": len(worst),
        "ranking_fields_found": topk_avail,
        "max_rank_available": max_k,
        "n_red": len(red),
        "n_orange": len(orange),
        "red_cells": red,
        "orange_cells": orange,
        "red_in_top20_cells": sorted(c for c in red if c in cell_to_rank),
        "orange_in_top20_cells": sorted(c for c in orange if c in cell_to_rank),
        "red_ranks_in_top20": red_ranks,
        "median_b1_rank_red": median_rank,
        "stats": stats,
    }
    if max_k < 200:
        rec["top50_100_200_note"] = (
            f"Only top-{max_k} stored in committed artifact; "
            "top-50/100/200 need full ranking and are null. "
            "No raw data read per task rules."
        )
    if not same_year:
        rec["year_mismatch_note"] = (
            "Different surveys. Report separately. "
            "Never mix as same ground truth."
        )
    if median_rank is None:
        rec["median_note"] = (
            "No red cell in stored B1 top list; "
            "median rank unknown beyond stored top."
            if red
            else "No red cells in ABC artifact."
        )
    full = full_ranking_supplement(watch_rel, red, orange)
    if full is not None:
        full["scope"] = ("LOCAL-ONLY supplement: derived from gitignored outputs/ CSVs, "
                         "reproducible only where those local files exist. Committed top-20 "
                         "stats above are the portable ground truth; medians below are not.")
        rec["full_ranking_supplement"] = full
        if full["median_b1_rank_red_full"] is not None:
            rec["median_b1_rank_red"] = full["median_b1_rank_red_full"]
    return rec


def main():
    matched_pairs = [
        ("triage/watchlist_on_2025.json", "triage/abc_on_2025.json"),
        ("triage/watchlist_pk1_2025_noedge.json", "triage/abc_pk1_2025.json"),
    ]
    cross_pairs = [
        ("triage/watchlist_on_2021.json", "triage/abc_on_2025.json"),
        ("triage/watchlist_pk1_2022.json", "triage/abc_pk1_2025.json"),
    ]
    matched = [analyze_pair(w, a) for w, a in matched_pairs]
    cross = [analyze_pair(w, a) for w, a in cross_pairs]
    no_b1 = []
    for rel in ["triage/abc_srto_2024.json", "triage/abc_srto1717_2021.json"]:
        a = load(rel)
        _, red, orange = extract_worst(a)
        no_b1.append(
            {
                "abc": rel,
                "abc_section": a.get("section"),
                "abc_survey": a.get("survey"),
                "n_cells_abc": len(a.get("worst", [])),
                "n_red": len(red),
                "n_orange": len(orange),
                "red_cells": red,
                "orange_cells": orange,
                "b1_watchlist": None,
                "note": "No B1 watchlist committed for this section. No overlap computed.",
            }
        )
    all_red_covered = all(
        (m["stats"]["red_in_top20"] or 0) == m["n_red"] and m["n_red"] > 0
        for m in matched
    )
    any_red_covered = any((m["stats"]["red_in_top20"] or 0) > 0 for m in matched)
    if any_red_covered and all_red_covered:
        verdict = "one map suffices: B1 top ranks cover ABC red cells."
    else:
        verdict = "two maps needed: B1 top ranks miss ABC red cells."
    result = {
        "matched_same_survey": matched,
        "cross_survey_reference_only": cross,
        "no_b1_counterpart": no_b1,
        "verdict": verdict,
        "git": git_hash(),
        "method": (
            "Committed artifacts only. Cell index equals worst-list index. "
            "Fraction in top-K uses stored ranking only; "
            "K above stored max is null. Cross-survey pairs are reference only."
        ),
    }
    result = clean(result)
    out = REPO / "experiments" / "results_overlap.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {out}")
    for m in matched:
        s = m["stats"]
        print(
            f"{m['abc_section']} {m['abc_survey']}: "
            f"red {s['red_in_top20']}/{m['n_red']} in top20 "
            f"(frac={s['red_frac_top20']}), "
            f"orange {s['orange_in_top20']}/{m['n_orange']} in top20 "
            f"(frac={s['orange_frac_top20']}), "
            f"median_red_rank={m['median_b1_rank_red']}"
        )
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
