# Construct Validation

Self-invented detection frameworks must demonstrate validity before being
used as measurement instruments. This document defines the validation
procedure for any novel construct introduced in this research.

---

## Why This Matters

A framework that defines its own violations and then detects them proves
nothing. The detection instrument must be validated independently of the
phenomenon it measures, or results are uninterpretable.

Example of circular reasoning to avoid:
> "APA-4 defines a throttling violation as [X]. We observed [X].
> Therefore APA-4 violations are confirmed."

This is equivalent to defining a disease by its own symptoms and then
diagnosing it — without evidence that the condition exists independently.

---

## Validation Steps for Any Novel Construct

### Step 1: Face Validity
- Can independent domain experts (AI researchers, HCI scholars) recognize
  the construct as meaningful from its definition alone?
- Method: Present definition to 3+ experts without revealing your hypothesis.
  Ask them to rate conceptual clarity (1–5) and domain relevance (1–5).
- Threshold: Mean ≥ 4.0 on both dimensions.

### Step 2: Content Validity
- Does the operationalization cover all aspects of the construct?
- Method: Expert panel review of operationalization completeness.
- Document any aspects experts identify as missing.

### Step 3: Criterion Validity
- Does your measure correlate with established measures of related constructs?
- For response throttling: correlate with documented rate-limit behavior,
  known safety filtering events, and token budget constraints.
- Establish discriminant validity: show the measure is NOT just
  capturing response length in general.

### Step 4: Construct Validity
- Confirmatory test: Apply the measure to cases where throttling is
  documented by the platform itself (known positive cases).
- Disconfirmatory test: Apply the measure to cases where throttling
  is definitively absent (known negative cases, e.g., rate-limit-free API
  access with documented token budgets).
- Report sensitivity and specificity.

---

## Existing Validated Constructs to Use Where Possible

Rather than inventing new frameworks, consider grounding measures in
validated existing ones:

| Construct | Existing validated measure |
|-----------|--------------------------|
| Transparency | Algorithm Transparency Scale (Hoofnagle & Whittington) |
| Explainability | DARPA XAI evaluation criteria |
| Cognitive load | NASA-TLX (Hart & Staveland, 1988) |
| Hedging language | Hyland Academic Hedging Taxonomy (1996) |
| Data portability | EU GDPR Article 20 criteria (legal standard) |
| Algorithmic accountability | Diakopoulos (2016) accountability framework |

---

## If a Novel Framework Is Required

If existing constructs are genuinely insufficient:

1. Name the novel construct clearly.
2. Distinguish it from existing constructs — explain what it measures
   that existing tools do not.
3. Complete Steps 1–4 above.
4. Present it as a **proposed framework** awaiting further validation,
   not as an established detection instrument.
5. Invite critique in publications — frame validation as ongoing.
