"""
Glyph Registry - Symbolic Language System

Manages the symbolic glyphs used for field interaction.
Each glyph represents a meaning and can trigger field actions.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class Glyph:
    """
    A symbolic glyph representing a field action or meaning.

    Attributes:
        id: Unique identifier
        symbol: Unicode symbol (e.g., ⊙, ◉, ≋)
        name: Human-readable name
        gesture: Gesture pattern for activation
        trigger: Function or action to trigger
        threshold: Threshold level (low, medium, high, critical)
        consent_required: Whether explicit consent is required
        description: Description of the glyph's meaning
        metadata: Additional metadata
    """
    id: str
    symbol: str
    name: str
    gesture: str
    trigger: str
    threshold: str
    consent_required: bool = False
    description: str = ""
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Glyph':
        """Create from dictionary"""
        return cls(**data)


class GlyphRegistry:
    """
    Registry for managing symbolic glyphs.

    Stores both system glyphs and personal/custom glyphs.
    """

    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            watchtower_dir = Path.home() / '.watchtower' / 'glyphs'
            watchtower_dir.mkdir(exist_ok=True, parents=True)
            registry_path = watchtower_dir / 'registry.json'

        self.registry_path = registry_path
        self.glyphs: Dict[str, Glyph] = {}
        self._load_registry()

    def _load_registry(self):
        """Load glyph registry from disk"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                self.glyphs = {
                    glyph_id: Glyph.from_dict(glyph_data)
                    for glyph_id, glyph_data in data.items()
                }

    def save(self):
        """Save glyph registry to disk"""
        data = {
            glyph_id: glyph.to_dict()
            for glyph_id, glyph in self.glyphs.items()
        }

        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, glyph: Glyph) -> bool:
        """
        Add a glyph to the registry.

        Args:
            glyph: Glyph to add

        Returns:
            True if added, False if ID already exists
        """
        if glyph.id in self.glyphs:
            return False

        self.glyphs[glyph.id] = glyph
        self.save()
        return True

    def add_from_dict(self, glyph_data: Dict[str, Any]) -> bool:
        """
        Add a glyph from dictionary.

        Args:
            glyph_data: Glyph data dictionary

        Returns:
            True if added, False if ID already exists
        """
        glyph = Glyph.from_dict(glyph_data)
        return self.add(glyph)

    def get(self, glyph_id: str) -> Optional[Glyph]:
        """
        Get a glyph by ID.

        Args:
            glyph_id: Glyph identifier

        Returns:
            Glyph or None if not found
        """
        return self.glyphs.get(glyph_id)

    def get_by_symbol(self, symbol: str) -> Optional[Glyph]:
        """
        Get a glyph by symbol.

        Args:
            symbol: Glyph symbol

        Returns:
            Glyph or None if not found
        """
        for glyph in self.glyphs.values():
            if glyph.symbol == symbol:
                return glyph
        return None

    def update(self, glyph_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a glyph.

        Args:
            glyph_id: Glyph identifier
            updates: Dictionary of fields to update

        Returns:
            True if updated, False if not found
        """
        if glyph_id not in self.glyphs:
            return False

        glyph = self.glyphs[glyph_id]
        for key, value in updates.items():
            if hasattr(glyph, key):
                setattr(glyph, key, value)

        self.save()
        return True

    def remove(self, glyph_id: str) -> bool:
        """
        Remove a glyph.

        Args:
            glyph_id: Glyph identifier

        Returns:
            True if removed, False if not found
        """
        if glyph_id not in self.glyphs:
            return False

        del self.glyphs[glyph_id]
        self.save()
        return True

    def list_all(self) -> List[Glyph]:
        """
        List all glyphs.

        Returns:
            List of all glyphs
        """
        return list(self.glyphs.values())

    def list_by_threshold(self, threshold: str) -> List[Glyph]:
        """
        List glyphs by threshold level.

        Args:
            threshold: Threshold level

        Returns:
            List of glyphs at that threshold
        """
        return [
            glyph for glyph in self.glyphs.values()
            if glyph.threshold == threshold
        ]

    def search(self, query: str) -> List[Glyph]:
        """
        Search glyphs by name, description, or trigger.

        Args:
            query: Search query

        Returns:
            List of matching glyphs
        """
        query_lower = query.lower()
        results = []

        for glyph in self.glyphs.values():
            if (query_lower in glyph.name.lower() or
                query_lower in glyph.description.lower() or
                query_lower in glyph.trigger.lower()):
                results.append(glyph)

        return results

    def export_markdown(self, output_path: Path):
        """
        Export glyph registry as markdown documentation.

        Args:
            output_path: Path to output markdown file
        """
        lines = [
            "# Watchtower Glyph Registry",
            "",
            "Symbolic glyphs for field interaction.",
            "",
            "| Symbol | Name | Gesture | Trigger | Threshold | Consent |",
            "|--------|------|---------|---------|-----------|---------|"
        ]

        for glyph in sorted(self.glyphs.values(), key=lambda g: g.threshold):
            consent = "✓" if glyph.consent_required else "–"
            lines.append(
                f"| {glyph.symbol} | {glyph.name} | {glyph.gesture} | "
                f"{glyph.trigger} | {glyph.threshold} | {consent} |"
            )

        lines.extend([
            "",
            "## Descriptions",
            ""
        ])

        for glyph in sorted(self.glyphs.values(), key=lambda g: g.name):
            lines.extend([
                f"### {glyph.symbol} {glyph.name}",
                "",
                f"**ID**: `{glyph.id}`  ",
                f"**Gesture**: {glyph.gesture}  ",
                f"**Trigger**: `{glyph.trigger}`  ",
                f"**Threshold**: {glyph.threshold}  ",
                f"**Consent Required**: {'Yes' if glyph.consent_required else 'No'}  ",
                "",
                glyph.description,
                ""
            ])

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics.

        Returns:
            Dictionary of statistics
        """
        threshold_counts = {}
        for glyph in self.glyphs.values():
            threshold_counts[glyph.threshold] = threshold_counts.get(glyph.threshold, 0) + 1

        return {
            'total_glyphs': len(self.glyphs),
            'consent_required_count': sum(1 for g in self.glyphs.values() if g.consent_required),
            'threshold_distribution': threshold_counts
        }
