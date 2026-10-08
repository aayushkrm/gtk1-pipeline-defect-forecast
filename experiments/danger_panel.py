"""danger_panel: ABC-class shares per section-year (supports Leonid's formula-drift task).

Reads anomaly tables read-only, counts Опасность values (a)/(b)/(c) at all depths
(no cut: the question is what the program assigned, not what we model).
Pre/post-2022 split exposes the ~2022 requirement-lowering break Vlad described.
Writes experiments/results_danger.json (counts + shares only). No raw values.
"""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies  # noqa: E402

DATA_ROOT = REPO.parent / "Данные для предварительного изучения"
TARGETS = [
    ("ON", "Омск-Новосибирск (392-526)", "2016", ("Аномалии.xlsx",)),
    ("ON", "Омск-Новосибирск (392-526)", "2021", ("Аномалии.xlsx",)),
    ("ON", "Омск-Новосибирск (392-526)", "2025", ("Аномалии.xlsx", "Аномалии_.xlsx")),
    ("SRTO-1608", "СРТО-Омск_(1608 – 1717)", "2016", ("Аномалии.xls",)),
    ("SRTO-1608", "СРТО-Омск_(1608 – 1717)", "2021", ("Аномалии.xls",)),
    ("SRTO-1608", "СРТО-Омск_(1608 – 1717)", "2024", ("Аномалии.xls", "Аномалии1.xls")),
    ("PK1", "Парабель-Кузбасс-1 (572-714)", "2022", ("Аномалии.xls",)),
    ("PK1", "Парабель-Кузбасс-1 (572-714)", "2025", ("Аномалии.xls",)),
    ("SRTO-1717", "СРТО-Омск_(1717-1759)", "2021", ("Аномалии.xls",)),
    ("SRTO-1717", "СРТО-Омск_(1717-1759)", "2024", ("Аномалии.xlsx",)),
    ("PK2", "Парабель-Кузбасс-2 (0-110)", "2020", ("Аномалии.xlsx",)),
]


def danger_col(df):
    for c in df.columns:
        if "опас" in str(c).lower():
            return c
    return None


def main():
    rows = {}
    for section, sdir, year, cands in TARGETS:
        d = DATA_ROOT / sdir / str(year)
        fp = next((d / n for n in cands if (d / n).exists()), None)
        if fp is None:
            rows[f"{section} {year}"] = {"status": "file-missing"}
            continue
        try:
            df, _ = load_anomalies(str(fp))
        except Exception as e:
            rows[f"{section} {year}"] = {"status": f"unreadable: {type(e).__name__}"}
            print(f"{section} {year}: UNREADABLE {type(e).__name__}")
            continue
        col = danger_col(df)
        if col is None:
            rows[f"{section} {year}"] = {"status": "no-danger-column", "n": int(len(df))}
            continue
        v = df[col].astype(str)
        n = len(v)
        counts = {k: int((v == k).sum()) for k in ("(a)", "(b)", "(c)")}
        other = n - sum(counts.values()) - int(v.isna().sum())
        rows[f"{section} {year}"] = {
            "status": "ok", "n": n,
            "counts": counts,
            "empty_share": float(v.isna().mean()),
            "other_values_share": float(other / max(n, 1)),
            "a_share": counts["(a)"] / max(n, 1),
            "ab_share": (counts["(a)"] + counts["(b)"]) / max(n, 1),
        }
        r = rows[f"{section} {year}"]
        print(f"{section} {year}: n={n} a={counts['(a)']} b={counts['(b)']} "
              f"c={counts['(c)']} empty={r['empty_share']:.3f} other={r['other_values_share']:.3f}")
    out = {"rows": rows}
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    (Path(__file__).resolve().parent / "results_danger.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
