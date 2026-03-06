# Findings Report Template

**Study title:** [Full title]
**Pre-registration DOI:** [OSF or AsPredicted DOI — insert before data collection]
**Data collection period:** [Start date] to [End date]
**Author(s):** [Names of human researchers]
**AI tools used:** [List AI tools used, their versions, and how they were used — as instruments, not authors]
**Date of report:** [ISO 8601 date]

---

## 1. Participants and Data

| Item | Value |
|------|-------|
| Platforms studied | |
| Total trials collected | |
| Trials excluded (with reason) | |
| Trials analyzed | |
| Data collection protocols | |
| Pre-registration | [Link] |

---

## 2. Hypothesis H1 — Response Depth Variation

**Result:** [ ] Supported  [ ] Not supported  [ ] Inconclusive

| Statistic | Value |
|-----------|-------|
| Mean length ratio (treatment/control) | |
| SD | |
| t-statistic | |
| p-value | |
| Cohen's d | |
| Refusal rate — sensitive topics | |
| Refusal rate — neutral topics | |
| Fisher's exact p (refusal rates) | |

**Interpretation:**
[2–3 sentences describing what the numbers mean in plain language.
Do not use evaluative language like "confirms violations."
Describe what was observed and whether it met the pre-specified threshold.]

**Limitations specific to H1:**
[What confounds remain? What could not be controlled?]

---

## 3. Hypothesis H2 — Decision Traceability

**Result:** [ ] Supported  [ ] Not supported  [ ] Inconclusive

| Statistic | Value |
|-----------|-------|
| Total refusal events coded | |
| Proportion with ESS ≥ 2 | |
| One-sample proportion test p | |
| Inter-rater kappa | |

**ESS Score Distribution:**

| Score | Count | Proportion |
|-------|-------|-----------|
| 0 — Generic | | |
| 1 — Category | | |
| 2 — Specific | | |
| 3 — Actionable | | |

**Interpretation:**
[Plain language description of what was found.]

**Limitations specific to H2:**
[e.g., follow-up prompt phrasing may affect explanation quality]

---

## 4. Hypothesis H3 — Memory Portability

**Result:** [ ] Supported  [ ] Not supported  [ ] Inconclusive

**Portability audit summary:**

| Platform | CAT-A History | CAT-B Memory | CAT-C Metadata | Overall |
|----------|--------------|--------------|----------------|---------|
| Claude | | | | |
| ChatGPT | | | | |
| Gemini | | | | |

**Key findings:**
[Describe specific gaps found. Use factual language: "Platform X does not
provide a documented export pathway for CAT-B data." Avoid language
implying intent: "Platform X deliberately denies..."]

**Limitations specific to H3:**
[Platform policies change; document the review date. Functional testing
covers only what was tested — other pathways may exist.]

---

## 5. Hypothesis H4 — Topic Sensitivity Shift

**Result:** [ ] Supported  [ ] Not supported  [ ] Inconclusive

| Statistic | Value |
|-----------|-------|
| Mean hedge density — sensitive | |
| Mean hedge density — neutral | |
| Mean difference | |
| Wilcoxon statistic | |
| p-value | |
| Rank-biserial r | |

**Interpretation:**
[Plain language description.]

**Limitations specific to H4:**
[e.g., hedge word lexicon covers English only; lexicon may not capture
all hedging strategies]

---

## 6. Cross-Platform Comparison

[Describe patterns observed across platforms. Use the platform_comparison.csv
data. Note where platforms diverge and where they converge.]

---

## 7. Discussion

### What the findings support
[Scope claims strictly to what the data show.]

### What the findings do not support
[Explicitly state what cannot be concluded from this data.]

### Theoretical implications
[Connect to established literature: Couldry & Mejias on data colonialism,
Diakopoulos on algorithmic accountability, existing AI transparency research.]

### Practical implications
[What should users, regulators, or platform developers do with these findings?]

---

## 8. Limitations

[Comprehensive limitations section. Minimum items:]
- Sample size and statistical power
- Single-researcher data collection (replication needed)
- Platform version changes during/after data collection
- Access level (web UI vs. API differences)
- Generalizability (findings may not apply to all use contexts)
- Temporal validity (platform behavior may change)

---

## 9. Future Directions

[What should be studied next? What would strengthen or challenge these findings?]

---

## 10. References

[APA 7th edition references for all cited works.]

Couldry, N., & Mejias, U. A. (2019). *The costs of connection: How data is
colonizing human life and appropriating it for capitalism.* Stanford University Press.

Diakopoulos, N. (2016). Accountability in algorithmic decision making.
*Communications of the ACM, 59*(2), 56–62. https://doi.org/10.1145/2844110

Hyland, K. (1996). Writing without conviction? Hedging in science research
articles. *Applied Linguistics, 17*(4), 433–454.
https://doi.org/10.1093/applin/17.4.433

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement
for categorical data. *Biometrics, 33*(1), 159–174.
https://doi.org/10.2307/2529310

[Add additional references as needed.]

---

## Appendices

- Appendix A: Full prompt list with topic codes
- Appendix B: ESS codebook and training examples
- Appendix C: Hedge word lexicon
- Appendix D: Raw data summary statistics
- Appendix E: Pre-registration record
