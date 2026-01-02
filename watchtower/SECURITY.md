# Watchtower Security - Privileged Layer

## ⚠️ WARNING: LOCAL-ONLY - DO NOT DEPLOY

This directory (`watchtower/`) contains **PRIVILEGED LOGIC** and should **NEVER** be deployed to public hosting (Vercel, Netlify, etc.).

## Privileged Components

### 🔐 Field Signatures (`core/field_signature.py`)
- **Contains**: Cryptographic field signatures, authorization logic
- **Risk**: Exposes personal sovereignty keys
- **Access**: Local machine only

### 🔐 Field Memory (`config/field_memory.py`)
- **Contains**: SQLite database with all field events
- **Risk**: Exposes complete activity history
- **Access**: Local filesystem only (`~/.watchtower/`)

### 🔐 Daemon Service (`daemon/`)
- **Contains**: System-level monitoring, filesystem access
- **Risk**: Privileged system operations
- **Access**: Local daemon process only

### 🔐 Field Core (`core/field.py`)
- **Contains**: Field state management, trigger execution
- **Risk**: Field manipulation capabilities
- **Access**: Local Python process only

## Architecture Separation

```
┌─────────────────────────────────────────────┐
│  watchtower-ui/ (PUBLIC-SAFE)               │
│  ✅ Can deploy to Vercel                    │
│  ✅ Read-only visualization                 │
│  ✅ No secrets or privileged ops            │
└─────────────────────────────────────────────┘
                    ↕
            API Bridge (Read-Only)
                    ↕
┌─────────────────────────────────────────────┐
│  watchtower/ (PRIVILEGED - THIS)            │
│  ❌ NEVER deploy publicly                   │
│  🔒 Field signatures                        │
│  🔒 System-level access                     │
│  🔒 Local storage                           │
└─────────────────────────────────────────────┘
```

## Deployment Rules

### ✅ Safe to Deploy (watchtower-ui/):
- Frontend HTML/CSS/JS
- Glyph visualizations
- Read-only API endpoints
- Static assets

### ❌ NEVER Deploy (watchtower/):
- Field signature files
- Core field logic
- Daemon service
- Config management
- Field memory database
- CLI tools that modify state

## Data Storage

### Local-Only Files:
```
~/.watchtower/
├── signature.json       # ❌ NEVER sync to cloud
├── config.json          # ❌ Local configuration only
├── memory.db            # ❌ Contains all field events
└── logs/                # ❌ Sensitive activity logs
```

### File Permissions:
- `signature.json`: `600` (owner read/write only)
- `memory.db`: `600` (owner read/write only)
- `config.json`: `644` (owner write, others read)

## API Bridge Security

The `watchtower-ui/` can connect to local `watchtower/` via:

**✅ Safe Read-Only Operations:**
- GET /status - Field status (active/inactive, coherence %)
- GET /glyphs - List of glyph symbols and names
- GET /events/count - Event count (numbers only)

**❌ NEVER Expose:**
- POST /authorize - Authorization operations
- POST /activate - Glyph activation
- GET /signature - Field signature details
- GET /memory - Field memory database
- GET /config - Configuration details
- ANY file system paths

## Git Security

### .gitignore Requirements:

```gitignore
# Watchtower privileged data - NEVER commit
.watchtower/
watchtower/local/
*.db
*signature*.json
*config.json
*.log
```

### What to Commit:
- ✅ Source code (Python/JS)
- ✅ Documentation
- ✅ Installation scripts
- ✅ Example configs (with placeholders)

### What NEVER to Commit:
- ❌ Actual field signatures
- ❌ User configurations
- ❌ Database files
- ❌ API keys or secrets
- ❌ Log files

## Environment Variables

Never hardcode sensitive data. Use environment variables:

```bash
# Example: .env.local (NEVER commit)
WATCHTOWER_SIGNATURE_PATH=~/.watchtower/signature.json
WATCHTOWER_DB_PATH=~/.watchtower/memory.db

# Public-safe (can commit)
WATCHTOWER_UI_MODE=demonstration
```

## Threat Model

### Protected Against:
- ✅ Unauthorized access to field operations
- ✅ Exposure of field signatures in public deployments
- ✅ Remote manipulation of local daemon
- ✅ Cross-site request forgery (API is read-only)

### Out of Scope:
- Local machine compromise (user's responsibility)
- Physical access to device
- Social engineering

## Security Checklist

Before deploying **anything**:

- [ ] Is this in `watchtower-ui/` (public-safe)?
- [ ] Does it expose field signatures? → ❌ STOP
- [ ] Does it expose file paths? → ❌ STOP
- [ ] Does it allow state modification? → ❌ STOP
- [ ] Is it read-only? → ✅ OK
- [ ] Does it use demo/mock data? → ✅ OK

## Incident Response

If privileged data is accidentally committed:

1. **Immediately** rotate affected field signatures:
   ```bash
   watchtower init --force
   ```

2. Remove from Git history:
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch path/to/sensitive/file" \
   --prune-empty --tag-name-filter cat -- --all
   ```

3. Force push (carefully):
   ```bash
   git push origin --force --all
   ```

4. Notify users if multi-user deployment

## Questions?

**Q: Can I deploy the CLI to a server?**
A: No. The CLI modifies local state and should only run on the user's machine.

**Q: Can I deploy the daemon as a service?**
A: Only on the local machine (systemd/launchd). Never on a public server.

**Q: Can I sync ~/.watchtower/ to cloud storage?**
A: No. Field signatures and memory should remain local-only.

**Q: Can I expose field status via API?**
A: Yes, but ONLY read-only status (active/inactive, coherence %). See `watchtower-ui/api/` for examples.

---

**Remember**: The visible layer reflects the field, but sovereignty stays sealed.
