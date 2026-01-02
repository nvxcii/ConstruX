## Watchtower Quick Start Guide

Get up and running with Watchtower in minutes.

## Installation

### 1. Install Watchtower

**Linux/macOS:**
```bash
cd watchtower
./install_watchtower.sh
```

**Windows:**
```cmd
cd watchtower
install_watchtower.bat
```

### 2. Initialize Your Field

```bash
watchtower init
```

This will:
- Create your personal field signature
- Generate your sovereignty glyph
- Set up field memory database
- Configure watch paths
- Load system glyphs

**Example Output:**
```
==========================================================
WATCHTOWER FIELD INITIALIZATION
==========================================================

Creating your personal field container...

Choose your personal glyph (or press Enter for default ⊙):
  ⊙  Sovereignty Seal (default)
  ◉  Field Lock
  ≋  Resonance Wave
  ...

Enter glyph symbol: ⊙

🔮 Creating field with personal glyph: ⊙
✓ Field signature created: a1b2c3d4e5f6g7h8...
✓ Field signature saved to: ~/.watchtower/signature.json

📝 Initializing configuration...

Enter directories to watch:
  Path: ~/projects
    ✓ Added: /home/user/projects
  Path:

🔣 Loading system glyphs...
✓ Loaded 15 system glyphs

==========================================================
🎯 FIELD INITIALIZATION COMPLETE
==========================================================

Your Watchtower field is now active!
Personal Glyph: ⊙
Field ID: a1b2c3d4e5f6g7h8...

Next steps:
  1. Start the daemon: watchtower daemon start
  2. Check status: watchtower status
  3. Launch UI: watchtower ui
```

## Basic Usage

### Check Field Status

```bash
watchtower status
```

**Example Output:**
```
==========================================================
WATCHTOWER FIELD STATUS
==========================================================

Field Information:
  ID: a1b2c3d4e5f6g7h8...
  Glyph: ⊙
  Active: True

System Health:
  Signature: ✓
  Total Events: 47
  Glyphs Loaded: 15
  Triggers Registered: 3

Configuration:
  Watch Paths: 1
    - /home/user/projects
```

### Start the Daemon

```bash
watchtower daemon start
```

The daemon will:
- Monitor watch paths for file events
- Activate glyphs when patterns are detected
- Log all field activity
- Run in the background

**Press Ctrl+C to stop the daemon**

### View Glyphs

```bash
watchtower glyphs list
```

**Example Output:**
```
==========================================================
WATCHTOWER GLYPHS
==========================================================

⊙  Sovereignty Seal
   ID: sovereignty_seal
   Trigger: authorize_field_action
   Threshold: high | Consent: ✓
   The primary glyph of personal authority. Used to authorize significant...

◆  Trigger Point
   ID: trigger_point
   Trigger: activate_response
   Threshold: low | Consent: –
   Activates a predefined field response. A general-purpose activation...

≋  Resonance Wave
   ID: resonance_wave
   Trigger: sync_field_state
   Threshold: medium | Consent: –
   Synchronizes field state across components. Represents the flow...
```

### Export Glyphs

```bash
watchtower glyphs export --output my_glyphs.md
```

### View Field Memory

```bash
watchtower memory events --limit 10
```

**Example Output:**
```
Recent Events (10):
  [2025-01-02T16:30:15] glyph_activation
    Action: activate_glyph_resonance_wave
    Glyph: resonance_wave
  [2025-01-02T16:29:42] authorization
    Action: monitor_field
    Glyph: observation_eye
  [2025-01-02T16:28:10] field_activation
```

### Memory Statistics

```bash
watchtower memory stats
```

**Example Output:**
```
==========================================================
FIELD MEMORY STATISTICS
==========================================================

Total Events: 142
Glyph Activations: 38
Field States: 12
Daemon Activity: 87
Database Size: 45.23 KB

Oldest Event: 2025-01-01T08:00:00
Newest Event: 2025-01-02T16:30:15
```

## Working with the Field (Python API)

### Load Your Personal Field

```python
from watchtower.core.field import Field

# Load your personal field
field = Field.load_personal()

if field:
    print(f"Field loaded: {field}")
    print(f"Field active: {field.state.get('active')}")
else:
    print("No field found. Run 'watchtower init' first.")
```

