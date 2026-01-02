# Watchtower Architecture - Visible vs Privileged Layers

## Overview

Watchtower implements a **two-layer security architecture** that separates public-safe visualization from privileged field operations.

```
┌─────────────────────────────────────────────────────────────┐
│                    VISIBLE LAYER                            │
│                 (Public-Safe - Vercel)                      │
│                                                             │
│  watchtower-ui/                                             │
│  ├── src/          Frontend (HTML/CSS/JS)                   │
│  ├── components/   React components (optional)              │
│  ├── api/          Read-only public API                     │
│  └── public/       Static assets                            │
│                                                             │
│  ✅ Can deploy to Vercel/Netlify                           │
│  ✅ No secrets or credentials                              │
│  ✅ Read-only visualization                                │
│  ✅ Safe for public access                                 │
└─────────────────────────────────────────────────────────────┘
                            ↕
                    API Bridge (Read-Only)
                    WebSocket (Optional)
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  PRIVILEGED LAYER                           │
│                 (Local-Only - Never Deploy)                 │
│                                                             │
│  watchtower/                                                │
│  ├── core/         Field signatures & authorization         │
│  ├── daemon/       Background system monitoring             │
│  ├── config/       Local storage & configuration            │
│  └── glyphs/       Glyph registry & triggers                │
│                                                             │
│  ❌ NEVER deploy to cloud                                  │
│  🔒 Field signatures & crypto                              │
│  🔒 System-level access                                    │
│  🔒 File system operations                                 │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
ConstruX/
│
├── watchtower-ui/              # ✅ PUBLIC-SAFE
│   ├── src/
│   │   ├── index.html          # Main UI
│   │   ├── app.js              # Application logic
│   │   └── glyphs.js           # Glyph rendering
│   ├── styles/
│   │   ├── main.css            # Main styles
│   │   └── glyphs.css          # Glyph animations
│   ├── api/
│   │   └── status.js           # Read-only status API
│   ├── components/             # UI components
│   ├── public/                 # Static assets
│   ├── package.json
│   ├── vercel.json             # Vercel config
│   └── README.md               # Public docs
│
└── watchtower/                 # ❌ PRIVILEGED
    ├── core/
    │   ├── field.py            # Field operations
    │   ├── field_signature.py  # Crypto signatures
    │   ├── field_init.py       # Initialization
    │   └── resonance.py        # Coherence engine
    ├── daemon/
    │   ├── daemon_service.py   # Background daemon
    │   ├── field_monitor.py    # File monitoring
    │   └── *.service/*.plist   # System services
    ├── config/
    │   ├── field_memory.py     # SQLite storage
    │   └── config_manager.py   # Configuration
    ├── glyphs/
    │   ├── glyph_registry.py   # Glyph management
    │   └── system_glyphs.py    # System glyphs
    ├── watchtower_cli.py       # CLI interface
    ├── SECURITY.md             # Security guidelines
    └── README.md               # Implementation docs
```

## Data Flow

### Read-Only Status Display

```
User Browser (watchtower-ui)
    ↓
  GET /api/status
    ↓
Vercel Serverless Function
    ↓
(Optional) WebSocket → Local Watchtower Instance
    ↓
Read-only status data
    ↓
JSON Response: { active, coherence, eventCount }
    ↓
UI Updates (pulse meter, field status)
```

### Privileged Field Operations (Local Only)

```
User Command: watchtower daemon start
    ↓
watchtower_cli.py (Local Python)
    ↓
Load Field Signature (~/.watchtower/signature.json)
    ↓
Verify Authorization (FieldAuthorizer)
    ↓
Start Daemon (WatchtowerDaemon)
    ↓
Monitor Filesystem (FieldMonitor)
    ↓
Activate Glyphs (Field.activate_glyph)
    ↓
Record to Memory (FieldMemory.record_event)
    ↓
Save to Local DB (~/.watchtower/memory.db)
```

## Security Boundaries

### Visible Layer (watchtower-ui/)

**Can Do:**
- ✅ Display glyph symbols and names
- ✅ Show field status (active/inactive)
- ✅ Display coherence percentage
- ✅ Show event counts
- ✅ Render animations
- ✅ Serve static assets

