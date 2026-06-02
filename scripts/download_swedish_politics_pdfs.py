#!/usr/bin/env python3
"""Discover, download, and index Swedish politics PDFs for the OD RAG database.

The script focuses on auditable public sources:
- Riksdagen document API PDFs, especially budget motions and political motions.
- Current parliamentary party websites, crawled shallowly for PDF links whose
  filenames/titles indicate party programmes, budgets, election manifestos, etc.

It stores raw PDFs under data/rag/pdf_sources/, extracted text as sidecar .txt
files, metadata as JSONL, and indexes extracted text into the existing
SQLite/FTS database used by scripts/build_swedish_party_rag.py.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from collections import deque
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover
    print("PyMuPDF is required. Install with: python3 -m pip install --user pymupdf", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data" / "rag" / "pdf_sources"
METADATA_JSONL = ROOT / "data" / "rag" / "pdf_sources.jsonl"
DEFAULT_DB = ROOT / "data" / "rag" / "swedish_parties.sqlite3"
USER_AGENT = "OberoendeDigitalRAG/0.2 (+https://oberoendedigital.se; Swedish politics PDF archive)"

PARTY_CODE_TO_NAME = {
    "S": "Socialdemokraterna",
    "M": "Moderaterna",
    "SD": "Sverigedemokraterna",
    "V": "Vänsterpartiet",
    "C": "Centerpartiet",
    "KD": "Kristdemokraterna",
    "MP": "Miljöpartiet",
    "L": "Liberalerna",
}

PARTY_SITES = [
    ("Socialdemokraterna", "https://www.socialdemokraterna.se/"),
    ("Moderaterna", "https://moderaterna.se/"),
    ("Sverigedemokraterna", "https://sd.se/"),
    ("Vänsterpartiet", "https://www.vansterpartiet.se/"),
    ("Centerpartiet", "https://www.centerpartiet.se/"),
    ("Kristdemokraterna", "https://kristdemokraterna.se/"),
    ("Miljöpartiet", "https://www.mp.se/"),
    ("Liberalerna", "https://www.liberalerna.se/"),
]

PDF_KEYWORDS = re.compile(
    r"(budget|budgetmotion|vårbudget|hostbudget|höstbudget|varbudget|motion|partiprogram|"
    r"principprogram|ideprogram|idéprogram|valmanifest|manifest|sakpolitik|politik|"
    r"reform|rapport|program|plattform|arbetsmarknad|skola|vard|vård|klimat|ekonomi)",
    re.I,
)
CRAWL_KEYWORDS = re.compile(r"(politik|program|budget|manifest|rapport|press|var-politik|vad-vi-vill|dokument)", re.I)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() == "a":
            attrs_d = dict(attrs)
            self._current_href = attrs_d.get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._current_href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href:
            self.links.append((self._current_href, " ".join(self._text).strip()))
            self._current_href = None
            self._text = []


@dataclass(frozen=True)
class PDFSource:
    url: str
    title: str
    party: str
    category: str
    origin: str
    year: str | None = None
    doc_id: str | None = None


def normalize_url(url: str) -> str:
    """Percent-encode non-ASCII path/query characters for urllib."""
    p = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(p.path, safe="/%:@")
    query = urllib.parse.quote(p.query, safe="=&%:+,;/?@")
    return urllib.parse.urlunsplit((p.scheme, p.netloc, path, query, p.fragment))


def request(url: str, timeout: int = 30) -> urllib.request.Request:
    return urllib.request.Request(normalize_url(url), headers={"User-Agent": USER_AGENT})


def read_url(url: str, timeout: int = 30, max_bytes: int | None = None) -> tuple[bytes, str, str]:
    with urllib.request.urlopen(request(url), timeout=timeout) as r:
        raw = r.read(max_bytes) if max_bytes is not None else r.read()
        return raw, r.headers.get("content-type", ""), r.geturl()


def slug(s: str, max_len: int = 90) -> str:
    s = s.lower()
    s = s.replace("å", "a").replace("ä", "a").replace("ö", "o")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:max_len].strip("-") or "document")


def infer_party_from_undertitel(text: str) -> str:
    m = re.search(r"\(([A-Z]{1,2})\)\s*$", text or "")
    if m:
        return PARTY_CODE_TO_NAME.get(m.group(1), m.group(1))
    # Riksdag government propositions, committee reports, etc.
    return "Riksdagen"


def infer_year(*parts: str | None) -> str | None:
    text = " ".join(p or "" for p in parts)
    # Prefer parliamentary year, e.g. 2025/26.
    m = re.search(r"(20\d{2}\s*/\s*\d{2})", text)
    if m:
        return m.group(1).replace(" ", "")
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return m.group(1) if m else None


def riksdag_documents(max_docs: int, pages: int) -> list[PDFSource]:
    queries = [
        ("budgetmotion", "mot", "riksdag_budget_motion"),
        ("vårproposition budget", "mot", "riksdag_spring_budget_motion"),
        ("utgiftsområde", "mot", "riksdag_expenditure_area_motion"),
        ("budgetproposition", "prop", "riksdag_budget_proposition"),
        ("ekonomiska vårproposition", "prop", "riksdag_spring_budget_proposition"),
        ("partimotion", "mot", "riksdag_party_motion"),
    ]
    seen: set[str] = set()
    out: list[PDFSource] = []
    for q, doktyp, category in queries:
        for p in range(1, pages + 1):
            if len(out) >= max_docs:
                return out
            params = urllib.parse.urlencode({"sok": q, "doktyp": doktyp, "utformat": "json", "p": p})
            url = f"https://data.riksdagen.se/dokumentlista/?{params}"
            try:
                raw, _, _ = read_url(url, timeout=35)
                data = json.loads(raw.decode("utf-8", "replace"))
                docs = data.get("dokumentlista", {}).get("dokument", [])
                if isinstance(docs, dict):
                    docs = [docs]
                if not docs:
                    break
            except Exception as exc:
                print(f"WARN riksdag query failed {url}: {exc}", file=sys.stderr)
                break
            for d in docs:
                doc_id = d.get("dok_id") or d.get("id")
                if not doc_id or doc_id in seen:
                    continue
                seen.add(doc_id)
                title = " ".join(x for x in [d.get("titel"), d.get("undertitel")] if x).strip() or doc_id
                party = infer_party_from_undertitel(d.get("undertitel", ""))
                year = infer_year(d.get("rm"), title, d.get("publicerad"))
                pdf_url = f"https://data.riksdagen.se/dokument/{doc_id}.pdf"
                out.append(PDFSource(pdf_url, title, party, category, "riksdagen_api", year, doc_id))
                if len(out) >= max_docs:
                    return out
            time.sleep(0.15)
    return out


def party_site_pdfs(max_pdfs: int, max_pages_per_site: int) -> list[PDFSource]:
    found: dict[str, PDFSource] = {}
    for party, base in PARTY_SITES:
        base_host = urllib.parse.urlparse(base).netloc
        q: deque[str] = deque([base])
        seen_pages: set[str] = set()
        pages = 0
        while q and pages < max_pages_per_site and len(found) < max_pdfs:
            url = q.popleft()
            if url in seen_pages:
                continue
            seen_pages.add(url)
            try:
                raw, ctype, final_url = read_url(url, timeout=25, max_bytes=2_000_000)
            except Exception:
                continue
            if "html" not in ctype.lower() and b"<html" not in raw[:500].lower():
                continue
            pages += 1
            try:
                body = raw.decode("utf-8", "replace")
            except Exception:
                body = raw.decode("latin-1", "replace")
            parser = LinkParser()
            try:
                parser.feed(body)
            except Exception:
                pass
            for href, text in parser.links:
                abs_url = urllib.parse.urljoin(final_url, html.unescape(href)).split("#", 1)[0]
                parsed = urllib.parse.urlparse(abs_url)
                if parsed.scheme not in {"http", "https"}:
                    continue
                label = f"{text} {parsed.path} {parsed.query}"
                if ".pdf" in parsed.path.lower() or ".pdf" in parsed.query.lower():
                    if PDF_KEYWORDS.search(label):
                        title = re.sub(r"\s+", " ", text).strip() or Path(parsed.path).name
                        year = infer_year(title, parsed.path)
                        key = abs_url
                        found.setdefault(key, PDFSource(abs_url, title, party, "party_pdf", "party_site_crawl", year, None))
                elif parsed.netloc == base_host and CRAWL_KEYWORDS.search(abs_url) and abs_url not in seen_pages:
                    if len(q) < max_pages_per_site * 3:
                        q.append(abs_url)
            time.sleep(0.12)
    return list(found.values())[:max_pdfs]


def init_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS sources(
            id INTEGER PRIMARY KEY,
            party TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            fetched_at TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            error TEXT
        );
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY,
            source_id INTEGER NOT NULL REFERENCES sources(id),
            content_type TEXT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chunks(
            id INTEGER PRIMARY KEY,
            document_id INTEGER NOT NULL REFERENCES documents(id),
            source_id INTEGER NOT NULL REFERENCES sources(id),
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            text,
            party UNINDEXED,
            category UNINDEXED,
            title UNINDEXED,
            url UNINDEXED
        );
        """
    )
    return con


