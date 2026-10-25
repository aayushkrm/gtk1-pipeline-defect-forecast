# AGENTS.md — project writing law (GTK1). Obey on every output for this repo.

## Hard rule: Telegram is read-only (2026-10-24)
- Never send, edit, delete, or react to a message in any Telegram chat.
- Never press the send key in a chat composer. No exceptions, even when a task says "send".
- Never upload files, images, or links to a chat.
- Reading chats and downloading attachments is allowed.
- Write partner-facing text to a draft file and give the user the path. The user sends it.

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

## Always use /humanizer skill when writing prose or long text etc

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
