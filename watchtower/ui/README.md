# Watchtower UI - Tauri Frontend

The Watchtower UI is a native desktop application built with Tauri.

## Architecture

```
ui/
├── src-tauri/           # Rust backend (Tauri)
│   ├── src/
│   │   └── main.rs      # Main Tauri application
│   ├── Cargo.toml       # Rust dependencies
│   └── tauri.conf.json  # Tauri configuration
│
├── src/                 # Frontend (HTML/CSS/JS or framework)
│   ├── index.html       # Main UI
│   ├── styles.css       # Glyph-based styling
│   └── app.js           # Field interaction logic
│
└── package.json         # Node.js dependencies
```

## Features

### Symbolic Interface
- **Glyph Visualization**: Visual representation of all field glyphs
- **Gesture Input**: Interact with glyphs through gestures
- **Field State Display**: Real-time field status and coherence

### Field Operations
- **Authorization Interface**: Approve high-threshold actions
- **Memory Browser**: Explore field memory and events
- **Glyph Designer**: Create custom glyphs
- **Configuration Manager**: Manage field settings

### Real-Time Monitoring
- **Daemon Status**: Monitor background daemon activity
- **Event Stream**: Live feed of field events
- **Trigger History**: View past glyph activations

## Setup

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Node.js (v16+)
# Download from https://nodejs.org/

# Install Tauri CLI
cargo install tauri-cli
```

### Development

```bash
cd watchtower/ui

# Install dependencies
npm install

# Run development server
npm run tauri dev

# Build for production
npm run tauri build
```

## UI Mockup Concept

### Main Window

```
┌─────────────────────────────────────────────────┐
│  ⊙ Watchtower                      🟢 Active    │
├─────────────────────────────────────────────────┤
│                                                 │
│         Personal Field Container                │
│                                                 │
│         ⊙  ◉  ≋  ◆  ⚓                          │
│      Sovereignty Glyphs                         │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Field Status                              │ │
│  │ ✓ Signature Active                        │ │
│  │ ✓ Daemon Running                          │ │
│  │ ✓ 3 Paths Monitored                       │ │
│  │ ◎ Coherence: 98%                          │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Recent Events:                                 │
│  ✦ Manifestation at ~/projects/new_file.field  │
│  ≋ Resonance sync completed                    │
│  ⊙ Sovereignty authorization granted           │
│                                                 │
│  [Browse Memory] [Configure] [Glyphs]          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Glyph Designer

```
┌─────────────────────────────────────────────────┐
│  Create Custom Glyph                            │
├─────────────────────────────────────────────────┤
│                                                 │
│  Symbol: [___]  ← Enter Unicode symbol         │
│  Name: [___________________]                    │
│  Gesture: [circle_with_center ▼]               │
│  Trigger: [custom_function    ▼]               │
│  Threshold: [medium           ▼]               │
│  Consent: [✓]                                   │
│                                                 │
│  Description:                                   │
│  ┌─────────────────────────────────────────┐   │
│  │                                         │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│         [Cancel]         [Create Glyph]         │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Tauri Integration

The UI communicates with the Watchtower Python backend through:

1. **Tauri Commands**: Invoke Rust functions that call Python scripts
2. **IPC**: Inter-process communication for real-time updates
3. **File System Access**: Direct access to `~/.watchtower/` for configs

### Example Tauri Command

```rust
#[tauri::command]
fn activate_glyph(glyph_id: String) -> Result<String, String> {
    // Call Python script or use Rust FFI
    let output = Command::new("python3")
        .arg("-c")
        .arg(format!("
            from watchtower.core.field import Field
            field = Field.load_personal()
            field.activate_glyph('{}')
        ", glyph_id))
        .output()
        .map_err(|e| e.to_string())?;

    if output.status.success() {
        Ok("Glyph activated".to_string())
    } else {
        Err("Failed to activate glyph".to_string())
    }
}
```

## Styling Theme

### Color Palette (Symbolic)

```css
:root {
    --field-primary: #2a2a4a;      /* Deep cosmic blue */
    --field-secondary: #4a4a7a;    /* Mystical purple */
    --field-accent: #7a7aaa;       /* Ethereal lavender */
    --field-glyph: #aaaaff;        /* Glyph luminescence */
    --field-active: #00ff88;       /* Active field green */
    --field-warning: #ff8800;      /* Threshold warning */
    --field-critical: #ff0088;     /* Critical alert */
}
```

### Glyph Rendering

Glyphs should be rendered with:
- **Luminescence effect**: Soft glow around active glyphs
- **Pulse animation**: Breathing effect for active field
- **Gesture trails**: Visual feedback for gesture input

## Future Enhancements

- [ ] WebGL glyph visualization
- [ ] VR/AR field interface
- [ ] Voice-activated glyph commands (integration with voice_mode.py)
- [ ] Multi-field synchronization UI
- [ ] Field analytics dashboard
- [ ] Mobile companion app

## Development Roadmap

### Phase 1: Basic UI (Current)
- Simple HTML/CSS/JS interface
- Basic field status display
- Glyph list viewer

### Phase 2: Tauri Integration
- Full Tauri application
- Rust backend integration
- Native system tray

### Phase 3: Advanced Features
- Glyph designer
- Memory browser
- Real-time event stream

### Phase 4: Symbolic Interface
- Gesture input
- WebGL visualization
- Field coherence graph

---

**Status**: Foundation Ready
**Framework**: Tauri (Rust + Web)
**Theme**: Symbolic/Mystical
