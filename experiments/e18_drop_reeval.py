"""E18: October 2026 partner drop — frozen-pair recheck + first-run evaluations.

Part 1 (frozen recheck): ON 2021->2025, PK1 2022->2025, SRTO1608 2021->2024 run on BOTH
the old raw room and the new drop tree through the same frozen machinery. Any delta is the
drop's impact, not a pipeline change.

Part 2 (newly unlocked): PK2 2020->2025 and YN 2020->2023 first-ever runs (old copies of
their 2025/2023 files were unreadable; the drop fixes them).

Part 3 (new sections): NVP, NB, UKPG2, SXV (+SXV long gap), singles PK1-110-242, OGRS3.

Frozen R1 throughout: depth>=10% before matching, pipe+2m/0.5m/1h greedy, 100m cells,
B1 past-count ranking, AP vs base + lift CI + P@20. Aggregates only; raw never stored.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gtk1.io import load_anomalies, normalize, _apply_tolerant_xlrd  # noqa: E402
from gtk1.features import build  # noqa: E402
from gtk1 import metrics as MET  # noqa: E402

OLD = ROOT.parent / "Данные для предварительного изучения"
NEW = ROOT.parent / "Датасет ВТД"
OUT = ROOT / "experiments" / "results_e18_drop_reeval.json"
CUT = 10


def read_any(fp: Path, sheet: str | int, header: int) -> pd.DataFrame:
    """Standard/tolerant read of one sheet; engine by extension with PK sniff."""
    fp = Path(fp)
    is_zip = fp.suffix.lower() == ".xlsx" or open(fp, "rb").read(2) == b"PK"
    try:
        return pd.read_excel(fp, sheet_name=sheet, header=header,
                             engine="openpyxl" if is_zip else "xlrd")
    except Exception:
        if not is_zip:
            _apply_tolerant_xlrd()
            return pd.read_excel(fp, sheet_name=sheet, header=header, engine="xlrd")
        raise


def find_file(d: Path, *prefixes: str) -> Path | None:
    for f in sorted(d.iterdir()):
        low = f.name.casefold()
        if any(low.startswith(p.casefold()) for p in prefixes) and f.suffix.lower() in (".xls", ".xlsx"):
            return f
    return None


def find_col(df: pd.DataFrame, *subs: str, exclude: tuple[str, ...] = ()) -> str | None:
    for c in df.columns:
        cs = str(c).replace("\n", " ").lower()
        if all(s in cs for s in subs) and not any(x in cs for x in exclude):
            return c
    return None


def manual_frame(df: pd.DataFrame, cmap: dict, kmax: int | None = None) -> pd.DataFrame:
    """Mirror normalize() for custom layouts, plus a comma-decimal tier."""
    def col(name):
        c = cmap.get(name)
        if c is None:
            return None
        if callable(c):
            c = c(df)
        if c is None:
            return None
        return df[c]

    def num(c):
        if c is None:
            return float("nan")
        s = c.astype(str).str.replace(",", ".", regex=False)
        return pd.to_numeric(s, errors="coerce")

    p = col("pipe")
    oriv = col("ori")
    o = pd.DataFrame({
        "dist": num(col("dist")),
        "depth": num(col("depth")),
        "pipe": p.astype(str).str.strip().str.replace(r"\.0$", "", regex=True) if p is not None else "",
        "off": float("nan"),
        "ori": oriv.astype(str) if oriv is not None else "",
        "char": col("char").astype(str),
        "abbr": "",
        "danger": "",
        "kbd": float("nan"),
    }).dropna(subset=["dist"]).copy()
    o["corr"] = o["char"].str.contains("оррози", na=False)
    o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    if kmax is not None:
        o["cell"] = (o["dist"] // 100).astype(int).clip(0, kmax)
    return o


SECTIONS = {
    # key: dir, resolver(year) -> (fp, sheet, header, custom-map or None), kmax
    "on": {"dir": "Омск-Новосибирск (392-526)", "kmax": 1330, "kind": "std"},
    "pk1": {"dir": "Парабель-Кузбасс-1 (572-714)", "kmax": 1400, "kind": "std"},
    "srto1608": {"dir": "СРТО-Омск_(1608 – 1717)", "kmax": 1040, "kind": "std"},
    "pk2": {"dir": "Парабель-Кузбасс-2 (0-110)", "kmax": 1100, "kind": "mixed"},
    "yn": {"dir": "Отчет ВТД_Ю-Н_0-154", "kmax": 1540, "kind": "mixed"},
    "nvp": {"dir": "Нижневартовский ГПЗ-Парабель I (306-448 км) (КС Вертикос - КС Парабель)", "kmax": 1420, "kind": "std"},
    "nb": {"dir": "Новосибирск - Барнаул 0 - 123 км", "kmax": 1230, "kind": "mixed"},
    "ukpg2": {"dir": "УКПГ2 - АГРС 216-388 км", "kmax": 1720, "kind": "std"},
    "sxv": {"dir": "СХВ_0-96", "kmax": 960, "kind": "std"},
    "pk1_110": {"dir": "Парабель - Кузбасс 1 110-242", "kmax": 1320, "kind": "single"},
    "ogrs3": {"dir": "Отвод ГРС-3 - Барнаул", "kmax": 100, "kind": "single"},
}

def _pipe_col(df: pd.DataFrame):
    return find_col(df, "трубы", exclude=("длина", "номер")) or find_col(df, "номер", "трубы")


YN2023_MAP = {
    "dist": lambda df: find_col(df, "дистанц"),
    "depth": lambda df: next((c for c in df.columns
                              if str(c).replace("\n", " ").strip().lower().startswith("d,")
                              and "%" in str(c)), None),
    "pipe": _pipe_col,
    "char": lambda df: find_col(df, "характер"),
    "ori": lambda df: find_col(df, "ориент"),
}
PK1_110_MAP = {
    "dist": lambda df: find_col(df, "дистанц"),
    "depth": lambda df: find_col(df, "глубина", "%") or find_col(df, "глубина"),
    "pipe": _pipe_col,
    "char": lambda df: find_col(df, "характер"),
    "ori": lambda df: find_col(df, "ориент"),
}
NB2020_MAP = {
    "dist": lambda df: find_col(df, "дистанц"),
    "depth": lambda df: find_col(df, "глубина", "%") or find_col(df, "глубина"),
    "pipe": lambda df: find_col(df, "номер", "трубы"),
    "char": lambda df: find_col(df, "характер"),
    "ori": None,
}
OGRS3_MAP = {
    "dist": lambda df: find_col(df, "расстоян"),
    "depth": lambda df: find_col(df, "глубина", "%") or find_col(df, "глубина"),
    "pipe": lambda df: find_col(df, "номер", "трубы"),
    "char": lambda df: find_col(df, "характер"),
    "ori": None,
}


def load_survey(root: Path, key: str, year: int) -> tuple[pd.DataFrame, dict]:
    cfg = SECTIONS[key]
    d = root / cfg["dir"] / str(year)
    kmax = cfg["kmax"]
    if key == "on":
        fp = next(d / n for n in ("Аномалии.xlsx", "Аномалии_.xlsx") if (d / n).exists())
        df = read_any(fp, "Аномалии", 3)
        meta = {"name": fp.name}
        return normalize(df, kmax=kmax), meta
    if key == "pk2":
        fp = find_file(d, "аномали")
        if year == 2020:
            df = read_any(fp, "Аномалии", 3)
        else:
            df = read_any(fp, "аномалии", 0)
            if "Значение глубины" in df.columns:
                val = pd.to_numeric(df["Значение глубины"].astype(str).str.replace(",", ".", regex=False),
                                    errors="coerce")
                if "Единица измерения" in df.columns:
                    unit = df["Единица измерения"].astype(str).str.strip().str.lower()
                else:
                    unit = pd.Series("", index=df.index)
                df = df.drop(columns=["Значение глубины"])
                df["Глубина, %"] = val.where(unit.eq("% от t"), other=float("nan"))
        meta = {"name": fp.name}
        return normalize(df, kmax=kmax), meta
    if key == "yn":
        if year == 2020:
            fp = find_file(d, "аномали")
            df = read_any(fp, "Аномалии", 3)
            return normalize(df, kmax=kmax), {"name": fp.name}
        fp = find_file(d, "otchet")
        df = read_any(fp, "Журнал выявленных аномалий", 0)
        return manual_frame(df, YN2023_MAP, kmax), {"name": fp.name}
    if key == "nb" and year == 2020:
        fp = find_file(d, "таблица дефектов")
        df = read_any(fp, 0, 0)
        return manual_frame(df, NB2020_MAP, kmax), {"name": fp.name}
    if key == "ogrs3":
        fp = find_file(d, "аномали")
        df = read_any(fp, "Лист1", 2)
        return manual_frame(df, OGRS3_MAP, kmax), {"name": fp.name}
    if key == "pk1_110":
        fp = find_file(d, "аномали")
        df = read_any(fp, "Журнал выявленных аномалий", 0)
        return manual_frame(df, PK1_110_MAP, kmax), {"name": fp.name}
    fp = find_file(d, "аномали")
    df = read_any(fp, "Аномалии", 3)
    return normalize(df, kmax=kmax), {"name": fp.name}


def evaluate(root: Path, key: str, past: int, future: int, kmax: int) -> dict:
    gp, m0 = load_survey(root, key, past)
    gf, m1 = load_survey(root, key, future)
    y, X, mr = build(gp, gf, CUT, kmax)
    s = X[:, 0] / max(float(X[:, 0].max()), 1.0)
    lc = MET.ap_lift_ci(y, s)
    est, lo, hi = MET.precision_at_k(y, s, 20)
    return {
        "section": key, "past": past, "future": future,
        "files": [m0["name"], m1["name"]],
        "n_past_rows": int(len(gp)), "n_fut_rows": int(len(gf)),
        "match_rate": float(mr), "prev": float(y.mean()), "n_pos": int(y.sum()), "n": int(len(y)),
        "B1": {"AP": lc["AP"], "base": lc["base"], "lift_CI": lc["lift_CI"]},
        "P@20": {"est": est, "CI": [lo, hi], "base": lc["base"]},
    }


def coverage(root: Path, key: str, year: int) -> dict:
    g, m = load_survey(root, key, year)
    top = g["char"].value_counts().head(5)
    return {
        "section": key, "year": year, "file": m["name"], "rows": int(len(g)),
        "rows_depth_ge10": int((g["depth"] >= CUT).sum()),
        "upper_rows_ge10": int(((g["depth"] >= 10) & (~g["corr"])).sum()),
        "corr_rows_ge10": int(((g["depth"] >= 10) & g["corr"]).sum()),
        "dist_min": float(np.nanmin(g["dist"])) if len(g) else None,
        "dist_max": float(np.nanmax(g["dist"])) if len(g) else None,
        "char_top": {str(k): int(v) for k, v in top.items()},
    }


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def main() -> None:
    out: dict = {}
    frozen = {}

    # Part 1: frozen-pair recheck, both rooms
    for key, (past, future) in {"on": (2021, 2025), "pk1": (2022, 2025), "srto1608": (2021, 2024)}.items():
        kmax = SECTIONS[key]["kmax"]
        old_res = evaluate(OLD, key, past, future, kmax)
        new_res = evaluate(NEW, key, past, future, kmax)
        frozen[key] = {"old_room": old_res, "new_drop": new_res,
                       "delta_AP": float(new_res["B1"]["AP"] - old_res["B1"]["AP"]),
                       "delta_base": float(new_res["B1"]["base"] - old_res["B1"]["base"])}
        print(f"[recheck] {key} {past}->{future}: AP old={old_res['B1']['AP']:.4f} new={new_res['B1']['AP']:.4f} "
              f"base old={old_res['B1']['base']:.4f} new={new_res['B1']['base']:.4f}")

    # Part 2: newly unlocked pairs
    unlocked = {}
    for key, (past, future) in {"pk2": (2020, 2025), "yn": (2020, 2023)}.items():
        kmax = SECTIONS[key]["kmax"]
        res = evaluate(NEW, key, past, future, kmax)
        unlocked[key] = res
        print(f"[unlocked] {key} {past}->{future}: AP={res['B1']['AP']:.4f} base={res['B1']['base']:.4f} "
              f"match={res['match_rate']:.3f} pos={res['n_pos']}/{res['n']}")

    # Part 3: new sections
    new_pairs = {}
    for key, pairs in {
        "nvp": [(2016, 2021)],
        "nb": [(2020, 2025)],
        "ukpg2": [(2016, 2023)],
        "sxv": [(2016, 2020), (2020, 2021), (2021, 2022), (2016, 2022)],
    }.items():
        kmax = SECTIONS[key]["kmax"]
        for past, future in pairs:
            tag = f"{key}_{past}_{future}"
            res = evaluate(NEW, key, past, future, kmax)
            new_pairs[tag] = res
            print(f"[new] {tag}: AP={res['B1']['AP']:.4f} base={res['B1']['base']:.4f} "
                  f"match={res['match_rate']:.3f} pos={res['n_pos']}/{res['n']}")

    singles = {}
    for key, year in {"pk1_110": 2018, "ogrs3": 2025}.items():
        res = coverage(NEW, key, year)
        singles[f"{key}_{year}"] = res
        print(f"[single] {key} {year}: rows={res['rows']} d10={res['rows_depth_ge10']} "
              f"corr10={res['corr_rows_ge10']} span={res['dist_min']}..{res['dist_max']}")

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "cut": CUT, "match": "pipe+2m/0.5m/1h greedy (frozen R1)",
        "frozen_recheck": frozen, "unlocked_first_run": unlocked,
        "new_section_pairs": new_pairs, "singles_coverage": singles,
        "repro": {"git": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                                        capture_output=True, text=True).stdout.strip()},
    }
    OUT.write_text(json.dumps(_clean(out), ensure_ascii=False, indent=1, allow_nan=False))
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
