# Watchtower UI - Visible Layer Container

**Public-safe frontend for Watchtower field visualization**

## 🔒 Security Architecture

This is the **VISIBLE LAYER** - safe for public deployment (Vercel, Netlify, etc.)

### ✅ What Lives Here (Public-Safe):
- Glyph visualization and animations
- Field status display (read-only)
- Pulse/coherence meter
- Alert notifications
- Public documentation

### ❌ What Does NOT Live Here (Privileged):
- Field signature operations
- Cryptographic keys
- Filesystem monitoring
- Daemon control
- Local storage access
- System-level operations

## Architecture Separation

```
┌─────────────────────────────────────────────┐
│  Watchtower UI (THIS - Public/Vercel)       │
│  - Glyph display                            │
│  - Status visualization                     │
│  - Read-only monitoring                     │
└─────────────────────────────────────────────┘
                    ↕ API Bridge
┌─────────────────────────────────────────────┐
│  Watchtower Core (Local Machine Only)       │
│  - Field signatures                         │
│  - Daemon operations                        │
│  - Privileged system access                 │
└─────────────────────────────────────────────┘
```

## Directory Structure

```
watchtower-ui/
├── public/              # Static assets
│   ├── glyphs/         # Glyph SVG/images
│   └── icons/          # UI icons
├── src/                # Frontend source
│   ├── index.html      # Main page
│   ├── app.js          # Application logic
│   └── glyphs.js       # Glyph rendering
├── components/         # React/Web components
│   ├── GlyphDisplay.js
│   ├── FieldStatus.js
│   ├── PulseMeter.js
│   └── AlertPanel.js
├── styles/             # CSS/styling
│   ├── main.css
│   └── glyphs.css
├── api/                # Public API endpoints
│   └── status.js       # Read-only status API
├── vercel.json         # Vercel deployment config
└── package.json        # Dependencies
```

## Quick Start

### Development

```bash
cd watchtower-ui
npm install
npm run dev
```

### Deploy to Vercel

```bash
vercel deploy
```

Or connect your GitHub repo to Vercel for automatic deployments.

## Features

### 1. Glyph Visualization
Interactive display of Watchtower glyphs with animations and hover effects.

### 2. Field Status Monitor
Real-time read-only view of field status:
- Field active/inactive
- Coherence score
- Recent events (non-sensitive)

### 3. Pulse Meter
Visual representation of field coherence and health.

### 4. Alert System
Notifications for field events (configurable, non-privileged).

## API Bridge

The UI communicates with local Watchtower instance via safe API:

```javascript
// Example: Get field status (read-only)
const status = await fetch('/api/status').then(r => r.json());

// ❌ NEVER exposed:
// - Field signatures
// - Authorization tokens
// - File system paths
// - Daemon control
```

## Environment Variables

Create `.env.local`:

```bash
# Optional: WebSocket URL for real-time updates
NEXT_PUBLIC_WS_URL=ws://localhost:8080

# Optional: API endpoint (defaults to /api)
NEXT_PUBLIC_API_URL=/api
```

## Security Guidelines

### ✅ DO:
- Display glyph symbols and names
- Show field status (active/inactive)
- Display coherence scores
- Show event counts
- Render animations and visualizations

### ❌ DON'T:
- Expose field signature IDs (beyond first 8 chars)
- Display file system paths
- Show authorization tokens
- Allow daemon control from UI
- Store sensitive data in localStorage

## Technology Stack

- **Framework**: Vanilla JS / React (optional)
- **Styling**: CSS3 with symbolic theme
- **Deployment**: Vercel / Netlify
- **API**: RESTful read-only endpoints
- **Real-time**: WebSocket (optional, for pulse updates)

## Deployment

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd watchtower-ui
vercel
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
cd watchtower-ui
netlify deploy
```

## Local Watchtower Connection

The UI can optionally connect to a local Watchtower instance for real-time updates:

```javascript
// Optional: Connect to local daemon
const ws = new WebSocket('ws://localhost:8080');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // Update UI with field pulse, coherence, etc.
};
```

**Important**: Local connection is OPTIONAL. The UI works standalone for demonstration/documentation purposes.

## Symbolic Theme

The UI uses the Watchtower symbolic visual language:

### Color Palette
```css
:root {
  --field-deep: #1a1a2e;      /* Deep cosmic background */
  --field-mystic: #2a2a4a;    /* Mystic purple */
  --field-glow: #4a4a7a;      /* Glyph glow */
  --field-pulse: #7a7aaa;     /* Pulse animation */
  --field-active: #00ff88;    /* Active field */
  --field-warning: #ff8800;   /* Warning threshold */
  --field-critical: #ff0088;  /* Critical alert */
}
```

### Typography
- **Headers**: Inter, bold
- **Body**: Inter, regular
- **Glyphs**: System UI (native emoji/symbols)

## Examples

### Display Field Status

```javascript
// src/app.js
async function displayFieldStatus() {
  const status = await fetch('/api/status').then(r => r.json());

  document.getElementById('field-active').textContent =
    status.active ? '🟢 Active' : '🔴 Inactive';

  document.getElementById('coherence').textContent =
    `${status.coherence}%`;
}
```

### Render Glyphs

```javascript
// src/glyphs.js
const glyphs = [
  { symbol: '⊙', name: 'Sovereignty Seal' },
  { symbol: '◉', name: 'Field Lock' },
  { symbol: '≋', name: 'Resonance Wave' }
];

function renderGlyphs() {
  const container = document.getElementById('glyphs');

  glyphs.forEach(glyph => {
    const el = document.createElement('div');
    el.className = 'glyph';
    el.innerHTML = `
      <span class="glyph-symbol">${glyph.symbol}</span>
      <span class="glyph-name">${glyph.name}</span>
    `;
    container.appendChild(el);
  });
}
```

## Contributing

When adding features to the visible layer:

1. **Security Check**: Does this expose privileged data?
2. **Read-Only**: Is this strictly read-only?
3. **Public-Safe**: Can this be publicly deployed?

If any answer is NO, the feature belongs in `watchtower/` core, not here.

## Resources

- **Core Documentation**: See `../watchtower/README.md`
- **API Specification**: See `api/README.md`
- **Glyph Reference**: See `public/glyphs/README.md`

---

**Version**: 1.0.0
**Status**: Visible Layer - Public Safe
**Deployment**: Vercel Ready ✅

*The visible container reflects the field, but does not contain its sovereignty.*
