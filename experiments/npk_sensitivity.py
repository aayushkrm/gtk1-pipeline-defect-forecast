#!/usr/bin/env python3
"""npk_sensitivity.py: cut and composition sensitivity for the NPK clean pair.

The primary result stays the frozen R1 pipeline at depth>=10%. This script only
adds robustness columns required by docs/GUARDRAILS.md: depth cut >=12% / >=15%,
a corrosion-only label variant, and a boundary-cell exclusion. No tuning, no
selection of the headline.

Output: experiments/results_npk_sensitivity.json (aggregates only, committable).
Usage: python3 experiments/npk_sensitivity.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1 import metrics as MET  # noqa: E402
from gtk1.features import build  # noqa: E402

spec = importlib.util.spec_from_file_location("npk_pairs", REPO / "experiments" / "npk_pairs.py")
npk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(npk)

CUTS = (10, 12, 15)


def score_pair(df, pair, cut, corr_only=False, drop_boundary=False):
    _, _, py, ps, fy, fs, _ = pair
    gp = npk.frame(df, py, ps)
    gf = npk.frame(df, fy, fs)
    if corr_only:
        gp = gp[gp["corr"]].reset_index(drop=True)
        gf = gf[gf["corr"]].reset_index(drop=True)
    kmax = int(max(gp["dist"].max(), gf["dist"].max()) // npk.WIDTH)
    y, X, mr = build(gp, gf, cut, kmax)
    if drop_boundary:
        y, X = y[:-1], X[:-1]
    score = X[:, 0] / max(float(X[:, 0].max()), 1.0)
    lc = MET.ap_lift_ci(y, score)
    p20 = MET.precision_at_k(y, score, 20)
    p50 = MET.precision_at_k(y, score, 50)
    return {
        "cut": cut, "corr_only": corr_only, "drop_boundary": drop_boundary,
        "cells": int(len(y)), "n_pos": int(lc["n_pos"]), "prev": float(lc["base"]),
        "match_rate": float(mr),
        "AP": float(lc["AP"]), "base": float(lc["base"]), "lift": float(lc["lift"]),
        "lift_CI": [float(x) for x in lc["lift_CI"]],
        "P@20": {"hits": int(round(p20[0] * 20)), "est": float(p20[0]),
                 "exact_CI": npk.exact_ci(int(round(p20[0] * 20)), 20)},
        "P@50": {"hits": int(round(p50[0] * 50)), "est": float(p50[0]),
                 "exact_CI": npk.exact_ci(int(round(p50[0] * 50)), 50)},
    }


def main() -> int:
    df = pd.read_csv(REPO / "outputs" / "npk" / "anomalies.csv", low_memory=False)
    pairs = {p[0]: p for p in npk.PAIRS}
    out = {"object": "НПК (new partner drop, 2026-10-21)",
           "note": "primary = frozen R1 cut 10; other rows are sensitivity only",
           "variants": {}}
    for pid in ("main572_2022_2025", "branch720_2016_2024"):
        pair = pairs[pid]
        rows = []
        for cut in CUTS:
            rows.append(score_pair(df, pair, cut))
        rows.append(score_pair(df, pair, 10, corr_only=True))
        rows.append(score_pair(df, pair, 10, drop_boundary=True))
        out["variants"][pid] = rows
        print(f"== {pid}")
        for r in rows:
            tag = f"cut{r['cut']}" + (" corr" if r["corr_only"] else "") + (" nobound" if r["drop_boundary"] else "")
            print(f"  {tag:12s} cells={r['cells']:5d} n_pos={r['n_pos']:4d} "
                  f"prev={r['prev']:.3f} AP={r['AP']:.4f} base={r['base']:.4f} "
                  f"liftCI=[{r['lift_CI'][0]:+.4f},{r['lift_CI'][1]:+.4f}] "
                  f"match={r['match_rate']:.3f} P@20={r['P@20']['hits']}/20 P@50={r['P@50']['hits']}/50")
    dest = REPO / "experiments" / "results_npk_sensitivity.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
