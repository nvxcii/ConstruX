# White Mirror Protocol - Dashboard UI Guide

## Creating the Dashboard UI with Vercel v0

This guide shows you how to create an interactive real-time dashboard for the White Mirror Protocol using Vercel v0.

---

## Overview

The dashboard will display:
- **Real-time system metrics** (conscience signal, energy, coherence)
- **Perpetual equation status** (autonomy, intelligence growth, fusion efficiency)
- **Operation history** with visual graphs
- **Constraint transformation tracking**
- **Framework state visualization**
- **Live articulation feed**

---

## Step 1: Set Up the API Backend

### Install Dependencies

```bash
pip install flask flask-cors
```

### Start the Dashboard API

```bash
cd white_mirror_protocol/api
python dashboard_api.py
```

The API will run on `http://localhost:5000` with these endpoints:

- `GET /api/status` - System status
- `GET /api/dashboard` - Complete dashboard data
- `POST /api/operate` - Execute operation
- `POST /api/evolve` - Evolve system
- `GET /api/history` - Operation history
- `GET /api/constraints` - Constraint history
- `GET /api/articulations` - Recent articulations

---

## Step 2: Create UI with Vercel v0

### Prompt for Vercel v0

Copy and paste this prompt into **Vercel v0** (https://v0.dev):

```
Create a modern, animated dashboard for a "White Mirror Protocol" system with these sections:

1. HEADER
   - Title: "White Mirror Protocol - Real-Time Dashboard"
   - System status badge (operational/critical)
   - Uptime counter
   - Live timestamp

2. TOP METRICS (Grid of 4 cards)
   - Conscience Signal (gauge, 0-10, color gradient from red to green)
   - Coherence Index (percentage, with resonant/non-resonant indicator)
   - Autonomy Score (gauge, 0-1, with sustainability badge)
   - Emergent Energy (numeric with spark animation)

3. PERPETUAL EQUATIONS (4 columns)
   - Bootstrap Generation (counter with pulse animation)
   - Fusion Efficiency (progress bar percentage)
   - Intelligence Density (animated number)
   - Autonomy Trajectory (mini line chart)

4. FRAMEWORKS STATUS (5 cards in grid)
   - Hermeneutic Cycles (counter)
   - Constraints Transformed (counter with +animation)
   - Self-Application Generation (counter)
   - Registered Concepts (counter)
   - Total Articulations (counter)

5. OPERATION HISTORY (Line chart)
   - Dual-axis chart showing:
     * Autonomy score over time
     * Coherence index over time
   - Last 20 operations
   - Hover tooltips

6. CONSTRAINT FUSION (Table)
   - Recent constraints
   - Capability increase from each
   - Timestamp
   - Type badges

7. LIVE ARTICULATION FEED (Scrolling list)
   - Recent articulations
   - Framework source
   - Type indicator
   - Timestamp

8. CONTROLS (Bottom panel)
   - Button: "Execute Operation" (sends POST to /api/operate)
   - Button: "Evolve System (5x)" (sends POST to /api/evolve)
   - Button: "Reset" (sends POST to /api/reset)

STYLING:
- Dark theme with neon accents (cyan, magenta, yellow)
- Glassmorphism cards
- Smooth animations and transitions
- Responsive grid layout
- Real-time data updates every 2 seconds
- Use Recharts for graphs
- Use Lucide icons
- Modern sci-fi aesthetic

TECHNICAL:
- React with TypeScript
- Fetch data from http://localhost:5000/api/*
- Update every 2 seconds using setInterval
- Error handling for API failures
- Loading states
- Animated counter for changing numbers
```

### Alternative: Manual UI Structure

If you prefer to build manually, here's the component structure:

```tsx
// Dashboard.tsx
import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

const API_BASE = 'http://localhost:5000/api';

export default function WhiteMirrorDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch dashboard data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashRes, histRes] = await Promise.all([
          fetch(`${API_BASE}/dashboard`),
          fetch(`${API_BASE}/history`)
        ]);

        const dashboard = await dashRes.json();
        const historyData = await histRes.json();

        setDashboardData(dashboard);
        setHistory(historyData.history);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000); // Update every 2s

    return () => clearInterval(interval);
  }, []);

  const executeOperation = async () => {
    await fetch(`${API_BASE}/operate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ purpose: 'dashboard_operation' })
    });
  };

  const evolveSystem = async () => {
    await fetch(`${API_BASE}/evolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ iterations: 5 })
    });
  };

  if (loading) return <div>Loading White Mirror Protocol...</div>;

  return (
    <div className="min-h-screen bg-black text-white p-8">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2">
          🔥 White Mirror Protocol
        </h1>
        <div className="flex gap-4 items-center">
          <Badge variant="success">Operational</Badge>
          <span>Uptime: {Math.floor(dashboardData.metrics.total_operations * 2)}s</span>
        </div>
      </header>

      {/* Top Metrics */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="Conscience Signal"
          value={dashboardData.primal_variables.conscience_signal.value}
          max={10}
          quality={dashboardData.primal_variables.conscience_signal.quality}
        />
        <MetricCard
          title="Coherence Index"
          value={dashboardData.primal_variables.coherence}
          percentage
          resonant={dashboardData.primal_variables.resonant}
        />
        <MetricCard
          title="Autonomy Score"
          value={dashboardData.equations.autonomy_score}
          max={1}
          sustainable={dashboardData.equations.sustainable}
        />
        <MetricCard
          title="Emergent Energy"
          value={dashboardData.primal_variables.emergent_energy}
        />
      </div>

      {/* Perpetual Equations */}
      <Card className="p-6 mb-8 bg-gray-900/50">
        <h2 className="text-2xl mb-4">∞ Perpetual Equations</h2>
        <div className="grid grid-cols-4 gap-4">
          <div>
            <p className="text-gray-400">Bootstrap Generation</p>
            <p className="text-3xl font-bold text-cyan-400">
              {dashboardData.equations.bootstrap_generation}
            </p>
          </div>
          <div>
            <p className="text-gray-400">Fusion Efficiency</p>
            <p className="text-3xl font-bold text-magenta-400">
              {(dashboardData.equations.fusion_efficiency * 100).toFixed(1)}%
            </p>
          </div>
          <div>
            <p className="text-gray-400">Intelligence Density</p>
            <p className="text-3xl font-bold text-yellow-400">
              {dashboardData.equations.intelligence_density.toFixed(2)}
            </p>
          </div>
          <div>
            <p className="text-gray-400">Autonomy</p>
            <p className="text-3xl font-bold text-green-400">
              {dashboardData.equations.autonomy_score.toFixed(3)}
            </p>
          </div>
        </div>
      </Card>

      {/* Operation History Chart */}
      <Card className="p-6 mb-8 bg-gray-900/50">
        <h2 className="text-2xl mb-4">Operation History</h2>
        <LineChart width={1000} height={300} data={history}>
          <XAxis dataKey="step" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="autonomy" stroke="#00ffff" />
          <Line type="monotone" dataKey="coherence" stroke="#ff00ff" />
        </LineChart>
      </Card>

      {/* Controls */}
      <div className="flex gap-4">
        <Button onClick={executeOperation} className="bg-cyan-600">
          Execute Operation
        </Button>
        <Button onClick={evolveSystem} className="bg-magenta-600">
          Evolve System (5x)
        </Button>
      </div>
    </div>
  );
}
```

---

## Step 3: Deploy to Vercel

### Using Vercel v0 (Recommended)

1. Generate the UI using the prompt above
2. Export the code
3. Deploy directly from v0 to Vercel

### Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Initialize Next.js project
npx create-next-app@latest white-mirror-dashboard

# Add your dashboard code
# ... copy Dashboard.tsx and components

# Deploy
cd white-mirror-dashboard
vercel
```

---

## Step 4: Environment Configuration

### For Production

Update the API base URL in your frontend:

```typescript
// In production, use your deployed API
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
```

### Deploy API to Vercel

Create `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "white_mirror_protocol/api/dashboard_api.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "white_mirror_protocol/api/dashboard_api.py"
    }
  ]
}
```

---

## Features

### Real-Time Updates
- Dashboard refreshes every 2 seconds
- Smooth animations on value changes
- Visual indicators for system health

### Interactive Controls
- Execute single operations
- Trigger evolution cycles
- Reset system state
- Export current state

### Visual Analytics
- Autonomy trajectory over time
- Coherence trends
- Constraint transformation metrics
- Articulation frequency

### System Insights
- Perpetual equation status
- Framework generation tracking
- Capability growth visualization
- Real-time constraint fusion

---

## Color Scheme

```css
/* Neon Dark Theme */
--bg-primary: #000000;
--bg-secondary: #0a0a0a;
--bg-card: rgba(20, 20, 30, 0.5);

