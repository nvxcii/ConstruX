# ConstruX — AI Assistant Guide

## Project Overview

ConstruX is a Python framework that orchestrates multiple AI models (Claude, Gemini, DeepSeek, ChatGPT) to execute complex, multi-phase missions. Its primary domain is legal/justice campaigns: gathering evidence, calculating leverage, predicting settlements, and generating regulatory complaints, media packages, and negotiation frameworks.

The repository has two independent components:
- `multi_ai_framework/` — the core orchestration framework
- `voice_mode.py` — standalone voice input/output utility for Claude Code Desktop

## Repository Structure

```
ConstruX/
├── multi_ai_framework/
│   ├── core/                     # AI base classes and coordination
│   │   ├── base_ai.py            # BaseAI ABC, AIResponse dataclass, AICapability enum
│   │   ├── ai_implementations.py # ClaudeAI, GeminiAI, DeepSeekAI, ChatGPTAI
│   │   ├── ai_coordinator.py     # AIJusticeLeague — routes tasks to AI models
│   │   └── task_distributor.py   # ThreadPoolExecutor-based parallel execution
│   ├── intelligence/             # Phase 1: data gathering
│   │   ├── evidence_database.py  # SQLite evidence store
│   │   ├── violation_tracker.py  # SQLite violation tracking + leverage scoring
│   │   └── research_coordinator.py # Distributes research tasks across AIs
│   ├── analysis/                 # Phase 2: strategic analysis
│   │   ├── leverage_calculator.py  # Weighted leverage score (violations, evidence, etc.)
│   │   ├── settlement_modeler.py   # Settlement range prediction by claim type
│   │   └── strategic_analyzer.py  # Selects strategy based on leverage threshold
│   ├── execution/                # Phase 3: campaign output generation
│   │   ├── complaint_generator.py  # OSHA, ADA, EEOC, settlement demand documents
│   │   ├── media_coordinator.py    # Press release, talking points, social strategy
│   │   ├── settlement_negotiator.py # Negotiation phases and concession strategy
│   │   └── execution_coordinator.py # Orchestrates all execution outputs
│   ├── missions/
│   │   ├── mission_orchestrator.py  # Top-level entry point for full missions
│   │   └── gaylord_justice_campaign/ # Example mission with config JSON
│   ├── config/
│   │   └── config_manager.py     # API key loading (env vars only, never saves keys)
│   ├── utils/
│   │   ├── data_sync.py          # JSON-based cross-component data sync
│   │   ├── result_aggregator.py  # Combines multi-AI outputs into summaries
│   │   └── export_utils.py       # JSON and human-readable report export
│   └── example_usage.py          # Runnable end-to-end demo
├── voice_mode.py                 # Voice I/O for Claude Code Desktop
└── .github/workflows/blank.yml   # Placeholder CI (not functional)
```

## Development Setup

### Requirements

Python 3.8+. No package manager lockfile is present. Install dependencies manually:

```bash
pip install anthropic google-generativeai openai
# For voice_mode.py only:
pip install SpeechRecognition pyttsx3 sounddevice numpy keyboard
```

### API Keys

All four API keys are required for full framework operation. Set them as environment variables — **never hardcode or commit keys**:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
export DEEPSEEK_API_KEY="..."
export OPENAI_API_KEY="sk-..."
```

`ConfigManager` reads these at runtime. It saves non-key settings to `~/.multi_ai_framework/config.json` but explicitly strips API keys before writing.

### Run the Example Mission

```bash
cd multi_ai_framework
python example_usage.py
```

## Architecture: Three-Phase Pipeline

```
case_data (dict)
    │
    ▼
Phase 1 — Intelligence (intelligence/)
    Evidence + Violations → SQLite DBs
    AI research → distributed via AIJusticeLeague.distribute_research()
    │
    ▼
Phase 2 — Analysis (analysis/)
    LeverageAnalysis + SettlementPrediction
    AI analysis → distributed via AIJusticeLeague.distribute_analysis()
    │
    ▼
Phase 3 — Execution (execution/)
    Complaints + MediaPackage + NegotiationFramework + Timeline
    AI execution → distributed via AIJusticeLeague.distribute_execution()
    │
    ▼