**Cannot Do:**
- ❌ Access field signatures
- ❌ Modify field state
- ❌ Execute glyphs
- ❌ Access file system
- ❌ Control daemon
- ❌ Read field memory database

### Privileged Layer (watchtower/)

**Can Do:**
- ✅ Generate field signatures
- ✅ Authorize actions
- ✅ Execute glyph triggers
- ✅ Monitor file system
- ✅ Control daemon
- ✅ Read/write field memory
- ✅ Modify configuration

**Cannot Do:**
- ❌ Be deployed to public hosting
- ❌ Expose secrets via network
- ❌ Accept remote commands

## Deployment

### Visible Layer (watchtower-ui/)

```bash
# Deploy to Vercel
cd watchtower-ui
vercel deploy

# Or connect GitHub repo for auto-deployment
```

**Result**: Public URL like `watchtower.vercel.app`

### Privileged Layer (watchtower/)

```bash
# Install locally
cd watchtower
./install_watchtower.sh

# Initialize field
watchtower init

# Install daemon service
./install_daemon.sh

# Start daemon
watchtower daemon start
```

**Result**: Local daemon running at `http://localhost:8080` (optional)

## API Bridge

The visible layer can optionally connect to the local privileged layer:

```javascript
// watchtower-ui/src/app.js
async function connectToLocal() {
    try {
        // Attempt to connect to local daemon
        const ws = new WebSocket('ws://localhost:8080');

        ws.onmessage = (event) => {
            const status = JSON.parse(event.data);
            updateFieldStatus(status);
        };
    } catch (error) {
        // Local daemon not running, use demo mode
        console.log('Using demonstration mode');
    }
}
```

**Important**: This connection is:
- ✅ Optional (UI works standalone)
- ✅ Read-only status updates
- ✅ Local network only (localhost)
- ❌ NOT deployed to Vercel
- ❌ NO privileged operations

## Use Cases

### Scenario 1: Public Demo
- Deploy `watchtower-ui/` to Vercel
- Shows demonstration mode
- All data is mock/simulated
- Safe for public viewing

### Scenario 2: Personal Use
- Deploy `watchtower-ui/` to Vercel
- Install `watchtower/` locally
- UI connects to local daemon for real-time updates
- Field operations stay local

### Scenario 3: Documentation
- Deploy `watchtower-ui/` to GitHub Pages
- Educational purpose
- Shows glyph language
- No backend connection

## Security Checklist

Before deploying to Vercel:

- [ ] ✅ Only deploying `watchtower-ui/`?
- [ ] ✅ No field signatures in code?
- [ ] ✅ No file system paths exposed?
- [ ] ✅ API endpoints are read-only?
- [ ] ✅ Environment variables checked?
- [ ] ✅ `.gitignore` configured correctly?
- [ ] ✅ No secrets in repository?

## File Permissions

### Visible Layer (watchtower-ui/)
- All files: Standard web permissions
- Can be publicly readable

### Privileged Layer (watchtower/)
- `~/.watchtower/signature.json`: `600` (owner only)
- `~/.watchtower/memory.db`: `600` (owner only)
- `~/.watchtower/config.json`: `644` (owner write, others read)

## Environment Variables

### Visible Layer (.env for Vercel)
```bash
# Optional: Connect to local daemon
NEXT_PUBLIC_LOCAL_WS_URL=ws://localhost:8080

# Mode
NEXT_PUBLIC_MODE=demonstration
```

### Privileged Layer (Local environment)
```bash
# Paths
WATCHTOWER_HOME=~/.watchtower
WATCHTOWER_SIGNATURE_PATH=~/.watchtower/signature.json
WATCHTOWER_DB_PATH=~/.watchtower/memory.db

# Daemon
WATCHTOWER_DAEMON_PORT=8080
WATCHTOWER_DAEMON_HOST=localhost
```

## Maintenance

### Updating Visible Layer
```bash
cd watchtower-ui
git pull origin watchtower/visible-layer
vercel deploy
```

### Updating Privileged Layer
```bash
cd watchtower
git pull origin watchtower/visible-layer
watchtower daemon stop
pip install -r requirements.txt --upgrade
watchtower daemon start
```

---

**Remember**: The visible layer reflects the field, but sovereignty stays sealed locally.
