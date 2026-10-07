"""Hard check: every Yu-N claim re-derived (2020A strict-fail + salvage, 2020 weld, 2023 all sheets).
Verdict per claim: CONFIRMED / CORRECTED(x). Read-only sources; salvaged CSVs in outputs/.
"""
import json
import sys
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
Y = REPO.parent / "Данные для предварительного изучения" / "Отчет ВТД_Ю-Н_0-154"
OUT = REPO / "outputs"
R = []


def check(name, cond, detail=""):
    R.append({"claim": name, "verdict": "CONFIRMED" if cond else "CORRECTED", "detail": detail})
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""), flush=True)


def main():
    # 1. 2020A container + sheets
    z = zipfile.ZipFile(Y / "2020" / "Аномалии.xlsx")
    names = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]
    check("2020A has 3 sheets", len(names) == 3, str(len(names)))
    # strict read must FAIL (the corrupt claim)
    try:
        pd.read_excel(Y / "2020" / "Аномалии.xlsx", sheet_name="Аномалии", header=3, engine="openpyxl")
        strict_fail = False
    except Exception as e:
        strict_fail = True
    check("2020A anomalies fail strict parse", strict_fail)
    # 2. salvaged 2020 rows
    a = pd.read_csv(OUT / "yn2020_anom_salvaged.csv")
    dc = "Расстояние, м"
    d = pd.to_numeric(a[dc].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    check("2020 salvaged rows ~2621", 2600 <= len(a) <= 2650, str(len(a)))
    check("2020 dist max ~37215", 37000 <= float(d.max()) <= 37500, str(float(d.max())))
    check("2020 dist monotonic non-decreasing", bool((d.dropna().diff().fillna(0) >= 0).all()))
    # 3. 2020 weld log
    w = pd.read_excel(Y / "2020" / "Поперечные сварные швы.xlsx",
                      sheet_name="Поперечные сварные швы", header=3, engine="openpyxl")
    wd = pd.to_numeric(w.iloc[:, 2], errors="coerce")
    check("2020 weld rows ~14095", 14000 <= len(w) <= 14200, str(len(w)))
    check("2020 weld max ~151492", 151000 <= float(wd.max()) <= 152000, str(float(wd.max())))
    # pipe join: salvaged anomalies within 12m of a weld
    wp = np.sort(wd.dropna().values)
    dd = d.dropna().values
    idx = np.searchsorted(wp, dd)
    best = np.full(len(dd), np.inf)
    m = idx < len(wp)
    best[m] = np.abs(wp[idx[m]] - dd[m])
    m2 = idx > 0
    best[m2] = np.minimum(best[m2], np.abs(wp[idx[m2] - 1] - dd[m2]))
    frac = float((best <= 12).mean())
    check("2020 anomalies join welds (>=99% within 12m)", frac >= 0.99, f"{frac:.4f}")
    # 4. 2023 sheets
    xl = pd.ExcelFile(Y / "2023" / "otchet_скорр.xlsx", engine="openpyxl")
    check("2023 has 11 sheets", len(xl.sheet_names) == 11, str(len(xl.sheet_names)))
    pl = pd.read_excel(xl, sheet_name="Трубный журнал", header=0)
    check("2023 pipe log 14160x10", len(pl) == 14160 and len(pl.columns) == 10,
          f"{len(pl)}x{len(pl.columns)}")
    # 5. salvaged 2023 tables
    an = pd.read_csv(OUT / "yn2023_anom_salvaged.csv")
    check("2023 anom salvaged rows ~4400", 4300 <= len(an) <= 4500, str(len(an)))
    for col, lo, hi, nm in [("Дистанция по\nодометру, м", 25000, 26000, "2023 anom dist max ~25655"),
                            ("d,\n%", None, None, None)]:
        pass
    dd2 = pd.to_numeric(an["Дистанция по\nодометру, м"].astype(str).str.replace(",", ".", regex=False),
                        errors="coerce")
    check("2023 anom dist max ~25655", 25000 <= float(dd2.max()) <= 26000, str(float(dd2.max())))
    dep = pd.to_numeric(an["d,\n%"].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    check("2023 anom depth has out-of-range values", bool((dep > 100).any()),
          f"max={float(dep.max())}")
    fe = pd.read_csv(OUT / "yn2023_feat_salvaged.csv")
    check("2023 feat salvaged rows ~21015", 20000 <= len(fe) <= 22000, str(len(fe)))
    (OUT.parent / "experiments" / "results_yn_hard.json").write_text(
        json.dumps({"checks": R}, indent=2, ensure_ascii=False))
    bad = [r for r in R if r["verdict"] != "CONFIRMED"]
    print(f"HARD CHECK: {len(R) - len(bad)}/{len(R)} confirmed; failed: {[b['claim'] for b in bad]}")


if __name__ == "__main__":
    main()
