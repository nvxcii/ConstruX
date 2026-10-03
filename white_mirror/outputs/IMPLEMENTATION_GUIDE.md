# White Mirror Implementation Guide

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nvxcii/ConstruX.git
cd ConstruX

# The white_mirror module is self-contained
# No additional installation required beyond Python 3.7+
```

### Basic Usage

```python
from white_mirror import WhiteMirrorOrchestrator

# Initialize the system
wm = WhiteMirrorOrchestrator(user_id="my_user")

# Evaluate an action
result = wm.evaluate({
    "type": "decision",
    "description": "Automated content moderation",
    "actor": "system",
    "target": "user_content"
})

print(f"Compliant: {result['compliant']}")
print(f"Score: {result['aggregate_score']:.2f}")
```

---

## Core Operations

### 1. Constitutional Evaluation

Evaluate any action against the 5 Constitutional Axioms:

```python
action = {
    "type": "policy_enforcement",
    "description": "Removing user account without notice",
    "actor": "platform_admin",
    "target": "user_123",
    "consent_obtained": False,
    "coercion_level": 0.0,
    "verification_score": 0.8
}

result = wm.evaluate(action)

# Check detailed axiom compliance
for axiom, (compliant, score, explanation) in result['results']['constitutional']['detailed_results'].items():
    print(f"{axiom}: {'✓' if compliant else '✗'} ({score:.2f}) - {explanation}")
```

### 2. Decision Tracking (POC1)

Track decisions with C-I-L weights:

```python
# Record a decision
wm.record_decision(
    description="Chose to work overtime to meet deadline",
    conscience=0.3,   # Some ethical consideration
    intuition=0.2,    # Moderate gut feeling
    logic=0.5,        # Primarily logical decision
    domain="professional"
)

# Get your profile
profile = wm.urce.get_profile_report()
print(f"Current state: {profile['current_state']}")
```

### 3. Predictions (POC3)

Generate predictions based on patterns:

```python
# Predict future compliance
prediction = wm.predict("compliance_score", horizon_days=7)

if "error" not in prediction:
    print(f"Predicted score: {prediction['prediction']['predicted_value']:.2f}")
    print(f"Confidence: {prediction['prediction']['confidence']:.2f}")

# Predict violation likelihood
likelihood = wm.predict_violation_likelihood()
print(f"Violation likelihood: {likelihood['violation_likelihood']:.2f}")
print(f"Risk category: {likelihood['risk_category']}")
```

### 4. Human-AI Collaboration

Start a collaboration session:

```python
# Start session
session = wm.start_collaboration(mode="integrated", context="Content review task")

# Check alignment between human and AI positions
alignment = wm.check_alignment(
    human_position={"action": "approve", "confidence": 0.8},
    ai_position={"action": "approve", "confidence": 0.75}
)

print(f"Alignment status: {alignment['alignment']['alignment_status']}")
```

---

## Framework Components

### Using Individual Enforcers

#### SFI Enforcer

```python
from white_mirror.enforcers import SFIEnforcer

sfi = SFIEnforcer()

# Analyze a restriction
result = sfi.analyze_restriction(
    expression={"content": "Political opinion", "category": "political"},
    restriction={"type": "content_based", "timing": "pre_publication"}
)

print(f"SFI Compliant: {result['compliant']}")
```

#### TVP Enforcer

```python
from white_mirror.enforcers import TVPEnforcer

tvp = TVPEnforcer()

# Verify a claim
result = tvp.verify_claim(
    claim_content="Product reduces carbon emissions by 50%",
    source="company_marketing",
    source_category="commercial"
)

print(f"Epistemic status: {result['verification_result']['epistemic_status']}")
```

#### APA Engine

```python
from white_mirror.engines import APAEngine

apa = APAEngine()

# Analyze for manipulation
result = apa.analyze_interaction(
    action_description="Limited time offer - only 3 left!",
    actor="marketing_system",
    target="potential_customer"
)

print(f"Manipulation signals: {len(result['manipulation_signals'])}")
```

### Using the DPAP Transformer

```python
from white_mirror.engines import DPAPTransformer

dpap = DPAPTransformer()

# Ingest a constraint
constraint = dpap.ingest_constraint(
    constraint_type="speech_suppression",
    source="SFI",
    severity=0.7,
    description="Viewpoint-based content removal",
    patterns=["political", "controversial"]
)

# Transform into capability
transformation = dpap.transform(constraint)

print(f"Capability generated: {transformation.output_capability.capability_type}")
print(f"Antifragility score: {dpap.get_antifragility_metrics()['antifragility_score']:.2f}")
```

### Using EchoVault

```python
from white_mirror.bridges import EchoVault

