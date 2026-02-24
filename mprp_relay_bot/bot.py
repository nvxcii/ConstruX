"""
MPRP Relay Bot - Discord client implementation.

Handles:
  - Automatic channel setup (!setup command)
  - Message detection in AI input channels
  - Relay queue posting with approval reactions
  - Reaction-based routing (!approve, emoji routing)
  - Codex logging of all approved relays
  - Status commands (!status, !pending, !codex)
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Optional

import discord
from discord.ext import commands

from mprp_relay_bot.config import BotConfig
from mprp_relay_bot.router import MessageRouter, PendingRelay

logger = logging.getLogger(__name__)


class MPRPRelayBot(commands.Bot):
    """
    Discord bot implementing the Multi-Platform Relay Protocol.

    Monitors AI input channels for messages, routes them through
    an approval queue, and delivers approved messages to destination
    channels with full codex logging.
    """

    def __init__(self, config: BotConfig):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix=config.command_prefix,
            intents=intents,
            help_command=None,
        )

        self.config = config
        self.router = MessageRouter(config)

        # Channel cache (populated on ready or after setup)
        self._channels: Dict[str, discord.TextChannel] = {}
        self._category: Optional[discord.CategoryChannel] = None
        self._ready = False

    # ═══════════════════════════════════════════════════════════════
    # LIFECYCLE
    # ═══════════════════════════════════════════════════════════════

    async def on_ready(self):
        logger.info("MPRP Relay Bot online as %s (ID: %s)", self.user, self.user.id)
        await self._cache_channels()
        self._ready = True
        logger.info(
            "Channels cached: %s",
            ", ".join(self._channels.keys()) or "(none -- run !setup)",
        )

    async def setup_hook(self):
        """Register all commands."""
        self.add_command(cmd_setup)
        self.add_command(cmd_status)
        self.add_command(cmd_pending)
        self.add_command(cmd_approve)
        self.add_command(cmd_reject)
        self.add_command(cmd_route)
        self.add_command(cmd_codex)
        self.add_command(cmd_help_mprp)

    # ═══════════════════════════════════════════════════════════════
    # MESSAGE HANDLING -- THE RELAY CORE
    # ═══════════════════════════════════════════════════════════════

    async def on_message(self, message: discord.Message):
        # Ignore own messages
        if message.author == self.user:
            return

        # Process commands first
        await self.process_commands(message)

        # Skip if not in a monitored AI input channel
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.channel.name not in self.router.input_channel_names:
            return

        # Detect which AI agent this message is from
        source = self.router.detect_source(
            message.content, message.channel.name
        )
        if source is None:
            return

        agent = self.router.get_agent(source)
        logger.info(
            "Detected %s message in #%s (ID: %d)",
            agent.name if agent else source,
            message.channel.name,
            message.id,
        )

        # Create pending relay
        relay = self.router.create_pending_relay(
            source_agent=source,
            content=message.content,
            message_id=message.id,
            channel_id=message.channel.id,
        )

        # Check if routing rule is auto-approve
        rule = self.router.get_routing_rule(source)
        if rule and rule.auto_approve and rule.destination:
            # Auto-approve and deliver immediately
            self.router.approve_relay(relay.relay_id, rule.destination)
            await self._deliver_relay(message.guild, relay)
            await self._log_to_codex(message.guild, relay)
            return

        # Post to relay queue for approval
        await self._post_to_queue(message.guild, relay)

    # ═══════════════════════════════════════════════════════════════
    # REACTION HANDLING -- ONE-CLICK ROUTING
    # ═══════════════════════════════════════════════════════════════

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle reactions on relay queue messages for quick routing."""
        if payload.user_id == self.user.id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return

        # Only process reactions in the relay queue channel
        queue_channel = self._channels.get(self.config.relay_queue_channel)
        if queue_channel is None or payload.channel_id != queue_channel.id:
            return

        # Find the pending relay for this message
        relay = self.router.find_pending_by_queue_message(payload.message_id)
        if relay is None or relay.approved is not None:
            return

        emoji = str(payload.emoji)

        # Check if user has overseer role
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        if not self._is_overseer(member):
            return

        # Route based on emoji
        if emoji == self.config.approval_emoji:
            # Approve with suggested destination
            self.router.approve_relay(relay.relay_id)
            await self._deliver_relay(guild, relay)
            await self._log_to_codex(guild, relay)
            await self._update_queue_message(queue_channel, relay, "APPROVED")

        elif emoji == self.config.reject_emoji:
            self.router.reject_relay(relay.relay_id)
            await self._update_queue_message(queue_channel, relay, "REJECTED")

        elif emoji == self.config.route_gemini_emoji:
            self.router.approve_relay(relay.relay_id, "gemini")
            await self._deliver_relay(guild, relay)
            await self._log_to_codex(guild, relay)
            await self._update_queue_message(queue_channel, relay, "ROUTED -> Gemini")

        elif emoji == self.config.route_deepseek_emoji:
            self.router.approve_relay(relay.relay_id, "deepseek")
            await self._deliver_relay(guild, relay)
            await self._log_to_codex(guild, relay)
            await self._update_queue_message(queue_channel, relay, "ROUTED -> DeepSeek")

        elif emoji == self.config.route_claude_emoji:
            self.router.approve_relay(relay.relay_id, "claude")
            await self._deliver_relay(guild, relay)
            await self._log_to_codex(guild, relay)
            await self._update_queue_message(queue_channel, relay, "ROUTED -> Claude")

        elif emoji == self.config.route_chatgpt_emoji:
            self.router.approve_relay(relay.relay_id, "chatgpt")
            await self._deliver_relay(guild, relay)
            await self._log_to_codex(guild, relay)
            await self._update_queue_message(queue_channel, relay, "ROUTED -> ChatGPT")

    # ═══════════════════════════════════════════════════════════════
    # INTERNAL METHODS
    # ═══════════════════════════════════════════════════════════════

    async def _cache_channels(self):
        """Cache channel references by name."""
        self._channels.clear()
        for guild in self.guilds:
            for channel in guild.text_channels:
                self._channels[channel.name] = channel
                if channel.category and channel.category.name == self.config.category_name:
                    self._category = channel.category

    async def _post_to_queue(
        self, guild: discord.Guild, relay: PendingRelay
    ):
        """Post a relay to the approval queue with reaction buttons."""
        queue = self._channels.get(self.config.relay_queue_channel)
        if queue is None:
            logger.warning("Relay queue channel '%s' not found", self.config.relay_queue_channel)
            return

        embed_data = self.router.format_relay_embed_data(relay)

        embed = discord.Embed(
            title=f"Relay #{relay.relay_id} | {embed_data['source_emoji']} {embed_data['source_name']}",
            description=embed_data["content"],
            color=embed_data["source_color"],
            timestamp=datetime.fromtimestamp(relay.timestamp, tz=timezone.utc),
        )
        embed.add_field(
            name="Routing",
            value=embed_data["label"],
            inline=False,
        )
        embed.add_field(
            name="Suggested Destination",
            value=embed_data["destination_name"],
            inline=True,
        )
        embed.set_footer(text=f"React to route | ID: {relay.relay_id}")

        msg = await queue.send(embed=embed)
        relay.queue_message_id = msg.id

        # Add reaction buttons
        await msg.add_reaction(self.config.approval_emoji)      # approve (suggested dest)
        await msg.add_reaction(self.config.reject_emoji)         # reject

        # Add agent routing reactions
        for key, agent in self.config.agents.items():
            if key != relay.source_agent:
                await msg.add_reaction(agent.emoji)

        logger.info("Posted relay #%d to queue", relay.relay_id)

    async def _deliver_relay(
        self, guild: discord.Guild, relay: PendingRelay
    ):
        """Deliver an approved relay to its destination channel."""
        dest_key = relay.actual_destination
        if dest_key is None:
            logger.warning("Relay #%d has no destination", relay.relay_id)
            return

        dest_agent = self.router.get_agent(dest_key)
        if dest_agent is None:
            logger.warning("Unknown destination agent: %s", dest_key)
            return

        dest_channel = self._channels.get(dest_agent.input_channel)
        if dest_channel is None:
            logger.warning(
                "Destination channel '%s' not found",
                dest_agent.input_channel,
            )
            return

        source_agent = self.router.get_agent(relay.source_agent)
        source_name = source_agent.name if source_agent else relay.source_agent

        # Build delivery embed
        embed = discord.Embed(
            title=f"Relayed from {source_name}",
            description=relay.source_message_content,
            color=source_agent.color if source_agent else 0x808080,
            timestamp=datetime.fromtimestamp(relay.timestamp, tz=timezone.utc),
        )
        embed.set_footer(text=f"Relay #{relay.relay_id} | Approved by Overseer")

        await dest_channel.send(embed=embed)
        logger.info(
            "Delivered relay #%d: %s -> %s",
            relay.relay_id,
            source_name,
            dest_agent.name,
        )

    async def _log_to_codex(
        self, guild: discord.Guild, relay: PendingRelay
    ):
        """Log an approved relay to the codex channel."""
        codex = self._channels.get(self.config.codex_channel)
        if codex is None:
            return

        source_agent = self.router.get_agent(relay.source_agent)
        dest_agent = self.router.get_agent(relay.actual_destination) if relay.actual_destination else None

        source_name = source_agent.name if source_agent else relay.source_agent
        dest_name = dest_agent.name if dest_agent else "Unknown"

        # Codex entry: compact log format
        embed = discord.Embed(
            title=f"Codex Entry #{relay.relay_id}",
            color=0xFFD700,  # Gold
            timestamp=datetime.fromtimestamp(relay.timestamp, tz=timezone.utc),
        )
        embed.add_field(name="Route", value=f"{source_name} -> {dest_name}", inline=True)
        embed.add_field(
            name="Status",
            value="Approved" if relay.approved else "Rejected",
            inline=True,
        )

        # Content preview
        preview = relay.source_message_content[:300]
        if len(relay.source_message_content) > 300:
            preview += "..."
        embed.add_field(name="Content Preview", value=preview, inline=False)

        await codex.send(embed=embed)

    async def _update_queue_message(
        self,
        channel: discord.TextChannel,
        relay: PendingRelay,
        status: str,
    ):
        """Update a queue message to show its resolved status."""
        if relay.queue_message_id is None:
            return

        try:
            msg = await channel.fetch_message(relay.queue_message_id)
            embed = msg.embeds[0] if msg.embeds else discord.Embed()

            embed.color = 0x00FF00 if "APPROVED" in status or "ROUTED" in status else 0xFF0000
            embed.set_footer(text=f"Status: {status} | ID: {relay.relay_id}")

            await msg.edit(embed=embed)
            await msg.clear_reactions()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            logger.warning("Missing permissions to edit queue message")

    def _is_overseer(self, member: discord.Member) -> bool:
        """Check if a member has the overseer role."""
        # Server owner is always an overseer
        if member.guild.owner_id == member.id:
            return True
        return any(
            role.name == self.config.overseer_role
            for role in member.roles
        )


