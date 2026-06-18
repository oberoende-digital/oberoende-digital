from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import re

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION_RE = re.compile(r"<@!?\d+>|<@&\d+>|<#\d+>")
# Swedish personnummer/samordningsnummer-like forms: YYMMDD-XXXX, YYMMDD+XXXX,
# YYYYMMDDXXXX, YYYYMMDD-XXXX. US SSN-like NNN-NN-NNNN is included because
# users may describe this generically as a social security number.
PERSONAL_ID_RE = re.compile(r"\b(?:\d{2})?\d{6}[-+ ]?\d{4}\b|\b\d{3}-\d{2}-\d{4}\b")
SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class MinimizedDiscordMessage:
    message_id: str
    channel_id: str
    author_hash: str
    created_at: str | None
    redacted_preview: str


def pseudonymize_identifier(identifier: str, secret: str) -> str:
    """Return a stable pseudonym without storing raw Discord user IDs."""
    digest = hmac.new(secret.encode("utf-8"), identifier.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"sha256:{digest[:24]}"


def redact_text(text: str, *, max_chars: int = 160) -> str:
    """Redact obvious direct identifiers and keep only a short preview."""
    clean = EMAIL_RE.sub("[email]", text or "")
    clean = URL_RE.sub("[url]", clean)
    clean = MENTION_RE.sub("[mention]", clean)
    clean = PERSONAL_ID_RE.sub("[personal_id]", clean)
    clean = SPACE_RE.sub(" ", clean).strip()
    if len(clean) <= max_chars:
        return clean
    return clean[: max(0, max_chars - 1)].rstrip() + "…"


def minimize_discord_message(
    *,
    message_id: str,
    channel_id: str,
    author_id: str,
    content: str,
    created_at: str | None,
    secret: str,
) -> MinimizedDiscordMessage:
    return MinimizedDiscordMessage(
        message_id=message_id,
        channel_id=channel_id,
        author_hash=pseudonymize_identifier(author_id, secret),
        created_at=created_at,
        redacted_preview=redact_text(content),
    )
