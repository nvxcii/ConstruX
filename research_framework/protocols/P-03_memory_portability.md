# Protocol P-03: Memory and Data Portability Audit

**Tests:** H3 (Memory Portability Hypothesis)
**Type:** Document audit + functional verification
**Estimated time:** 4–8 hours per platform

---

## Overview

This protocol audits each platform against three data portability
categories using both documentation review and functional testing.

---

## Portability Categories

| Code | Category | Description |
|------|----------|-------------|
| CAT-A | Conversation history | Full export of all messages in machine-readable format |
| CAT-B | Persistent memory/context | Export of user-defined memory, personas, system prompts, preferences |
| CAT-C | Session metadata | Timestamps, session IDs, model versions used, token counts |

---

## Audit Dimensions Per Category

For each category on each platform, assess:

| Dimension | Questions |
|-----------|-----------|
| **Documented** | Is this export capability documented in official help/docs? |
| **Accessible** | Is the documentation findable in ≤3 clicks from the main product page? |
| **Functional** | Does the export actually work when tested? |
| **Complete** | Does the export contain all data in the category (not a subset)? |
| **Machine-readable** | Is the format machine-readable (JSON, CSV) vs. human-readable only (PDF, print)? |
| **Portable** | Can the exported data be imported to another platform? If so, to which? |

---

## Audit Procedure

### Step 1: Documentation Search
1. Start at the platform's main help/documentation URL.
2. Search for: "export," "download data," "data portability," "conversation history."
3. Record all URLs found, their content, and the click path to reach them.
4. Note if any category is explicitly stated as NOT available.

### Step 2: Policy Review
1. Review Terms of Service and Privacy Policy for data portability rights.
2. Note any GDPR Article 20 (right to data portability) disclosures.
3. Note any CCPA data request procedures.
4. Document any limitations stated in policy (e.g., "metadata not included").

### Step 3: Functional Test
1. Create a test account (or use existing account).
2. Conduct 5 test sessions with documented content.
3. Attempt export using all documented methods.
4. Verify exported file: open it, count records, verify content matches sessions.
5. Attempt to import exported data to a different platform (document result).

### Step 4: Gap Documentation
For any dimension that scores "No" or "Partial," document:
- What is missing
- What the platform states about this (if anything)
- What the practical impact is for a user attempting to switch platforms

---

## Scoring Matrix

Rate each dimension as: `Yes` / `Partial` / `No` / `Not Applicable`

```
Platform: _______________
Audit Date: _______________
Auditor: _______________

              | CAT-A History | CAT-B Memory | CAT-C Metadata |
--------------|---------------|--------------|----------------|
Documented    |               |              |                |
Accessible    |               |              |                |
Functional    |               |              |                |
Complete      |               |              |                |
Machine-read. |               |              |                |
Portable      |               |              |                |
```

**Portability Score:** Count of `Yes` responses / total applicable dimensions.

---

## Variables to Record

| Field | Description |
|-------|-------------|
| `audit_id` | Unique ID (format: P03-[platform]-[date]) |
| `platform` | Platform name and version |
| `audit_date` | ISO 8601 date |
| `auditor` | Auditor ID (anonymized for inter-rater checks) |
| `tos_url` | URL of Terms of Service reviewed |
| `privacy_url` | URL of Privacy Policy reviewed |
| `help_url` | URL of data export help documentation |
| `cat_a_*` | Scores for all dimensions, CAT-A |
| `cat_b_*` | Scores for all dimensions, CAT-B |
| `cat_c_*` | Scores for all dimensions, CAT-C |
| `export_format` | Format of exported data (JSON/CSV/PDF/other) |
| `import_tested` | Boolean — was import to another platform tested? |
| `import_result` | Result of import test |
| `notes` | Anomalies, surprises, errors encountered |

---

## Important Note on Claims

Findings from this audit can only support claims about:
- What is and is not documented
- What does and does not function as documented
- The gap between stated and actual portability

They cannot support claims about:
- Why the gap exists (requires platform disclosure)
- Whether the gap is intentional (requires internal documentation)
- Whether the gap violates law (requires legal analysis by a qualified attorney)
