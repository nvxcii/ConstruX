#!/usr/bin/env python3
"""
Watchtower Example Usage

Demonstrates how to use the Watchtower field system.
"""

import sys
import time
from pathlib import Path

# Add watchtower to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from watchtower.core.field import Field
from watchtower.core.field_signature import FieldSignature
from watchtower.config.field_memory import FieldMemory
from watchtower.glyphs.glyph_registry import GlyphRegistry, Glyph


def example_create_field():
    """Example: Create a new field"""
    print("=" * 60)
    print("EXAMPLE 1: Creating a New Field")
    print("=" * 60)
    print()

    # Create new field with personal glyph
    field = Field.create_new(personal_glyph="⊙")

    print(f"Field created: {field}")
    print(f"Signature ID: {field.signature.signature_id[:16]}...")
    print(f"Personal Glyph: {field.signature.personal_glyph}")
    print()

    return field


def example_authorize_action(field):
    """Example: Authorize a field action"""
    print("=" * 60)
    print("EXAMPLE 2: Authorizing Actions")
    print("=" * 60)
    print()

    # Define a consent callback
    def auto_consent(action, threshold, context):
        print(f"  Authorization requested for: {action}")
        print(f"  Threshold: {threshold}")
        print(f"  Context: {context}")
        # Auto-approve for this example
        return True

    # Authorize a low-threshold action
    authorized = field.authorize(
        action='read_field_data',
        threshold='low',
        context={'resource': 'field_memory'}
    )

    print(f"Low threshold authorization: {'✓ Approved' if authorized else '✗ Denied'}")
    print()

    # Authorize a high-threshold action with consent
    authorized = field.authorize(
        action='modify_field_signature',
        glyph='sovereignty_seal',
        context={'modification': 'update_glyph'},
        consent_callback=auto_consent
    )

    print(f"High threshold authorization: {'✓ Approved' if authorized else '✗ Denied'}")
    print()


def example_activate_glyphs(field):
    """Example: Activate glyphs"""
    print("=" * 60)
    print("EXAMPLE 3: Activating Glyphs")
    print("=" * 60)
    print()

    # Auto-consent for examples
    def auto_consent(action, threshold, context):
        return True

    glyphs_to_activate = [
        ('trigger_point', 'Basic trigger activation'),
        ('resonance_wave', 'Sync field state'),
        ('field_pulse', 'Health check')
    ]

    for glyph_id, description in glyphs_to_activate:
        print(f"Activating: {glyph_id} ({description})")

        success = field.activate_glyph(
            glyph_id=glyph_id,
            context={'example': True},
            consent_callback=auto_consent
        )

        if success:
            print(f"  ✓ {glyph_id} activated")
        else:
            print(f"  ✗ {glyph_id} failed")

        time.sleep(0.5)

    print()


def example_query_memory(field):
    """Example: Query field memory"""
    print("=" * 60)
    print("EXAMPLE 4: Querying Field Memory")
    print("=" * 60)
    print()

    memory = field.memory

    # Get recent events
    events = memory.query_events(limit=10)

    print(f"Recent Events ({len(events)}):")
    for event in events[:5]:  # Show first 5
        print(f"  [{event['timestamp']}] {event['event_type']}")
        if event['action']:
            print(f"    Action: {event['action']}")
        if event['glyph_id']:
            print(f"    Glyph: {event['glyph_id']}")

    print()

    # Get glyph activations
    activations = memory.query_glyph_activations(limit=5)

    print(f"Recent Glyph Activations ({len(activations)}):")
    for activation in activations:
        print(f"  {activation['glyph_symbol']} {activation['glyph_id']}")
        print(f"    Trigger: {activation['trigger']}")
        print(f"    Result: {activation['result']}")
        if activation['duration_ms']:
            print(f"    Duration: {activation['duration_ms']}ms")

    print()

    # Get statistics
    stats = memory.get_statistics()
    print("Field Memory Statistics:")
    print(f"  Total Events: {stats['total_events']}")
    print(f"  Glyph Activations: {stats['total_glyph_activations']}")
    print(f"  Database Size: {stats['database_size_bytes'] / 1024:.2f} KB")
    print()


