"""GTK1 frozen pipeline — single source of truth (consolidated from experiments E02-E12).
Operational framing: newly-reported >=10% @100m. See docs/GUARDRAILS.md.
Modules: io (loaders+normalize), match (greedy/Hungarian), features (cell build),
metrics (AP/CI/delta/P@K). Experiments keep their frozen copies for provenance.
"""
__all__ = ["io", "match", "features", "metrics"]
