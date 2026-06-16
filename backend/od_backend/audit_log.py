from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    agent_slug TEXT,
    channel TEXT,
    synthetic_disclosure TEXT NOT NULL,
    payload_json TEXT NOT NULL
);
"""


class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as con:
            con.execute(SCHEMA)

    def record(
        self,
        event_type: str,
        *,
        agent_slug: str | None,
        channel: str | None,
        synthetic_disclosure: str,
        payload: dict[str, Any],
    ) -> int:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "INSERT INTO audit_events(created_at,event_type,agent_slug,channel,synthetic_disclosure,payload_json) VALUES(?,?,?,?,?,?)",
                (utc_now(), event_type, agent_slug, channel, synthetic_disclosure, json.dumps(payload, sort_keys=True)),
            )
            event_id = cur.lastrowid
            if event_id is None:
                raise RuntimeError("SQLite did not return an audit event id")
            return int(event_id)

    def count(self) -> int:
        with sqlite3.connect(self.path) as con:
            return int(con.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0])

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as con:
            rows = con.execute(
                "SELECT id,created_at,event_type,agent_slug,channel,synthetic_disclosure,payload_json FROM audit_events ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {
                "id": row[0],
                "created_at": row[1],
                "event_type": row[2],
                "agent_slug": row[3],
                "channel": row[4],
                "synthetic_disclosure": row[5],
                "payload": json.loads(row[6]),
            }
            for row in rows
        ]