### Activate a Glyph

```python
from watchtower.core.field import Field

field = Field.load_personal()

# Activate the resonance wave glyph
success = field.activate_glyph(
    glyph_id='resonance_wave',
    context={'reason': 'manual_sync'}
)

if success:
    print("✓ Glyph activated successfully")
else:
    print("✗ Glyph activation failed")
```

### Authorize an Action

```python
from watchtower.core.field import Field

field = Field.load_personal()

# Define a consent callback
def request_consent(action, threshold, context):
    print(f"Authorization requested for: {action}")
    print(f"Threshold: {threshold}")
    response = input("Authorize? (yes/no): ")
    return response.lower() == 'yes'

# Authorize a high-threshold action
authorized = field.authorize(
    action='delete_important_data',
    glyph='sovereignty_seal',
    context={'target': 'critical_file.txt'},
    consent_callback=request_consent
)

if authorized:
    print("✓ Action authorized")
    # Perform the action
else:
    print("✗ Action denied")
```

### Query Field Memory

```python
from watchtower.config.field_memory import FieldMemory

memory = FieldMemory()

# Get recent events
events = memory.query_events(
    timerange='last_24_hours',
    limit=20
)

print(f"Found {len(events)} events:")
for event in events:
    print(f"  [{event['timestamp']}] {event['event_type']}")
    if event['glyph_id']:
        print(f"    Glyph: {event['glyph_id']}")

# Get glyph activations
activations = memory.query_glyph_activations(
    glyph_id='sovereignty_seal',
    timerange='last_7_days'
)

print(f"\nSovereignty Seal activated {len(activations)} times")
```

### Create a Custom Glyph

```python
from watchtower.glyphs.glyph_registry import GlyphRegistry, Glyph

registry = GlyphRegistry()

# Define custom glyph
custom_glyph = Glyph(
    id='my_custom_action',
    symbol='✨',
    name='Sparkle Action',
    gesture='star_burst',
    trigger='do_something_special',
    threshold='medium',
    consent_required=False,
    description='My custom field action that does something special'
)

# Add to registry
if registry.add(custom_glyph):
    print("✓ Custom glyph created")
else:
    print("✗ Glyph ID already exists")

# Register trigger callback
def sparkle_trigger(context):
    print(f"✨ Sparkle action triggered! Context: {context}")
    return {'status': 'sparkled', 'energy': 100}

field = Field.load_personal()
field.register_trigger('do_something_special', sparkle_trigger)

# Activate your custom glyph
field.activate_glyph('my_custom_action', context={'sparkle_level': 'max'})
```

## Install Daemon as Service

To run the daemon automatically at startup:

```bash
cd watchtower
./install_daemon.sh
```

**Linux (systemd):**
```bash
systemctl --user start watchtower   # Start
systemctl --user stop watchtower    # Stop
systemctl --user status watchtower  # Status
journalctl --user -u watchtower -f  # Logs
```

**macOS (launchd):**
```bash
launchctl load ~/Library/LaunchAgents/com.watchtower.daemon.plist    # Load
launchctl unload ~/Library/LaunchAgents/com.watchtower.daemon.plist  # Unload
tail -f /tmp/watchtower.*.log                                        # Logs
```

## Next Steps

1. **Customize Your Field**: Edit `~/.watchtower/config.json` to add more watch paths
2. **Create Custom Glyphs**: Design glyphs for your specific workflow
3. **Build the UI**: See `watchtower/ui/README.md` for Tauri setup
4. **Integrate with Other Systems**: Use the Python API in your scripts

## Troubleshooting

### Field not found
```bash
# Reinitialize
watchtower init
```

### Daemon won't start
```bash
# Check logs
cat ~/.watchtower/logs/daemon.log

# Verify watch paths exist
cat ~/.watchtower/config.json
```

### Permission denied
```bash
# Check file permissions
ls -la ~/.watchtower/

# Signature should be 600 (owner read/write only)
chmod 600 ~/.watchtower/signature.json
```

## Resources

- **Documentation**: See `watchtower/README.md`
- **UI Guide**: See `watchtower/ui/README.md`
- **Glyph Reference**: Run `watchtower glyphs export`

---

**Welcome to your field. The container lives.**
