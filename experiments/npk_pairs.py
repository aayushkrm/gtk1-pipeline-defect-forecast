#!/usr/bin/env python3
"""npk_pairs.py: build NPK survey pairs, run the frozen B1 scoring, apply R1-R4.

Reuses the frozen machinery unchanged:
  gtk1.features.build  (depth>=10 cut, pipe+2m/0.5m/1h greedy match, 100 m cells)
  gtk1.metrics         (AP, cell-bootstrap lift CI, P@K)
Pair identity comes from the partner "Общая информация" sheet: same pipeline,
diameter, and km range in two survey years.

Output: experiments/results_npk_pairs.json (aggregates only, committable).
Usage: python3 experiments/npk_pairs.py [--csv outputs/npk/anomalies.csv]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1 import metrics as MET  # noqa: E402
from gtk1.features import build  # noqa: E402

CUT = 10
WIDTH = 100

# (id, kind, past_year, past_section, future_year, future_section, tier)
PAIRS = [
    ("main242_2017_2020", "main", 2017, "Основная труба (242-404 км)",
     2020, "Основная труба (242-404 км)", "primary"),
    ("main110_2019_2020", "main", 2019, "Основная труба (0-110 км)",
     2020, "Основная труба (0-110 км)", "primary"),
    ("main572_2022_2025", "main", 2022, "Основная труба (572-714 км)",
     2025, "Основная труба (572-714)", "primary"),
    ("branch720_2016_2024", "branch", 2016, "Отвод основной трубы (0 - 94 км)",
     2024, "Отвод (0 - 91 км)", "primary"),
    ("branch720_2022_2024", "branch", 2022, "Отвод (0-21,7 км)",
     2024, "Отвод (0 - 91 км)", "sensitivity"),
]


def exact_ci(k: int, n: int, level: float = 0.95):
    """Clopper-Pearson interval (same method as docs/CHOSEN_CLASS_80.md)."""
    if n == 0:
        return [float("nan"), float("nan")]
    a = 1 - level
    lo = 0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k))
    return [lo, hi]


def frame(df: pd.DataFrame, year: int, section: str) -> pd.DataFrame:
    g = df[(df["year"] == year) & (df["section"] == section)].copy()
    if g.empty:
        raise SystemExit(f"empty slice: {year} {section}")
    pipe = pd.to_numeric(g["pipe_no"], errors="coerce")
    keep = pipe.notna()
    g = g.loc[keep].copy()
    pipe = pipe.loc[keep]
    out = pd.DataFrame({
        "dist": pd.to_numeric(g["dist"], errors="coerce"),
        "depth": pd.to_numeric(g["depth_pct"], errors="coerce"),
        "pipe": pipe.astype(str).str.replace(r"\.0$", "", regex=True),
        "off": pd.to_numeric(g["off"], errors="coerce"),
        "h": pd.to_numeric(g["h"], errors="coerce").fillna(-99.0),
        "char": g["char"].astype(str),
        "danger": g["danger"].astype(str),
    })
    out = out.dropna(subset=["dist"]).reset_index(drop=True)
    out["corr"] = out["char"].str.contains("оррози", na=False)
    return out


def run_pair(df: pd.DataFrame, pid: str, kind: str, py: int, ps: str,
             fy: int, fs: str, tier: str) -> dict:
    gp_all = frame(df, py, ps)
    gf_all = frame(df, fy, fs)
    kmax = int(max(gp_all["dist"].max(), gf_all["dist"].max()) // WIDTH)
    y, X, mr = build(gp_all, gf_all, CUT, kmax)
    score = X[:, 0] / max(float(X[:, 0].max()), 1.0)

    lc = MET.ap_lift_ci(y, score)
    p20 = MET.precision_at_k(y, score, 20)
    p50 = MET.precision_at_k(y, score, 50)

    past_cut = int((gp_all["depth"] >= CUT).sum())
    fut_cut = int((gf_all["depth"] >= CUT).sum())
    ratio = (fut_cut / past_cut) if past_cut else float("nan")
    # R3: ratio in [0.5, 2.0] AND (match >= 0.20 OR match >= 0.5 * same-section prior).
    # No pair here has an independent same-section prior match, so the 0.20 floor applies.
    r3 = bool(0.5 <= ratio <= 2.0) and bool(mr >= 0.20)
    r4 = bool(lc["n_pos"] >= 30 and np.isfinite(lc["lift_CI"][0]) and lc["lift_CI"][0] > 0)

    hits20 = int(round(p20[0] * 20))
    hits50 = int(round(p50[0] * 50))
    return {
        "pair": pid, "tier": tier, "kind": kind,
        "past": {"year": py, "section": ps, "rows": int(len(gp_all)),
                 "rows_ge_cut": past_cut},
        "future": {"year": fy, "section": fs, "rows": int(len(gf_all)),
                   "rows_ge_cut": fut_cut},
        "cut": CUT, "cells": int(len(y)),
        "match_rate": float(mr), "prev": float(y.mean()),
        "n_pos": int(lc["n_pos"]),
        "B1": {"AP": lc["AP"], "base": lc["base"], "lift": lc["lift"],
               "lift_CI": lc["lift_CI"]},
        "P@20": {"hits": hits20, "est": float(p20[0]), "CI": list(p20[1:]),
                 "exact_CI": exact_ci(hits20, 20), "base": lc["base"]},
        "P@50": {"hits": hits50, "est": float(p50[0]), "CI": list(p50[1:]),
                 "exact_CI": exact_ci(hits50, 50), "base": lc["base"]},
        "R3": {"future_past_ratio": float(ratio), "pass": r3},
        "R4": {"n_pos_ge_30": bool(lc["n_pos"] >= 30),
               "lift_lower_gt_0": bool(np.isfinite(lc["lift_CI"][0]) and lc["lift_CI"][0] > 0),
               "pass": r4},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="outputs/npk/anomalies.csv")
    ap.add_argument("--out", default="experiments/results_npk_pairs.json")
    args = ap.parse_args()

    df = pd.read_csv(REPO / args.csv, low_memory=False)
    results = []
    for pid, kind, py, ps, fy, fs, tier in PAIRS:
        r = run_pair(df, pid, kind, py, ps, fy, fs, tier)
        results.append(r)
        b = r["B1"]
        print(f"{pid:22s} n_pos={r['n_pos']:5d} cells={r['cells']:5d} "
              f"prev={r['prev']:.3f} AP={b['AP']:.4f} base={b['base']:.4f} "
              f"liftCI=[{b['lift_CI'][0]:+.4f},{b['lift_CI'][1]:+.4f}] "
              f"match={r['match_rate']:.3f} R3={r['R3']['pass']} R4={r['R4']['pass']} "
              f"P@20={r['P@20']['hits']}/20")

    out = {
        "object": "НПК (new partner drop, 2026-10-21)",
        "cut": CUT, "width_m": WIDTH,
        "matcher": "pipe + |dd|<=2m + |doff|<=0.5m + circular |dh|<=1h (frozen R1)",
        "label": "future depth>=10% row unmatched to past depth>=10% rows, 100 m cells",
        "pairs": results,
        "summary": {
            "n_pairs": len(results),
            "r4_pass": [r["pair"] for r in results if r["R4"]["pass"]],
            "r3_pass": [r["pair"] for r in results if r["R3"]["pass"]],
            "clean": [r["pair"] for r in results
                      if r["R3"]["pass"] and r["R4"]["pass"] and r["tier"] == "primary"],
        },
    }
    (REPO / args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nclean (R3+R4, primary):", out["summary"]["clean"])
    print("->", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
