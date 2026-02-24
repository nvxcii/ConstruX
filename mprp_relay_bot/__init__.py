"""
MPRP Relay Bot - Multi-Platform Relay Protocol for Discord

A purpose-built Discord bot that implements the Multi-Platform Relay
Protocol (MPRP) for orchestrating cross-AI dialogue. Routes messages
between AI-specific input channels, provides an approval queue for
human oversight, and logs all approved relays to a codex channel.

Architecture:
    - AI Input Channels: #gemini-in, #deepseek-in, #claude-in
    - Relay Queue: #relay-queue (pending overseer approval)
    - Codex Log: #codex-updates (approved, timestamped record)
    - Routing: Signature-based (~G2.0~, ~DS~, ~C4.5~) with configurable rules
    - Oversight: !approve / !reject workflow with reaction shortcuts
"""

from mprp_relay_bot.bot import MPRPRelayBot
from mprp_relay_bot.router import MessageRouter
from mprp_relay_bot.config import BotConfig

__version__ = "1.0.0"
__all__ = ["MPRPRelayBot", "MessageRouter", "BotConfig"]