# ═══════════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════════

@commands.command(name="setup")
async def cmd_setup(ctx: commands.Context):
    """Create all MPRP channels and the Overseer role."""
    bot: MPRPRelayBot = ctx.bot
    guild = ctx.guild

    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("You need **Manage Channels** permission to run setup.")
        return

    await ctx.send("Setting up MPRP Relay channels...")

    # Create category
    category = discord.utils.get(guild.categories, name=bot.config.category_name)
    if category is None:
        category = await guild.create_category(bot.config.category_name)
        await ctx.send(f"Created category: **{bot.config.category_name}**")

    # Create AI input channels
    created = []
    for key, agent in bot.config.agents.items():
        ch = discord.utils.get(guild.text_channels, name=agent.input_channel)
        if ch is None:
            ch = await guild.create_text_channel(
                agent.input_channel,
                category=category,
                topic=f"{agent.name} input channel | {agent.description}",
            )
            created.append(agent.input_channel)

    # Create relay queue
    ch = discord.utils.get(guild.text_channels, name=bot.config.relay_queue_channel)
    if ch is None:
        ch = await guild.create_text_channel(
            bot.config.relay_queue_channel,
            category=category,
            topic="Messages pending overseer approval",
        )
        created.append(bot.config.relay_queue_channel)

    # Create codex channel
    ch = discord.utils.get(guild.text_channels, name=bot.config.codex_channel)
    if ch is None:
        ch = await guild.create_text_channel(
            bot.config.codex_channel,
            category=category,
            topic="Approved relay log -- the codex of cross-AI dialogue",
        )
        created.append(bot.config.codex_channel)

    # Create Overseer role
    role = discord.utils.get(guild.roles, name=bot.config.overseer_role)
    if role is None:
        role = await guild.create_role(
            name=bot.config.overseer_role,
            color=discord.Color.gold(),
            reason="MPRP Relay Bot setup",
        )
        # Assign to command invoker
        await ctx.author.add_roles(role)
        created.append(f"@{bot.config.overseer_role} role")

    # Refresh channel cache
    await bot._cache_channels()

    if created:
        await ctx.send(
            f"Setup complete. Created: {', '.join(created)}\n"
            f"You have been assigned the **{bot.config.overseer_role}** role."
        )
    else:
        await ctx.send("All channels and roles already exist. Setup verified.")


