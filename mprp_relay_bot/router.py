"""
Message routing engine for the MPRP Relay Bot.

Detects AI signatures in messages, determines routing destinations,
manages the approval queue, and logs relayed messages to the codex.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from mprp_relay_bot.config import AIAgent, BotConfig, RoutingRule


@dataclass
class PendingRelay:
    """A message waiting in the relay queue for approval."""
    relay_id: int
    source_agent: str
    source_message_content: str
    source_message_id: int
    source_channel_id: int
    suggested_destination: Optional[str]
    label: str
    queue_message_id: Optional[int] = None  # The message ID in #relay-queue
    timestamp: float = field(default_factory=time.time)
    approved: Optional[bool] = None
    actual_destination: Optional[str] = None


class MessageRouter:
    """
    Routes messages between AI input channels based on signature
    detection and configurable routing rules.
    """

    def __init__(self, config: BotConfig):
        self.config = config
        self._pending: Dict[int, PendingRelay] = {}
        self._next_id = 1
        self._codex_log: List[Dict] = []

        # Pre-compile signature patterns
        self._signature_patterns: Dict[str, re.Pattern] = {}
        for key, agent in config.agents.items():
            # Escape the signature for regex, match it anywhere in message
            escaped = re.escape(agent.signature)
            self._signature_patterns[key] = re.compile(escaped)

    def detect_source(self, content: str, channel_name: str) -> Optional[str]:
        """
        Detect which AI agent authored a message.
        Uses both the channel name and the message signature.
        Returns the agent key or None if unrecognized.
        """
        # Check by channel name first
        for key, agent in self.config.agents.items():
            if channel_name == agent.input_channel:
                return key

        # Fallback: check by signature in message content
        for key, pattern in self._signature_patterns.items():
            if pattern.search(content):
                return key

        return None

    def get_routing_rule(self, source_key: str) -> Optional[RoutingRule]:
        """Find the routing rule for a given source agent."""
        for rule in self.config.routing_rules:
            if rule.source == source_key:
                return rule
        return None

    def create_pending_relay(
        self,
        source_agent: str,
        content: str,
        message_id: int,
        channel_id: int,
    ) -> PendingRelay:
        """
        Create a pending relay entry for the approval queue.
        """
        rule = self.get_routing_rule(source_agent)

        relay = PendingRelay(
            relay_id=self._next_id,
            source_agent=source_agent,
            source_message_content=content,
            source_message_id=message_id,
            source_channel_id=channel_id,
            suggested_destination=rule.destination if rule else None,
            label=rule.label if rule else "[Routing: overseer decision required]",
        )
        self._next_id += 1
        self._pending[relay.relay_id] = relay
        return relay

    def approve_relay(
        self, relay_id: int, destination: Optional[str] = None
    ) -> Optional[PendingRelay]:
        """
        Approve a pending relay. If destination is provided, it
        overrides the suggested destination.
        """
        relay = self._pending.get(relay_id)
        if relay is None:
            return None

        relay.approved = True
        relay.actual_destination = destination or relay.suggested_destination

        # Log to codex
        self._codex_log.append({
            "relay_id": relay.relay_id,
            "source": relay.source_agent,
            "destination": relay.actual_destination,
            "timestamp": time.time(),
            "content_preview": relay.source_message_content[:200],
            "status": "approved",
        })

        return relay

    def reject_relay(self, relay_id: int) -> Optional[PendingRelay]:
        """Reject a pending relay."""
        relay = self._pending.get(relay_id)
        if relay is None:
            return None

        relay.approved = False
        self._codex_log.append({
            "relay_id": relay.relay_id,
            "source": relay.source_agent,
            "destination": None,
            "timestamp": time.time(),
            "content_preview": relay.source_message_content[:200],
            "status": "rejected",
        })

        return relay

    def get_pending(self, relay_id: int) -> Optional[PendingRelay]:
        """Get a pending relay by ID."""
        return self._pending.get(relay_id)

    def find_pending_by_queue_message(self, message_id: int) -> Optional[PendingRelay]:
        """Find a pending relay by its queue message ID."""
        for relay in self._pending.values():
            if relay.queue_message_id == message_id:
                return relay
        return None

    def list_pending(self) -> List[PendingRelay]:
        """List all pending (unapproved) relays."""
        return [
            r for r in self._pending.values()
            if r.approved is None
        ]

    def get_agent(self, key: str) -> Optional[AIAgent]:
        """Get an AI agent by key."""
        return self.config.agents.get(key)

    @property
    def agent_keys(self) -> Set[str]:
        return set(self.config.agents.keys())

    @property
    def input_channel_names(self) -> Set[str]:
        return {a.input_channel for a in self.config.agents.values()}

    @property
    def codex_log(self) -> List[Dict]:
        return list(self._codex_log)

    def format_relay_embed_data(self, relay: PendingRelay) -> Dict:
        """
        Prepare data for building a Discord embed for a relay message.
        Returns a dict with all the fields needed to build the embed.
        """
        source_agent = self.get_agent(relay.source_agent)
        dest_agent = self.get_agent(relay.suggested_destination) if relay.suggested_destination else None

        # Truncate content for the embed
        content = relay.source_message_content
        if len(content) > 1500:
            content = content[:1500] + "\n\n*[truncated -- full message in source channel]*"

        return {
            "relay_id": relay.relay_id,
            "source_name": source_agent.name if source_agent else relay.source_agent,
            "source_color": source_agent.color if source_agent else 0x808080,
            "source_emoji": source_agent.emoji if source_agent else "",
            "destination_name": dest_agent.name if dest_agent else "Overseer Decision",
            "label": relay.label,
            "content": content,
            "timestamp": relay.timestamp,
        }