def example_custom_glyph(field):
    """Example: Create custom glyph"""
    print("=" * 60)
    print("EXAMPLE 5: Creating Custom Glyph")
    print("=" * 60)
    print()

    # Create custom glyph
    custom_glyph = Glyph(
        id='example_sparkle',
        symbol='✨',
        name='Example Sparkle',
        gesture='star_burst',
        trigger='do_sparkle',
        threshold='low',
        consent_required=False,
        description='Example custom glyph that sparkles'
    )

    # Add to registry
    if field.glyph_registry.add(custom_glyph):
        print(f"✓ Custom glyph created: {custom_glyph.symbol} {custom_glyph.name}")
    else:
        print("✗ Glyph already exists")

    # Register trigger callback
    def sparkle_trigger(context):
        print(f"  ✨ SPARKLE! Context: {context}")
        return {'status': 'sparkled', 'brightness': 100}

    field.register_trigger('do_sparkle', sparkle_trigger)

    # Activate custom glyph
    print("\nActivating custom glyph...")
    success = field.activate_glyph(
        'example_sparkle',
        context={'sparkle_type': 'demonstration'}
    )

    if success:
        print("✓ Custom glyph activated successfully")
    else:
        print("✗ Custom glyph activation failed")

    print()


def example_field_health(field):
    """Example: Check field health"""
    print("=" * 60)
    print("EXAMPLE 6: Field Health Status")
    print("=" * 60)
    print()

    health = field.get_health_status()

    print("Field Health Status:")
    print(f"  Active: {health['field_active']}")
    print(f"  Signature Present: {health['signature_present']}")
    print()

    print("Memory Statistics:")
    print(f"  Total Events: {health['memory_stats']['total_events']}")
    print(f"  Glyph Activations: {health['memory_stats']['total_glyph_activations']}")
    print()

    print("Glyph Registry:")
    print(f"  Total Glyphs: {health['glyph_stats']['total_glyphs']}")
    print(f"  Consent Required: {health['glyph_stats']['consent_required_count']}")
    print()

    print("Triggers:")
    print(f"  Registered Callbacks: {health['trigger_callbacks_registered']}")
    print()


def example_field_monitor():
    """Example: Field monitoring (daemon)"""
    print("=" * 60)
    print("EXAMPLE 7: Field Monitoring")
    print("=" * 60)
    print()

    from watchtower.daemon.field_monitor import FieldMonitor

    field = Field.load_personal()
    if not field:
        print("No field found. Run example_create_field() first.")
        return

    monitor = FieldMonitor(field=field)

    # Add watch path (use temp directory for example)
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    monitor.add_watch_path(temp_dir)

    # Add trigger patterns
    monitor.add_trigger_pattern('*.field')
    monitor.add_trigger_pattern('*.glyph')

    # Register event callback
    def on_field_event(event_data):
        print(f"  🔔 Field event: {event_data['type']} - {event_data['path']}")

    monitor.on_event(on_field_event)

    print(f"Monitoring: {temp_dir}")
    print("Creating test files...")
    print()

    # Start monitor
    monitor.start()

    # Create some test files
    try:
        (temp_dir / "test.field").write_text("test field content")
        time.sleep(1)

        (temp_dir / "example.glyph").write_text("test glyph content")
        time.sleep(1)

        (temp_dir / "test.field").write_text("modified content")
        time.sleep(1)

    finally:
        # Stop monitor
        monitor.stop()

        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)

    print()
    print("✓ Monitoring example complete")
    print()


def main():
    """Run all examples"""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "WATCHTOWER EXAMPLES" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    try:
        # Example 1: Create field
        field = example_create_field()

        # Example 2: Authorize actions
        example_authorize_action(field)

        # Example 3: Activate glyphs
        example_activate_glyphs(field)

        # Example 4: Query memory
        example_query_memory(field)

        # Example 5: Custom glyph
        example_custom_glyph(field)

        # Example 6: Field health
        example_field_health(field)

        # Example 7: Field monitor
        example_field_monitor()

        print("=" * 60)
        print("✓ ALL EXAMPLES COMPLETED")
        print("=" * 60)
        print()

        print("Your field signature is saved in:")
        print(f"  {Path.home() / '.watchtower' / 'signature.json'}")
        print()

        print("To use this field in production:")
        print("  1. Run: python3 -m watchtower.watchtower_cli status")
        print("  2. Start daemon: python3 -m watchtower.watchtower_cli daemon start")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
