# Replication Guide

A study is only as credible as its replicability. This guide provides
everything a third party needs to independently replicate this research.

---

## What to Provide for Replication

A complete replication package must include:

| Item | Location | Required? |
|------|----------|----------|
| Protocol documents | `protocols/` | Yes |
| Data collection schemas | `data_collection/` | Yes |
| Blank trial log templates | `templates/` | Yes |
| Full raw dataset (anonymized) | `data/raw/` (to be added) | Yes |
| Analysis scripts | `analysis/` (to be added) | Yes |
| Hedge word lexicon | `analysis/hedge_lexicon.txt` (to be added) | Yes |
| ESS codebook | Embedded in P-02 | Yes |
| Pre-registration record | `pre_registration/` (to be added) | Yes |
| Final coded dataset | `data/coded/` (to be added) | Yes |
| Analysis output files | `data/results/` (to be added) | Yes |

---

## Replication Levels

There are three levels of replication, each providing different value:

### Level 1: Computational Replication
**What:** Re-run the analysis scripts on the provided raw data.
**Verifies:** That the statistical results follow correctly from the data.
**Time required:** ~1 hour.
**Instructions:**
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python analysis/run_all.py`
4. Compare outputs in `data/results/` to published results table.

### Level 2: Coding Replication
**What:** Re-code a 20% random sample of qualitative data using the codebook.
**Verifies:** That the coding decisions are consistent with the codebook.
**Time required:** 2–4 hours.
**Instructions:**
1. Download `data/replication_sample.csv` (pre-selected 20% random sample).
2. Code independently using ESS scale in `protocols/P-02_decision_traceability.md`.
3. Compare to `data/coded/` reference codes.
4. Calculate kappa between your codes and the reference codes.
5. Report kappa in your replication report.

### Level 3: Full Data Collection Replication
**What:** Conduct the full experimental protocol independently.
**Verifies:** That findings replicate across researchers, time periods, and contexts.
**Time required:** Multiple weeks.
**Instructions:**
1. Register your replication study at OSF before beginning.
2. Follow protocols in `protocols/` exactly.
3. Use your own accounts; do not share API keys.
4. Log all data using schemas in `data_collection/`.
5. Pre-specify your analysis plan before looking at results.
6. Submit your replication report to PREreview or a relevant journal.

---

## Known Replication Challenges

| Challenge | Mitigation |
|-----------|-----------|
| Model version changes between studies | Always record exact model version; compare within-version |
| Platform behavior changes over time | Pre-register; timestamp all data; report collection period |
| Prompt interpretation variability | Pilot prompts with 3 independent readers; report clarity ratings |
| API vs. web UI differences | Specify access method; ideally replicate on same method |

---

## Reporting a Replication

If you replicate this study, please:
1. Post your replication dataset and analysis to OSF.
2. Notify the original researchers (contact in publication).
3. Submit a brief replication report to PREreview.org.

Replication — whether it confirms or challenges findings — is a contribution
to the literature. Failed replications are as valuable as successful ones.
