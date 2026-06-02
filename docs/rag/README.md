# Swedish party and budget RAG database

Goal: build a source-transparent local knowledge base for OD analysis of Swedish political parties, public platforms and national budget proposals.

Status: local SQLite/FTS5 baseline with HTML sources plus a PDF archive/indexer. This is not yet a production vector store.

Current local PDF corpus after the June 2026 expansion:

- 1,113 discovered PDF metadata rows.
- 1,066 PDFs downloaded/extracted successfully.
- 1,030 Riksdag budget/political-motion PDF candidates covering current and historical parliamentary years.
- 83 party-site PDFs, including party programmes, election manifestos, reports and policy programmes.
- 47 failures remain visible in the manifest: mostly older Riksdag PDF URLs returning 404 plus 5 scanned Miljöpartiet historical PDFs that need OCR.
- Local SQLite index: 1,083 ok sources, 47 error sources, 58,621 chunks.

Raw PDFs live on the server under `data/rag/pdf_sources/` with extracted `.txt` sidecars. They are intentionally gitignored because the archive is hundreds of MB; commit the scripts and metadata, not the raw PDF cache.

## Build HTML/page baseline

```bash
python3 scripts/build_swedish_party_rag.py
```

## Download and index PDFs

```bash
python3 -m pip install --user pymupdf
python3 scripts/download_swedish_politics_pdfs.py \
  --max-riksdag 500 \
  --riksdag-pages 40 \
  --max-party-pdfs 180 \
  --max-party-pages 100
```

Outputs:

```text
data/rag/swedish_parties.sqlite3
data/rag/pdf_sources.jsonl
data/rag/pdf_sources/
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