@commands.command(name="status")
async def cmd_status(ctx: commands.Context):
    """Show relay bot status and channel overview."""
    bot: MPRPRelayBot = ctx.bot

    embed = discord.Embed(
        title="MPRP Relay Bot Status",
        color=0xFFD700,
        timestamp=datetime.now(timezone.utc),
    )

    # Agent status
    agents_text = ""
    for key, agent in bot.config.agents.items():
        ch = bot._channels.get(agent.input_channel)
        status = "online" if ch else "missing"
        agents_text += f"{agent.emoji} **{agent.name}** (`{agent.signature}`) — #{agent.input_channel} [{status}]\n"
    embed.add_field(name="AI Agents", value=agents_text, inline=False)

    # Queue status
    pending = bot.router.list_pending()
    embed.add_field(name="Pending Relays", value=str(len(pending)), inline=True)
    embed.add_field(
        name="Codex Entries",
        value=str(len(bot.router.codex_log)),
        inline=True,
    )

    # Routing instructions
    instructions = (
        f"React with {bot.config.approval_emoji} to approve (suggested route)\n"
        f"React with {bot.config.reject_emoji} to reject\n"
        f"React with an agent emoji to route to that agent"
    )
    embed.add_field(name="Quick Routing", value=instructions, inline=False)

    await ctx.send(embed=embed)


