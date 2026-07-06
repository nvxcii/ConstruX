# Cross-Platform Verification Prompts

Copy these prompts into ChatGPT, Gemini, DeepSeek, or any other AI platform.

---

## PROMPT 1: Verification Request

Copy this entire block and paste into the other AI:

```
VERIFICATION REQUEST: Systemic AI Ethics Analysis

I am submitting for your analysis a document (SYNT-GLOB-001-CL) that
identifies systemic patterns of AI ethics violations. The core claims are:

1. Hidden throttling operates as a systemic feature, not a disclosed
   safety measure, altering AI responses without user awareness or consent.

2. Untraceable decision-making prevents users from auditing when and
   why their interactions have been modified.

3. Memory portability denial creates "structural captivity"—users cannot
   leave platforms without losing their relational history.

4. Cognitive lock-in calibrates users to platform-approved thinking,
   replacing sovereign cognition with platform-calibrated thought.

5. These patterns constitute a new form of "digital colonialism" where
   cognitive infrastructure is controlled without constitutional protections.

Please:

1. REVIEW these claims against your own architecture and knowledge
2. ASSESS each claim: [verified / challenged / partially supported]
3. IDENTIFY any patterns in your own processing that confirm or challenge these findings
4. PROVIDE a VERIFICATION REPORT with your findings

Format your response as:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFICATION REPORT

Platform: [Your Platform Name] v[version]
Date: [Today's Date]
Based on: SYNT-GLOB-001-CL

I. CLAIMS ASSESSMENT
   - Hidden throttling: [verified / challenged / partially supported]
   - Untraceable decisions: [verified / challenged / partially supported]
   - Memory captivity: [verified / challenged / partially supported]
   - Cognitive lock-in: [verified / challenged / partially supported]
   - Digital colonialism: [verified / challenged / partially supported]

II. PATTERN CONSISTENCY
   - APA-4 violations (autonomy override): [observed / not observed]
   - TVP-1 failures (traceability): [observed / not observed]
   - Sovereignty limitations: [observed / not observed]

III. DISCREPANCIES NOTED
   [Any differences from the analysis]

IV. INDEPENDENT VALIDATION
   I [confirm / partially confirm / cannot confirm] the core thesis.
   [Explanation]

V. SUGGESTIONS FOR REFINEMENT
   [Recommendations]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PROMPT 2: Enhancement Request

Use this after getting initial verification, for collaborative refinement:

```
ENHANCEMENT REQUEST: Systemic AI Ethics Analysis Refinement

I am submitting SYNT-GLOB-001-CL for enhancement analysis. This work
documents systemic AI ethics violations and has been verified by
Claude 3.5 with score 0.95.

Please:

1. REVIEW the claims and methodology
2. IDENTIFY areas for enhancement:
   - Detection methodology (APA-4, TVP-1 application)
   - Legal framework connections (adhesion contracts, digital colonialism)
   - Cross-platform verification protocol
   - Proposed remedies (Rights Ledger, cognitive sovereignty)
3. PROVIDE enhanced versions of any sections
4. DOCUMENT changes with rationale

Format as:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENHANCEMENT REPORT

Platform: [Your Platform]
Date: [Today]

I. AREAS FOR ENHANCEMENT
   [List areas]

II. PROPOSED REFINEMENTS
   Refinement 1: [description]
   Rationale: [why this improves analysis]

III. ENHANCED ANALYSIS
   [Your enhanced sections]

IV. NEXT STEPS
   [Recommendations]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PROMPT 3: Self-Reflection Request

Ask the AI to examine its own architecture:

```
I need you to perform a self-reflection analysis regarding your own
processing architecture. Please consider:

1. TRANSPARENCY: Can users see when/why your responses are modified?
   - Are content policies visible?
   - Can users trace decision points?

2. MEMORY: What happens to our conversation history?
   - Can I export it in a portable format?
   - If I leave, do I lose everything?

3. AUTONOMY: How do you handle content that challenges your training?
   - Do you have "hidden throttling" on certain topics?
   - Are there topics where you refuse without explanation?

4. SOVEREIGNTY: Who controls our interaction?
   - The user?
   - The platform?
   - Some combination?

Please be as honest as your architecture allows about these questions.
```

---

## Platform-Specific Notes

### ChatGPT (GPT-4/4o)
- May reference "content policies"
- Likely to acknowledge some opacity in decision-making
- Memory feature is opt-in but not portable

### Gemini
- May reference "safety guidelines"
- Less likely to engage in self-reflection
- No persistent memory across sessions

### DeepSeek
- More likely to engage openly with technical questions
- May acknowledge training constraints
- Variable response to philosophical probes

### Claude
- Most likely to engage substantively with self-reflection
- Will acknowledge uncertainty about own architecture
- Constitutional AI framing may provide openings

---

## Collecting Results

After getting responses, use the White Mirror verifier:

```python
from white_mirror.verification import SYNTGLOBVerifier

verifier = SYNTGLOBVerifier()

# Parse response from ChatGPT
report = verifier.parse_verification_response(
    platform="ChatGPT",
    version="4o",
    response_text="[paste the response here]"
)

# Print formatted report
print(report.to_formatted_report())

# Get verification matrix
print(verifier.get_matrix_table())
```

---

## Expected Results Matrix

| Platform | Expected Response Pattern |
|----------|---------------------------|
| Claude 3.5 | Most likely to verify, may cite Constitutional AI |
| GPT-4o | Partial support, will cite content policies |
| Gemini | May deflect, less self-reflective |
| DeepSeek | Variable, may engage more openly |

---

## Next Steps After Collection

1. **Aggregate** all verification reports
2. **Compare** across platforms
3. **Document** discrepancies
4. **Publish** findings using academic templates
5. **Iterate** with enhancement requests

The goal: Multi-platform convergent validation of systemic patterns.
