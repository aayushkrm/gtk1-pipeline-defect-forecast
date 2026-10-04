"""Triage prototype v0 (B1 primary, retrospective, ON @100m, cut>=10).
Past = 2021 survey (B1 = past corr count/cell, score = count/max).
Future = 2025 matched-new labels (pipe+2m/0.5m/1h greedy) — display only.
Outputs de-identified aggregates only: ranked top-20 + full-length SVG heatmap +
audit columns + precision@K retrospective + GUARDRAILS disclaimer.
No training, no tuning, no raw rows. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "experiments"))
from e02_matched import load_anom
from e07b_null import build
from e07_ablation import raw
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent
KMAX, W = 1330, 100

def run():
    d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    from e07_ablation import raw
    r21, r25 = raw(d21), raw(d25)
    yte, Xte, mr = build(r21, r25, 10, KMAX)
    past = Xte[:, 0]
    score = past / max(past.max(), 1)
    order = np.argsort(-score, kind="stable")
    ap = float(average_precision_score(yte, score))
    base = float(yte.mean())
    def p_at_k(k):
        top = order[:k]
        rng = np.random.default_rng(7)
        bs = []
        for _ in range(2000):
            i = rng.integers(0, len(yte), len(yte))
            # rank-stable CI: resample cells, take same top-K positions of resample by score order
            o = np.argsort(-score[i], kind="stable")[:k]
            bs.append(float(yte[i][o].mean()))
        return float(yte[top].mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    rows = []
    for r, i in enumerate(order[:20], 1):
        rows.append((r, int(i), int(past[i]), float(score[i]), int(yte[i])))
    # SVG heatmap: 1331 cells, width scaled, color by score, tick where yte=1
    cell_w = 1200 / (KMAX + 1)
    rects = []
    for i in range(KMAX + 1):
        v = score[i]
        red = int(240 * v + 15)
        rects.append(f'<rect x="{i * cell_w:.2f}" y="20" width="{cell_w + 0.05:.2f}" height="40" fill="rgb({red},40,40)"/>')
        if yte[i]:
            rects.append(f'<rect x="{i * cell_w:.2f}" y="62" width="{cell_w + 0.05:.2f}" height="6" fill="black"/>')
    svg = ("<svg width='1220' height='90' viewBox='0 0 1220 90'>"
           "<text x='5' y='12'>B1 intensity (red) per 100m, 0-133km; black ticks = newly-reported in 2025 (retrospective)</text>"
           + "".join(rects) + "</svg>")
    trh = "".join(f"<tr><td>{r}</td><td>{i} ({i/10:.1f} km)</td><td>{p}</td><td>{s:.3f}</td>"
                  f"<td>{'YES' if y else 'no'}</td></tr>" for r, i, p, s, y in rows)
    pk = "".join(f"<li>P@{k}: {p_at_k(k)[0]:.3f} [{p_at_k(k)[1]:.3f},{p_at_k(k)[2]:.3f}] "
                  f"({int(round(p_at_k(k)[0] * k))}/{k}, base rate {base:.3f})</li>" for k in (10, 20, 50))
    caption = ("<p><i>Retrospective only on the spent 2021→2025 ON pair (base rate 0.268): P@K is a display "
               "statistic on frozen labels, not a prospective precision claim. Ranking is threshold-free B1 "
               "past-count; do not quote 1.000 as future accuracy. Prospective use requires next-survey data + "
               "per-section recalibration. K = 10/20/50 display-chosen.</i></p>")
    html = f"""<html><head><meta charset='utf-8'><title>GTK1 triage prototype v0 (B1, ON retrospective)</title></head><body>
<h1>Inspection-report triage — prototype v0 (B1 primary, retrospective demo)</h1>
<p><b>NOT a physical prediction. Retrospective: test pair 2021→2025 already spent in E04–E09;
this page re-runs frozen labels for display only (no re-tuning).</b>
"Newly-reported" = unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match; includes
initiation + re-detected misaligned old + sensitivity gain. Match-rate (test, forward, E02): 0.612.
Vanished-frac (forward, E02):
0.596 train / 0.388 test. Cut-sensitivity of B1 AP (E04): 0.644 / 0.546 / 0.364 at ≥10/12/15%.
Absolute AP is cut- and survey-conditional. Per-section thresholds required — do not pool.</p>
<p>AP={ap:.3f} base={base:.3f} (frozen E04 number reproduced live: B1 0.644).</p>
<h2>Linear heatmap</h2>{svg}
<h2>Top-20 ranked 100m cells (audit)</h2>
<table border='1'><tr><th>rank</th><th>cell (km)</th><th>past count</th><th>B1 score</th><th>newly-reported 2025</th></tr>{trh}</table>
<h2>Retrospective precision@K</h2><ul>{pk}</ul>{caption}
<p>Model: B1 past-count only. Overlay (LR-nlag) OFF by default (ON-only experimental, kill-switch).
See docs/GUARDRAILS.md, docs/TRIAGE_SPEC.md, PROGRESS.md for audit trail.</p></body></html>"""
    (OUT / "triage_demo.html").write_text(html)
    try:
        gh = subprocess.run(["git", "-C", str(Path(__file__).resolve().parents[1]),
                             "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    (OUT / "triage_demo.json").write_text(json.dumps(
        {"git": gh, "AP": ap, "base": base, "match_rate": mr, "top20": rows,
         "p_at_k": {k: {"est": p_at_k(k)[0], "CI": [p_at_k(k)[1], p_at_k(k)[2]]} for k in (10, 20, 50)}}, indent=2))
    print(f"git={gh} AP={ap:.3f} base={base:.3f} match={mr:.3f} " +
          " ".join(f"P@{k}={p_at_k(k)[0]:.3f}[{p_at_k(k)[1]:.3f},{p_at_k(k)[2]:.3f}]" for k in (10, 20, 50)))

if __name__ == "__main__":
    run()
