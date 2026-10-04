"""E14: SRTO-1717 2021->2024 second pair (frozen pipeline; 5th replication pair).
2024A = REPAIRED copy (salvage spike: rebuilt sharedStrings, 5 placeholder-pipe rows dropped;
source file corrupt, repo untouched). Provenance: /tmp repair_spike (see PROGRESS E-salvage entry).
Rules: Depth>=10%, match pipe+2m/0.5m/1h greedy, 100m matched-new (KMAX=420), B1/B2 + lift CI.
Caveats: placeholder rows dropped (distance-only pairing refused); empty depth = N/A per class;
repaired copy is internal evidence, NOT handover-grade — source re-export still required.
Read-only everywhere (source + repaired copy only read).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize
from gtk1.features import build
from gtk1.metrics import ap_lift_ci

OUT = Path(__file__).resolve().parent
SEC = REPO.parent / "Данные для предварительного изучения" / "СРТО-Омск_(1717-1759)"
REPAIRED = Path("/private/var/folders/gv/ymp49j297d1979m9c8hy8_000000gn/T/opencode/repair_spike/GTK1_2024_Anomalii_REPAIRED.xlsx")
KMAX = 420


def run():
    df21, h21 = load_anomalies(sorted(SEC.glob("2021/Аномалии.xls"))[0])
    df24, h24 = load_anomalies(REPAIRED)
    r21, r24 = normalize(df21), normalize(df24)
    ph = r24["pipe"].str.contains("UNRECOVERABLE", na=False)
    dropped = int(ph.sum())
    r24 = r24[~ph].copy()
    y, X, mr = build(r21, r24, 10, KMAX)
    b1 = X[:, 0] / max(X[:, 0].max(), 1)
    stat = ap_lift_ci(y, b1, n=2000, seed=0)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out = {"files": [h21, {**h24, "note": "REPAIRED copy, provenance /tmp repair_spike; source corrupt"}],
           "dropped_placeholder_rows": dropped,
           "counts": {"2021_d10": int((r21["depth"] >= 10).sum()), "2024_d10": int((r24["depth"] >= 10).sum())},
           "match_rate": mr, **stat, "repro": {"git": gh}}
    (OUT / "results_e14.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E14 SRTO-1717 2021->2024 (frozen; 2024 = repaired copy, 5 placeholder rows dropped)",
         f"d>=10: {out['counts']} dropped={dropped} match={mr:.3f} prev={stat['base']:.3f} pos={stat['n_pos']} "
         f"B1={stat['AP']:.3f} base={stat['base']:.3f} liftCI=[{stat['lift_CI'][0]:.3f},{stat['lift_CI'][1]:.3f}]",
         "- caveats: repaired-copy evidence only (re-export still required); 2021 covers ~30/42km."]
    (OUT / "results_e14.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
