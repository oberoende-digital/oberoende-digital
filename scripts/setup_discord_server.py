#!/usr/bin/env python3
"""Create the recommended Oberoende Digital Discord roles/channels.

Requirements:
  export DISCORD_BOT_TOKEN='...'
  export DISCORD_GUILD_ID='...'
  python3 scripts/setup_discord_server.py

The bot must already be invited to the server with Manage Roles and Manage Channels.
Run once, then configure Discord Community Onboarding manually in Server Settings.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

API = "https://discord.com/api/v10"
TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("DISCORD_TOKEN")
GUILD_ID = os.environ.get("DISCORD_GUILD_ID")
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"

if not TOKEN or not GUILD_ID:
    print("Missing DISCORD_BOT_TOKEN/DISCORD_TOKEN or DISCORD_GUILD_ID", file=sys.stderr)
    sys.exit(2)


def request(method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
    url = API + path
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "OberoendeDigitalDiscordSetup/0.1",
    }
    if DRY_RUN and method not in {"GET"}:
        print(f"DRY_RUN {method} {path}: {json.dumps(payload, ensure_ascii=False)}")
        return {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 204:
                return None
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"Discord API {method} {path} failed: {e.code} {body}") from e


def create_role(name: str, reason: str = "Oberoende Digital setup") -> Any:
    existing = request("GET", f"/guilds/{GUILD_ID}/roles")
    for role in existing:
        if role["name"] == name:
            print(f"role exists: {name}")
            return role
    print(f"creating role: {name}")
    return request("POST", f"/guilds/{GUILD_ID}/roles", {"name": name, "mentionable": True, "reason": reason})


def create_channel(name: str, channel_type: int, parent_id: Optional[str] = None, topic: Optional[str] = None) -> Any:
    existing = request("GET", f"/guilds/{GUILD_ID}/channels")
    for ch in existing:
        if ch["name"] == name and ch.get("parent_id") == parent_id:
            print(f"channel exists: {name}")
            return ch
    payload: Dict[str, Any] = {"name": name, "type": channel_type}
    if parent_id:
        payload["parent_id"] = parent_id
    if topic and channel_type in (0, 15):
        payload["topic"] = topic[:1024]
    print(f"creating channel: {name}")
    return request("POST", f"/guilds/{GUILD_ID}/channels", payload)


roles = [
    "Visitor",
    "Info & AI",
    "Political Participation",
    "Platform Developer",
    "Developer Applicant",
    "Reviewer",
    "Moderator",
    "Admin",
    "OD AI",
]
for role in roles:
    create_role(role)
    time.sleep(0.25)

categories = [
    ("START HERE", [
        ("👋 welcome", "Welcome to Independent Digital. This server is a space for learning about the project, discussing policy, testing ideas, and helping build the platform."),
        ("📌 what-is-independent-digital", "Independent Digital is a policy experiment exploring how AI-supported political participation, transparency, and platform-based governance could work in practice. Important: Independent Digital is currently a policy experiment and debate platform, not a registered political party."),
        ("📜 rules-and-principles", "Be constructive. Argue with ideas, not people. Use evidence where possible. AI-generated content must be transparent. No harassment, spam, impersonation, or manipulation."),
        ("📣 announcements", None),
    ]),
    ("GENERAL", [
        ("🌐 general", None),
        ("🤖 talk-to-od-ai", "Ask OD’s AI questions about the project, policy ideas, platform design, or the experiment itself. The AI can explain, summarize, and structure ideas, but it does not make political decisions."),
        ("❓ questions-and-answers", None),
        ("🗳️ polls", None),
    ]),
    ("POLITICS & POLICY", [
        ("🏛️ political-forum", "A forum for political discussion, democratic participation, and structured debate about the direction of Independent Digital."),
        ("💡 policy-proposals", None),
        ("🔎 scrutiny-and-critique", None),
        ("🧪 ai-party-experiment", None),
        ("📚 sources-and-background", None),
    ]),
    ("PLATFORM DEVELOPMENT", [
        ("🛠️ dev-start", None),
        ("🧩 platform-architecture", None),
        ("🐛 bugs", None),
        ("🚀 feature-requests", None),
        ("🔐 security-and-risk", None),
        ("📦 github-feed", None),
        ("🧪 ai-test-channel", None),
    ]),
    ("INTERNAL", [
        ("🧭 moderator-log", None),
        ("🧯 incidents", None),
        ("📋 decisions-and-minutes", None),
    ]),
]

for category_name, channels in categories:
    category = create_channel(category_name, 4)
    parent_id = category.get("id")
    time.sleep(0.25)
    for channel_name, topic in channels:
        create_channel(channel_name, 0, parent_id=parent_id, topic=topic)
        time.sleep(0.25)

print("Done. Next: configure Discord Community Onboarding manually using docs/discord-onboarding-structure.md.")
