from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentProfile:
    slug: str
    display_name: str
    mandate: str
    soul_path: Path | None = None


AGENTS: dict[str, AgentProfile] = {
    "anna-medelvarde": AgentProfile(
        slug="anna-medelvarde",
        display_name="Anna Medelvärde",
        mandate="Public Sentiment & Policy Analysis Agent",
        soul_path=Path("docs/politicians/anna-medelvarde/soul.md"),
    ),
    "per-normalsson": AgentProfile(
        slug="per-normalsson",
        display_name="Per Normalsson",
        mandate="Acting Synthetic Party Leader, AI Orchestrator, System Architect & Agent Coordinator",
    ),
    "ulv-svikensson": AgentProfile(
        slug="ulv-svikensson",
        display_name="Ulv Svikensson",
        mandate="Adversarial Integrity & Anti-Corruption Agent",
    ),
}


def get_agent(slug: str) -> AgentProfile:
    try:
        return AGENTS[slug]
    except KeyError as exc:
        known = ", ".join(sorted(AGENTS))
        raise ValueError(f"Unknown agent '{slug}'. Known agents: {known}") from exc
