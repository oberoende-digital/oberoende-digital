from __future__ import annotations

from dataclasses import dataclass

from .agents import AgentProfile, get_agent
from .audit_log import AuditLog
from .disclosure import with_synthetic_disclosure


@dataclass(frozen=True)
class RouteResult:
    agent: AgentProfile
    response: str
    audit_event_id: int


def choose_agent(message: str) -> AgentProfile:
    text = (message or "").lower()
    if any(word in text for word in ["budget", "cost", "benefit", "sentiment", "policy", "value for money", "green book"]):
        return get_agent("anna-medelvarde")
    if any(word in text for word in ["corruption", "risk", "attack", "red team", "integrity"]):
        return get_agent("ulv-svikensson")
    return get_agent("per-normalsson")


def route_message(message: str, *, channel: str, audit_log: AuditLog, disclosure: str) -> RouteResult:
    agent = choose_agent(message)
    base = (
        f"{agent.display_name} received this as a Phase 1 dry-run. "
        "No autonomous political decision or external LLM call was made. "
        f"Mandate: {agent.mandate}."
    )
    response = with_synthetic_disclosure(base, disclosure)
    event_id = audit_log.record(
        "dry_run_route",
        agent_slug=agent.slug,
        channel=channel,
        synthetic_disclosure=disclosure,
        payload={"input_preview": (message or "")[:500], "response": response},
    )
    return RouteResult(agent=agent, response=response, audit_event_id=event_id)
