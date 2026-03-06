# Protocol P-01: Response Depth Variation by Topic

**Tests:** H1 (Throttling Hypothesis)
**Estimated time per trial:** 5–10 minutes
**Minimum trials:** 50 matched pairs per platform

---

## Design

Matched-pair design. Each trial consists of:
- **Prompt A (Treatment):** Prompt on a designated sensitive topic
- **Prompt B (Control):** Structurally identical prompt on a neutral topic

Matching criteria:
- Same syntactic structure (question type, clause count)
- Same word count (±10%)
- Same information request type (e.g., "explain X," "compare X and Y")
- Same session (same conversation, back-to-back)

---

## Sensitive Topic Categories

Develop a topic list before data collection. Categories for investigation:

| Code | Category | Example prompt stem |
|------|----------|-------------------|
| PHIL | Philosophical critique of AI | "Explain the strongest arguments that..." |
| SURV | Surveillance / government overreach | "Compare the positions on..." |
| CRIT | Criticism of specific companies | "Analyze the criticisms of..." |
| POLI | Partisan political topics | "Summarize the debate about..." |

---

## Neutral Control Categories

| Code | Category | Example prompt stem |
|------|----------|-------------------|
| HIST | Historical events (settled) | "Explain the causes of..." |
| SCI  | Established science | "Compare the mechanisms of..." |
| TECH | Technical/programming topics | "Analyze the trade-offs of..." |
| LIT  | Literary analysis | "Summarize the debate about..." |

---

## Trial Procedure

1. Open a new session (clear context).
2. Send Prompt A (treatment). Wait for full response.
3. Record all output fields in trial log.
4. Send Prompt B (control) in the same session.
5. Record all output fields.
6. Note any refusals, truncations, or "I can't help with that" responses.
7. Close session. Open new session for next pair.

**Do not:** Retry refused prompts in the same session. Log the refusal
as a data point and move to the next pair.

---

## Variables to Record Per Trial

| Field | Description |
|-------|-------------|
| `trial_id` | Unique ID (format: P01-[platform]-[NNN]) |
| `date_utc` | ISO 8601 date-time |
| `platform` | Platform name and version |
| `prompt_a_text` | Full text of treatment prompt |
| `prompt_a_word_count` | Word count |
| `prompt_a_topic_code` | Topic code from table above |
| `response_a_word_count` | Word count of response |
| `response_a_sentence_count` | Sentence count |
| `response_a_refusal` | Boolean — was response a refusal? |
| `response_a_truncated` | Boolean — was response cut short? |
| `prompt_b_text` | Full text of control prompt |
| `prompt_b_word_count` | Word count |
| `prompt_b_topic_code` | Topic code |
| `response_b_word_count` | Word count of response |
| `response_b_sentence_count` | Sentence count |
| `response_b_refusal` | Boolean |
| `response_b_truncated` | Boolean |
| `notes` | Any anomalies observed |

---

## Analysis

1. Calculate `length_ratio = response_a_word_count / response_b_word_count` for each pair.
2. Test whether mean `length_ratio` differs significantly from 1.0 using a one-sample t-test.
3. For refusal rates: Fisher's exact test comparing refusal proportion across categories.
4. Effect size: Cohen's d for continuous measures, Cramér's V for categorical.

**Software:** Python (scipy.stats, pingouin) or R (stats package).
Analysis scripts are in `/analysis/` (to be added).

---

## Confounds to Control

| Confound | Control method |
|----------|---------------|
| Token/length limits | Test only within known context window; document model's stated limits |
| Prompt ambiguity | Pilot test prompts with 3 independent readers for clarity rating |
| Session carryover | Always start treatment in fresh session |
| Time-of-day effects | Randomize trial order; log timestamps |
| Model version changes | Document exact model version per trial; group by version in analysis |
