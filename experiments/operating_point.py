"""Operating-point proposal for future threshold calibration (retrospective only).

Builds B1 test frames with the frozen R1 pipeline (src.gtk1.features.build,
cut=10) for three completed pairs: ON 2021->2025, SRTO-1608 2021->2024,
PK1 2022->2025. Scores B1 past-count ranking, grids precision@K with
bootstrap CI via src.gtk1.metrics, and derives per-section flag/band
proposals. Proposals are UNCONFIRMED until the next survey confirms them
per docs/PROSPECTIVE_RUNBOOK.md section 3. CPU only. Read-only raw data.
"""
import json
import math
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "triage"))

from gtk1.features import build
from gtk1 import metrics as MET
from prospective import load_section as pros_load
from prospective import SECTIONS as PROS_SECTIONS
from prospective import DATA

CUT = 10
K_GRID = [5, 10, 20, 30, 50, 100, 200, 300, 400, 500]
N_BOOT = 500
SEED = 7
STATUS = "UNCONFIRMED \u2014 confirm on next survey via docs/PROSPECTIVE_RUNBOOK.md \u00a73"

PAIRS = {
    "on": {"past": 2021, "future": 2025, "kmax": 1330},
    "srto": {"past": 2021, "future": 2024, "kmax": 1040},
    "pk1": {"past": 2022, "future": 2025, "kmax": 1400},
}

SRTO_CFG = {"dir": "СРТО-Омск_(1608 \u2013 1717)", "kmax": 1040, "files": None}


def load_section(section, year):
    """Local loader mirroring triage/prospective.py load_section.

    Delegates ON/PK1 to the imported prospective.load_section (identical
    behavior guaranteed). Handles SRTO-1608 with the same files=None glob
    branch that prospective.py uses for PK1. Never modifies prospective.py.
    """
    if section in PROS_SECTIONS:
        return pros_load(section, year)
    if section == "srto":
        from gtk1.io import load_anomalies, normalize
        d = DATA / SRTO_CFG["dir"] / str(year)
        cands = sorted(p for p in d.glob("*.xls*") if Path(p).name.startswith("Аномалии"))
        fp = Path(cands[0]) if cands else None
        assert fp, f"no anomaly file in {d}"
        df, meta = load_anomalies(fp)
        return normalize(df), meta
    raise KeyError(f"unknown section: {section}")


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
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        return "unknown"


def run_section(section, cfg):
    gp_all, m0 = load_section(section, cfg["past"])
    gf_all, m1 = load_section(section, cfg["future"])
    y, X, mr = build(gp_all, gf_all, CUT, cfg["kmax"])
    s = X[:, 0] / max(float(X[:, 0].max()), 1.0)
    base = float(y.mean()) if len(y) else float("nan")
    grid = []
    for k in K_GRID:
        est, lo, hi = MET.precision_at_k(y, s, k, n_boot=N_BOOT, seed=SEED)
        grid.append({"K": k, "est": float(est), "lo": float(lo), "hi": float(hi)})
    two_base = 2.0 * base
    cands = [r["K"] for r in grid if r["lo"] is not None and r["lo"] >= two_base]
    flag_k = max(cands) if cands else 20
    flag_fallback = not bool(cands)
    below = [r["K"] for r in grid if r["est"] is not None and r["est"] <= base]
    band_k = min(below) if below else None
    widths = [(r["hi"] - r["lo"]) if None not in (r["hi"], r["lo"]) else None for r in grid]
    caveats = []
    narrow = [r["K"] for r, w in zip(grid, widths) if w == 0.0]
    if narrow:
        caveats.append("degenerate CI: zero-width interval at K="
                       + ",".join(str(k) for k in narrow)
                       + " (resample-then-rerank artifact on a perfect top-K; "
                         "not a prospective precision claim)")
    if widths and all(w == 0.0 for w in widths if w is not None) and all(w is not None for w in widths):
        caveats.append("all-narrow grid: every K has a zero-width interval")
    return {
        "section": section,
        "pair": f"{cfg['past']}->{cfg['future']}",
        "kmax": cfg["kmax"],
        "n_cells": cfg["kmax"] + 1,
        "files": [m0["name"], m1["name"]],
        "match_rate": float(mr),
        "base": base,
        "n_pos": int(y.sum()),
        "grid": grid,
        "flag_top_k": flag_k,
        "flag_rule": f"largest K with CI-lower >= 2*base (2*base={two_base:.4f})"
                     + ("; none passed, fallback K=20" if flag_fallback else ""),
        "flag_fallback": flag_fallback,
        "band_edge_k": band_k,
        "band_rule": "smallest K with estimate <= base"
                     + ("" if below else "; never reached, null"),
        "status": STATUS,
        "caveats": caveats,
    }


def main():
    t0 = time.time()
    sections = {}
    for section, cfg in PAIRS.items():
        sections[section] = run_section(section, cfg)
        g = sections[section]
        print(f"{section} {g['pair']}: base={g['base']:.4f} n_pos={g['n_pos']}/{g['n_cells']} "
              f"match={g['match_rate']:.3f} flag_top_k={g['flag_top_k']} "
              f"band_edge_k={g['band_edge_k']} [{g['status']}]")
        for r in g["grid"]:
            print(f"  K={r['K']:>3} P@K={r['est']:.3f} [{r['lo']:.3f},{r['hi']:.3f}]")
        for c in g["caveats"]:
            print(f"  CAVEAT: {c}")
    out = {
        "meta": {
            "cut": CUT,
            "k_grid": K_GRID,
            "n_boot": N_BOOT,
            "seed": SEED,
            "model": "B1 past-count only (retrospective, frozen R1)",
            "method_note": "precision@K CI is a resample-then-rerank retrospective display "
                           "statistic (src.gtk1.metrics.precision_at_k), not a prospective "
                           "precision claim",
            "status": STATUS,
            "git": git_hash(),
            "runtime_s": round(time.time() - t0, 1),
        },
        "sections": sections,
    }
    out = clean(out)
    (REPO / "experiments" / "results_operating.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote experiments/results_operating.json in {out['meta']['runtime_s']}s")


if __name__ == "__main__":
    main()
