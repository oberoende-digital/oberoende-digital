from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MonitorState:
    last_seen_message_id: str | None
    seen_message_ids: frozenset[str]


def load_monitor_state(path: Path) -> MonitorState:
    if not path.exists():
        return MonitorState(None, frozenset())
    data = json.loads(path.read_text())
    seen = data.get("seen_message_ids", [])
    if not isinstance(seen, list):
        seen = []
    last_seen = data.get("last_seen_message_id")
    return MonitorState(str(last_seen) if last_seen else None, frozenset(str(item) for item in seen))


def save_monitor_state(path: Path, state: MonitorState, *, max_seen: int = 1000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    seen_sorted = sorted(state.seen_message_ids, key=_snowflake_sort_key)
    if len(seen_sorted) > max_seen:
        seen_sorted = seen_sorted[-max_seen:]
    payload: dict[str, Any] = {
        "last_seen_message_id": state.last_seen_message_id,
        "seen_message_ids": seen_sorted,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _snowflake_sort_key(value: str) -> tuple[int, str]:
    try:
        return (int(value), value)
    except ValueError:
        return (0, value)


def max_message_id(values: list[str]) -> str | None:
    if not values:
        return None
    return max(values, key=_snowflake_sort_key)
