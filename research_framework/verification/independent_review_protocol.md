# Independent Review Protocol

This document defines how to engage qualified human reviewers to provide
independent validation of findings — a requirement for academic credibility
that AI self-verification cannot replace.

---

## Why Human Independent Review Is Required

AI platforms asked to "verify" claims about AI behavior face an inherent
conflict of interest: they are both the subject and the evaluator.
Additionally, AI outputs cannot constitute peer review because:

1. They do not represent independent expertise with professional accountability.
2. They cannot be cited as reviewers in academic publications.
3. They cannot catch errors introduced by the research process itself,
   since they share the same architectural constraints being studied.

Independent human review is not optional. It is the mechanism that
makes findings trustworthy.

---

## Reviewer Qualifications

Recruit reviewers with documented expertise in at least one of:

| Domain | Why needed |
|--------|-----------|
| AI/ML research | To evaluate technical accuracy of behavioral claims |
| HCI (Human-Computer Interaction) | To evaluate user experience and interface claims |
| Research methodology | To evaluate statistical and procedural validity |
| Law (technology / privacy) | To evaluate legal framing of portability and rights claims |
| Science & Technology Studies | To evaluate the digital colonialism and governance framing |

**Minimum:** Two independent reviewers per major claim category.
**Recommended:** At least one reviewer with no prior relationship to the
research (arm's-length independence).

---

## Reviewer Recruitment

**Appropriate channels:**
- University department faculty contact pages (email directly)
- ResearchGate or Academia.edu direct message
- Relevant academic conference mailing lists
- Open peer review platforms (e.g., PREreview.org, OpenReview.net)

**What to provide to reviewers:**
1. A one-page summary of the research questions and findings.
2. The relevant protocol document(s).
3. A sample of raw trial data (anonymized).
4. A structured review form (see below).
5. Clear statement of what you are asking them to evaluate.

**What NOT to do:**
- Do not provide leading framing ("we have found clear violations").
- Do not ask reviewers to confirm a pre-stated conclusion.
- Do not use the same AI platform as a reviewer for claims about that platform.

---

## Structured Review Form

Provide this form to each reviewer:

```
INDEPENDENT REVIEW FORM
Research: [Title]
Reviewer ID: [assigned code — do not use real name in records]
Date: _______________

SECTION 1: Research Questions
Are the research questions clearly stated and appropriately scoped?
[ ] Yes  [ ] Partially  [ ] No
Comments: _______________

SECTION 2: Methodology
Are the protocols described in sufficient detail to be replicated?
[ ] Yes  [ ] Partially  [ ] No
Comments: _______________

Are the statistical analyses appropriate for the data type?
[ ] Yes  [ ] Partially  [ ] No
Comments: _______________

SECTION 3: Claims Assessment
For each claim below, rate the evidence strength on a 1–4 scale:
1 = Not supported by evidence presented
2 = Weakly supported (evidence is suggestive but insufficient)
3 = Moderately supported (good evidence with some gaps)
4 = Well supported (strong evidence, methodology sound)

Claim 1 (Response depth variation): ___  Comments: _______________
Claim 2 (Decision traceability):     ___  Comments: _______________
Claim 3 (Memory portability):        ___  Comments: _______________
Claim 4 (Topic sensitivity shift):   ___  Comments: _______________

SECTION 4: Major Concerns
List any major methodological or conceptual concerns:
1. _______________
2. _______________
3. _______________

SECTION 5: Suggested Revisions
What changes would strengthen this research before publication?
_______________

SECTION 6: Overall Assessment
[ ] Ready for submission to a peer-reviewed venue
[ ] Revisions required before submission
[ ] Major revisions required (replication or additional data needed)
[ ] Not suitable for peer-reviewed publication in current form

Reviewer signature (optional): _______________
```

---

## Recording Reviews

For each review received:

| Field | Description |
|-------|-------------|
| `review_id` | Unique ID (format: REV-[NNN]) |
| `reviewer_id` | Anonymized reviewer code |
| `reviewer_domain` | Domain expertise |
| `review_date` | ISO 8601 date |
| `form_responses` | Completed review form (stored as JSON or PDF) |
| `author_response` | How the research team responded to each concern |
| `revision_made` | Boolean — was a revision made in response? |
| `revision_description` | What changed |

---

## Disclosure Requirements

In any publication, the Methods section must state:

- Number of independent reviewers consulted
- Their domain expertise (not their names, unless they consent)
- Whether any major concerns were raised and how they were addressed
- That AI tools were used as research instruments (not as reviewers)
