# Research protocol: standing orders for every research (sub)agent (effective 2026-10-06)

## No-skip rule (user directive, absolute)
If one tool or search fails, find another way. Never skip and miss anything. Forbidden outcomes: silent omission of a briefed sub-topic. "could not access" with no fallback attempt. Single-source reliance where verification was possible.

## Fallback ladder (climb until covered or a HARD boundary below is hit)
1. Run websearch (several query phrasings, EN + RU where relevant).
2. Run webfetch on result URLs.
3. Query OpenAlex API (works.openalex.org/works?search=, filter citation counts).
4. Query arXiv API (export.arxiv.org/api/query).
5. Check publisher/HTML mirrors (Garant/meganorm for RU standards, vendor blogs, conference pages, Mendeley/Kaggle/HF dataset pages).
6. Use secondary citations (review papers, NTSB/PHMSA HTML reports, Federal Register).
7. Record NEGATIVE result ("no X exists / not found after ladder", with queries tried).

## Per-file disclosure (mandatory header/footer lines)
- State which tools worked and which failed this track (e.g. "websearch HTTP-400, OpenAlex used").
- Cite every paywalled/bot-walled primary via summary/secondary. Mark it "full text not verified".
- State every negative result. State what was sought and where.

## Minimums (unchanged)
Provide 8+ sources/items per track. Give each link + content + RELEVANCE + USE/ADAPT/REJECT verdict. Include Russian-language sources where the brief requires them. Make no commits (lead commits).

## HARD boundaries (stop and report, do not circumvent)
- Treat paywalled standards for purchase as summaries/secondaries only (API 1104/1163 full text, BS 7910). Flag the exact document + price page. Do not buy. Full purchase is the user's decision.
- Treat login-walled / members-only data as rejected-in-file, then move on (EGIG, Kaggle private).
- Use no credentials. Request no keys from third parties. Do not scrape in violation of robots/ToS. Use official APIs and public pages only.