output/{case_id}/
    MISSION_REPORT.txt, mission_results.json
    execution/complaints/*.txt, execution/media/*.txt
```

### Multi-AI Task Routing

Each AI model has declared `AICapability` values. `AIJusticeLeague` routes tasks by phase:

| Phase | Claude | Gemini | DeepSeek | ChatGPT |
|-------|--------|--------|----------|---------|
| Research | Narrative development | Real-time research | Legal analysis | Regulatory procedures |
| Analysis | Leverage calculation | Trend analysis | Risk assessment | Communication strategy |
| Execution | Complaint drafting | Timeline | Settlement modeling | Media content |

### Parallel Execution

`TaskDistributor` uses `ThreadPoolExecutor` (not async/await) to call multiple AI APIs concurrently. Each task gets a UUID. Failed tasks are marked `success=False` in `AIResponse` and collected into the synthesis — they do not stop the pipeline.

## Coding Conventions

### Naming
- Classes: `PascalCase` (`AIJusticeLeague`, `TaskDistributor`, `ComplaintPackage`)
- Methods and variables: `snake_case`
- Private methods: `_underscore_prefix()`
- Constants / enums: `UPPER_CASE` values inside `Enum` subclasses

### Typing
All public methods have type hints. Use `Dict[str, Any]`, `List`, `Optional` from `typing`.

### Data Models
Use `@dataclass` for all data-transfer objects. Do not use plain dicts where a dataclass already exists. Key dataclasses:

| Dataclass | Location |
|-----------|----------|
| `AIResponse` | `core/base_ai.py` |
| `TaskResult` | `core/task_distributor.py` |
| `Evidence` | `intelligence/evidence_database.py` |
| `Violation` | `intelligence/violation_tracker.py` |
| `LeverageAnalysis` | `analysis/leverage_calculator.py` |
| `SettlementPrediction` | `analysis/settlement_modeler.py` |
| `ComplaintPackage` | `execution/complaint_generator.py` |
| `NegotiationFramework` | `execution/settlement_negotiator.py` |
| `MediaPackage` | `execution/media_coordinator.py` |

### Import Order
1. Standard library (`typing`, `dataclasses`, `datetime`, `sqlite3`, `os`, `json`, `threading`)
2. Third-party (`anthropic`, `google.generativeai`, `openai`)
3. Local relative imports (`from ..core.base_ai import BaseAI`)

### Error Handling
Wrap all AI API calls in try/except. Return `AIResponse` with `success=False` and the error message in the `error` field. Never let an individual AI failure raise uncaught to the pipeline caller.

```python
try:
    response = client.messages.create(...)
    return self._create_response(task_id, content, metadata, success=True)
except Exception as e:
    return self._create_response(task_id, "", {}, success=False, error=str(e))
```

### Comments
Write comments only for non-obvious business logic (e.g., leverage score weight rationale, jurisdiction-specific thresholds). Do not comment obvious control flow.

## Extending the Framework

### Adding a New AI Model

1. Subclass `BaseAI` in `core/ai_implementations.py`
2. Set `self.model_name` and populate `self.capabilities` with `AICapability` values
3. Implement `execute_task(task: Dict) -> AIResponse` and `validate_task(task: Dict) -> bool`
4. Register the instance in `AIJusticeLeague.__init__()` under `self.models`
5. Add it to the appropriate phase distribution methods in `ai_coordinator.py`

```python
class MyModelAI(BaseAI):
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self.model_name = "my_model"
        self.capabilities = [AICapability.DATA_SYNTHESIS]

    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        try:
            result = call_my_api(task["prompt"])
            return self._create_response(task["id"], result, {})
        except Exception as e:
            return self._create_response(task["id"], "", {}, success=False, error=str(e))

    def validate_task(self, task: Dict[str, Any]) -> bool:
        return "prompt" in task and "id" in task
```

### Adding a New Analysis Module

1. Create a file in `analysis/` with a coordinator class and a result dataclass
2. Call it from `strategic_analyzer.py` in `coordinate_analysis()`
3. Include the result in the dict returned by `coordinate_analysis()`

### Adding a New Complaint Type

Add a new template branch in `complaint_generator.py` inside `generate_complaint()`, following the existing pattern for `osha`, `ada`, `eeoc`.

## Configuration Reference

`ConfigManager` at `config/config_manager.py` loads from:
1. `~/.multi_ai_framework/config.json` (non-sensitive settings only)
2. Environment variables (override file, includes API keys)

Key settings you can set via `config.set()`:

| Key | Default | Description |
|-----|---------|-------------|
| `max_workers` | `4` | ThreadPoolExecutor worker count |
| `claude_config` | `{}` | Dict with `model` and `max_tokens` |
| `gemini_config` | `{}` | Dict with `model` |
| `deepseek_config` | `{}` | Dict with `model` |
| `chatgpt_config` | `{}` | Dict with `model` |

Current Claude model used in code: `claude-sonnet-4-5-20250929`

## Output Directory Structure

```
output/{case_id}/
├── MISSION_REPORT.txt
├── mission_results.json
├── research_phase.json
├── analysis_phase.json
├── execution_phase.json
└── execution/
    ├── DEPLOYMENT_SUMMARY.txt
    ├── campaign_timeline.json
    ├── execution_playbook.json
    ├── negotiation_framework.json
    ├── complaints/
    │   ├── osha_complaint.txt
    │   ├── ada_complaint.txt
    │   ├── eeoc_complaint.txt
    │   └── settlement_demand_complaint.txt
    └── media/
        ├── press_release.txt
        ├── talking_points.txt
        ├── media_faq.txt
        └── media_package.json
```

## Security Rules

- **Never hardcode API keys.** Use environment variables only.
- `ConfigManager.save()` explicitly strips all keys ending in `_api_key` before writing to disk.
- Do not commit `.env` files, `config.json` with real keys, or any file containing case-sensitive data (evidence, PII).
- SQLite databases and JSON sync files in `data/` may contain sensitive case information — treat them as confidential.

## Voice Mode (voice_mode.py)

A standalone script for Claude Code Desktop. Not part of the framework — has no imports from `multi_ai_framework/`.

**Dependencies**: `speech_recognition`, `pyttsx3`, `sounddevice`, `numpy`, `keyboard`

**Default hotkeys**:
- `Ctrl+Shift+V` — toggle voice mode
- `Ctrl+Space` — push to talk
- `Ctrl+Shift+S` — stop speaking

**Run**:
```bash
python voice_mode.py           # Start with hotkeys
python voice_mode.py --setup   # Interactive setup wizard
python voice_mode.py --list-devices  # Show audio devices
```

Config persisted to `voice_config.json` in the working directory.

## Known Gaps

- **No tests.** No test files exist anywhere. When adding functionality, write tests in a `tests/` directory using `pytest`.
- **CI is a placeholder.** `.github/workflows/blank.yml` just echoes "Hello, world!" — it does not run the framework or any checks.
- **No linting config.** No `pylintrc`, `pyproject.toml`, or `ruff.toml` present. Follow PEP 8 manually.
- **No `requirements.txt`.** Dependencies are documented in `multi_ai_framework/README.md` but not in a machine-readable format. Consider adding one.
