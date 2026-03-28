# AI Dynamic Workflow Assistant

**Intelligent file analysis, pattern recognition, and workflow suggestions with adaptive learning**

---

## Overview

The AI Dynamic Workflow Assistant analyzes files, compares them, summarizes key points, and suggests deployment strategies. It learns from context over time, adapting and improving to become more intuitive through integration with the White Mirror Protocol.

### Key Features

- 🔍 **Intelligent File Analysis** - Understands file purpose, dependencies, and readiness
- 📊 **File Comparison** - Compares multiple files and identifies relationships
- 📝 **Key Point Extraction** - Summarizes important aspects of each file
- 🚀 **Deployment Suggestions** - Recommends deployment strategies based on analysis
- 🧠 **Pattern Recognition** - Learns workflow patterns across operations
- 🔥 **Adaptive Learning** - Uses White Mirror Protocol for meta-learning
- 💡 **Context Accumulation** - Builds knowledge from interactions
- ⚡ **Multi-AI Integration** - Optional AI-powered analysis (Claude, Gemini, etc.)

---

## Quick Start

### Basic Usage

```python
from white_mirror_protocol.workflow_assistant import WorkflowAssistant

# Initialize
assistant = WorkflowAssistant(config={
    'enable_learning': True,  # Enable White Mirror learning
    'use_ai': False  # Set True if you have API keys
})

# Analyze files
result = assistant.analyze_files([
    'src/main.py',
    'src/utils.py',
    'README.md'
])

# Get deployment suggestions
workflow = assistant.suggest_workflow(
    file_paths=['src/main.py', 'src/utils.py'],
    goal='deploy'
)

# View dashboard
print(assistant.get_dashboard_summary())
```

### With Multi-AI Framework

```python
assistant = WorkflowAssistant(config={
    'enable_learning': True,
    'use_ai': True,
    'anthropic_api_key': 'your-key',
    'google_api_key': 'your-key'
})

# AI-powered analysis
result = assistant.analyze_files(['complex_file.py'])
```

---

## Core Components

### 1. FileAnalyzer

Analyzes individual files to extract:
- **Purpose** - What the file does
- **Key points** - Important aspects
- **Dependencies** - Required libraries/files
- **Deployment readiness** - How production-ready it is (0-100%)
- **Suggestions** - Recommendations for improvement

```python
from white_mirror_protocol.workflow_assistant import FileAnalyzer

analyzer = FileAnalyzer()
analysis = analyzer.analyze_file('myfile.py')

print(f"Purpose: {analysis.purpose}")
print(f"Readiness: {analysis.deployment_readiness:.1%}")
print(f"Key points: {analysis.key_points}")
```

### 2. WorkflowPatternRecognizer

Learns patterns from file operations over time:

```python
from white_mirror_protocol.workflow_assistant import WorkflowPatternRecognizer

recognizer = WorkflowPatternRecognizer()

# Record operations
recognizer.record_operation('deploy', ['file1.py', 'file2.py'], 'success')
recognizer.record_operation('test', ['file1.py', 'file3.py'], 'success')

# Get patterns
patterns = recognizer.get_patterns_for_files(['file1.py'])
```

### 3. DeploymentSuggester

Suggests deployment strategies based on file analysis:

```python
from white_mirror_protocol.workflow_assistant import DeploymentSuggester

suggester = DeploymentSuggester()
suggestions = suggester.suggest_deployment(analyses, patterns)

for suggestion in suggestions:
    print(f"\nStrategy: {suggestion.strategy_name}")
    print(f"Confidence: {suggestion.confidence:.1%}")
    print(f"Steps: {len(suggestion.steps)}")
```

---

## Features in Detail

### Adaptive Learning

The assistant learns from:

1. **Operation History** - Recognizes recurring workflows
2. **User Feedback** - Adapts based on ratings and comments
3. **Context Accumulation** - Builds knowledge over sessions
4. **Meta-Learning** - Uses White Mirror Protocol for deep adaptation

```python
# Provide feedback
assistant.learn_from_feedback(
    operation_id='op_001',
    feedback={
        'rating': 0.9,  # 0-1 scale
        'comments': 'Great deployment suggestion!'
    }
)

# Negative feedback is treated as a constraint and transformed
assistant.learn_from_feedback(
    operation_id='op_002',
    feedback={
        'rating': 0.3,
        'comments': 'Missing testing steps'
    }
)
# → System learns to include testing in future suggestions
```