@commands.command(name="pending")
async def cmd_pending(ctx: commands.Context):
    """List all pending relays awaiting approval."""
    bot: MPRPRelayBot = ctx.bot
    pending = bot.router.list_pending()

    if not pending:
        await ctx.send("No pending relays.")
        return

    embed = discord.Embed(
        title=f"Pending Relays ({len(pending)})",
        color=0xFFA500,
    )

    for relay in pending[:10]:
        source = bot.router.get_agent(relay.source_agent)
        name = source.name if source else relay.source_agent
        preview = relay.source_message_content[:100] + "..."
        embed.add_field(
            name=f"#{relay.relay_id} from {name}",
            value=f"{relay.label}\n`{preview}`",
            inline=False,
        )

    await ctx.send(embed=embed)


@commands.command(name="approve")
async def cmd_approve(ctx: commands.Context, relay_id: int, destination: str = None):
    """Approve a pending relay. Usage: !approve <id> [destination]"""
    bot: MPRPRelayBot = ctx.bot

    if not bot._is_overseer(ctx.author):
        await ctx.send("Only overseers can approve relays.")
        return

    relay = bot.router.approve_relay(relay_id, destination)
    if relay is None:
        await ctx.send(f"Relay #{relay_id} not found.")
        return

    await bot._deliver_relay(ctx.guild, relay)
    await bot._log_to_codex(ctx.guild, relay)

    dest = relay.actual_destination or "none"
    await ctx.send(f"Relay #{relay_id} approved and delivered to **{dest}**.")


