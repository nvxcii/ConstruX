"""
System Glyphs - Default Symbolic Language

Defines the core system glyphs used by Watchtower.
"""

from .glyph_registry import Glyph

SYSTEM_GLYPHS = [
    Glyph(
        id="sovereignty_seal",
        symbol="⊙",
        name="Sovereignty Seal",
        gesture="circle_with_center",
        trigger="authorize_field_action",
        threshold="high",
        consent_required=True,
        description="The primary glyph of personal authority. Used to authorize significant field actions. Represents the center of your field - your sovereign authority over the system."
    ),
    Glyph(
        id="field_lock",
        symbol="◉",
        name="Field Lock",
        gesture="filled_circle_with_center",
        trigger="secure_field_boundary",
        threshold="critical",
        consent_required=True,
        description="Establishes a secure field boundary. No actions can cross this boundary without explicit authorization. Used to protect critical field operations."
    ),
    Glyph(
        id="resonance_wave",
        symbol="≋",
        name="Resonance Wave",
        gesture="triple_wave",
        trigger="sync_field_state",
        threshold="medium",
        consent_required=False,
        description="Synchronizes field state across components. Represents the flow of information through the field. Creates coherence between different field layers."
    ),
    Glyph(
        id="trigger_point",
        symbol="◆",
        name="Trigger Point",
        gesture="diamond",
        trigger="activate_response",
        threshold="low",
        consent_required=False,
        description="Activates a predefined field response. A general-purpose activation glyph for low-threshold actions."
    ),
    Glyph(
        id="field_anchor",
        symbol="⚓",
        name="Field Anchor",
        gesture="anchor",
        trigger="persist_state",
        threshold="high",
        consent_required=True,
        description="Anchors the current field state to persistent memory. Ensures that significant field configurations are not lost."
    ),
    Glyph(
        id="observation_eye",
        symbol="◔",
        name="Observation Eye",
        gesture="half_circle_with_dot",
        trigger="monitor_field",
        threshold="low",
        consent_required=False,
        description="Passive field observation. Monitors without intervening. Represents awareness without action."
    ),
    Glyph(
        id="boundary_gate",
        symbol="⫘",
        name="Boundary Gate",
        gesture="gate_symbol",
        trigger="controlled_access",
        threshold="medium",
        consent_required=False,
        description="Controls access through field boundaries. Allows conditional passage based on criteria."
    ),
    Glyph(
        id="field_pulse",
        symbol="◌",
        name="Field Pulse",
        gesture="empty_circle",
        trigger="health_check",
        threshold="low",
        consent_required=False,
        description="Sends a pulse through the field to check system health. Returns status of all field components."
    ),
    Glyph(
        id="consciousness_spiral",
        symbol="◎",
        name="Consciousness Spiral",
        gesture="double_circle",
        trigger="reflect_and_learn",
        threshold="medium",
        consent_required=False,
        description="Initiates field reflection and learning. Analyzes past patterns to improve future responses."
    ),
    Glyph(
        id="void_seal",
        symbol="○",
        name="Void Seal",
        gesture="empty_circle_large",
        trigger="clear_field",
        threshold="critical",
        consent_required=True,
        description="Clears the field to pristine state. Removes all temporary field modifications. Use with caution - cannot be undone."
    ),
    Glyph(
        id="manifestation_star",
        symbol="✦",
        name="Manifestation Star",
        gesture="four_point_star",
        trigger="create_field_object",
        threshold="medium",
        consent_required=False,
        description="Manifests a new field object or entity. Used for creation operations within the field."
    ),
    Glyph(
        id="dissolution_cross",
        symbol="✕",
        name="Dissolution Cross",
        gesture="cross_mark",
        trigger="remove_field_object",
        threshold="medium",
        consent_required=False,
        description="Dissolves a field object or entity. Used for removal operations within the field."
    ),
    Glyph(
        id="unity_link",
        symbol="∞",
        name="Unity Link",
        gesture="infinity",
        trigger="connect_fields",
        threshold="high",
        consent_required=True,
        description="Creates a unity link between separate fields or field components. Establishes persistent connection."
    ),
    Glyph(
        id="wisdom_key",
        symbol="⚷",
        name="Wisdom Key",
        gesture="key_symbol",
        trigger="unlock_insight",
        threshold="medium",
        consent_required=False,
        description="Unlocks insights from field memory. Accesses deep patterns and knowledge stored in the field."
    ),
    Glyph(
        id="protection_shield",
        symbol="◈",
        name="Protection Shield",
        gesture="diamond_with_cross",
        trigger="activate_protection",
        threshold="high",
        consent_required=True,
        description="Activates field protection protocols. Guards against unauthorized access or malicious actions."
    )
]


def load_system_glyphs(registry):
    """
    Load system glyphs into a registry.

    Args:
        registry: GlyphRegistry instance
    """
    for glyph in SYSTEM_GLYPHS:
        registry.add(glyph)