### Pattern Recognition

Automatically identifies patterns such as:
- **File collaboration** - Which files are often used together
- **Workflow sequences** - Common operation orders
- **Deployment patterns** - Successful deployment approaches

Patterns improve with:
- **Confidence** - Increases with occurrences
- **Effectiveness** - Updated from user feedback

### Context Insights

View accumulated learning:

```python
insights = assistant.get_context_insights()

print(f"Files analyzed: {insights['statistics']['files_analyzed']}")
print(f"Patterns recognized: {insights['pattern_count']}")
print(f"Learned preferences: {insights['learned_preferences']}")

# Meta-learning insights
if 'meta_learning' in insights:
    print(f"System generation: {insights['meta_learning']['generation']}")
    print(f"Autonomy: {insights['meta_learning']['autonomy']}")
```

### Persistence

Save and load learned context:

```python
# Export context
assistant.export_learned_context('context.json')

# Later, in a new session
new_assistant = WorkflowAssistant()
new_assistant.load_learned_context('context.json')
# → Continues learning from previous sessions
```

---

## Supported File Types

The assistant recognizes and analyzes:

- **Python** (.py) - Classes, functions, imports
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx) - Modules, components
- **Markdown** (.md) - Documentation structure
- **JSON/YAML** (.json, .yml) - Configuration files
- **Shell scripts** (.sh) - Automation scripts
- **And more** - Extensible to any text-based format

---

## Workflow Suggestions

The assistant can suggest workflows for various goals:

### Deployment Workflows

```python
workflow = assistant.suggest_workflow(files, goal='deploy')
```

Suggests:
- Python package deployment (PyPI)
- Web app deployment (Vercel/Netlify)
- API deployment (Docker/Cloud)
- Documentation deployment (GitHub Pages)

### Testing Workflows

```python
workflow = assistant.suggest_workflow(files, goal='test')
```

Suggests:
- Unit testing strategies
- Integration testing
- Coverage requirements

### Integration Workflows

```python
workflow = assistant.suggest_workflow(files, goal='integrate')
```

Suggests:
- Dependency resolution
- Merge strategies
- Integration testing

---

## Integration with White Mirror Protocol

When `enable_learning=True`, the assistant uses the White Mirror Protocol for:

### 1. Constraint Transformation

Negative feedback or limitations are transformed into capabilities:

```
User feedback: "Missing feature X" (rating 0.3)
  ↓
White Mirror: Treat as constraint
  ↓
Transformation: Generate workaround and learn pattern
  ↓
Future suggestions: Include feature X
```

### 2. Meta-Learning

The system evolves through:
- **Self-application** - Improving its own analysis
- **Articulation** - Better understanding of patterns
- **Coherence checking** - Maintaining consistency

### 3. Perpetual Improvement

Each interaction:
- Increases system **generation**
- Develops new **capabilities**
- Boosts **autonomy** and **intelligence**

View meta-learning status:

```python
dashboard = assistant.get_dashboard_summary()
print(dashboard)
# Shows White Mirror Protocol generation, capabilities, autonomy
```

---

## Examples

### Example 1: Analyze Project Files

```bash
python example_usage.py
```

Demonstrates:
- File analysis
- Deployment suggestions
- Pattern learning
- Feedback integration
- Dashboard display

### Example 2: Real-World Usage

```python
# Analyze your project
assistant = WorkflowAssistant(config={'enable_learning': True})

# Get all Python files
import glob
python_files = glob.glob('src/**/*.py', recursive=True)

# Analyze
result = assistant.analyze_files(python_files, context={
    'purpose': 'prepare_release',
    'project': 'MyProject'
})

# Get deployment strategy
workflow = assistant.suggest_workflow(
    python_files,
    goal='deploy'
)

# Execute suggested steps
for step in workflow['steps']:
    print(f"{step['step']}. {step['action']}")
    # Run: step['command']
```

---

## API Reference

### WorkflowAssistant

**Main class for workflow assistance**

#### Methods

