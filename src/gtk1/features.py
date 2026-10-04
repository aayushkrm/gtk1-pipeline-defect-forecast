"""features: 100m-cell build (consolidated from e07b; identical).
Pre-registered 7 past-only features: n_past, nlag, maxd, meand, gwan, mech, npipes.
Labels: matched-new binary (Y=1 iff >=1 UNMATCHED future corr row in cell).
"""
import numpy as np
import pandas as pd
from .match import match_win

FEATS = ["n_past", "nlag", "maxd", "meand", "gwan", "mech", "npipes"]
WIDTH_M = 100


def build(gp_all, gf_all, cut, kmax, width_m=WIDTH_M):
    gp = gp_all[gp_all["depth"] >= cut].copy()
    gf = gf_all[gf_all["depth"] >= cut].copy()
    m = match_win(gp, gf, 2)
    mr = float(m.mean())
    new = gf[~np.asarray(m)]
    newc = new[new["corr"]]
    ck = lambda g: (g["dist"] // width_m).astype(int).clip(0, kmax)
    y = (newc.groupby(ck(newc)).size().reindex(range(kmax + 1), fill_value=0).values > 0).astype(int)
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
