# Swedish party and budget RAG database

Goal: build a source-transparent local knowledge base for OD analysis of Swedish political parties, public platforms and national budget proposals.

Status: initial scaffold. The database is local SQLite with FTS5 search, not yet a production vector store.

## Build

```bash
python3 scripts/build_swedish_party_rag.py
```

Output:

```text
data/rag/swedish_parties.sqlite3
```

## Query

```bash
python3 scripts/build_swedish_party_rag.py --query 'psykisk hälsa'
python3 scripts/build_swedish_party_rag.py --query 'budget skola vinst'
```

## Source policy

Every row keeps party, category, title, URL, fetch status and timestamp. Failed URLs remain visible in `sources.status='error'` so the manifest can be corrected instead of silently dropping material.

## Expansion checklist

1. Add verified direct links to each party's latest budget motion PDF/page.
2. Add Riksdag document IDs for budget motions once confirmed.
3. Add official election manifestos and party programmes as separate entries.
4. Add government budget bill and opposition shadow budgets.
5. Add embeddings later if needed; keep FTS5 as the transparent baseline.