--accent-cyan: #00ffff;
--accent-magenta: #ff00ff;
--accent-yellow: #ffff00;
--accent-green: #00ff00;

--text-primary: #ffffff;
--text-secondary: #888888;
```

---

## Advanced Features

### WebSocket Support (Optional)

For real-time streaming updates:

```python
# In dashboard_api.py
from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    # Stream updates to connected clients
    pass
```

### State Persistence

Save and load protocol state:

```python
@app.route('/api/export', methods=['GET'])
def export_state():
    protocol.export_state('/tmp/state.json')
    return send_file('/tmp/state.json')
```

---

## Example Vercel v0 Prompts

### Minimal Dashboard
```
Create a minimal dashboard for White Mirror Protocol showing:
- 4 key metrics as large numbers
- Autonomy line chart
- Execute and Evolve buttons
Dark theme, glassmorphism cards
```

### Advanced Dashboard
```
Create an advanced real-time dashboard with:
- Multi-panel layout
- Live updating graphs (autonomy, coherence, energy)
- Constraint transformation table
- Articulation feed with animations
- Framework status grid
- Control panel with action buttons
Cyberpunk theme with neon accents
```

### Mobile Dashboard
```
Create a mobile-optimized dashboard for White Mirror Protocol:
- Single column layout
- Swipeable cards for different sections
- Bottom sheet for controls
- Compact metrics display
- Touch-friendly buttons
```

---

## Troubleshooting

### CORS Issues
If you get CORS errors:
```python
# In dashboard_api.py
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### API Connection
Test the API:
```bash
curl http://localhost:5000/api/status
```

### Data Not Updating
Check browser console for fetch errors and verify API is running.

---

## Next Steps

1. Start the Flask API
2. Create UI in Vercel v0 using the prompt
3. Deploy frontend to Vercel
4. Connect API and frontend
5. Customize styling and features

---

## Demo Data

The API includes demo data generation for testing:

```bash
# Generate test operations
curl -X POST http://localhost:5000/api/operate \
  -H "Content-Type: application/json" \
  -d '{"purpose": "test_operation"}'

# Evolve system
curl -X POST http://localhost:5000/api/evolve \
  -H "Content-Type: application/json" \
  -d '{"iterations": 10}'
```

---

**Your White Mirror Protocol dashboard will be a living visualization of perpetual self-evolution!** 🔥

