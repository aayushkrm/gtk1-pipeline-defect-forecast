"""evaluate_pair: matched-new label build + B1 scoring for ANY completed pair.

Recalibration engine for docs/PROSPECTIVE_RUNBOOK.md §3 (replaces the old
"same pattern as e11_pk1.py" pointer with a runnable command).
Frozen R1 machinery throughout: Depth>=10%, pipe+2m/0.5m/1h greedy match, 100m cells,
B1 past-count ranking, AP vs base + 2000 lift CI, P@K with base comparator.
Usage: python3 experiments/evaluate_pair.py --section on|pk1 --past YYYY --future YYYY
        [--k 20] [--out experiments/results_eval_<auto>.json]
Read-only raw data. Writes one aggregate JSON (committable).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "triage"))
from gtk1.features import build
from gtk1 import metrics as MET
from prospective import load_section, SECTIONS

CUT = 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", choices=tuple(SECTIONS), required=True)
    ap.add_argument("--past", type=int, required=True)
    ap.add_argument("--future", type=int, required=True)
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cfg = SECTIONS[a.section]
    gp_all, m0 = load_section(a.section, a.past)
    gf_all, m1 = load_section(a.section, a.future)
    y, X, mr = build(gp_all, gf_all, CUT, cfg["kmax"])
    s = X[:, 0] / max(float(X[:, 0].max()), 1.0)
    lc = MET.ap_lift_ci(y, s)
    est, lo, hi = MET.precision_at_k(y, s, a.k)
    out = {
        "section": a.section, "past": a.past, "future": a.future, "cut": CUT,
        "files": [m0["name"], m1["name"]],
        "match_rate": mr, "prev": float(y.mean()),
        "n_pos": int(y.sum()), "n": len(y),
        "B1": {"AP": lc["AP"], "base": lc["base"], "lift_CI": lc["lift_CI"]},
        f"P@{a.k}": {"est": est, "CI": [lo, hi], "base": lc["base"]},
    }
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    tag = a.out or f"experiments/results_eval_{a.section}_{a.past}_{a.future}.json"
    (REPO / tag).write_text(json.dumps(out, indent=2))
    print(f"{a.section} {a.past}->{a.future}: AP={lc['AP']:.4f} base={lc['base']:.4f} "
          f"match={mr:.4f} P@{a.k}={est:.3f} [{lo:.3f},{hi:.3f}] -> {tag}")


if __name__ == "__main__":
    main()
