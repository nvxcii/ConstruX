/**
 * Watchtower UI - Main Application Logic
 *
 * PUBLIC-SAFE: This file contains NO privileged operations.
 * All data is demonstration/mock data or read-only API calls.
 */

// Demonstration mode - uses mock data
const DEMO_MODE = true;

// Field status state
const fieldState = {
    active: false,
    coherence: 0,
    eventCount: 0,
    resonance: 'Initializing...',
    lastUpdate: null
};

/**
 * Initialize the application
 */
function init() {
    console.log('🔮 Watchtower UI initialized');

    // Start demo mode or connect to API
    if (DEMO_MODE) {
        startDemoMode();
    } else {
        connectToAPI();
    }

    // Update UI
    updateFieldStatus();
    updatePulseMeter();

    // Start animation loop
    requestAnimationFrame(animationLoop);
}

/**
 * Demo mode - simulates field activity
 */
function startDemoMode() {
    console.log('📊 Starting demonstration mode');

    // Simulate field activation
    setTimeout(() => {
        fieldState.active = true;
        fieldState.coherence = 85;
        fieldState.eventCount = 12;
        fieldState.resonance = 'Synced';
        updateFieldStatus();
        updatePulseMeter();

        addActivity('⊙', 'Field Activated', 'Demonstration mode enabled');
    }, 1000);

    // Simulate periodic events
    setInterval(() => {
        if (fieldState.active) {
            // Random coherence fluctuation
            fieldState.coherence = Math.max(75, Math.min(100,
                fieldState.coherence + (Math.random() - 0.5) * 10
            ));

            updatePulseMeter();
        }
    }, 3000);

    // Simulate random events
    setInterval(() => {
        if (fieldState.active && Math.random() > 0.7) {
            const events = [
                { glyph: '≋', title: 'Resonance Sync', desc: 'Field coherence adjusted' },
                { glyph: '✦', title: 'Manifestation', desc: 'New field object created' },
                { glyph: '◔', title: 'Observation', desc: 'Field state observed' },
                { glyph: '◎', title: 'Reflection', desc: 'Pattern analysis complete' }
            ];

            const event = events[Math.floor(Math.random() * events.length)];
            addActivity(event.glyph, event.title, event.desc);

            fieldState.eventCount++;
            updateFieldStatus();
        }
    }, 5000);
}

/**
 * Connect to Watchtower API (when not in demo mode)
 */
async function connectToAPI() {
    try {
        const response = await fetch('/api/status');

        if (response.ok) {
            const data = await response.json();

            fieldState.active = data.active || false;
            fieldState.coherence = data.coherence || 0;
            fieldState.eventCount = data.eventCount || 0;
            fieldState.resonance = data.resonance || 'Unknown';

            updateFieldStatus();
            updatePulseMeter();

            console.log('✅ Connected to Watchtower API');
        } else {
            console.warn('⚠️ API not available, using demo mode');
            startDemoMode();
        }
    } catch (error) {
        console.warn('⚠️ Failed to connect to API:', error.message);
        console.log('📊 Falling back to demo mode');
        startDemoMode();
    }
}

/**
 * Update field status display
 */
function updateFieldStatus() {
    // Update header status
    const statusIndicator = document.getElementById('fieldStatus');
    if (statusIndicator) {
        const statusDot = statusIndicator.querySelector('.status-dot');
        const statusText = statusIndicator.querySelector('.status-text');

        if (fieldState.active) {
            statusDot.style.background = 'var(--field-active)';
            statusText.textContent = 'Active';
        } else {
            statusDot.style.background = 'var(--field-text-dim)';
            statusText.textContent = 'Inactive';
        }
    }

    // Update status cards
    const fieldStateEl = document.getElementById('fieldState');
    if (fieldStateEl) {
        fieldStateEl.textContent = fieldState.active ? 'Active' : 'Inactive';
        fieldStateEl.style.color = fieldState.active ? 'var(--field-active)' : 'var(--field-text-dim)';
    }

    const coherenceEl = document.getElementById('coherence');
    if (coherenceEl) {
        coherenceEl.textContent = `${Math.round(fieldState.coherence)}%`;
    }

    const resonanceEl = document.getElementById('resonance');
    if (resonanceEl) {
        resonanceEl.textContent = fieldState.resonance;
    }

    const eventCountEl = document.getElementById('eventCount');
    if (eventCountEl) {
        eventCountEl.textContent = fieldState.eventCount;
    }
}

/**
 * Update pulse meter visualization
 */
function updatePulseMeter() {
    const coherenceScore = document.getElementById('coherenceScore');
    if (coherenceScore) {
        coherenceScore.textContent = fieldState.active
            ? `${Math.round(fieldState.coherence)}%`
            : '--';
    }

    const pulseCircle = document.querySelector('.pulse-circle');
    if (pulseCircle && fieldState.active) {
        // Adjust color based on coherence
        if (fieldState.coherence >= 90) {
            pulseCircle.style.borderColor = 'var(--field-active)';
        } else if (fieldState.coherence >= 70) {
            pulseCircle.style.borderColor = 'var(--field-pulse)';
        } else {
            pulseCircle.style.borderColor = 'var(--field-warning)';
        }
    }
}

/**
 * Add activity to feed
 */
function addActivity(glyph, title, description) {
    const feed = document.getElementById('activityFeed');
    if (!feed) return;

    const item = document.createElement('div');
    item.className = 'activity-item glyph-animate-in';
    item.innerHTML = `
        <span class="activity-glyph">${glyph}</span>
        <div class="activity-content">
            <div class="activity-title">${title}</div>
            <div class="activity-time">${description}</div>
        </div>
    `;

    // Insert at top
    if (feed.firstChild) {
        feed.insertBefore(item, feed.firstChild);
    } else {
        feed.appendChild(item);
    }

    // Limit feed to 10 items
    while (feed.children.length > 10) {
        feed.removeChild(feed.lastChild);
    }
}

/**
 * Animation loop for dynamic effects
 */
let animationTime = 0;
function animationLoop(timestamp) {
    animationTime = timestamp;

    // Add subtle animations here if needed

    requestAnimationFrame(animationLoop);
}

/**
 * Handle window resize
 */
function handleResize() {
    // Adjust layout if needed
}

// Event listeners
window.addEventListener('DOMContentLoaded', init);
window.addEventListener('resize', handleResize);

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        init,
        updateFieldStatus,
        addActivity
    };
}
