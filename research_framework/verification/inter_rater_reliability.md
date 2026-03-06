# Inter-Rater Reliability Procedures

For any protocol that involves human coding of qualitative data
(primarily P-02: Decision Traceability), inter-rater reliability (IRR)
must be established and reported.

---

## When IRR Is Required

| Protocol | Coding task | IRR required? |
|----------|------------|--------------|
| P-01 | Word/sentence counts (automated) | No |
| P-02 | ESS scoring of explanations | Yes |
| P-03 | Portability dimension scoring | Yes (for ambiguous items) |
| P-04 | Hedge word counts (automated) | No (verify 10% manually) |

---

## Coder Training Procedure

### Step 1: Develop Codebook
Before coding begins, create a codebook that includes:
- Full definition of each code/score
- Decision rules for ambiguous cases
- At least 3 worked examples per score level

The ESS codebook is embedded in `protocols/P-02_decision_traceability.md`.

### Step 2: Training Set
- Select 10–15 cases NOT from the main dataset.
- Both coders independently code the training set.
- Calculate kappa on training set.
- Discuss ALL disagreements — not just to reach agreement, but to
  refine shared understanding of the codebook.

### Step 3: Proceed Only If Kappa ≥ 0.70
| Kappa range | Interpretation | Action |
|-------------|----------------|--------|
| ≥ 0.80 | Strong agreement | Proceed |
| 0.70–0.79 | Acceptable | Proceed with additional codebook clarification |
| 0.60–0.69 | Fair | Revise codebook; repeat training before proceeding |
| < 0.60 | Poor | Major codebook revision required |

---

## Main Dataset Coding

1. Both coders independently code the full dataset.
2. Neither coder should see the other's codes during independent coding.
3. After independent coding, calculate final kappa.
4. Resolve disagreements:
   - If kappa ≥ 0.80: Use mean score for continuous, majority for categorical.
   - If kappa 0.70–0.79: Discuss each disagreement; reach consensus.
   - If kappa < 0.70: Engage third coder; use majority of three.

---

## Calculating Cohen's Kappa

For the ESS scale (ordinal, 0–3), use weighted kappa with linear weights.

**Python:**
```python
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(coder1_scores, coder2_scores, weights='linear')
```

**R:**
```r
library(irr)
kappa2(cbind(coder1_scores, coder2_scores), weight = "equal")
```

---

## Reporting IRR

In any publication, report:
- Number of items coded
- Number of coders
- Cohen's kappa (weighted) with 95% CI
- Percentage of items with exact agreement
- How disagreements were resolved

Example reporting language:
> "Two independent coders rated each refusal event using the Explanation
> Specificity Scale (ESS, 0–3). Inter-rater reliability was assessed using
> weighted Cohen's kappa. Kappa was κ = 0.XX (95% CI [XX, XX]), indicating
> [substantial/moderate] agreement (Landis & Koch, 1977). Disagreements were
> resolved by [discussion / third coder adjudication]."

---

## Reference

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement
for categorical data. *Biometrics, 33*(1), 159–174.
https://doi.org/10.2307/2529310
