"""metrics: AP + bootstrap CIs + paired deltas + P@K (consolidated from E02/E03/E07b)."""
import warnings

import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve


def ap(y, s):
    return float(average_precision_score(y, s)) if np.asarray(y).sum() > 0 else 0.0


def ap_lift_ci(y, s, n=2000, seed=0):
    """AP, base, lift and lift CI (cell bootstrap). The reviewer's 'single number'."""
    y = np.asarray(y)
    s = np.asarray(s)
    if len(y) == 0:
        warnings.warn("ap_lift_ci: empty input; returning NaN interval", UserWarning, stacklevel=2)
        return {"AP": float("nan"), "base": float("nan"), "lift": float("nan"),
                "lift_CI": [float("nan"), float("nan")], "n_pos": 0, "n": 0}
    base = float(y.mean())
    a = ap(y, s)
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].sum() > 0:
            bs.append(float(average_precision_score(y[i], s[i]) - y[i].mean()))
    if len(bs) == 0:
        warnings.warn("ap_lift_ci: no bootstrap resample contained positives; returning NaN interval",
                      UserWarning, stacklevel=2)
        return {"AP": a, "base": base, "lift": a - base,
                "lift_CI": [float("nan"), float("nan")],
                "n_pos": int(y.sum()), "n": len(y)}
    return {"AP": a, "base": base, "lift": a - base,
            "lift_CI": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "n_pos": int(y.sum()), "n": len(y)}


def paired_delta_ci(y, a, b, n=1000, seed=0):
    """Paired bootstrap CI of AP(a)-AP(b) on the same resamples. For beat-B1 proof."""
    y = np.asarray(y)
    a = np.asarray(a)
    b = np.asarray(b)
    if len(y) == 0:
        warnings.warn("paired_delta_ci: empty input; returning NaN interval", UserWarning, stacklevel=2)
        return 0.0, float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    d0 = ap(y, a) - ap(y, b)
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].sum() > 0:
            bs.append(float(average_precision_score(y[i], a[i]) - average_precision_score(y[i], b[i])))
    if len(bs) == 0:
        warnings.warn("paired_delta_ci: no bootstrap resample contained positives; returning NaN interval",
                      UserWarning, stacklevel=2)
        return d0, float("nan"), float("nan")
    return d0, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def precision_at_k(y, score, k, n_boot=2000, seed=7):
    """Precision@K with cell-bootstrap CI.

    Estimand note: each bootstrap resample draws cells with replacement,
    then re-ranks the resampled cells by score and takes the top-K.
    The interval reflects resample-then-rerank variability of that
    retrospective display statistic, not a prospective precision claim.
    """
    y = np.asarray(y)
    score = np.asarray(score)
    if len(y) == 0 or k <= 0:
        warnings.warn("precision_at_k: empty input or k<=0; returning NaN interval",
                      UserWarning, stacklevel=2)
        return float("nan"), float("nan"), float("nan")
    order = np.argsort(-score, kind="stable")
    est = float(y[order[:k]].mean())
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        o = np.argsort(-score[i], kind="stable")[:k]
        bs.append(float(y[i][o].mean()))
    if len(bs) == 0:
        warnings.warn("precision_at_k: no bootstrap resamples; returning NaN interval",
                      UserWarning, stacklevel=2)
        return est, float("nan"), float("nan")
    return est, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def recall_at_p(y, s, p0=0.85):
    """Max recall at precision>=p0 on raw step curve with grouped ties; 0.0 if unattained."""
    y = np.asarray(y)
    if len(y) == 0:
        return 0.0
    prec, rec, _ = precision_recall_curve(y, s)
    best = 0.0
    for p, r in zip(prec, rec):
        if p >= p0 and r > best:
            best = float(r)
    return best


def count_mae(y_true, y_pred):
    """Mean absolute error for per-cell counts (P2 use per EVAL_SPEC)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if len(y_true) == 0:
        return 0.0
    return float(np.mean(np.abs(y_true - y_pred)))


def rank_corr(y_true, y_pred):
    """Spearman rank correlation for per-cell counts (P2 use per EVAL_SPEC).
    Returns NaN when undefined (e.g. constant input); JSON layers map NaN to null."""
    from scipy.stats import spearmanr
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if len(y_true) == 0:
        return float("nan")
    with np.errstate(all="ignore"):
        rho, _ = spearmanr(y_true, y_pred)
    return float(rho) if rho == rho else float("nan")
