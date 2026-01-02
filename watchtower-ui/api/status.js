/**
 * Watchtower API - Status Endpoint
 *
 * PUBLIC-SAFE: Read-only status information.
 * NO privileged operations, signatures, or file system access.
 *
 * This API can be deployed to Vercel safely.
 */

/**
 * Get field status (read-only, demonstration data)
 *
 * In production, this would connect to a local Watchtower instance
 * via WebSocket or HTTP, but ONLY for read-only status data.
 */
export default async function handler(req, res) {
    // CORS headers for API access
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'GET') {
        res.status(405).json({ error: 'Method not allowed' });
        return;
    }

    try {
        // ✅ PUBLIC-SAFE: Demonstration data only
        const status = {
            active: true,
            coherence: 92,
            eventCount: 47,
            resonance: 'Synced',
            lastUpdate: new Date().toISOString(),

            // ✅ Safe to expose: general statistics only
            stats: {
                totalGlyphs: 15,
                activationsToday: 12,
                coherenceAvg: 88
            },

            // ❌ NEVER exposed:
            // - Field signature IDs (beyond first 8 chars)
            // - Authorization tokens
            // - File system paths
            // - Daemon control endpoints
            // - Local storage data

            meta: {
                mode: 'demonstration',
                version: '1.0.0',
                disclaimer: 'This is demonstration data. Connect to local Watchtower instance for real-time updates.'
            }
        };

        res.status(200).json(status);

    } catch (error) {
        console.error('API Error:', error);

        res.status(500).json({
            error: 'Internal server error',
            message: 'Failed to fetch status'
        });
    }
}

/**
 * Future: Connect to local Watchtower instance
 *
 * This would use WebSocket or HTTP to connect to a local
 * Watchtower daemon, but ONLY for read-only status data.
 *
 * Example:
 *
 * async function getLocalStatus() {
 *     try {
 *         const response = await fetch('http://localhost:8080/status', {
 *             timeout: 2000
 *         });
 *
 *         if (response.ok) {
 *             return await response.json();
 *         }
 *     } catch (error) {
 *         // Local daemon not running, use demo data
 *     }
 *
 *     return getDemoStatus();
 * }
 */
