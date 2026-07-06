#!/usr/bin/env python3
"""
Watchtower CLI - Command Line Interface

Main CLI for interacting with the Watchtower field system.
"""

import sys
import json
from pathlib import Path
from typing import Optional


def cmd_init(args):
    """Initialize a new field"""
    from watchtower.core.field_init import initialize_field
    initialize_field(personal_glyph=args.glyph)


def cmd_status(args):
    """Show field status"""
    from watchtower.core.field import Field

    field = Field.load_personal()
    if not field:
        print("❌ No field found. Run 'watchtower init' first.")
        return 1

    print("=" * 60)
    print("WATCHTOWER FIELD STATUS")
    print("=" * 60)
    print()

    # Field info
    print("Field Information:")
    print(f"  ID: {field.signature.signature_id[:16]}...")
    print(f"  Glyph: {field.signature.personal_glyph}")
    print(f"  Active: {field.state.get('active', False)}")
    print()

    # Health status
    health = field.get_health_status()
    print("System Health:")
    print(f"  Signature: {'✓' if health['signature_present'] else '✗'}")
    print(f"  Total Events: {health['memory_stats']['total_events']}")
    print(f"  Glyphs Loaded: {health['glyph_stats']['total_glyphs']}")
    print(f"  Triggers Registered: {health['trigger_callbacks_registered']}")
    print()

    # Configuration
    config_path = Path.home() / '.watchtower' / 'config.json'
    if config_path.exists():
        watch_paths = field.config.get('daemon.watch_paths', [])
        print("Configuration:")
        print(f"  Watch Paths: {len(watch_paths)}")
        for path in watch_paths:
            print(f"    - {path}")
        print()

    return 0


def cmd_daemon(args):
    """Daemon commands"""
    from watchtower.daemon.daemon_service import WatchtowerDaemon

    try:
        daemon = WatchtowerDaemon()

        if args.daemon_cmd == 'start':
            daemon.start()
        elif args.daemon_cmd == 'stop':
            daemon.stop()
        elif args.daemon_cmd == 'status':
            status = daemon.get_status()
            print(json.dumps(status, indent=2))
        elif args.daemon_cmd == 'reload':
            daemon.reload_config()

    except Exception as e:
        print(f"❌ Daemon error: {e}")
        return 1

    return 0


def cmd_glyphs(args):
    """Glyph management commands"""
    from watchtower.glyphs.glyph_registry import GlyphRegistry

    registry = GlyphRegistry()

    if args.glyph_cmd == 'list':
        glyphs = registry.list_all()
        print("=" * 60)
        print("WATCHTOWER GLYPHS")
        print("=" * 60)
        print()

        for glyph in sorted(glyphs, key=lambda g: g.threshold):
            consent = "✓" if glyph.consent_required else "–"
            print(f"{glyph.symbol}  {glyph.name}")
            print(f"   ID: {glyph.id}")
            print(f"   Trigger: {glyph.trigger}")
            print(f"   Threshold: {glyph.threshold} | Consent: {consent}")
            print(f"   {glyph.description[:80]}...")
            print()

    elif args.glyph_cmd == 'export':
        output_path = Path(args.output or 'glyphs.md')
        registry.export_markdown(output_path)
        print(f"✓ Glyphs exported to: {output_path}")

    return 0


def cmd_memory(args):
    """Field memory commands"""
    from watchtower.config.field_memory import FieldMemory

    memory = FieldMemory()

    if args.memory_cmd == 'stats':
        stats = memory.get_statistics()
        print("=" * 60)
        print("FIELD MEMORY STATISTICS")
        print("=" * 60)
        print()
        print(f"Total Events: {stats['total_events']}")
        print(f"Glyph Activations: {stats['total_glyph_activations']}")
        print(f"Field States: {stats['total_field_states']}")
        print(f"Daemon Activity: {stats['total_daemon_activity']}")
        print(f"Database Size: {stats['database_size_bytes'] / 1024:.2f} KB")
        print()

        if stats['oldest_event']:
            print(f"Oldest Event: {stats['oldest_event']}")
        if stats['newest_event']:
            print(f"Newest Event: {stats['newest_event']}")

    elif args.memory_cmd == 'events':
        events = memory.query_events(
            timerange=args.timerange,
            limit=args.limit
        )

        print(f"\nRecent Events ({len(events)}):")
        for event in events:
            print(f"  [{event['timestamp']}] {event['event_type']}")
            if event['action']:
                print(f"    Action: {event['action']}")
            if event['glyph_id']:
                print(f"    Glyph: {event['glyph_id']}")

    elif args.memory_cmd == 'export':
        output_path = Path(args.output or 'field_memory.json')
        memory.export_json(output_path)
        print(f"✓ Memory exported to: {output_path}")

    return 0


def cmd_ui(args):
    """Launch Watchtower UI"""
    print("🚀 Launching Watchtower UI...")
    print()
    print("⚠️  UI not yet implemented.")
    print("    The UI will be a Tauri-based native application.")
    print("    See watchtower/ui/ for future implementation.")
    print()
    return 1


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Watchtower - Persistent Field Container System'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize new field')
    init_parser.add_argument('--glyph', type=str, help='Personal glyph symbol')
    init_parser.set_defaults(func=cmd_init)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show field status')
    status_parser.set_defaults(func=cmd_status)

    # Daemon command
    daemon_parser = subparsers.add_parser('daemon', help='Daemon management')
    daemon_parser.add_argument(
        'daemon_cmd',
        choices=['start', 'stop', 'status', 'reload'],
        help='Daemon command'
    )
    daemon_parser.set_defaults(func=cmd_daemon)

    # Glyphs command
    glyphs_parser = subparsers.add_parser('glyphs', help='Glyph management')
    glyphs_parser.add_argument(
        'glyph_cmd',
        choices=['list', 'export'],
        help='Glyph command'
    )
    glyphs_parser.add_argument('--output', type=str, help='Output file')
    glyphs_parser.set_defaults(func=cmd_glyphs)

    # Memory command
    memory_parser = subparsers.add_parser('memory', help='Field memory management')
    memory_parser.add_argument(
        'memory_cmd',
        choices=['stats', 'events', 'export'],
        help='Memory command'
    )
    memory_parser.add_argument('--timerange', type=str, default='last_24_hours')
    memory_parser.add_argument('--limit', type=int, default=20)
    memory_parser.add_argument('--output', type=str, help='Output file')
    memory_parser.set_defaults(func=cmd_memory)

    # UI command
    ui_parser = subparsers.add_parser('ui', help='Launch UI')
    ui_parser.set_defaults(func=cmd_ui)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
