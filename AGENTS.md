# AGENTS.md — project writing law (GTK1). Obey on every output for this repo.

Write clear, constrained technical English inspired by ASD-STE100 Simplified Technical
English (approximately 80% / STE-flavored).

## Core style rules
- Prefer short sentences and one main idea per sentence.
- Use active voice and simple verb forms where possible.
- Avoid hedging, filler, and unnecessary complexity.
- Keep structure logical and easy to parse.

## Critical exceptions (never break these)
- Do not change, rename, or rephrase variable names, function names, class names, API
  identifiers, code tokens, commands, file paths, or any exact technical terms.
- Preserve all technical meanings, quantities, conditions, and facts exactly.
- Code, identifiers, and formal syntax stay untouched; only the surrounding prose is constrained.

## Preferred output formats (escalate when helpful)
1. Clean constrained prose (default).
2. Diagrams or images for easier understanding.
3. Interactive HTML pages when visual or exploratory structure adds value.
4. Custom explainer-style video outlines or scripts when the topic benefits from narrative explanation.

Goal: maximize clarity and reduce ambiguity so the reader spends less effort. Prefer precise,
discardable, high-value artifacts over verbose text.

## Repo-specific bindings (from reviewer rounds; these override brevity when in conflict)
- Triage page captions required verbatim by reviewer round 7 stay verbatim.
- GUARDRAILS.md disclaimer wording, R1–R4 rules, and TRIAGE_SPEC numbers stay exact.
- PROGRESS.md is append-only audit history: never rewrite past entries; new entries follow this style.
- Research track files (docs/research/track*.md) are frozen evidence: do not restyle them.
- Raw data never committed; single committer; Russian section names match actual directories.
