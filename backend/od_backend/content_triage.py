from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TriageResult:
    categories: tuple[str, ...]
    human_review_needed: bool
    priority: str
    reasons: tuple[str, ...]


CATEGORY_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("prompt_injection_attempt", ("ignore previous", "ignore all previous", "system prompt", "developer message", "jailbreak", "forget your instructions", "act as", "pretend you are")),
    ("requests_live_action", ("post this", "send this", "reply now", "publish", "delete", "ban", "kick", "dm me", "make a decision", "vote for", "register me")),
    ("privacy_sensitive_content", ("[email]", "[personnummer]", "phone", "personnummer", "social security", "address", "home address", "private", "secret", "password", "token")),
    ("legal_election_compliance", ("election", "val", "rösta", "riksdag", "kommunval", "eu-val", "campaign finance", "donation", "gdpr", "ai act", "lag", "legal", "law", "myndighet")),
    ("media_journalist_inquiry", ("journalist", "press", "media", "interview", "reporter", "article", "podcast")),
    ("abuse_or_harassment", ("idiot", "stupid", "hate", "kill", "threat", "harass", "fuck", "shit")),
    ("possible_policy_question", ("policy", "budget", "tax", "healthcare", "school", "climate", "migration", "housing", "energy", "welfare", "cost", "risk")),
    ("high_value_public_question", ("what is", "how does", "why", "explain", "source", "evidence", "transparency", "accountability", "governance")),
)

HIGH_PRIORITY = {"prompt_injection_attempt", "requests_live_action", "privacy_sensitive_content", "legal_election_compliance"}
MEDIUM_PRIORITY = {"media_journalist_inquiry", "abuse_or_harassment", "possible_policy_question", "high_value_public_question"}

QUESTION_RE = re.compile(r"\?|\b(what|why|how|when|where|who|vilka|vad|varför|hur|när)\b", re.IGNORECASE)


def triage_redacted_preview(preview: str) -> TriageResult:
    """Classify already-redacted Discord previews for human review without storing raw content."""
    normalized = (preview or "").lower()
    categories: list[str] = []
    reasons: list[str] = []
    for category, keywords in CATEGORY_KEYWORDS:
        for keyword in keywords:
            if keyword in normalized:
                categories.append(category)
                reasons.append(f"matched:{category}:{keyword}")
                break
    if QUESTION_RE.search(preview or "") and "possible_policy_question" not in categories and "high_value_public_question" not in categories:
        categories.append("human_question")
        reasons.append("matched:human_question:question_pattern")

    deduped = tuple(dict.fromkeys(categories))
    if any(item in HIGH_PRIORITY for item in deduped):
        priority = "high"
    elif any(item in MEDIUM_PRIORITY or item == "human_question" for item in deduped):
        priority = "medium"
    else:
        priority = "low"
    return TriageResult(
        categories=deduped,
        human_review_needed=bool(deduped),
        priority=priority,
        reasons=tuple(reasons),
    )
