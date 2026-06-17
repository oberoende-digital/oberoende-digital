from __future__ import annotations

DEFAULT_DISCLOSURE = "AI-generated synthetic OD agent response; human operator remains accountable."


def with_synthetic_disclosure(message: str, disclosure: str = DEFAULT_DISCLOSURE) -> str:
    """Attach a clear AI/synthetic disclosure to every outbound agent message."""
    clean = (message or "").strip()
    notice = (disclosure or DEFAULT_DISCLOSURE).strip()
    if not clean:
        clean = "No substantive response was generated."
    if notice.lower() in clean.lower():
        return clean
    return f"{clean}\n\n— {notice}"
