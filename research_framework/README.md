# AI Behavior Research Framework

A structured methodology for empirically investigating AI platform behavior,
transparency, and user sovereignty constraints.

## Purpose

This framework operationalizes claims about AI platform behavior into testable
hypotheses with documented protocols, reproducible data collection, and
independent verification procedures.

## Structure

```
research_framework/
├── methodology/
│   ├── 01_framework_overview.md       # Research design and epistemology
│   ├── 02_hypothesis_register.md      # Formal hypotheses with operationalizations
│   └── 03_construct_validation.md     # How detection constructs are validated
│
├── protocols/
│   ├── P-01_response_throttling.md    # Controlled tests for response variation
│   ├── P-02_decision_traceability.md  # Tests for explainability of refusals
│   ├── P-03_memory_portability.md     # Tests for data export and continuity
│   └── P-04_topic_sensitivity.md      # Tests for topic-based response shifts
│
├── data_collection/
│   ├── schema_trial_record.json       # Schema for a single test trial
│   ├── schema_session_log.json        # Schema for a full session log
│   └── schema_cross_platform.json     # Schema for multi-platform comparison
│
├── verification/
│   ├── independent_review_protocol.md # How to engage human expert reviewers
│   ├── inter_rater_reliability.md     # Coding reliability procedures
│   └── replication_guide.md          # How a third party replicates the study
│
└── templates/
    ├── trial_log.csv                  # Blank trial log
    ├── platform_comparison.csv        # Blank cross-platform sheet
    └── findings_report.md             # Report template for findings
```

## Quick Start

1. Read `methodology/01_framework_overview.md` for research design.
2. Select a protocol from `protocols/` matching your research question.
3. Use `data_collection/schema_trial_record.json` to log each trial.
4. Follow `verification/replication_guide.md` before publishing findings.

## Authorship Note

Per COPE and ICMJE guidelines, AI tools used in this research are documented
as instruments in the Methods section, not listed as authors. Authorship
requires the ability to take responsibility for the work — a property AI
systems do not currently have.
