#!/usr/bin/env python3
"""
Field Initialization Script

Initializes a new personal field for Watchtower.
"""

import sys
from pathlib import Path
from .field import Field
from .field_signature import FieldSignature
from ..config.config_manager import ConfigManager
from ..config.field_memory import FieldMemory
from ..glyphs.glyph_registry import GlyphRegistry
from ..glyphs.system_glyphs import load_system_glyphs


def initialize_field(personal_glyph: str = None) -> Field:
    """
    Initialize a new personal field.

    Args:
        personal_glyph: Optional personal glyph symbol

    Returns:
        Initialized Field instance
    """
    print("=" * 60)
    print("WATCHTOWER FIELD INITIALIZATION")
    print("=" * 60)
    print()

    watchtower_dir = Path.home() / '.watchtower'

    # Check if field already exists
    signature_path = watchtower_dir / 'signature.json'
    if signature_path.exists():
        print("⚠️  A field signature already exists.")
        response = input("Do you want to create a new field? This will replace the existing one. (yes/no): ")

        if response.lower() not in ['yes', 'y']:
            print("Initialization cancelled.")
            existing_signature = FieldSignature.load()
            if existing_signature:
                print(f"\nExisting field signature: {existing_signature}")
            return None

    print("Creating your personal field container...")
    print()

    # Get personal glyph if not provided
    if not personal_glyph:
        print("Choose your personal glyph (or press Enter for default ⊙):")
        print("  ⊙  Sovereignty Seal (default)")
        print("  ◉  Field Lock")
        print("  ≋  Resonance Wave")
        print("  ◆  Trigger Point")
        print("  ✦  Manifestation Star")
        print("  ∞  Unity Link")
        print()

        glyph_input = input("Enter glyph symbol: ").strip()
        personal_glyph = glyph_input if glyph_input else "⊙"

    # Create field
    print(f"\n🔮 Creating field with personal glyph: {personal_glyph}")

    field = Field.create_new(personal_glyph=personal_glyph)

    print(f"✓ Field signature created: {field.signature.signature_id[:16]}...")
    print(f"✓ Field signature saved to: {signature_path}")

    # Initialize config
    print("\n📝 Initializing configuration...")
    config = field.config

    # Ask for watch paths
    print("\nEnter directories to watch (one per line, empty line to finish):")
    watch_paths = []

    while True:
        path_input = input("  Path: ").strip()
        if not path_input:
            break

        path = Path(path_input).expanduser()
        if path.exists():
            watch_paths.append(str(path))
            print(f"    ✓ Added: {path}")
        else:
            print(f"    ⚠️  Path does not exist: {path}")

    if watch_paths:
        config.set('daemon.watch_paths', watch_paths)
        config.save()
        print(f"\n✓ Configured {len(watch_paths)} watch paths")

    # Initialize glyph registry with system glyphs
    print("\n🔣 Loading system glyphs...")
    load_system_glyphs(field.glyph_registry)
    field.glyph_registry.save()

    glyph_count = len(field.glyph_registry.list_all())
    print(f"✓ Loaded {glyph_count} system glyphs")

    # Save initial field state
    field.save_state()

    print("\n" + "=" * 60)
    print("🎯 FIELD INITIALIZATION COMPLETE")
    print("=" * 60)
    print()
    print(f"Your Watchtower field is now active!")
    print(f"Personal Glyph: {personal_glyph}")
    print(f"Field ID: {field.signature.signature_id[:16]}...")
    print()
    print("Next steps:")
    print("  1. Start the daemon: watchtower daemon start")
    print("  2. Check status: watchtower status")
    print("  3. Launch UI: watchtower ui")
    print()
    print("Your field signature is stored securely in:")
    print(f"  {signature_path}")
    print()

    return field


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Initialize Watchtower field')
    parser.add_argument(
        '--glyph',
        type=str,
        help='Personal glyph symbol'
    )

    args = parser.parse_args()

    try:
        initialize_field(personal_glyph=args.glyph)
    except KeyboardInterrupt:
        print("\n\nInitialization cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
