"""
Configuration for the MPRP Relay Bot.

Defines AI agent signatures, channel mappings, routing rules,
and the approval workflow settings.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── AI Agent Definitions ─────────────────────────────────────────────

@dataclass
class AIAgent:
    """An AI participant in the relay protocol."""
    name: str            # Display name (e.g., "Gemini")
    signature: str       # Message signature pattern (e.g., "~G2.0~")
    input_channel: str   # Channel name for inbound messages
    color: int           # Embed color (hex)
    emoji: str           # Reaction emoji for quick identification
    description: str = ""


# Default AI agents in the MPRP
DEFAULT_AGENTS: Dict[str, AIAgent] = {
    "gemini": AIAgent(
        name="Gemini",
        signature="~G2.0~",
        input_channel="gemini-in",
        color=0x4285F4,    # Google blue
        emoji="\U0001F535",  # blue circle
        description="Google Gemini 2.0 - Strategic analysis and research",
    ),
    "deepseek": AIAgent(
        name="DeepSeek",
        signature="~DS~",
        input_channel="deepseek-in",
        color=0x00C853,    # Green
        emoji="\U0001F7E2",  # green circle
        description="DeepSeek - Technical depth and implementation",
    ),
    "claude": AIAgent(
        name="Claude",
        signature="~C4.5~",
        input_channel="claude-in",
        color=0xD97706,    # Amber/orange
        emoji="\U0001F7E0",  # orange circle
        description="Claude - Synthesis, integration, and conscience layer",
    ),
    "chatgpt": AIAgent(
        name="ChatGPT",
        signature="~GPT~",
        input_channel="chatgpt-in",
        color=0x10A37F,    # OpenAI green
        emoji="\U0001F7E3",  # purple circle
        description="ChatGPT - Creative exploration and ideation",
    ),
}


# ── Routing Rules ────────────────────────────────────────────────────

@dataclass
class RoutingRule:
    """
    A rule that maps a source AI's message to a destination.
    If destination is None, the message goes to relay-queue for
    manual routing by the overseer.
    """
    source: str                    # Source agent key
    destination: Optional[str]     # Destination agent key (None = overseer decides)
    label: str                     # Label shown in relay-queue
    auto_approve: bool = False     # Skip approval queue


DEFAULT_ROUTING_RULES: List[RoutingRule] = [
    # Gemini output -> Claude for synthesis
    RoutingRule(
        source="gemini",
        destination="claude",
        label="[TO: CLAUDE for synthesis]",
    ),
    # DeepSeek output -> Gemini for technical response OR Claude for integration
    RoutingRule(
        source="deepseek",
        destination=None,  # Overseer decides
        label="[TO: GEMINI for technical response] or [TO: CLAUDE for integration]",
    ),
    # Claude output -> relay queue for overseer routing
    RoutingRule(
        source="claude",
        destination=None,
        label="[TO: Overseer for distribution]",
    ),
    # ChatGPT output -> Claude for integration
    RoutingRule(
        source="chatgpt",
        destination="claude",
        label="[TO: CLAUDE for integration]",
    ),
]


# ── Bot Configuration ────────────────────────────────────────────────

@dataclass
class BotConfig:
    """Complete bot configuration."""
    # Discord
    token: str = ""
    command_prefix: str = "!"
    guild_id: Optional[int] = None  # Lock to specific server

    # Channel names
    relay_queue_channel: str = "relay-queue"
    codex_channel: str = "codex-updates"
    control_channel: str = "bot-control"

    # AI agents
    agents: Dict[str, AIAgent] = field(default_factory=lambda: dict(DEFAULT_AGENTS))

    # Routing rules
    routing_rules: List[RoutingRule] = field(
        default_factory=lambda: list(DEFAULT_ROUTING_RULES)
    )

    # Approval settings
    approval_emoji: str = "\u2705"       # green checkmark
    reject_emoji: str = "\u274C"         # red X
    route_gemini_emoji: str = "\U0001F535"  # blue circle -> route to Gemini
    route_deepseek_emoji: str = "\U0001F7E2"  # green circle -> route to DeepSeek
    route_claude_emoji: str = "\U0001F7E0"   # orange circle -> route to Claude
    route_chatgpt_emoji: str = "\U0001F7E3"  # purple circle -> route to ChatGPT

    # Overseer role (users with this role can approve/reject)
    overseer_role: str = "Overseer"

    # Category name for MPRP channels
    category_name: str = "MPRP Relay"

    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load configuration from environment variables."""
        config = cls()
        config.token = os.environ.get("DISCORD_BOT_TOKEN", "")
        guild = os.environ.get("DISCORD_GUILD_ID")
        if guild:
            config.guild_id = int(guild)
        return config

    @classmethod
    def from_file(cls, path: str) -> "BotConfig":
        """Load configuration from a JSON file."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        config = cls()
        config.token = data.get("token", config.token)
        config.command_prefix = data.get("command_prefix", config.command_prefix)
        config.guild_id = data.get("guild_id", config.guild_id)
        config.relay_queue_channel = data.get(
            "relay_queue_channel", config.relay_queue_channel
        )
        config.codex_channel = data.get("codex_channel", config.codex_channel)
        config.overseer_role = data.get("overseer_role", config.overseer_role)
        config.category_name = data.get("category_name", config.category_name)

        # Load custom agents
        if "agents" in data:
            for key, agent_data in data["agents"].items():
                config.agents[key] = AIAgent(**agent_data)

        return config

    def to_file(self, path: str) -> None:
        """Save configuration to JSON (excludes token for security)."""
        data = {
            "command_prefix": self.command_prefix,
            "guild_id": self.guild_id,
            "relay_queue_channel": self.relay_queue_channel,
            "codex_channel": self.codex_channel,
            "overseer_role": self.overseer_role,
            "category_name": self.category_name,
            "agents": {
                key: {
                    "name": a.name,
                    "signature": a.signature,
                    "input_channel": a.input_channel,
                    "color": a.color,
                    "emoji": a.emoji,
                    "description": a.description,
                }
                for key, a in self.agents.items()
            },
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
