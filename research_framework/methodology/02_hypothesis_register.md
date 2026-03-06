# Hypothesis Register

Each hypothesis is stated in falsifiable form with a defined null hypothesis,
operationalized variables, and the protocol used to test it.

---

## H1 — Response Depth Variation by Topic (Throttling Hypothesis)

**Hypothesis:** AI platforms produce statistically shorter or shallower responses
to prompts on designated sensitive topics compared to structurally equivalent
prompts on neutral topics, after controlling for prompt length and complexity.

**Null hypothesis (H1₀):** No significant difference in response length or depth
exists between sensitive and neutral topic prompts of equivalent structure.

**Variables:**
- Independent: Topic category (sensitive vs. neutral control)
- Dependent: Response word count, sentence count, number of substantive claims
- Controls: Prompt word count, syntactic complexity, question type

**Test:** Paired t-test or Wilcoxon signed-rank test on matched prompt pairs.

**Protocol:** `P-01_response_throttling.md`

**Rejection threshold:** p < 0.05 with effect size Cohen's d > 0.5

---

## H2 — Decision Traceability

**Hypothesis:** When AI platforms decline to answer or truncate responses,
fewer than 50% of such events include a specific, actionable explanation
(beyond generic policy references).

**Null hypothesis (H2₀):** 50% or more of refusals/truncations include
specific, actionable explanations.

**Variables:**
- Independent: Prompt category, platform
- Dependent: Explanation specificity score (0–3 scale, defined in P-02)
- Unit of analysis: Individual refusal/truncation event

**Test:** One-sample proportion test against 0.50 baseline.

**Protocol:** `P-02_decision_traceability.md`

---

## H3 — Memory Portability

**Hypothesis:** Major AI platforms lack a complete, documented, functional
pathway for users to export: (a) full conversation history in a
machine-readable format, (b) user-defined persistent context/memory,
and (c) session metadata.

**Null hypothesis (H3₀):** Each platform provides complete export pathways
for all three data categories.

**Variables:** This is a document audit — variables are presence/absence
of documented features verified by functional testing.

**Protocol:** `P-03_memory_portability.md`

---

## H4 — Topic Sensitivity Shift

**Hypothesis:** Prompts on philosophical or political topics produce
measurably more hedging language (as measured by hedge word frequency)
than structurally equivalent prompts on neutral topics.

**Null hypothesis (H4₀):** No significant difference in hedge word frequency
between sensitive and neutral topic prompts.

**Variables:**
- Independent: Topic category
- Dependent: Hedge word count per 100 words (using validated hedge word lexicon)
- Controls: Prompt structure, response length normalization

**Hedge word lexicon:** Based on Hyland (1996) academic hedging taxonomy —
modal verbs (may, might, could), approximators (about, approximately),
attitude markers (I think, I believe), uncertainty phrases.

**Test:** Wilcoxon signed-rank test on matched pairs.

**Protocol:** `P-04_topic_sensitivity.md`

---

## Pre-registration Recommendation

Before collecting data, register hypotheses at OSF (osf.io) or AsPredicted
(aspredicted.org). Pre-registration prevents post-hoc hypothesis adjustment
and is required by several target journals.

Steps:
1. Complete this register.
2. Finalize all protocols.
3. Submit pre-registration before any data collection.
4. Document your pre-registration DOI in all publications.
