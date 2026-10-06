# Research protocol — standing orders for every research (sub)agent (effective 2026-10-06)

## No-skip rule (user directive, absolute)
If one tool or search fails, find another way. Never skip and miss anything.
Forbidden outcomes: silent omission of a briefed sub-topic, "could not access" with no fallback
attempt, single-source reliance where verification was possible.

## Fallback ladder (climb until covered or a HARD boundary below is hit)
1. websearch (several query phrasings, EN + RU where relevant) → 2. webfetch on result URLs →
3. OpenAlex API (works.openalex.org/works?search=, filter citation counts) → 4. arXiv API
(export.arxiv.org/api/query) → 5. publisher/HTML mirrors (Garant/meganorm for RU standards,
vendor blogs, conference pages, Mendeley/Kaggle/HF dataset pages) → 6. secondary citations
(review papers, NTSB/PHMSA HTML reports, Federal Register) → 7. record NEGATIVE result
("no X exists / not found after ladder", with queries tried).

## Per-file disclosure (mandatory header/footer lines)
- Which tools worked/failed this track (e.g. "websearch HTTP-400, OpenAlex used").
- Every paywalled/bot-walled primary: cite via summary/secondary AND mark "full text not verified".
- Every negative result: state what was sought and where.

## Minimums (unchanged)
8+ sources/items per track, each with link + content + RELEVANCE + USE/ADAPT/REJECT verdict.
Russian-language sources required where the brief says so. No commits (lead commits).

## HARD boundaries (stop and report, do not circumvent)
- Paywalled standards for purchase (API 1104/1163 full text, BS 7910): summaries/secondaries only.
  Full purchase is the user's decision — flag the exact document + price page, do not buy.
- Login-walled / members-only data (EGIG, Kaggle private): record as rejected-in-file, move on.
- No credential use, no key requests to third parties, no scraping that violates robots/ToS —
  use official APIs and public pages only.
