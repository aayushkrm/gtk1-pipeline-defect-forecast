"""E05: SRTO-1608 replication with the FROZEN ON pipeline (external test, no refit).
Section SRTO-Omsk 1608-1717 (~104km, D1220): train 2016->2021, test 2021->2024.
Same rules: Depth>=10%, match same-pipe + |dd|<=2 + |doff|<=0.5 + |dh|<=1h (greedy),
100m matched-new binary, B1/B2/B3. Report per-pair AP/prev/match separately; no pooling.
Supports .xls (xlrd) + .xlsx (openpyxl). Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e04b_robust import match_win
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
SEC = REPO.parent / "Данные для предварительного изучения" / "СРТО-Омск_(1608 – 1717)"
W, KMAX = 100, 1040
YEARS = (2016, 2021, 2024)

def load_any(year):
    d = SEC / str(year)
    cands = sorted(d.glob("Аномалии*.xls*"))
    assert cands, f"no anomaly file in {d}"
    fp = cands[0]
    if fp.suffix == ".xlsx":
        df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine="openpyxl")
    else:
        df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine="xlrd")
    df.columns = [str(c).strip() for c in df.columns]
    return df, {"name": fp.name, "bytes": fp.stat().st_size, "mtime": fp.stat().st_mtime}

def norm(df):
    g = lambda *k: next((c for c in df.columns if all(x.lower() in c.lower() for x in k)), None)
    cd, cc, cp = g("расстояние"), g("глубина"), g("номер", "трубы")
    co = g("левого", "начала") or g("левого")
    cr = g("ориентация", "максимума") or g("ориентация", "центра")
    ch = [c for c in df.columns if "характер" in c.lower()][0]
    o = pd.DataFrame({"dist": pd.to_numeric(df[cd], errors="coerce"),
                      "depth": pd.to_numeric(df[cc], errors="coerce"),
                      "pipe": df[cp].astype(str).str.strip().str.replace(r"\.0$", "", regex=True),
                      "off": pd.to_numeric(df[co], errors="coerce") if co else np.nan,
                      "ori": df[cr].astype(str) if cr else "", "char": df[ch].astype(str)})
    o = o.dropna(subset=["dist"])
    o = o[o["depth"] >= 10].copy()
    o["corr"] = o["char"].str.contains("оррози", na=False)
    o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    o["km"] = o["dist"] // 1000
    o["cell"] = (o["dist"] // W).astype(int).clip(0, KMAX)
    return o

def run():
    frames, hashes = {}, []
    for y in YEARS:
        df, h = load_any(y)
        frames[y] = norm(df)
        hashes.append(h)
    out = {"section": "SRTO-Omsk 1608-1717", "pairs": {"train": "2016->2021", "test": "2021->2024"},
           "files": hashes,
           "counts": {str(y): int(len(frames[y])) for y in YEARS}}
    for tag, gp, gf in (("train", frames[2016], frames[2021]), ("test", frames[2021], frames[2024])):
        m = match_win(gp, gf, 2)
        new = gf[~m]; new = new[new["corr"]]
        y = (new.groupby("cell").size().reindex(range(KMAX + 1), fill_value=0).values > 0).astype(int)
        past = (gp[gp["corr"]].groupby("cell").size().reindex(range(KMAX + 1), fill_value=0).values.astype(float))
        ppast = set(gp[gp["corr"]]["pipe"])
        # B3 past-only (mirrors e02_matched.py:127-128): per-cell pipes from the
        # PAST frame gp, never the future frame gf. First branch is 1 iff the
        # past cell holds corr rows, so value == (past > 0); gf is not read.
        gpipes = gp[gp["corr"]].groupby("cell")["pipe"].apply(set)
        b3 = np.array([1.0 if (gpipes.get(k, set()) & ppast)
                       else (1.0 if past[k] > 0 else 0.0) for k in range(KMAX + 1)])
        b1 = past / max(past.max(), 1)
        b2 = np.full(KMAX + 1, float(y.mean()))
        cell = {"match_rate": float(m.mean()), "prev": float(y.mean()), "n_pos": int(y.sum())}
        for name, s in (("B1", b1), ("B2", b2), ("B3", b3)):
            cell[name] = float(average_precision_score(y, s)) if y.sum() > 0 else 0.0
        out["pairs"][tag] = cell
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e05.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E05 SRTO-1608 replication, frozen pipeline (Depth>=10, match pipe+2m, 100m matched-new)",
         f"counts: {out['counts']}"]
    for tag, label in (("train", "2016->2021"), ("test", "2021->2024")):
        v = out["pairs"][tag]
        L.append(f"- {tag} ({label}): match={v['match_rate']:.3f} prev={v['prev']:.3f} "
                 f"pos={v['n_pos']} B1={v['B1']:.3f} B2(base)={v['B2']:.3f} B3={v['B3']:.3f}")
    (OUT / "results_e05.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
