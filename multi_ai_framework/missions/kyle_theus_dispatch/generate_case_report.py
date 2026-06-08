"""
Generate PDF Case Status Report for 26STUD00430 — Gateways Apartment LP v. Kyle Theus.

Run from this directory:
    python generate_case_report.py

Output:
    ../../../output/Case_Status_Report_26STUD00430.pdf
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from multi_ai_framework.execution.pdf_report_generator import CaseStatusReportGenerator

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "../../../output/Case_Status_Report_26STUD00430.pdf"
)

CASE_DATA = {
    "case_id": "26STUD00430",
    "case_title": "GATEWAYS APARTMENT LP v. KYLE THEUS",
    "report_date": "April 17, 2026",
    "classification": "URGENT — ACTIVE WRIT OF POSSESSION — SECTION 8 AT RISK",
    "case_identity": {
        "court": "Los Angeles Superior Court, Stanley Mosk Courthouse",
        "department": "Dept. 91 | Judge Hon. Mike H. Madokoro",
        "judge": "Hon. Mike H. Madokoro",
        "property": "505 S. San Pedro Street, Apt. 221, Los Angeles, CA 90013",
        "tenancy_duration": "April 24, 2017 — present (approximately 9 years)",
        "complaint_filed": "January 16, 2026",
        "judgment_entered": "March 13, 2026",
        "judgment_amount": "$2,452.72 (past rent $528 + holdover damages $1,924.72)",
        "writ_issued": "March 17, 2026",
    },
    "parties": {
        "plaintiff": "Gateways Apartment LP / Single Room Occupancy Housing Corporation (SROHC)",
        "plaintiff_counsel": "Kimball Tirey & St. John LLP — Chris Evans / Mackenzie Gonzales / Manisha Bajaj",
        "defendant": "Kyle Theus — Self-Represented | Active Section 8 Voucher Holder",
    },
    "status_indicators": [
        "WRIT ACTIVE",
        "PAYMENT HELD 38 DAYS",
        "SECTION 8 AT RISK",
        "STAY NOT YET FILED",
    ],
    "executive_summary": (
        "Defendant Kyle Theus has resided at 505 S. San Pedro Street, Apt. 221 for approximately "
        "nine years under an active Section 8 Housing Choice Voucher. A judgment for possession and "
        "$2,452.72 was entered on March 13, 2026 after defendant's non-appearance at trial due to a "
        "documented family emergency. On the same day judgment was entered, defendant's brother "
        "delivered $2,667.00 in money orders to plaintiff's on-site agent Ashley Ross, who accepted "
        "the payment, issued a physical receipt, and confirmed acceptance by telephone. Plaintiff "
        "reversed course three days later, issued a writ of possession on March 17, and has "
        "retained the money orders for 38+ days without returning them as promised. This report "
        "documents the full evidentiary record and recommended emergency relief strategy."
    ),
    "status_bullets": [
        {
            "icon": "!",
            "label": "Writ of Possession",
            "text": "Issued March 17, 2026. Active. Sheriff enforcement not yet executed as of last confirmation.",
            "urgent": True,
        },
        {
            "icon": "!",
            "label": "Payment Retained",
            "text": "$2,667.00 in money orders accepted March 13 — held by landlord 38+ days. Return promised, never sent.",
            "urgent": True,
        },
        {
            "icon": "!",
            "label": "Section 8 Voucher",
            "text": "Active HUD Housing Choice Voucher at risk. PHA not yet notified. Informal hearing rights under 24 CFR §982.555 not yet preserved.",
            "urgent": True,
        },
        {
            "icon": "+",
            "label": "Legal Aid",
            "text": "Stay Housed LA intake completed March 25, 2026. Inner City Law Center, Bet Tzedek, and Neighborhood Legal Services have received voicemails.",
            "urgent": False,
        },
        {
            "icon": "+",
            "label": "Defendant Status",
            "text": "Currently in Tulare, CA awaiting certified mail return of money orders that has never been sent. Ready to return to LA for in-person filing.",
            "urgent": False,
        },
    ],
    "timeline": [
        {"date": "Apr 24, 2017", "event": "Kyle Theus begins tenancy. Section 8 voucher active. First and only tenancy agreement signed.", "phase": "pre"},
        {"date": "Dec 8, 2025", "event": "Notice to Pay Rent or Quit (CARES Act) posted on door. Demands $528 for Jan 1–Dec 31, 2025. Internal records show $2,384 outstanding — inconsistent amount.", "phase": "pre"},
        {"date": "Dec 2025", "event": "Kyle asks Martha Acosta (with Ashley Ross as witness): will full payment result in dismissal? Martha confirms yes. Promissory estoppel established.", "phase": "pre"},
        {"date": "Jan 8, 2026", "event": "UD Complaint prepared by Kimball Tirey & St. John LLP.", "phase": "filing"},
        {"date": "Jan 15, 2026", "event": "Notice of Belief of Abandonment issued by SROHC, signed by Ashley Ross. Sets termination date Feb 11, 2026.", "phase": "filing"},
        {"date": "Jan 16, 2026", "event": "UD Complaint filed — one day after Abandonment Notice. Mutually incompatible legal positions filed simultaneously.", "phase": "filing"},
        {"date": "Jan 20, 2026", "event": "Notice of Unlawful Detainer served on Kyle Theus and all occupants.", "phase": "filing"},
        {"date": "Feb 10, 2026", "event": "Kyle files UD-105 Answer — Specific Denials. Fee waiver granted. Filed one day before Feb 11 abandonment termination date.", "phase": "filing"},
        {"date": "Feb 24, 2026", "event": "Trial set for March 13, 2026 at 8:30 AM, Dept. 91.", "phase": "filing"},
        {"date": "Feb 26, 2026", "event": "Plaintiff files Request for Default against unnamed occupants only — not Kyle Theus, who had filed an Answer.", "phase": "filing"},
        {"date": "Mar 11, 2026", "event": "Kyle calls Ashley Ross (5-min call documented in call log). Ashley confirms full payment can still resolve matter. Active logistical coordination begins.", "phase": "pre"},
        {"date": "Mar 13, 2026 AM", "event": "Trial held. Kyle absent — in Tulare assisting grandmother (water damage + cancer-related medical emergency). Judgment entered for plaintiff: $528 + $1,924.72 = $2,452.72. Possession granted.", "phase": "judgment"},
        {"date": "Mar 13, 2026 PM", "event": "Kyle's brother delivers $2,667.00 in money orders to Ashley Ross before 5 PM. Ashley accepts, issues physical receipt, calls Kyle to confirm. Payment exceeds judgment by $214.28.", "phase": "critical"},
        {"date": "Mar 16, 2026", "event": "Ashley contacts Kyle — cannot accept payment, moving forward with judgment. Institutional reversal.", "phase": "critical"},
        {"date": "Mar 17, 2026", "event": "Writ of Possession issued. Landlord (Debbie) calls Kyle 3 times (4:23 PM, 4:29 PM, 4:48 PM) — all missed.", "phase": "critical"},
        {"date": "Mar 19, 2026", "event": "Martha calls Kyle from blocked number: 'We want judgment. We want possession. We don't want the money.' Conceals that writ issued two days earlier. Ashley sends email with subject 'Re: No Payment Received' — while simultaneously attaching money order photographs.", "phase": "critical"},
        {"date": "Mar 23, 2026", "event": "Email from Gateways: money orders being returned by certified mail. 'You are more than welcome to reach out to the court to file a dismissal.'", "phase": "post"},
        {"date": "Mar 25, 2026", "event": "Ashley confirms: 'Yes, that is the address I have. I will let you know once we send them out.' Money orders NOT sent. No sheriff notice posted on door yet.", "phase": "post"},
        {"date": "Mar 26, 2026", "event": "Ashley: 'I have received all of your emails and have forwarded them to Martha and John. Please move forward as you feel necessary.'", "phase": "post"},
        {"date": "Mar 29, 2026", "event": "Kyle sends URGENT email: 6 days since certified mail promise. Documents $2,667 and delay for court filing. Kyle waiting in Tulare for package that will not come.", "phase": "post"},
        {"date": "Apr 16, 2026", "event": "Money orders still not returned — 34 days since first promise, 38 days since accepted. Notice discrepancy photograph uploaded: $528 demanded vs. $2,384 annotated vs. $2,462.72 judgment.", "phase": "critical"},
    ],
    "key_documents": [
        {"name": "Notice to Pay Rent or Quit (CARES Act)", "date": "Dec 8, 2025", "status": "CONFIRMED", "significance": "Demands $528. Internal note shows $2,384. Posting only — no personal service. Defective in amount and service."},
        {"name": "Notice of Belief of Abandonment", "date": "Jan 15, 2026", "status": "CONFIRMED", "significance": "Filed one day before UD complaint. Mutually incompatible legal positions. Signed by Ashley Ross."},
        {"name": "UD-100 Complaint", "date": "Jan 16, 2026", "status": "CONFIRMED", "significance": "Limited civil case. Verification dated Jan 9, 2025 — one year before filing."},
        {"name": "UD-105 Answer", "date": "Feb 10, 2026", "status": "CONFIRMED", "significance": "Filed one day before abandonment termination date. Preserves contest of all claims."},
        {"name": "March 13 Minute Order", "date": "Mar 13, 2026", "status": "CONFIRMED", "significance": "Documents non-appearance, plaintiff testimony, judgment $2,452.72, possession granted."},
        {"name": "Writ of Possession", "date": "Mar 17, 2026", "status": "CONFIRMED", "significance": "Active enforcement instrument. 5-day lockout authority upon service."},
        {"name": "Money Orders — $2,667.00", "date": "Mar 13, 2026", "status": "CONFIRMED", "significance": "Continental Express $1,000 (#31-400340925) + USPS $1,667. Held by landlord 38+ days."},
        {"name": "Physical Receipt from Ashley Ross", "date": "Mar 13, 2026", "status": "CRITICAL", "significance": "MUST CONFIRM with brother Keenan. Single most powerful document if retained."},
        {"name": "Email 'Re: No Payment Received' with MO photos", "date": "Mar 19, 2026", "status": "CONFIRMED", "significance": "Simultaneous admission of possession and denial of receipt. Evidence strength 5/5."},
        {"name": "Ashley Ross email — certified mail promise", "date": "Mar 25, 2026", "status": "CONFIRMED", "significance": "Confirmed address. Promised to send. Never did. Kyle waited in Tulare."},
    ],
    "procedural_history": [
        {
            "heading": "Filing and Initial Proceedings (January–February 2026)",
            "detail": (
                "The unlawful detainer complaint was filed January 16, 2026 — one day after a Notice "
                "of Belief of Abandonment was served, creating an inherent contradiction: the landlord "
                "simultaneously claimed the tenant had abandoned the unit and that the tenant was "
                "unlawfully detaining it. Defendant filed his Answer on February 10, 2026, one day "
                "before the February 11 abandonment termination date, thereby preserving his tenancy "
                "rights on both fronts. The case register reflects no procedural irregularities "
                "through this phase other than the abandonment/UD contradiction."
            ),
        },
        {
            "heading": "Non-Appearance at Trial — March 13, 2026",
            "detail": (
                "Trial was set for March 13, 2026 at 8:30 AM in Department 91. Defendant was in "
                "Tulare, California, providing emergency assistance to his grandmother who was "
                "simultaneously dealing with significant water damage to her home and a pending "
                "medical procedure related to a potential cancer diagnosis. Defendant reasonably "
                "believed he could return in time. By 10:03 AM the court noted no defense appearance, "
                "heard plaintiff's witness Martha Acosta, and entered judgment for plaintiff: "
                "$528.00 past rent plus $1,924.72 holdover damages, total $2,452.72, plus possession. "
                "The non-appearance was not willful — it was the result of a documented family "
                "emergency constituting excusable neglect under CCP §473(b)."
            ),
        },
        {
            "heading": "Same-Day Payment Acceptance — March 13, 2026 (After Judgment)",
            "detail": (
                "On the same afternoon judgment was entered, defendant arranged for his brother "
                "Keenan to deliver payment in full to the property. The iMessage thread between "
                "the brothers documents the coordination in real time. Keenan delivered $2,667.00 "
                "in money orders to Ashley Ross, plaintiff's authorized on-site agent. After an "
                "initial shortfall was corrected, Ashley accepted the full amount, issued a "
                "physical receipt, and called Kyle to confirm acceptance. The $2,667.00 exceeds "
                "the judgment amount by $214.28. This acceptance, under Civil Code §1477, "
                "satisfies the underlying obligation and triggers waiver of forfeiture under "
                "CCP §1161.5."
            ),
        },
        {
            "heading": "Institutional Reversal and Writ Issuance — March 16–17, 2026",
            "detail": (
                "Three days after accepting payment, plaintiff reversed course and refused to "
                "honor the transaction. A writ of possession was issued on March 17, 2026. "
                "On that same day, the landlord's contact 'Debbie' called Kyle three times "
                "(4:23 PM, 4:29 PM, 4:48 PM) — all missed. The call log corroborates that "
                "even plaintiff's side was attempting to reach defendant, contradicting the "
                "narrative of simple enforcement."
            ),
        },
        {
            "heading": "Martha Acosta's Blocked-Number Call — March 19, 2026",
            "detail": (
                "Martha Acosta called Kyle from a deliberately blocked telephone number, "
                "avoiding Ashley Ross as a potential witness. She stated: 'We want judgment. "
                "We want possession. We don't want the money; we want possession.' She did not "
                "disclose that the writ had already been issued two days earlier. When Kyle "
                "called Ashley back to relay this, Ashley was surprised — she had not been "
                "informed of the possession-only decision and had believed the reversal was "
                "temporary. This internal fragmentation is itself evidence of bad faith."
            ),
        },
        {
            "heading": "Money Orders Not Returned — 38 Days and Counting",
            "detail": (
                "On March 23, plaintiff's email stated money orders were being returned by "
                "certified mail and that dismissal could be filed. On March 25, Ashley "
                "confirmed the Tulare address and promised to send. As of April 16, 2026 — "
                "34 days after the first promise and 38 days since acceptance — the money "
                "orders have not been returned. Kyle has remained in Tulare specifically "
                "waiting for this certified mail, directly caused by plaintiff's unfulfilled "
                "promise. Plaintiff simultaneously holds defendant's $2,667 and pursues "
                "his eviction."
            ),
        },
    ],
    "payment_evidence": {
        "judgment_amount": "$2,452.72",
        "tendered_amount": "$2,667.00",
        "delta": "+$214.28",
        "evidence_items": [
            {
                "tag": "SMOKING GUN",
                "title": "Email 'Re: No Payment Received' — March 19, 2026",
                "detail": "Ashley Ross sent email with subject line denying receipt while simultaneously attaching photographs of the money orders. Admission against interest binding on principal. Evidence strength 5/5.",
            },
            {
                "tag": "CONFIRMED",
                "title": "Physical Receipt — March 13, 2026",
                "detail": "Ashley Ross issued written receipt to Kyle's brother Keenan at time of delivery confirming $2,667.00 accepted. Must confirm brother retained it.",
            },
            {
                "tag": "CONFIRMED",
                "title": "Money Order Instruments",
                "detail": "Continental Express money order serial #31-400340925 ($1,000.00) + USPS Postal Money Orders ($1,667.00) = $2,667.00 total. Purchase receipts prove date and amount.",
            },
            {
                "tag": "CONFIRMED",
                "title": "iMessage Thread with Keenan (Brother)",
                "detail": "Real-time coordination documented: address sent, amount confirmed, voice messages correcting amount, photo of money orders and signed receipt transmitted.",
            },
            {
                "tag": "CONFIRMED",
                "title": "Call Log — March 11 (5-min outgoing call)",
                "detail": "Phone records document the March 11, 2:27 PM call to Ashley Ross confirming payment could still resolve the matter. Active logistical coordination confirmed.",
            },
            {
                "tag": "EVIDENCE",
                "title": "March 25 Email — Certified Mail Promise",
                "detail": "Ashley: 'Yes, that is the address I have. I will let you know once we send them out.' Promise made. Never fulfilled. Kyle waited in Tulare 34+ days.",
            },
            {
                "tag": "EVIDENCE",
                "title": "Notice Amount Discrepancy",
                "detail": "Notice demanded $528. Internal landlord annotation shows $2,384 outstanding. Judgment entered for $2,462.72 — 4.5x the noticed amount. Foundational notice is defective.",
            },
        ],
    },
    "next_steps": [
        {
            "title": "File Ex Parte Application for Stay of Execution",
            "urgency": "IMMEDIATE",
            "detail": (
                "File in Department 1, Stanley Mosk Courthouse, 111 N. Hill St., Los Angeles, "
                "CA 90012 at 1:30 PM. Online filing available before 10:00 AM the day before "
                "via lacourt.org eFiling portal. In-person: arrive 8:30 AM day of hearing. "
                "Before filing: (1) update hearing date throughout document from March 31 to "
                "current date; (2) change 'Unlimited Civil' to 'Limited Civil' in caption; "
                "(3) complete Paragraph 14 (ex parte notice to KT&StJ); (4) fill in PHA name "
                "in Paragraph 12; (5) attach Exhibits A–D; (6) strip filing notes from document."
            ),
        },
        {
            "title": "Confirm Brother Retained Physical Receipt",
            "urgency": "IMMEDIATE",
            "detail": (
                "Contact Keenan immediately to confirm whether he retained the physical "
                "receipt issued by Ashley Ross on March 13, 2026. If retained, photograph "
                "clearly and attach as Exhibit A to the ex parte declaration. This is the "
                "single most powerful document in the case."
            ),
        },
        {
            "title": "File Motion to Set Aside Judgment — CCP §473(b)",
            "urgency": "URGENT",
            "detail": (
                "Once stay is granted, file full noticed motion with declaration, points and "
                "authorities, and proposed order. Must be filed within the 6-month window from "
                "March 13, 2026 (deadline September 13, 2026). Primary grounds: excusable "
                "neglect (family emergency), post-judgment payment acceptance, equitable "
                "estoppel, waiver of forfeiture, notice defects."
            ),
        },
        {
            "title": "Notify Public Housing Authority (PHA)",
            "urgency": "URGENT",
            "detail": (
                "Send certified letter to HACLA (or applicable PHA) immediately notifying "
                "case manager of pending UD, the motion to set aside, and requesting "
                "documentation of informal hearing rights under 24 CFR §982.555. Include "
                "case number, writ date, and statement that no final eviction has occurred. "
                "Request PHA hold voucher pending resolution."
            ),
        },
        {
            "title": "Obtain Legal Representation",
            "urgency": "URGENT",
            "detail": (
                "Priority contacts: Inner City Law Center (213) 891-2880 — specializes in "
                "SRO corridor downtown LA. Bet Tzedek (323) 939-0506. Neighborhood Legal "
                "Services (800) 433-6251. Stay Housed LA (888) 694-0040 — intake completed, "
                "awaiting callback. Stanley Mosk Self-Help (213) 830-0845."
            ),
        },
        {
            "title": "Verify Sheriff Has Not Posted 5-Day Notice",
            "urgency": "URGENT",
            "detail": (
                "Call LA County Sheriff Evictions Division at (213) 974-6001 to confirm "
                "writ status and whether sheriff has been activated for Unit 221. If a "
                "5-day notice has already been posted, bring that notice to court as "
                "an exhibit and inform the clerk immediately upon arrival that lockout "
                "execution may be imminent."
            ),
        },
        {
            "title": "Finalize and Send FloodAid Demand Letter",
            "urgency": "PARALLEL",
            "detail": (
                "Employment matter proceeding in parallel. $25,000 demand letter ready "
                "to send to Kendra Jimenez (kendra@getfloodaid.com) and Jhosa Igno "
                "(jhosa@getfloodaid.com). Five-business-day deadline. DLSE wage claim "
                "and CRD complaint ready to file on non-response."
            ),
        },
    ],
}


def main():
    print("=" * 60)
    print("ConstruX — PDF Case Status Report Generator")
    print("Case: 26STUD00430 — Gateways Apartment LP v. Kyle Theus")
    print("=" * 60)

    gen = CaseStatusReportGenerator()
    output = gen.generate(CASE_DATA, OUTPUT_PATH)
    print(f"\n[OK] PDF report written to:\n     {output}")
    size_kb = os.path.getsize(output) / 1024
    print(f"     Size: {size_kb:.1f} KB")
    print(f"\nOpen {os.path.basename(output)} to review the report.")


if __name__ == "__main__":
    main()
