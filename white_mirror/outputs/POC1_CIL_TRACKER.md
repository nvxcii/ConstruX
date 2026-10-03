# POC1: C-I-L Decision Alignment Tracker

## Overview

The C-I-L (Conscience-Intuition-Logic) Decision Alignment Tracker is the first Proof of Concept for the White Mirror framework. It validates the hypothesis that tracking decisions across the C-I-L dimensions can detect alignment drift and improve decision quality.

---

## The C-I-L Triad

```
                    CONSCIENCE (C)
                         △
                        /│\
                       / │ \
                      /  │  \
                     /   │   \
                    /    │    \
                   /     │     \
                  /      │      \
                 /       │       \
                /        │        \
               ▽─────────┼─────────▽
        INTUITION (I)    │    LOGIC (L)
                         │
                    ALIGNMENT
```

### Dimension Definitions

| Dimension | Question | Function |
|-----------|----------|----------|
| **Conscience (C)** | "What should I do?" | Ethical/moral compass |
| **Intuition (I)** | "What feels right?" | Pattern recognition |
| **Logic (L)** | "What makes sense?" | Analytical reasoning |

---

## Tracking Protocol

### Step 1: Record Each Decision

For each decision, rate how much each dimension influenced you (0.0 to 1.0):

```python
from white_mirror import WhiteMirrorOrchestrator

wm = WhiteMirrorOrchestrator(user_id="your_id")

# Record a decision
result = wm.record_decision(
    description="Decided to take the job offer",
    conscience=0.4,  # How much ethics/values influenced
    intuition=0.3,   # How much gut feeling influenced
    logic=0.3,       # How much analysis influenced
    domain="professional"
)
```

### Step 2: Reach Statistical Validity

**Minimum Threshold**: 30 decisions

After 30 decisions, the system can perform statistically valid analysis.

### Step 3: Review Alignment Reports

```python
# Get your profile
report = wm.urce.get_profile_report()

print(f"Decisions tracked: {report['total_decisions']}")
print(f"Current state: {report['current_state']}")
print(f"C-I-L Profile:")
print(f"  Conscience: {report['cil_profile']['conscience']['mean']:.2f}")
print(f"  Intuition: {report['cil_profile']['intuition']['mean']:.2f}")
print(f"  Logic: {report['cil_profile']['logic']['mean']:.2f}")
```

---

## Alignment States

| State | Description | Action |
|-------|-------------|--------|
| **INTEGRATED** | All three in harmony | Maintain |
| **C_DOMINANT** | Over-reliance on conscience | Balance with logic |
| **I_DOMINANT** | Over-reliance on intuition | Validate with data |
| **L_DOMINANT** | Over-reliance on logic | Trust feelings more |
| **CI_DRIFT** | Ignoring logic | Add analytical rigor |
| **CL_DRIFT** | Ignoring intuition | Trust gut more |
| **IL_DRIFT** | Ignoring conscience | Reconnect with values |
| **FRAGMENTED** | All in conflict | Seek integration |

---

## Drift Detection

The system detects drift by comparing recent decisions to your baseline:

```python
# Detect temporal drift
drift = wm.urce.alignment_tracker.detect_temporal_drift(window_days=30)

if drift.get("significant_drift"):
    print("Significant drift detected!")
    print(f"Conscience drift: {drift['conscience_drift']['drift']:.2f}")
    print(f"Intuition drift: {drift['intuition_drift']['drift']:.2f}")
    print(f"Logic drift: {drift['logic_drift']['drift']:.2f}")
```

---

## Precommitments

Precommitments are decisions made in advance to maintain alignment under pressure:

```python
# Add a precommitment
wm.urce.add_precommitment(
    principle="Integrity over expedience",
    trigger_condition="When facing time pressure to compromise quality",
    intended_response="Take the extra time to do it right",
    conscience_weight=0.6,
    intuition_weight=0.2,
    logic_weight=0.2
)
```

