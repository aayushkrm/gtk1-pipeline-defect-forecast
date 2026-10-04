"""E08: vanished-row depth audit + repair-exclusion proxy (release-blocker, reviewer rounds 2-3).
Forward matcher flags FUTURE rows; here reverse-match flags PAST rows with a future partner.
Vanished = past corr rows with no future partner (pipe+2m/0.5m/1h, greedy, cut>=10%).
Report depth distributions (median, tail>=20%/>=30%) for matched-past vs vanished-past,
corr-only, ON train (16->21) + test (21->25). Deep-vanished fraction = repair/miss suspect rate.
No repair logs exist in VTD package -> deep-vanished cannot be excluded, only quantified;
repair-log request logged as data dependency. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom, PARAMS
from e04b_robust import match_win
from e07_ablation import raw

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]

def audit(gp_all, gf_all, cut, tag):
    gp = gp_all[gp_all["depth"] >= cut].copy()
    gf = gf_all[gf_all["depth"] >= cut].copy()
    past_has_partner = match_win(gf, gp, 2)  # flags PAST rows (gf<->gp swapped roles)
    assert len(past_has_partner) == len(gp)
    matched = gp[past_has_partner]
    vanished = gp[~past_has_partner]
    def desc(d):
        d = d[d["corr"]]["depth"]
        return {"n": int(len(d)), "med": float(d.median()) if len(d) else None,
                "tail20": float((d >= 20).mean()) if len(d) else 0.0,
                "tail30": float((d >= 30).mean()) if len(d) else 0.0}
    return {"vanished_frac": float((~past_has_partner).mean()),
            "matched_past": desc(matched), "vanished_past": desc(vanished)}

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    out = {"cut": 10, "pairs": {}}
    for tag, a, b in (("train_16_21", r16, r21), ("test_21_25", r21, r25)):
        out["pairs"][tag] = audit(a, b, 10, tag)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e08.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E08 vanished-row depth audit (ON, cut>=10, corr-only, reverse greedy match)"]
    for tag, v in out["pairs"].items():
        L.append(f"- {tag}: vanished_frac={v['vanished_frac']:.3f} "
                 f"matched med={v['matched_past']['med']} tail20/30={v['matched_past']['tail20']:.3f}/{v['matched_past']['tail30']:.3f} | "
                 f"vanished med={v['vanished_past']['med']} tail20/30={v['vanished_past']['tail20']:.3f}/{v['vanished_past']['tail30']:.3f}")
    L.append("- repair logs: absent from VTD package; deep-vanished (tail30) quantified above, exclusion pending partner data.")
    (OUT / "results_e08.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
