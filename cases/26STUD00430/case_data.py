"""
CASE 26STUD00430 — Gateways Apartment LP v. Kyle Theus
Structured case data for Multi-AI Framework integration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import date

CASE_ID = "26STUD00430"
CASE_NAME = "Gateways Apartment LP v. Kyle Theus"
COURT = "Los Angeles Superior Court — Stanley Mosk Courthouse"
GOAL = "Stipulated dismissal, no eviction record, voucher intact, $2,667 returned"

# ──────────────────────────────────────────────
# CHRONOLOGY (Layer 0 — raw factual record)
# ──────────────────────────────────────────────
CHRONOLOGY = [
    {
        "date": "2026-01-28",
        "time": None,
        "event": "Cooperative meeting with management; Abandonment Response delivered",
        "method": "In-person + Mailsuite tracking",
        "witness_record": "Mailsuite open/read receipt",
        "exhibit": "EX-01",
    },
    {
        "date": "2026-02-10",
        "time": None,
        "event": "Kyle Theus filed written Answer (UD-105)",
        "method": "Court filing",
        "witness_record": "Court file stamp",
        "exhibit": "EX-02",
    },
    {
        "date": "2026-03-13",
        "time": "~10:00 AM",
        "event": "Default judgment entered in defendant's absence",
        "method": "Court record",
        "witness_record": "Judgment document",
        "exhibit": "EX-03",
    },
    {
        "date": "2026-03-13",
        "time": "~4:30 PM",
        "event": "Ashley Ross accepted $2,667.00 (four postal money orders); issued written receipt; no non-waiver letter issued",
        "method": "In-person payment, written receipt",
        "witness_record": "Signed receipt by Ashley Ross",
        "exhibit": "EX-04",
    },
    {
        "date": "2026-03-16",
        "time": None,
        "event": "Martha Acosta called from blocked number; stated 'we already won judgment, we want possession, not the money'",
        "method": "Phone call (recorded)",
        "witness_record": "Audio recording",
        "exhibit": "EX-05",
    },
    {
        "date": "2026-05-09",
        "time": None,
        "event": "Notice to Vacate posted; execution date field left blank (LASD File No. 2026030008)",
        "method": "LASD posting",
        "witness_record": "Photograph of posted notice",
        "exhibit": "EX-06",
    },
    {
        "date": "2026-05-22",
        "time": None,
        "event": "LASD officer Raul acknowledged blank execution date but stated enforcement would proceed",
        "method": "In-person acknowledgment (recorded)",
        "witness_record": "Audio recording",
        "exhibit": "EX-07",
    },
]

# ──────────────────────────────────────────────
# DEFECT TIERS
# ──────────────────────────────────────────────
TIER_1_DEFECTS = [
    {
        "id": "T1-A",
        "constraint_ref": "T-12 / Constraint 7",
        "label": "Blank Execution Date on Notice to Vacate",
        "statute": "CCP § 712.020(a)",
        "fact_statement": (
            "The Notice to Vacate served on May 9, 2026 (LASD Levying Officer File No. 2026030008) "
            "contains a blank field where the execution date is required by CCP § 712.020(a)."
        ),
        "relief": "Motion to Quash Writ + Stay of Execution",
        "plaintiffs_best_response": (
            "The blank date is a clerical error that does not prejudice defendant because LASD "
            "served the notice in person and the five-day period ran from actual service date."
        ),
        "counter": (
            "LASD officer acknowledged the defect on record. CCP § 712.020 uses 'shall' — mandatory. "
            "Five-day calculation depends on the date. Kyle was confirmed absent in Tulare when posted "
            "— no personal service to anchor the timeline."
        ),
        "exhibit_refs": ["EX-06", "EX-07"],
        "dispositive": True,
    },
    {
        "id": "T1-B",
        "constraint_ref": "T-10 / Constraint 5",
        "label": "Payment Accepted Same Day as Judgment",
        "statute": "Civil Code § 1945",
        "fact_statement": (
            "Judgment was entered at approximately 10:00 AM on March 13, 2026. "
            "At approximately 4:30 PM the same day, Ashley Ross, property manager, accepted "
            "four postal money orders totaling $2,667.00 and issued a written receipt; "
            "no non-waiver letter was issued before or after this acceptance."
        ),
        "relief": "Motion to Set Aside Judgment (post-judgment act revived tenancy)",
        "plaintiffs_best_response": (
            "Acceptance of payment did not constitute waiver because the funds were never deposited "
            "and management immediately instructed non-deposit under supervisor direction."
        ),
        "counter": (
            "Civil Code § 1945 does not require deposit — it requires acceptance. "
            "Ashley Ross accepted the funds, issued a written receipt, and retained them 70+ days. "
            "Rejection of deposit is evidence of intentional withholding. Under EDC Associates, "
            "absence of a non-waiver letter strengthens the presumption."
        ),
        "exhibit_refs": ["EX-03", "EX-04"],
        "dispositive": True,
    },
    {
        "id": "T1-C",
        "constraint_ref": "T-7 / Constraint 15",
        "label": "Default Entered While Defendant Was Actively Defending",
        "statute": "CCP § 473(b)",
        "fact_statement": (
            "Kyle Theus filed a written Answer on February 10, 2026. "
            "The default judgment was entered on March 13, 2026. "
            "Between January 28, 2026 and March 13, 2026, Kyle Theus received no written or verbal "
            "notice of the trial date."
        ),
        "relief": "Motion to Set Aside Default Judgment (excusable neglect)",
        "plaintiffs_best_response": (
            "Court records show notice was properly mailed per CCP § 1013 to defendant's address of record."
        ),
        "counter": (
            "Kyle's documented continuous engagement through January 28 evidences he was monitoring "
            "communications. The 44-day silence — while management maintained a facade of cooperation "
            "— constitutes excusable neglect. If notice was mailed, produce it; if mailed to an "
            "incorrect or unmonitored address, that itself is the error."
        ),
        "exhibit_refs": ["EX-01", "EX-02", "EX-03"],
        "dispositive": True,
    },
]

TIER_2_DEFECTS = [
    {
        "id": "T2-A",
        "label": "Verification Predates Complaint by 364 Days",
        "statute": "CCP § 473(d)",
        "relief": "Motion to Set Aside as Void Judgment",
        "note": "Attacks foundational document integrity",
    },
    {
        "id": "T2-B",
        "label": "Lease Never Admitted Into Evidence",
        "statute": "Evidence rules",
        "relief": "Undermines evidentiary basis for judgment",
        "note": "Supporting argument, not standalone",
    },
    {
        "id": "T2-C",
        "label": "$528 Demand vs. $2,384 Stated Balance Discrepancy",
        "statute": "CCP § 1161(2)",
        "relief": "Notice defect argument",
        "note": "Constraint 8 — demonstrates notice defect",
    },
    {
        "id": "T2-D",
        "label": "Dual Service Method Ambiguity",
        "statute": "CCP § 1162",
        "relief": "Jurisdictional seam argument",
        "note": "Constraint 11",
    },
    {
        "id": "T2-E",
        "label": "Wrong Deadline in Complaint",
        "statute": "CCP § 1161",
        "relief": "Motion to dismiss underlying action",
        "note": "T-1 — potential dismissal vehicle",
    },
]

TIER_3_LEVERS = [
    {
        "id": "T3-A",
        "label": "HUD Region 9 Complaint",
        "basis": "24 CFR § 5.2005 (retaliation) + Section 8 just-cause requirements",
        "trigger": "Martha's recorded admission + Section 8 voucher",
        "note": "Regulatory pressure — not a court filing",
    },
    {
        "id": "T3-B",
        "label": "HACLA Complaint",
        "basis": "HAP contract compliance obligations",
        "trigger": "HACLA has direct relationship with property through HAP contract",
        "note": "Triggers inspection + HAP payment review",
    },
    {
        "id": "T3-C",
        "label": "Martha's Recorded Admission",
        "basis": "Civil Code § 1942.5 (retaliation)",
        "trigger": "'We want possession, not money' — within 180 days of protected activity",
        "note": "Affirmative defense in Answer",
    },
]

# ──────────────────────────────────────────────
# LEGAL THEORY MAP (Statute → Fact → Relief)
# ──────────────────────────────────────────────
LEGAL_THEORY_MAP = [
    {
        "statute": "CCP § 712.020(a)",
        "documented_fact": "Blank execution date on Notice to Vacate",
        "relief": "Motion to Quash Writ + Stay of Execution",
    },
    {
        "statute": "Civil Code § 1945",
        "documented_fact": "$2,667 accepted March 13 with signed receipt; no non-waiver letter; funds retained 70+ days",
        "relief": "Motion to Set Aside Judgment (post-judgment act revived tenancy)",
    },
    {
        "statute": "CCP § 473(b)",
        "documented_fact": "Answer filed Feb. 10; no trial notice received; 44-day facade of cooperation documented",
        "relief": "Motion to Set Aside Default Judgment (excusable neglect)",
    },
    {
        "statute": "CCP § 473(d)",
        "documented_fact": "Verification predates complaint 364 days; lease never admitted",
        "relief": "Motion to Set Aside as Void Judgment",
    },
    {
        "statute": "Civil Code § 1942.5",
        "documented_fact": "Martha: 'paid late, don't want that relationship'; eviction within 180 days of protected activity",
        "relief": "Affirmative defense (retaliation) in Answer",
    },
    {
        "statute": "24 CFR § 982.310",
        "documented_fact": "Section 8 tenancy; no PHA notice copy confirmed",
        "relief": "HUD / HACLA complaint (pressure lever, not court filing)",
    },
]

# ──────────────────────────────────────────────
# FILING SEQUENCE
# ──────────────────────────────────────────────
FILING_SEQUENCE_PRE_LOCKOUT = [
    {
        "order": 1,
        "urgency": "IMMEDIATE",
        "filing": "Ex Parte Application for Stay of Execution",
        "authority": "CCP § 1176 + CCP § 128(a)",
        "lead_argument": "Blank execution date = writ facially deficient",
        "supporting": "CC § 1945 post-judgment payment acceptance",
        "location": "Stanley Mosk, Room 102, before 8:30 AM",
    },
    {
        "order": 2,
        "urgency": "SAME DAY / NEXT DAY",
        "filing": "Motion to Set Aside (CCP §§ 473(b), 473(d))",
        "authority": "CCP §§ 473(b), 473(d)",
        "lead_argument": "Excusable neglect + void judgment elements",
        "supporting": "Attach Proposed Answer (UD-105) with all affirmative defenses",
        "location": "Stanley Mosk",
    },
]

FILING_SEQUENCE_POST_LOCKOUT = [
    {
        "order": 1,
        "urgency": "EMERGENCY",
        "filing": "Motion to Restore Possession",
        "authority": "CCP § 1174.3",
        "condition": "Available if CP10.5 was not properly served",
    },
    {
        "order": 2,
        "urgency": "PARALLEL",
        "filing": "Motion to Set Aside",
        "authority": "CCP § 473(b)",
    },
    {
        "order": 3,
        "urgency": "PARALLEL",
        "filing": "Application to Stay Enforcement Pending Appeal",
        "authority": "CCP § 918",
    },
]

# ──────────────────────────────────────────────
# PRESSURE LEVERS (ordered by deployment)
# ──────────────────────────────────────────────
PRESSURE_LEVERS = [
    {
        "lever": 1,
        "label": "Interrogatory Letter to Martha Acosta",
        "status": "PULLED",
        "note": "Primary value now is the documented request. Non-response noted in declaration.",
    },
    {
        "lever": 2,
        "label": "Court Filings (Motion to Quash + Motion to Set Aside)",
        "status": "PENDING",
        "note": "Every filing creates compliance cost for Kimball, Tirey & St. John.",
    },
    {
        "lever": 3,
        "label": "HUD Region 9 Complaint",
        "status": "PENDING",
        "note": "SROHC as HUD-funded nonprofit has compliance obligations a private landlord does not.",
    },
    {
        "lever": 4,
        "label": "HACLA Complaint",
        "status": "PENDING",
        "note": "Triggers inspection obligation and HAP payment review.",
    },
    {
        "lever": 5,
        "label": "Tia Boatman Patterson / Network Contact to Anita U. Nelson (SROHC CEO)",
        "status": "RESERVE",
        "note": "Hold in reserve. Deploy only if Levers 1-4 produce no movement.",
    },
]

# ──────────────────────────────────────────────
# SETTLEMENT PACKAGE
# ──────────────────────────────────────────────
SETTLEMENT_OFFER = {
    "frame": "Both parties have an exit that costs less than continued litigation.",
    "kyle_receives": [
        "Stipulated dismissal of the UD action",
        "No adverse reporting to credit bureaus",
        "No eviction record",
        "Return of $2,667.00",
        "HACLA voucher portable and intact",
    ],
    "plaintiff_receives": [
        "No HUD exposure",
        "No HACLA inspection",
        "No regulatory complaint",
        "No ongoing attorney's fees",
        "Unit available",
    ],
}

# ──────────────────────────────────────────────
# MASTER SYNTHESIS
# ──────────────────────────────────────────────
MASTER_SYNTHESIS = {
    "micro": (
        "On March 13, 2026, at approximately 10:00 AM, a default judgment was entered against "
        "Kyle Theus in his absence, despite his having filed an Answer and maintained active "
        "documented communication with management through January 28, having received no notice "
        "of the trial date during a 44-day period in which management maintained a facade of "
        "cooperation while secretly prosecuting the eviction. At approximately 4:30 PM the same "
        "day, Ashley Ross accepted $2,667.00 in postal money orders and issued a written receipt. "
        "No non-waiver letter was issued. Funds were retained for 70+ days. On May 9, 2026, a "
        "Notice to Vacate was posted with the execution date field left blank."
    ),
    "pattern": (
        "The documents reveal a sequence — wrong deadline, underclaimed damages, delayed service, "
        "held proof of service, coordinated default, minimal trial notice, judgment before payment, "
        "blank-dated writ — each step reducing the defendant's ability to respond, each individually "
        "explicable as error, collectively consistent with strategic manipulation of procedure."
    ),
    "legal_theory": (
        "The judgment may be set aside under CCP § 473(b) (excusable neglect) and § 473(d) (void "
        "judgment elements); the writ may be quashed under CCP § 712.020 (blank date, mandatory "
        "content); and the tenancy may be argued to have been legally renewed under Civil Code § 1945 "
        "by the post-judgment payment acceptance without a non-waiver letter."
    ),
    "macro": (
        "A stipulated dismissal resolves all of this — cleanly, quickly, without trial, without "
        "appeal, without HUD exposure, without HACLA inspection, without a published eviction "
        "record. That is the destination. Every filing, every letter, every lever exists to make "
        "that the rational choice for the other side."
    ),
}


def get_case_data() -> Dict[str, Any]:
    """Return complete case data dict for use with MissionOrchestrator."""
    return {
        "case_id": CASE_ID,
        "case_name": CASE_NAME,
        "court": COURT,
        "goal": GOAL,
        "chronology": CHRONOLOGY,
        "tier1_defects": TIER_1_DEFECTS,
        "tier2_defects": TIER_2_DEFECTS,
        "tier3_levers": TIER_3_LEVERS,
        "legal_theory_map": LEGAL_THEORY_MAP,
        "filing_sequence_pre_lockout": FILING_SEQUENCE_PRE_LOCKOUT,
        "filing_sequence_post_lockout": FILING_SEQUENCE_POST_LOCKOUT,
        "pressure_levers": PRESSURE_LEVERS,
        "settlement_offer": SETTLEMENT_OFFER,
        "master_synthesis": MASTER_SYNTHESIS,
    }