- `analyze_files(file_paths, context=None)` - Analyze multiple files
- `suggest_workflow(file_paths, goal)` - Suggest workflow for goal
- `learn_from_feedback(operation_id, feedback)` - Learn from user feedback
- `get_context_insights()` - Get accumulated learning insights
- `export_learned_context(filepath)` - Save learned context
- `load_learned_context(filepath)` - Load learned context
- `get_dashboard_summary()` - Get human-readable dashboard

#### Configuration

```python
config = {
    'enable_learning': True,  # Enable White Mirror integration
    'use_ai': False,  # Use Multi-AI Framework for analysis
    # If use_ai=True, provide API keys:
    'anthropic_api_key': 'sk-...',
    'google_api_key': '...',
    'openai_api_key': '...',
    'deepseek_api_key': '...'
}
```

### FileAnalysis

**Result of file analysis**

#### Attributes

- `file_path` - Path to analyzed file
- `file_type` - Detected file type
- `language` - Programming language
- `purpose` - Inferred purpose
- `key_points` - Important aspects (list)
- `dependencies` - Required dependencies (list)
- `deployment_readiness` - Readiness score (0-1)
- `suggestions` - Improvement suggestions (list)

### WorkflowPattern

**Recognized workflow pattern**

#### Attributes

- `pattern_id` - Unique pattern identifier
- `pattern_type` - Type of pattern
- `files_involved` - Files in pattern
- `sequence` - Operation sequence
- `confidence` - Pattern confidence (0-1)
- `occurrences` - Times pattern seen
- `effectiveness` - Pattern effectiveness (0-1)

### DeploymentSuggestion

**Suggested deployment strategy**

#### Attributes

- `strategy_name` - Name of strategy
- `description` - Description
- `steps` - Deployment steps (list)
- `estimated_time` - Time estimate
- `confidence` - Suggestion confidence (0-1)
- `risks` - Potential risks (list)
- `benefits` - Benefits (list)

---

## Use Cases

### 1. Project Analysis

Quickly understand a new codebase:

```python
files = glob.glob('**/*.py', recursive=True)
result = assistant.analyze_files(files)
# Get overview of project structure, dependencies, readiness
```

### 2. Deployment Planning

Get deployment strategy for your project:

```python
workflow = assistant.suggest_workflow(files, goal='deploy')
# Receive step-by-step deployment plan
```

### 3. Code Review Preparation

Analyze files before review:

```python
result = assistant.analyze_files(changed_files)
# Get key points, deployment readiness, suggestions
```

### 4. Workflow Optimization

Learn optimal workflows over time:

```python
# System learns from your operations
# Recognizes patterns
# Suggests optimized workflows automatically
```

### 5. Team Knowledge Base

Build shared knowledge:

```python
# Export team's learned context
assistant.export_learned_context('team_knowledge.json')

# Team members load it
assistant.load_learned_context('team_knowledge.json')
# → Shared workflow intelligence
```

---

## Roadmap

Future enhancements:

- [ ] Git integration for change analysis
- [ ] Dependency graph visualization
- [ ] Test coverage analysis
- [ ] Performance profiling suggestions
- [ ] Security vulnerability detection
- [ ] Automated refactoring suggestions
- [ ] Team collaboration features
- [ ] Real-time file watching

---

## Architecture

```
WorkflowAssistant
├── FileAnalyzer
│   ├── Heuristic analysis
│   └── AI-powered analysis (optional)
├── WorkflowPatternRecognizer
│   ├── Operation recording
│   └── Pattern identification
├── DeploymentSuggester
│   ├── Strategy generation
│   └── Risk/benefit analysis
└── WhiteMirrorProtocol (optional)
    ├── Meta-learning
    ├── Constraint transformation
    └── Perpetual improvement
```

---

## Requirements

- Python 3.8+
- **Optional**: Multi-AI Framework (for AI-powered analysis)
- **Optional**: White Mirror Protocol (for adaptive learning)

No additional dependencies for basic functionality.

---

## Contributing

Contributions welcome! Areas for improvement:

- Additional file type support
- More deployment strategies
- Enhanced pattern recognition
- Better heuristic analysis
- UI/Dashboard integration

---

## License

Part of the White Mirror Protocol system.
Educational and research use.

---

**The AI Dynamic Workflow Assistant learns and adapts with every interaction, becoming more intuitive over time!** 🧠✨

