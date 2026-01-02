# Watchtower API - Public Safe Endpoints

This directory contains PUBLIC-SAFE API endpoints that can be deployed to Vercel.

## Security Principles

### ✅ What IS Exposed (Safe):
- Field active/inactive status (boolean)
- Coherence score (0-100 percentage)
- Event count (integer)
- Resonance state (text status)
- General statistics (non-sensitive aggregates)

### ❌ What is NOT Exposed (Privileged):
- Field signature IDs (beyond first 8 chars for display)
- Authorization tokens
- Cryptographic keys
- File system paths
- Daemon control endpoints
- Local storage data
- User-specific sensitive information

## Available Endpoints

### GET /api/status

Returns read-only field status.

**Response:**
```json
{
  "active": true,
  "coherence": 92,
  "eventCount": 47,
  "resonance": "Synced",
  "lastUpdate": "2025-01-02T16:30:00Z",
  "stats": {
    "totalGlyphs": 15,
    "activationsToday": 12,
    "coherenceAvg": 88
  },
  "meta": {
    "mode": "demonstration",
    "version": "1.0.0"
  }
}
```

## Deployment

These endpoints are designed for serverless deployment:

```bash
# Vercel
vercel deploy

# Netlify
netlify deploy --prod
```

## Local Development

```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev
```

## Connecting to Local Watchtower

The API can optionally connect to a local Watchtower instance for real-time data:

```javascript
// In status.js
const LOCAL_WATCHTOWER_URL = process.env.LOCAL_WATCHTOWER_URL || 'http://localhost:8080';

async function getLocalStatus() {
    try {
        const response = await fetch(`${LOCAL_WATCHTOWER_URL}/status`, {
            timeout: 2000
        });

        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        // Daemon not running, use demo data
    }

    return getDemoStatus();
}
```

**Important:** Local connection is OPTIONAL and read-only. Never expose privileged operations via public API.

## Environment Variables

Create `.env.local`:

```bash
# Optional: Connect to local Watchtower instance
LOCAL_WATCHTOWER_URL=http://localhost:8080

# Mode: demonstration or connected
API_MODE=demonstration
```

## Security Checklist

Before deploying any new endpoint:

- [ ] Does it expose field signatures? ❌ NO
- [ ] Does it expose authorization tokens? ❌ NO
- [ ] Does it expose file paths? ❌ NO
- [ ] Does it allow daemon control? ❌ NO
- [ ] Is it read-only? ✅ YES
- [ ] Can it be publicly cached? ✅ YES (for demo data)

## Rate Limiting

Consider adding rate limiting for production:

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});

export default limiter(handler);
```

---

**Remember**: This API is the visible layer. Keep sovereignty sealed in the local daemon.
