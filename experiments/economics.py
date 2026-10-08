"""economics: parametric dig-plan cost framework (costs ILLUSTRATIVE until partner names figures).

Regulation rule (Vlad, meeting 08.10.2026): A = repair-yes, B/C = monitor.
Inputs: committed triage/abc_*.json (red/orange cells) + unit costs via CLI.
Outputs: dig counts per section, expected cost equation, miss exposure readout.
No cost figure here is real. Framework complete; numbers pending partner.
Read-only committed artifacts. Writes experiments/results_economics.json (aggregates).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRI = REPO / "triage"

SECTIONS = ["on_2025", "pk1_2025", "srto_2024", "srto1717_2021"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dig-cost", type=float, default=1000000.0,
                    help="ILLUSTRATIVE cost per dig in RUB (partner to confirm)")
    ap.add_argument("--miss-cost", type=float, default=10000000.0,
                    help="ILLUSTRATIVE cost per missed critical in RUB (partner to confirm)")
    ap.add_argument("--include-orange", action="store_true",
                    help="also dig orange (B) cells; default digs red (A) cells only")
    a = ap.parse_args()
    plan, digs, exposed = {}, 0, 0
    for tag in SECTIONS:
        d = json.loads((TRI / f"abc_{tag}.json").read_text())
        red = [i for i, v in enumerate(d["worst"]) if v == 2]
        orange = [i for i, v in enumerate(d["worst"]) if v == 1]
        dig_here = red + (orange if a.include_orange else [])
        plan[tag] = {"dig_cells": len(dig_here), "red_cells": len(red),
                     "orange_cells": len(orange),
                     "monitored_not_dug": 0 if a.include_orange else len(orange)}
        digs += len(dig_here)
        exposed += 0 if a.include_orange else len(orange)
    out = {
        "rule": "A=repair, B/C=monitor (Vlad); red cells dug" +
                (" + orange cells dug" if a.include_orange else ""),
        "unit_costs_rub": {"dig_cost": a.dig_cost, "miss_cost": a.miss_cost,
                           "status": "ILLUSTRATIVE — partner to confirm"},
        "per_section": plan,
        "total_digs": digs,
        "expected_dig_cost_rub": digs * a.dig_cost,
        "orange_left_unrepaired": exposed,
        "miss_exposure_rub": exposed * a.miss_cost,
    }
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    (Path(__file__).resolve().parent / "results_economics.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(f"digs={digs} cost={out['expected_dig_cost_rub']:,.0f}RUB "
          f"orange_exposed={exposed} (illustrative units)")


if __name__ == "__main__":
    main()
