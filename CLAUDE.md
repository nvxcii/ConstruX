# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup

```bash
# Install multi-AI framework dependencies
pip install -r multi_ai_framework/requirements.txt

# Install web interface + voice mode dependencies
pip install -r requirements.txt
```

### Running

```bash
# Run the chat web interface (http://localhost:5000)
python app.py

# Run the multi-AI framework directly via CLI (from repo root)
python -m multi_ai_framework.example_usage

# Run voice mode (Linux/macOS)
bash start_voice_mode.sh

# Run voice mode (Windows)
start_voice_mode.bat

# Install voice mode (Linux/macOS)
bash install_voice_mode.sh
```

### API Keys

Set API keys as environment variables before running:

```bash
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
export OPENAI_API_KEY=...
export DEEPSEEK_API_KEY=...
```

`ConfigManager` reads non-key settings from `~/.multi_ai_framework/config.json` (created automatically), then **overrides** with any matching environment variables. API keys are never persisted to disk by `save()` — environment variables are the only supported way to supply them.

> There is no test suite and no linter configured in this repository.

---

## Architecture

ConstruX has three independent components: the **Web Interface**, the **Multi-AI Framework**, and the **Voice Mode** script. There is also a static marketing page (`index.html`) for a product called FOPE.

---

### Web Interface (`app.py` + `templates/chat.html`)

A Flask chat interface for running live missions. The conversation collects four fields (situation, employer, client, violations), then runs all three framework phases in a background thread. The frontend polls `/api/mission/<id>` every 2 seconds for phase progress and renders a results card (leverage score, settlement range, execution package) when complete.

Routes: `GET /` serves the UI · `POST /api/start` begins a session · `POST /api/message` handles each chat turn · `GET /api/mission/<id>` returns mission state.

---

### Multi-AI Framework (`multi_ai_framework/`)

A 3-phase orchestration pipeline that fans work out across four AI providers (Claude, Gemini, DeepSeek, ChatGPT) and consolidates results.

**Entry point**: `missions/mission_orchestrator.py` → `MissionOrchestrator.execute_complete_mission(case_data)`

```
MissionOrchestrator
  │
  ├─ Phase 1: IntelligenceGathering   (intelligence/)
  │    Distributes research tasks to all 4 AIs in parallel via TaskDistributor.
  │    Outputs: EvidenceDatabase, ViolationTracker
  │
  ├─ Phase 2: StrategicAnalysis        (analysis/)
  │    Runs leverage scoring (0–100 across 6 dimensions), settlement modeling,
  │    and AI strategic insights. Consumes Phase 1 output.
  │
  └─ Phase 3: ExecutionCoordination    (execution/)
       Generates regulatory complaints (OSHA, EEOC, ADA, settlement demand),
       media strategy, and negotiation frameworks. Consumes Phase 2 output.
```

**Core layer** (`core/`):
- `base_ai.py` — `AICapability` enum + `AIResponse` dataclass; all AI classes conform to this interface.
- `ai_implementations.py` — Concrete adapters for each provider.
- `ai_coordinator.py` — `AIJusticeLeague` holds all four model instances and routes tasks.
- `task_distributor.py` — `TaskDistributor` runs tasks in a `ThreadPoolExecutor` (4 workers by default).

**Utilities** (`utils/`):
- `data_sync.py` — Synchronizes shared state (evidence, violations, analysis) across phases.
- `result_aggregator.py` — Merges responses from multiple AI models into a single result.
- `export_utils.py` — Writes final results to JSON and human-readable text reports.

**Mission data** lives in `missions/gaylord_justice_campaign/` as an example. A mission is driven by a large JSON config (`campaign_config.json`) with ~82 fields describing the legal case.

---

### Voice Mode (`voice_mode.py`)

Standalone ~415-line Python script providing a voice assistant interface for Claude Code Desktop. Uses `sounddevice` (not PyAudio) for audio I/O, `SpeechRecognition` for STT, and `pyttsx3` for TTS.

Configuration is read from `voice_config.json` at startup (hotkeys, speech engine settings, recognition thresholds). The script is self-contained and has no dependency on the multi-AI framework.

---

### Web Frontend (`index.html`)

Static marketing landing page for FOPE (Field Optimization Protocol Engine). Uses Tailwind CSS via CDN — no build step. Not connected to any backend.