def chunks(text: str, size: int = 1400, overlap: int = 220) -> Iterable[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    start = 0
    while start < len(clean):
        end = min(len(clean), start + size)
        if end < len(clean):
            split = clean.rfind(". ", start, end)
            if split > start + size // 2:
                end = split + 1
        piece = clean[start:end].strip()
        if piece:
            yield piece
        if end >= len(clean):
            break
        start = max(end - overlap, start + 1)


def reset_source(con: sqlite3.Connection, source_id: int) -> None:
    doc_ids = [r[0] for r in con.execute("SELECT id FROM documents WHERE source_id=?", (source_id,))]
    for doc_id in doc_ids:
        con.execute("DELETE FROM chunks_fts WHERE rowid IN (SELECT id FROM chunks WHERE document_id=?)", (doc_id,))
    con.execute("DELETE FROM chunks WHERE source_id=?", (source_id,))
    con.execute("DELETE FROM documents WHERE source_id=?", (source_id,))


def pdf_text(path: Path) -> tuple[str, int]:
    doc = fitz.open(path)
    parts: list[str] = []
    for page in doc:
        parts.append(str(page.get_text("text")))
    return re.sub(r"\s+", " ", "\n".join(parts)).strip(), doc.page_count


def local_pdf_path(src: PDFSource) -> Path:
    digest = hashlib.sha256(src.url.encode()).hexdigest()[:12]
    year = slug(src.year or "unknown", 20)
    party = slug(src.party, 35)
    cat = slug(src.category, 35)
    title = slug(src.title, 90)
    return PDF_DIR / party / cat / f"{year}-{title}-{digest}.pdf"


def load_existing_metadata() -> dict[str, dict]:
    if not METADATA_JSONL.exists():
        return {}
    out: dict[str, dict] = {}
    for line in METADATA_JSONL.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(line)
            out[d["url"]] = d
        except Exception:
            pass
    return out


def write_metadata(all_rows: dict[str, dict]) -> None:
    METADATA_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with METADATA_JSONL.open("w", encoding="utf-8") as f:
        for url in sorted(all_rows):
            f.write(json.dumps(all_rows[url], ensure_ascii=False, sort_keys=True) + "\n")


def download_and_index(sources: list[PDFSource], db_path: Path, max_bytes: int, sleep_s: float) -> dict:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    con = init_db(db_path)
    metadata = load_existing_metadata()
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    stats = {"candidates": len(sources), "downloaded": 0, "reused": 0, "indexed": 0, "failed": 0, "too_large": 0, "chunks": 0}
    for i, src in enumerate(sources, 1):
        path = local_pdf_path(src)
        txt_path = path.with_suffix(".txt")
        row = {**asdict(src), "pdf_path": str(path.relative_to(ROOT)), "text_path": str(txt_path.relative_to(ROOT)), "fetched_at": now}
        try:
            if path.exists() and path.stat().st_size > 0:
                stats["reused"] += 1
            else:
                print(f"[{i}/{len(sources)}] download {src.party} · {src.category} · {src.title[:80]}", flush=True)
                raw, ctype, final_url = read_url(src.url, timeout=45)
                if len(raw) > max_bytes:
                    stats["too_large"] += 1
                    row.update({"status": "too_large", "bytes": len(raw), "final_url": final_url})
                    metadata[src.url] = row
                    continue
                if not raw.startswith(b"%PDF") and "pdf" not in ctype.lower():
                    raise ValueError(f"not a PDF: content_type={ctype!r} first_bytes={raw[:20]!r}")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                row.update({"final_url": final_url, "content_type": ctype, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
                stats["downloaded"] += 1
            text = txt_path.read_text(encoding="utf-8", errors="replace") if txt_path.exists() else ""
            pages = None
            if len(text) < 200:
                text, pages = pdf_text(path)
                txt_path.write_text(text, encoding="utf-8")
            if len(text) < 200:
                raise ValueError(f"too little extracted text ({len(text)} chars)")
            row.update({"status": "ok", "pages": pages, "text_chars": len(text), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            con.execute(
                "INSERT OR IGNORE INTO sources(party,category,title,url,status) VALUES(?,?,?,?, 'pending')",
                (src.party, src.category, src.title, src.url),
            )
            source_id = con.execute("SELECT id FROM sources WHERE url=?", (src.url,)).fetchone()[0]
            reset_source(con, source_id)
            cur = con.execute(
                "INSERT INTO documents(source_id,content_type,text,created_at) VALUES(?,?,?,?)",
                (source_id, "application/pdf", text, now),
            )
            doc_id = cur.lastrowid
            chunk_count = 0
            for idx, chunk in enumerate(chunks(text)):
                ccur = con.execute(
                    "INSERT INTO chunks(document_id,source_id,chunk_index,text) VALUES(?,?,?,?)",
                    (doc_id, source_id, idx, chunk),
                )
                con.execute(
                    "INSERT INTO chunks_fts(rowid,text,party,category,title,url) VALUES(?,?,?,?,?,?)",
                    (ccur.lastrowid, chunk, src.party, src.category, src.title, src.url),
                )
                chunk_count += 1
            con.execute("UPDATE sources SET fetched_at=?, status='ok', error=NULL WHERE id=?", (now, source_id))
            con.commit()
            row["chunks"] = chunk_count
            stats["chunks"] += chunk_count
            stats["indexed"] += 1
        except Exception as exc:
            stats["failed"] += 1
            row.update({"status": "error", "error": str(exc)})
            try:
                con.execute(
                    "INSERT OR IGNORE INTO sources(party,category,title,url,status) VALUES(?,?,?,?, 'pending')",
                    (src.party, src.category, src.title, src.url),
                )
                source_id = con.execute("SELECT id FROM sources WHERE url=?", (src.url,)).fetchone()[0]
                con.execute("UPDATE sources SET fetched_at=?, status='error', error=? WHERE id=?", (now, str(exc), source_id))
                con.commit()
            except Exception:
                pass
            print(f"  ERROR {src.url}: {exc}", file=sys.stderr, flush=True)
        metadata[src.url] = row
        if i % 25 == 0:
            write_metadata(metadata)
        time.sleep(sleep_s)
    write_metadata(metadata)
    stats["db_total_sources"] = con.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    stats["db_ok_sources"] = con.execute("SELECT COUNT(*) FROM sources WHERE status='ok'").fetchone()[0]
    stats["db_total_chunks"] = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    return stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--max-riksdag", type=int, default=500)
    ap.add_argument("--riksdag-pages", type=int, default=40)
    ap.add_argument("--max-party-pdfs", type=int, default=250)
    ap.add_argument("--max-party-pages", type=int, default=80)
    ap.add_argument("--max-bytes", type=int, default=25_000_000)
    ap.add_argument("--sleep", type=float, default=0.08)
    ap.add_argument("--discover-only", action="store_true")
    args = ap.parse_args()

    sources: dict[str, PDFSource] = {}
    for src in riksdag_documents(args.max_riksdag, args.riksdag_pages):
        sources[src.url] = src
    for src in party_site_pdfs(args.max_party_pdfs, args.max_party_pages):
        sources[src.url] = src
    ordered = list(sources.values())
    print(json.dumps({"discovered": len(ordered), "riksdag": sum(s.origin == "riksdagen_api" for s in ordered), "party_site": sum(s.origin == "party_site_crawl" for s in ordered)}, ensure_ascii=False), flush=True)
    if args.discover_only:
        for src in ordered[:50]:
            print(json.dumps(asdict(src), ensure_ascii=False))
        return
    stats = download_and_index(ordered, args.db, args.max_bytes, args.sleep)
    print(json.dumps(stats, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
