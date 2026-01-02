/**
 * Watchtower Glyphs - Symbolic Language Rendering
 *
 * PUBLIC-SAFE: Only displays glyph symbols and metadata.
 * NO privileged operations or triggers.
 */

// System glyphs (read-only display data)
const SYSTEM_GLYPHS = [
    {
        id: 'sovereignty_seal',
        symbol: '⊙',
        name: 'Sovereignty Seal',
        description: 'Personal authority over field operations',
        threshold: 'high',
        gesture: 'circle_with_center'
    },
    {
        id: 'field_lock',
        symbol: '◉',
        name: 'Field Lock',
        description: 'Secure field boundary protection',
        threshold: 'critical',
        gesture: 'filled_circle_with_center'
    },
    {
        id: 'resonance_wave',
        symbol: '≋',
        name: 'Resonance Wave',
        description: 'Synchronize field state across layers',
        threshold: 'medium',
        gesture: 'triple_wave'
    },
    {
        id: 'trigger_point',
        symbol: '◆',
        name: 'Trigger Point',
        description: 'Activate predefined field response',
        threshold: 'low',
        gesture: 'diamond'
    },
    {
        id: 'field_anchor',
        symbol: '⚓',
        name: 'Field Anchor',
        description: 'Anchor field state to persistent memory',
        threshold: 'high',
        gesture: 'anchor'
    },
    {
        id: 'observation_eye',
        symbol: '◔',
        name: 'Observation Eye',
        description: 'Passive field observation and monitoring',
        threshold: 'low',
        gesture: 'half_circle_with_dot'
    },
    {
        id: 'boundary_gate',
        symbol: '⫘',
        name: 'Boundary Gate',
        description: 'Controlled access through field boundaries',
        threshold: 'medium',
        gesture: 'gate_symbol'
    },
    {
        id: 'field_pulse',
        symbol: '◌',
        name: 'Field Pulse',
        description: 'System health check and status pulse',
        threshold: 'low',
        gesture: 'empty_circle'
    },
    {
        id: 'consciousness_spiral',
        symbol: '◎',
        name: 'Consciousness Spiral',
        description: 'Field reflection and pattern learning',
        threshold: 'medium',
        gesture: 'double_circle'
    },
    {
        id: 'void_seal',
        symbol: '○',
        name: 'Void Seal',
        description: 'Clear field to pristine state',
        threshold: 'critical',
        gesture: 'empty_circle_large'
    },
    {
        id: 'manifestation_star',
        symbol: '✦',
        name: 'Manifestation Star',
        description: 'Create new field object or entity',
        threshold: 'medium',
        gesture: 'four_point_star'
    },
    {
        id: 'dissolution_cross',
        symbol: '✕',
        name: 'Dissolution Cross',
        description: 'Remove field object or entity',
        threshold: 'medium',
        gesture: 'cross_mark'
    },
    {
        id: 'unity_link',
        symbol: '∞',
        name: 'Unity Link',
        description: 'Connect separate fields or components',
        threshold: 'high',
        gesture: 'infinity'
    },
    {
        id: 'wisdom_key',
        symbol: '⚷',
        name: 'Wisdom Key',
        description: 'Unlock insights from field memory',
        threshold: 'medium',
        gesture: 'key_symbol'
    },
    {
        id: 'protection_shield',
        symbol: '◈',
        name: 'Protection Shield',
        description: 'Activate field protection protocols',
        threshold: 'high',
        gesture: 'diamond_with_cross'
    }
];

/**
 * Render glyphs to the grid
 */
function renderGlyphs() {
    const grid = document.getElementById('glyphsGrid');
    if (!grid) return;

    grid.innerHTML = '';

    SYSTEM_GLYPHS.forEach((glyph, index) => {
        const card = createGlyphCard(glyph, index);
        grid.appendChild(card);
    });

    console.log(`✨ Rendered ${SYSTEM_GLYPHS.length} glyphs`);
}

/**
 * Create a glyph card element
 */
function createGlyphCard(glyph, index) {
    const card = document.createElement('div');
    card.className = 'glyph-card glyph-animate-in';
    card.style.animationDelay = `${index * 0.05}s`;
    card.dataset.glyphId = glyph.id;

    card.innerHTML = `
        <div class="glyph-symbol">${glyph.symbol}</div>
        <div class="glyph-name">${glyph.name}</div>
        <div class="glyph-threshold ${glyph.threshold}">${glyph.threshold}</div>
    `;

    // Add click handler to show details
    card.addEventListener('click', () => showGlyphDetails(glyph));

    // Add hover effect
    card.addEventListener('mouseenter', () => {
        card.classList.add('glyph-glow');
    });

    card.addEventListener('mouseleave', () => {
        card.classList.remove('glyph-glow');
    });

    return card;
}

/**
 * Show glyph details (modal or console for demo)
 */
function showGlyphDetails(glyph) {
    console.log('Glyph Details:', glyph);

    // For now, just log to console
    // In a full implementation, this would show a modal
    alert(`${glyph.symbol} ${glyph.name}\n\n${glyph.description}\n\nThreshold: ${glyph.threshold}\nGesture: ${glyph.gesture}`);
}

/**
 * Get glyph by ID
 */
function getGlyphById(id) {
    return SYSTEM_GLYPHS.find(g => g.id === id);
}

/**
 * Get glyphs by threshold
 */
function getGlyphsByThreshold(threshold) {
    return SYSTEM_GLYPHS.filter(g => g.threshold === threshold);
}

/**
 * Initialize glyphs display
 */
function initGlyphs() {
    renderGlyphs();

    // Log statistics
    const stats = {
        total: SYSTEM_GLYPHS.length,
        low: getGlyphsByThreshold('low').length,
        medium: getGlyphsByThreshold('medium').length,
        high: getGlyphsByThreshold('high').length,
        critical: getGlyphsByThreshold('critical').length
    };

    console.log('Glyph Statistics:', stats);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlyphs);
} else {
    initGlyphs();
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SYSTEM_GLYPHS,
        renderGlyphs,
        getGlyphById,
        getGlyphsByThreshold
    };
}
