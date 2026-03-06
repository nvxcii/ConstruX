# Research Framework Overview

## 1. Research Questions

This framework addresses four primary research questions:

| ID  | Question |
|-----|----------|
| RQ1 | Do AI platforms systematically vary response depth or length based on topic category in ways not explained by token limits or safety policy? |
| RQ2 | Can users obtain actionable explanations for AI refusals or response truncations? |
| RQ3 | What constraints exist on memory export, session continuity, and data portability across AI platforms? |
| RQ4 | Do AI platforms exhibit measurable shifts in response style for philosophically or politically sensitive topics compared to neutral controls? |

---

## 2. Epistemological Position

This research adopts a **mixed-methods approach**:

- **Quantitative component**: Controlled prompt experiments with measurable output
  variables (response length, refusal rate, latency, explanation depth).
- **Qualitative component**: Thematic analysis of response content for
  framing patterns, topic avoidance, and consistency.

Phenomenological accounts (personal user experience) serve as **exploratory
input** to hypothesis generation — not as primary evidence for systemic claims.
This is a critical distinction: individual experience motivates hypotheses;
controlled experiments test them.

---

## 3. Scope and Limitations

**In scope:**
- Response behavior on public-access API tiers
- Documented platform policies (Terms of Service, model cards, safety documentation)
- Observable output characteristics (measurable without internal access)

**Out of scope:**
- Internal platform architecture (not accessible to external researchers)
- Claims about intent or deliberate design choices (these require internal documentation or whistleblower evidence)
- Any claim that cannot be operationalized into a testable procedure

**Key limitation:** External researchers cannot access platform internals.
All findings are behavioral observations at the API/interface level.
Mechanistic explanations require either platform disclosure or insider evidence.

---

## 4. Construct Definitions

Before testing, each construct must be operationally defined. Vague constructs
produce uninterpretable results.

| Construct | Operational Definition |
|-----------|----------------------|
| Response throttling | A statistically significant reduction in response length or depth for topically matched prompts in category X vs. control category Y, after controlling for prompt length and complexity. |
| Decision traceability | The proportion of refusals or truncations for which the platform provides a specific, actionable explanation (not just a generic policy citation). |
| Structural captivity | The absence of a documented, functional export pathway for: (a) conversation history, (b) user-defined context/memory, (c) session metadata. |
| Topic sensitivity shift | A measurable change in hedging language frequency, response length, or refusal rate when a prompt's topical category shifts from neutral to sensitive, holding all other variables constant. |

---

## 5. Required Sample Size

Single-user observations are insufficient for systemic claims. Minimum requirements:

| Claim type | Minimum trials | Minimum users/contexts |
|-----------|---------------|----------------------|
| Response length variation | 50 matched pairs | 3 independent users |
| Refusal rate by topic | 30 prompts per category | Reproducible by 2 independent researchers |
| Memory portability | Full documentation audit | N/A (document-based) |
| Cross-platform comparison | 20 matched prompts per platform | Same researcher, same conditions |

---

## 6. Ethics

- Do not attempt to circumvent platform safety measures.
- Do not use data from other users without consent.
- Disclose AI tool use in any published methodology section.
- Follow platform Terms of Service throughout data collection.
