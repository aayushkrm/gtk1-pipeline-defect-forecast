"""features: 100m-cell build (consolidated from e07b; identical).
Pre-registered 7 past-only features: n_past, nlag, maxd, meand, gwan, mech, npipes.
Labels: matched-new binary (Y=1 iff >=1 UNMATCHED future corr row in cell).
R1 frozen semantics: the depth cut applies BEFORE matching, so a past row below
the cut can never match a future row above it. A defect that crosses the reporting
threshold between surveys therefore counts as newly-reported BY DESIGN (report-
threshold semantics per GUARDRAILS.md, not physical initiation). Do not reorder
without a pipeline version bump plus full recompute and reviewer approval.
"""
import numpy as np
import pandas as pd
from .match import match_win

FEATS = ["n_past", "nlag", "maxd", "meand", "gwan", "mech", "npipes"]
WIDTH_M = 100


def build(gp_all, gf_all, cut, kmax, width_m=WIDTH_M):
    # Precondition: finite dist (normalize() drops non-finite rows first). NaN dist here
    # raises IntCastingNaNError by construction; never bypass normalize().
    gp = gp_all[gp_all["depth"] >= cut].copy()
    gf = gf_all[gf_all["depth"] >= cut].copy()
    m = match_win(gp, gf, 2)
    mr = float(m.mean()) if len(m) else 0.0
    new = gf[~np.asarray(m)]
    newc = new[new["corr"]]
    ck = lambda g: (g["dist"] // width_m).astype(int).clip(0, kmax)
    y = (newc.groupby(ck(newc)).size().reindex(range(kmax + 1), fill_value=0).values > 0).astype(int)
    gp = gp_all[gp_all["depth"] >= cut].copy()
    past = gp[gp["corr"]]
    X = pd.DataFrame(index=range(kmax + 1))
    X["n_past"] = past.groupby(ck(past)).size().reindex(X.index, fill_value=0).astype(float)
    X["nlag"] = X["n_past"].shift(1, fill_value=0) + X["n_past"].shift(-1, fill_value=0)
    X["maxd"] = past.groupby(ck(past))["depth"].max().reindex(X.index, fill_value=0).astype(float)
    X["meand"] = past.groupby(ck(past))["depth"].mean().reindex(X.index, fill_value=0).astype(float)
    gw = gp[gp["char"].str.contains("кольцевого", na=False)]
    X["gwan"] = gw.groupby(ck(gw)).size().reindex(X.index, fill_value=0).astype(float)
    me = gp[gp["char"].str.contains("механич|вмятина|заводск", case=False, na=False)]
    X["mech"] = me.groupby(ck(me)).size().reindex(X.index, fill_value=0).astype(float)
    X["npipes"] = past.groupby(ck(past))["pipe"].nunique().reindex(X.index, fill_value=0).astype(float)
    return y, X[FEATS].values, mr


ABCRANK = {"c": 0, "b": 1, "a": 2}


def cell_abc(g, kmax, width_m=WIDTH_M):
    """Per-cell worst repair class from the danger passthrough (sanctioned ABC track).
    Additive diagnostic: reads g["danger"] values (a)/(b)/(c), returns per-cell worst level
    (2=a most severe, 0=c or empty/absent) plus per-class row counts. Never alters build().
    n_c counts rows explicitly labeled (c); clean cells read n_a=n_b=n_c=0 with worst=0,
    so yellow (C) separates from white (clean). Cells clip to [0, kmax] by construction."""
    ck = (g["dist"] // width_m).astype(int).clip(0, kmax)
    idx = pd.Index(range(kmax + 1))
    if len(g) == 0 or "danger" not in g.columns:
        return pd.DataFrame({"worst": 0, "n_a": 0, "n_b": 0, "n_c": 0}, index=idx)
    dang = g["danger"].astype(str).str.lower()
    lvl = (dang.str.extract(r"\(([abc])\)", expand=False)
           .map(ABCRANK).fillna(0).astype(int))
    gl = pd.Series(lvl.to_numpy(), index=ck.to_numpy())
    worst = gl.groupby(level=0).max().reindex(idx, fill_value=0).astype(int)
    arr = lvl.to_numpy()
    keys = ck.to_numpy()
    out = pd.DataFrame({"worst": worst})
    for code, col in ((2, "n_a"), (1, "n_b")):
        col_s = pd.Series((arr == code).astype(int), index=keys).groupby(level=0).sum()
        out[col] = col_s.reindex(idx, fill_value=0).astype(int)
    # n_c counts explicitly-labeled-(c) rows only (empty/absent danger also maps to
    # level 0, so it cannot come from the level map): clean cells read n_a=n_b=n_c=0.
    lab_c = (dang == "(c)").to_numpy().astype(int)
    out["n_c"] = (pd.Series(lab_c, index=keys).groupby(level=0).sum()
                  .reindex(idx, fill_value=0).astype(int))
    return out
