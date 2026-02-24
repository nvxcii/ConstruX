"""Run the MPRP Relay Bot: python -m mprp_relay_bot"""

import argparse
import logging
import os
import sys

from mprp_relay_bot.config import BotConfig
from mprp_relay_bot.bot import MPRPRelayBot


def main():
    parser = argparse.ArgumentParser(
        description="MPRP Relay Bot -- Multi-Platform Relay Protocol for Discord"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to bot config JSON file",
    )
    parser.add_argument(
        "--token", "-t",
        type=str,
        default=None,
        help="Discord bot token (overrides config/env)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase verbosity",
    )
    args = parser.parse_args()

    # Configure logging
    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Load configuration
    if args.config and os.path.isfile(args.config):
        config = BotConfig.from_file(args.config)
    else:
        config = BotConfig.from_env()

    # Token priority: CLI arg > config file > env var
    if args.token:
        config.token = args.token
    if not config.token:
        config.token = os.environ.get("DISCORD_BOT_TOKEN", "")

    if not config.token:
        print(
            "Error: No Discord bot token provided.\n"
            "Set DISCORD_BOT_TOKEN environment variable, use --token, or\n"
            "add 'token' to your config file.",
            file=sys.stderr,
        )
        return 1

    # Create and run bot
    bot = MPRPRelayBot(config)

    print("Starting MPRP Relay Bot...")
    print(f"  Agents: {', '.join(a.name for a in config.agents.values())}")
    print(f"  Prefix: {config.command_prefix}")
    print(f"  Queue:  #{config.relay_queue_channel}")
    print(f"  Codex:  #{config.codex_channel}")
    print()

    try:
        bot.run(config.token, log_handler=None)
    except KeyboardInterrupt:
        print("\nShutting down.")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
