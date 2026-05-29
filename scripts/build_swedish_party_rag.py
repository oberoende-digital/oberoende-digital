#!/usr/bin/env python3
"""Build a small, source-transparent RAG/FTS database for Swedish party material.

The script reads docs/rag/swedish_party_sources.json, downloads listed sources,
extracts readable text, chunks it, and stores everything in SQLite with FTS5.
It intentionally stores source URLs and retrieval timestamps for auditability.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "rag" / "swedish_party_sources.json"
DEFAULT_DB = ROOT / "data" / "rag" / "swedish_parties.sqlite3"
USER_AGENT = "OberoendeDigitalRAG/0.1 (+https://oberoendedigital.se; research archive)"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag in {"script", "style", "noscript", "svg", "canvas"}:
            self.skip += 1
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "tr", "section", "article"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str):
        if tag in {"script", "style", "noscript", "svg", "canvas"} and self.skip:
            self.skip -= 1
        if tag in {"p", "li", "h1", "h2", "h3", "h4", "tr", "section", "article"}:
            self.parts.append("\n")

    def handle_data(self, data: str):
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        text = html.unescape(" ".join(self.parts))
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()


def fetch(url: str, timeout: int = 25) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        content_type = r.headers.get("content-type", "")
        raw = r.read(5_000_000)
    charset_match = re.search(r"charset=([^;]+)", content_type, re.I)
    charset = charset_match.group(1) if charset_match else "utf-8"
    text = raw.decode(charset, errors="replace")
    return content_type, text


def extract_text(content_type: str, body: str) -> str:
    if "html" in content_type.lower() or "<html" in body[:500].lower():
        parser = TextExtractor()
        parser.feed(body)
        return parser.text()
    return re.sub(r"\s+", " ", body).strip()


def chunks(text: str, size: int = 1400, overlap: int = 220) -> Iterable[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return
    start = 0
    while start < len(clean):
        end = min(len(clean), start + size)
        if end < len(clean):
            split = clean.rfind(". ", start, end)
            if split > start + size // 2:
                end = split + 1
        yield clean[start:end].strip()
        if end >= len(clean):
            break
        start = max(end - overlap, start + 1)


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


def reset_source(con: sqlite3.Connection, source_id: int) -> None:
    doc_ids = [r[0] for r in con.execute("SELECT id FROM documents WHERE source_id=?", (source_id,))]
    for doc_id in doc_ids:
        con.execute("DELETE FROM chunks_fts WHERE rowid IN (SELECT id FROM chunks WHERE document_id=?)", (doc_id,))
    con.execute("DELETE FROM chunks WHERE source_id=?", (source_id,))
    con.execute("DELETE FROM documents WHERE source_id=?", (source_id,))


def build(manifest_path: Path, db_path: Path, limit: int | None = None, sleep_s: float = 0.5) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    con = init_db(db_path)
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    sources = manifest["sources"][:limit]
    for item in sources:
        con.execute(
            "INSERT OR IGNORE INTO sources(party,category,title,url,status) VALUES(?,?,?,?, 'pending')",
            (item["party"], item["category"], item["title"], item["url"]),
        )
    con.commit()

    ok = fail = 0
    for item in sources:
        row = con.execute("SELECT id FROM sources WHERE url=?", (item["url"],)).fetchone()
        source_id = row[0]
        print(f"fetch {item['party']} · {item['category']} · {item['title']}", flush=True)
        try:
            content_type, body = fetch(item["url"])
            text = extract_text(content_type, body)
            if len(text) < 200:
                raise ValueError(f"too little extracted text ({len(text)} chars)")
            reset_source(con, source_id)
            cur = con.execute(
                "INSERT INTO documents(source_id,content_type,text,created_at) VALUES(?,?,?,?)",
                (source_id, content_type, text, now),
            )
            doc_id = cur.lastrowid
            for idx, chunk in enumerate(chunks(text)):
                ccur = con.execute(
                    "INSERT INTO chunks(document_id,source_id,chunk_index,text) VALUES(?,?,?,?)",
                    (doc_id, source_id, idx, chunk),
                )
                con.execute(
                    "INSERT INTO chunks_fts(rowid,text,party,category,title,url) VALUES(?,?,?,?,?,?)",
                    (ccur.lastrowid, chunk, item["party"], item["category"], item["title"], item["url"]),
                )
            con.execute("UPDATE sources SET fetched_at=?, status='ok', error=NULL WHERE id=?", (now, source_id))
            con.commit()
            ok += 1
        except Exception as e:  # keep building; failed URLs are audit-visible
            con.execute("UPDATE sources SET fetched_at=?, status='error', error=? WHERE id=?", (now, str(e), source_id))
            con.commit()
            print(f"  ERROR: {e}", file=sys.stderr, flush=True)
            fail += 1
        time.sleep(sleep_s)
    total_chunks = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(json.dumps({"ok": ok, "failed": fail, "chunks": total_chunks, "db": str(db_path)}, ensure_ascii=False))


def query(db_path: Path, q: str, limit: int = 8) -> None:
    con = sqlite3.connect(db_path)
    rows = con.execute(
        """
        SELECT party, category, title, url, snippet(chunks_fts, 0, '[', ']', '…', 18)
        FROM chunks_fts WHERE chunks_fts MATCH ? LIMIT ?
        """,
        (q, limit),
    ).fetchall()
    for party, category, title, url, snippet in rows:
        print(f"[{party} · {category}] {title}\n{url}\n{snippet}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--query")
    args = ap.parse_args()
    if args.query:
        query(args.db, args.query)
    else:
        build(args.manifest, args.db, args.limit)


if __name__ == "__main__":
    main()