@commands.command(name="reject")
async def cmd_reject(ctx: commands.Context, relay_id: int):
    """Reject a pending relay. Usage: !reject <id>"""
    bot: MPRPRelayBot = ctx.bot

    if not bot._is_overseer(ctx.author):
        await ctx.send("Only overseers can reject relays.")
        return

    relay = bot.router.reject_relay(relay_id)
    if relay is None:
        await ctx.send(f"Relay #{relay_id} not found.")
        return

    await ctx.send(f"Relay #{relay_id} rejected.")


@commands.command(name="route")
async def cmd_route(ctx: commands.Context, relay_id: int, destination: str):
    """Route a pending relay to a specific agent. Usage: !route <id> <agent>"""
    bot: MPRPRelayBot = ctx.bot

    if not bot._is_overseer(ctx.author):
        await ctx.send("Only overseers can route relays.")
        return

    if destination not in bot.router.agent_keys:
        agents = ", ".join(bot.router.agent_keys)
        await ctx.send(f"Unknown agent `{destination}`. Available: {agents}")
        return

    relay = bot.router.approve_relay(relay_id, destination)
    if relay is None:
        await ctx.send(f"Relay #{relay_id} not found.")
        return

    await bot._deliver_relay(ctx.guild, relay)
    await bot._log_to_codex(ctx.guild, relay)

    agent = bot.router.get_agent(destination)
    await ctx.send(
        f"Relay #{relay_id} routed to **{agent.name}** (#{agent.input_channel})."
    )


@commands.command(name="codex")
async def cmd_codex(ctx: commands.Context, count: int = 10):
    """Show recent codex entries. Usage: !codex [count]"""
    bot: MPRPRelayBot = ctx.bot
    log = bot.router.codex_log

    if not log:
        await ctx.send("Codex is empty. No relays have been processed yet.")
        return

    recent = log[-count:]
    embed = discord.Embed(
        title=f"Codex Log (last {len(recent)} entries)",
        color=0xFFD700,
    )

    for entry in recent:
        src = entry.get("source", "?")
        dst = entry.get("destination", "?")
        status = entry.get("status", "?")
        preview = entry.get("content_preview", "")[:80]
        embed.add_field(
            name=f"#{entry['relay_id']} | {src} -> {dst} [{status}]",
            value=f"`{preview}...`" if preview else "*empty*",
            inline=False,
        )

    await ctx.send(embed=embed)


@commands.command(name="mprp")
async def cmd_help_mprp(ctx: commands.Context):
    """Show MPRP Relay Bot help."""
    bot: MPRPRelayBot = ctx.bot

    embed = discord.Embed(
        title="MPRP Relay Bot -- Help",
        description="Multi-Platform Relay Protocol for cross-AI dialogue orchestration.",
        color=0xFFD700,
    )

    commands_text = (
        "**!setup** -- Create all MPRP channels and roles\n"
        "**!status** -- Show bot status and agent overview\n"
        "**!pending** -- List relays awaiting approval\n"
        "**!approve <id> [dest]** -- Approve a relay\n"
        "**!reject <id>** -- Reject a relay\n"
        "**!route <id> <agent>** -- Route to a specific agent\n"
        "**!codex [n]** -- Show last N codex entries\n"
        "**!mprp** -- This help message"
    )
    embed.add_field(name="Commands", value=commands_text, inline=False)

    routing_text = (
        f"{bot.config.approval_emoji} Approve (use suggested destination)\n"
        f"{bot.config.reject_emoji} Reject\n"
    )
    for key, agent in bot.config.agents.items():
        routing_text += f"{agent.emoji} Route to {agent.name}\n"
    embed.add_field(name="Reaction Routing", value=routing_text, inline=False)

    embed.add_field(
        name="Workflow",
        value=(
            "1. Paste AI output in the appropriate `#<agent>-in` channel\n"
            "2. Bot detects the signature and posts to `#relay-queue`\n"
            "3. React or use `!approve` to route to the destination\n"
            "4. Bot delivers to the target channel and logs to `#codex-updates`"
        ),
        inline=False,
    )

    await ctx.send(embed=embed)