When a trigger condition is detected, the system reminds you of your precommitment.

---

## Domain Analysis

Track patterns across different life domains:

```python
# Get domain-specific analysis
domain_analysis = wm.urce.alignment_tracker.get_domain_analysis()

for domain, data in domain_analysis.items():
    print(f"\n{domain.upper()}:")
    print(f"  Decisions: {data['decision_count']}")
    print(f"  Dominant dimension: {data['dominant_dimension']}")
```

---

## Research Export Format

For academic analysis, export in research-ready format:

```python
# Export for research
export = wm.urce.export_data()

# Save to file
import json
with open("poc1_data_export.json", "w") as f:
    json.dump(export, f, indent=2)
```

### Export Schema

```json
{
  "metadata": {
    "user_id": "string",
    "export_timestamp": "ISO8601",
    "framework_version": "URCE_v1.0"
  },
  "profile": {
    "total_decisions": "int",
    "statistically_valid": "bool",
    "current_state": "string",
    "cil_profile": {
      "conscience": {"mean": "float", "std": "float"},
      "intuition": {"mean": "float", "std": "float"},
      "logic": {"mean": "float", "std": "float"}
    }
  },
  "decisions": [
    {
      "id": "string",
      "timestamp": "ISO8601",
      "description": "string",
      "cil_weights": {"C": "float", "I": "float", "L": "float"},
      "domain": "string"
    }
  ],
  "precommitments": [...],
  "snapshots": [...]
}
```

---

## Validation Study Design

### Hypothesis

Individuals who track their C-I-L alignment will show:
1. Improved decision satisfaction over time
2. Reduced alignment drift
3. Better outcomes in tracked domains

### Study Protocol

1. **Baseline Period** (Week 1-2)
   - Track 30+ decisions without intervention
   - Establish personal C-I-L profile

2. **Intervention Period** (Week 3-8)
   - Receive alignment feedback after each decision
   - Use precommitment system
   - Weekly drift reports

3. **Measurement Period** (Week 9-12)
   - Track outcomes of decisions
   - Measure decision satisfaction
   - Compare to baseline

### Metrics

- **Primary**: Decision satisfaction score (0-10)
- **Secondary**: Alignment variance (lower = more consistent)
- **Tertiary**: Precommitment adherence rate

---

## Example Data Collection Template

### Daily Decision Log

| Date | Decision | Domain | C | I | L | Outcome (later) |
|------|----------|--------|---|---|---|-----------------|
| 2024-01-15 | Accepted project deadline | Professional | 0.3 | 0.2 | 0.5 | |
| 2024-01-15 | Chose restaurant for dinner | Personal | 0.1 | 0.7 | 0.2 | |
| 2024-01-16 | Responded to difficult email | Relational | 0.5 | 0.2 | 0.3 | |

---

## Optimization Recommendations

Based on your profile, the system generates personalized recommendations:

```python
recs = wm.urce.get_optimization_recommendations()

for rec in recs:
    print(f"\n[{rec['category'].upper()}] - Priority: {rec['priority']:.1f}")
    print(f"  {rec['recommendation']}")
    print("  Steps:")
    for step in rec['implementation_steps']:
        print(f"    - {step}")
```

---

## Integration with Rights Ledger

All decisions are recorded in the immutable Rights Ledger:

```python
# View decision patterns from ledger
patterns = wm.ledger.get_decision_patterns()

print(f"Total decisions in ledger: {patterns['total_decisions']}")
print(f"C-I-L averages: {patterns['cil_averages']}")
```

This creates an audit trail of your decision-making evolution over time.

---

## Next Steps

1. **Start Tracking**: Record your next 30 decisions
2. **Review Weekly**: Check alignment reports every Sunday
3. **Set Precommitments**: Define 3-5 key principles
4. **Export Monthly**: Save data for long-term analysis
5. **Share Findings**: Contribute to research pool (optional)
