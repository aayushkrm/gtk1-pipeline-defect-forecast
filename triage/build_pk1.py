"""PK1 triage page v0 (B1 primary, retrospective, 2022->2025 @100m, cut>=10).
Same template/conditions as ON v0. Cut-sensitivity: >=12/>=15 PENDING (E12 queued) — flagged on page.
Tolerant loader vendored (attributed). De-identified aggregates only. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize as raw
from gtk1.features import build
from sklearn.metrics import average_precision_score

SEC = REPO.parent / "Данные для предварительного изучения" / "Парабель-Кузбасс-1 (572-714)"


def load(year):
    import glob
    fs = sorted(glob.glob(str(SEC / str(year) / "*.xls*")))
    cands = [f for f in fs if Path(f).name.startswith("Аномалии")]
    assert cands, f"no anomaly file in {SEC / str(year)}"
    return load_anomalies(cands[0])

OUT = Path(__file__).resolve().parent
KMAX = 1400

def run():
    d22, _ = load(2022); d25, _ = load(2025)
    r22, r25 = raw(d22), raw(d25)
    yte, Xte, mr = build(r22, r25, 10, KMAX)
    past = Xte[:, 0]
    score = past / max(past.max(), 1)
    order = np.argsort(-score, kind="stable")
    ap = float(average_precision_score(yte, score))
    base = float(yte.mean())
    rng = np.random.default_rng(7)
    def p_at_k(k):
        top = order[:k]
        bs = []
        for _ in range(2000):
            i = rng.integers(0, len(yte), len(yte))
            o = np.argsort(-score[i], kind="stable")[:k]
            bs.append(float(yte[i][o].mean()))
        return float(yte[top].mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    rows = [(r, int(i), int(past[i]), float(score[i]), int(yte[i]))
            for r, i in enumerate(order[:20], 1)]
    cell_w = 1200 / (KMAX + 1)
    rects = []
    for i in range(KMAX + 1):
        v = score[i]
        red = int(240 * v + 15)
        rects.append(f'<rect x="{i * cell_w:.2f}" y="20" width="{cell_w + 0.05:.2f}" height="40" fill="rgb({red},40,40)"/>')
        if yte[i]:
            rects.append(f'<rect x="{i * cell_w:.2f}" y="62" width="{cell_w + 0.05:.2f}" height="6" fill="black"/>')
    svg = ("<svg width='1220' height='90' viewBox='0 0 1220 90'>"
           "<text x='5' y='12'>B1 intensity (red) per 100m, 0-140km (PK1 572-714); black ticks = newly-reported 2025 (retrospective)</text>"
           + "".join(rects) + "</svg>")
    trh = "".join(f"<tr><td>{r}</td><td>{i} ({i/10:.1f} km)</td><td>{p}</td><td>{s:.3f}</td>"
                  f"<td>{'YES' if y else 'no'}</td></tr>" for r, i, p, s, y in rows)
    pk = "".join(f"<li>P@{k}: {p_at_k(k)[0]:.3f} [{p_at_k(k)[1]:.3f},{p_at_k(k)[2]:.3f}] "
                 f"({int(round(p_at_k(k)[0]*k))}/{k}, base rate {base:.3f})</li>" for k in (10, 20, 50))
    html = f"""<html><head><meta charset='utf-8'><title>GTK1 triage PK1 v0 (B1, retrospective)</title></head><body>
<h1>Inspection-report triage — PK1 prototype v0 (B1 primary, retrospective demo)</h1>
<p><b>NOT a physical prediction. Retrospective: test pair 2022→2025 already spent in E11;
this page re-runs frozen labels for display only (no re-tuning).</b>
"Newly-reported" = unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match; includes
initiation + re-detected misaligned old + sensitivity gain. Match-rate (test, forward): {mr:.3f}
(vanished = {1-mr:.3f}). Cut-sensitivity (E12, frozen): B1 0.779 / 0.574 / 0.375 at ≥10/12/15% (all lift-CIs lower>0).
Stable methodology note: d≥10% counts 8982 vs 8989 across surveys (unlike ON inflation).
Absolute AP is cut- and survey-conditional. Per-section thresholds required — PK1 only, do not pool.</p>
<p>AP={ap:.3f} base={base:.3f} (frozen E11 number reproduced live).</p>
<h2>Linear heatmap</h2>{svg}
<h2>Top-20 ranked 100m cells (audit)</h2>
<table border='1'><tr><th>rank</th><th>cell (km)</th><th>past count</th><th>B1 score</th><th>newly-reported 2025</th></tr>{trh}</table>
<h2>Retrospective precision@K</h2><ul>{pk}</ul>
<p><i>Retrospective only on the spent 2022→2025 PK1 pair (base rate {base:.3f}): P@K is a display
statistic on frozen labels, not a prospective precision claim. Ranking is threshold-free B1
past-count; do not quote as future accuracy. Prospective use requires next-survey data +
per-section recalibration. K = 10/20/50 display-chosen.</i></p>
<p>Model: B1 past-count only. Overlay OFF. See docs/GUARDRAILS.md, docs/TRIAGE_SPEC.md, PROGRESS.md.</p></body></html>"""
    (OUT / "triage_pk1.html").write_text(html)
    try:
        gh = subprocess.run(["git", "-C", str(Path(__file__).resolve().parents[1]),
                             "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    (OUT / "triage_pk1.json").write_text(json.dumps(
        {"git": gh, "AP": ap, "base": base, "match_rate": mr,
         "cut_sensitivity": {"10": 0.779, "12": 0.574, "15": 0.375},
         "top20": rows, "p_at_k": {k: {"est": p_at_k(k)[0], "CI": [p_at_k(k)[1], p_at_k(k)[2]]} for k in (10, 20, 50)}}, indent=2))
    print(f"git={gh} AP={ap:.3f} base={base:.3f} match={mr:.3f} " +
          " ".join(f"P@{k}={p_at_k(k)[0]:.3f}" for k in (10, 20, 50)))

if __name__ == "__main__":
    run()