vault = EchoVault()

# Get symbolic frame for a concept
frame = vault.get_symbolic_frame("A1_SOVEREIGNTY")

print(f"Archetype: {frame['archetype']['name']}")
print(f"Invocation: {frame['invocation']}")

# Get narrative for a situation
narrative = vault.get_narrative_for_situation("manipulation_detected")

print(f"Narrative: {narrative['narrative']['title']}")
print(f"Resolution: {narrative['narrative']['resolution_path']}")
```

---

## Integration with Multi-AI Justice League

```python
from white_mirror.integrations import JusticeLeagueIntegration

# Initialize integration
integration = JusticeLeagueIntegration()

# Verify a mission configuration
mission_config = {
    "mission_name": "Workplace Rights Campaign",
    "target": {"name": "Corporation XYZ"},
    "violations": [
        {"type": "labor_violation", "description": "Unpaid overtime"}
    ]
}

compliance = integration.verify_mission_constitutional_compliance(mission_config)

print(f"Constitutional compliance: {compliance['constitutional_compliance']}")
print(f"Proceed recommendation: {compliance['proceed_recommendation']}")
```

---

## Configuration

### Custom Primal Variables

```python
from white_mirror.core import PrimalVariables

# Create custom configuration
variables = PrimalVariables(
    lambda_conscience=0.5,    # Higher ethical weight
    lambda_intuition=0.25,
    lambda_logic=0.25,
    lambda_antifragility=2.0  # More aggressive antifragile response
)

wm = WhiteMirrorOrchestrator(variables=variables)
```

### Custom Ledger Path

```python
wm = WhiteMirrorOrchestrator(
    user_id="user_001",
    ledger_path="/path/to/custom/ledger.db"
)
```

---

## Data Export

### Full System Export

```python
# Export everything
export = wm.export_full_state("white_mirror_backup.json")

# Export includes:
# - System state
# - Framework status
# - Ledger entries
# - URCE data
# - CIL data
# - DPAP capabilities
# - Predictions
# - FOPE translations
# - EchoVault mappings
```

### Ledger Export

```python
# Export just the ledger
ledger_export = wm.ledger.export_ledger("ledger_backup.json")

# Verify integrity
integrity = wm.ledger.verify_integrity()
print(f"Ledger valid: {integrity['valid']}")
```

---

## Best Practices

### 1. Regular Evaluations

```python
# Evaluate before any significant action
def safe_action(action_data):
    result = wm.evaluate(action_data)
    if not result['compliant']:
        print("Action blocked - constitutional violation")
        return None
    return execute_action(action_data)
```

### 2. Decision Tracking Discipline

```python
# Track all significant decisions
# Aim for 30+ in first month
# Review weekly
```

### 3. Precommitment Hygiene

```python
# Set precommitments for known challenges
wm.urce.add_precommitment(
    principle="Data privacy first",
    trigger_condition="When asked to share user data",
    intended_response="Verify consent and minimize data shared",
    conscience_weight=0.6,
    intuition_weight=0.2,
    logic_weight=0.2
)
```

### 4. Regular Meta-Recursion

```python
# Weekly self-evaluation
meta = wm.apply_meta_recursion()
print(f"System integrity: {meta['system_integrity']}")
```

---

## Troubleshooting

### Import Errors

```python
# If imports fail, ensure you're in the right directory
import sys
sys.path.insert(0, '/path/to/ConstruX')

from white_mirror import WhiteMirrorOrchestrator
```

### Database Issues

```python
# Reset the ledger if corrupted
import os
os.remove("rights_ledger.db")
wm = WhiteMirrorOrchestrator()  # Creates fresh ledger
```

### Insufficient Data for Predictions

```python
# Check data requirements
predictor_summary = wm.predictor.get_dimension_summary("compliance_score")
print(f"Data points: {predictor_summary.get('data_points', 0)}")
print(f"Ready for prediction: {predictor_summary.get('ready_for_prediction', False)}")
```

---

## API Reference

### WhiteMirrorOrchestrator

| Method | Description |
|--------|-------------|
| `evaluate(action, context)` | Evaluate action against all frameworks |
| `record_decision(...)` | Track a C-I-L decision |
| `predict(dimension, horizon)` | Generate prediction |
| `start_collaboration(mode)` | Start human-AI session |
| `get_system_state()` | Get current system state |
| `apply_meta_recursion()` | Self-evaluate the system |
| `export_full_state(path)` | Export all data |

### Full API documentation available in source code docstrings.
