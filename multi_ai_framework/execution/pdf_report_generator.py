"""
PDF Case Status Report Generator
Produces professional letter-size PDF reports for legal case matters using reportlab.
"""

import os
from datetime import datetime
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Brand Colors ─────────────────────────────────────────────────────────────
NAVY = colors.HexColor("#1a3a5c")
RED = colors.HexColor("#c0392b")
GOLD = colors.HexColor("#d4a017")
LIGHT_GRAY = colors.HexColor("#f5f6fa")
MID_GRAY = colors.HexColor("#7f8c8d")
DARK_GRAY = colors.HexColor("#2c3e50")
GREEN = colors.HexColor("#27ae60")
ORANGE = colors.HexColor("#e67e22")
WHITE = colors.white
BLACK = colors.black


def _styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontSize=20,
            textColor=WHITE,
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#cce4f7"),
            spaceAfter=2,
            alignment=TA_CENTER,
            fontName="Helvetica",
        ),
        "section_head": ParagraphStyle(
            "section_head",
            parent=base["Heading2"],
            fontSize=12,
            textColor=WHITE,
            spaceBefore=0,
            spaceAfter=0,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=9,
            textColor=DARK_GRAY,
            spaceAfter=4,
            leading=14,
            fontName="Helvetica",
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            parent=base["Normal"],
            fontSize=9,
            textColor=DARK_GRAY,
            spaceAfter=4,
            leading=14,
            fontName="Helvetica-Bold",
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["Normal"],
            fontSize=8,
            textColor=MID_GRAY,
            spaceAfter=1,
            fontName="Helvetica",
        ),
        "value": ParagraphStyle(
            "value",
            parent=base["Normal"],
            fontSize=9,
            textColor=DARK_GRAY,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "urgent_badge": ParagraphStyle(
            "urgent_badge",
            parent=base["Normal"],
            fontSize=10,
            textColor=WHITE,
            spaceAfter=0,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontSize=7,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            fontName="Helvetica",
        ),
        "step": ParagraphStyle(
            "step",
            parent=base["Normal"],
            fontSize=9,
            textColor=DARK_GRAY,
            spaceAfter=5,
            leftIndent=12,
            leading=14,
            fontName="Helvetica",
        ),
    }


class CaseStatusReportGenerator:
    """Generates professional PDF case status reports using reportlab platypus."""

    PAGE_W, PAGE_H = letter
    MARGIN = 0.75 * inch

    def generate(self, case_data: Dict[str, Any], output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        S = _styles()

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=self.MARGIN,
            rightMargin=self.MARGIN,
            topMargin=self.MARGIN,
            bottomMargin=self.MARGIN + 0.25 * inch,
            title=f"Case Status Report — {case_data.get('case_id', '')}",
            author="ConstruX Legal Intelligence",
        )

        case_id = case_data.get("case_id", "")
        story = []

        self._build_cover(story, S, case_data)
        story.append(PageBreak())
        self._build_executive_summary(story, S, case_data)
        self._build_timeline(story, S, case_data.get("timeline", []))
        story.append(PageBreak())
        self._build_key_documents(story, S, case_data.get("key_documents", []))
        self._build_procedural_history(story, S, case_data)
        self._build_payment_evidence(story, S, case_data.get("payment_evidence", {}))
        story.append(PageBreak())
        self._build_next_steps(story, S, case_data.get("next_steps", []))

        def _on_page(canvas, doc):
            self._header_footer(canvas, doc, case_id)

        doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
        return output_path

    # ── Cover Page ────────────────────────────────────────────────────────────

    def _build_cover(self, story, S, case_data):
        story.append(Spacer(1, 0.3 * inch))

        # Main header band
        header_data = [
            [Paragraph("CASE STATUS REPORT", S["title"])],
            [Paragraph(case_data.get("case_title", ""), S["subtitle"])],
            [Paragraph(f"Case No. {case_data.get('case_id', '')}", S["subtitle"])],
        ]
        header_table = Table(header_data, colWidths=[self.PAGE_W - 2 * self.MARGIN])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ("LEFTPADDING", (0, 0), (-1, -1), 20),
            ("RIGHTPADDING", (0, 0), (-1, -1), 20),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [NAVY]),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.15 * inch))

        # Classification badge
        classification = case_data.get("classification", "URGENT — ACTIVE PROCEEDINGS")
        badge_data = [[Paragraph(f"  {classification}  ", S["urgent_badge"])]]
        badge = Table(badge_data, colWidths=[self.PAGE_W - 2 * self.MARGIN])
        badge.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), RED),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(badge)
        story.append(Spacer(1, 0.25 * inch))

        # Case identity grid
        ci = case_data.get("case_identity", {})
        parties = case_data.get("parties", {})
        rows = [
            ("Court", ci.get("court", "")),
            ("Department", ci.get("department", "")),
            ("Judge", ci.get("judge", "")),
            ("Plaintiff", parties.get("plaintiff", "")),
            ("Plaintiff Counsel", parties.get("plaintiff_counsel", "")),
            ("Defendant", parties.get("defendant", "")),
            ("Property", ci.get("property", "")),
            ("Tenancy Duration", ci.get("tenancy_duration", "")),
            ("Complaint Filed", ci.get("complaint_filed", "")),
            ("Judgment Entered", ci.get("judgment_entered", "")),
            ("Judgment Amount", ci.get("judgment_amount", "")),
            ("Writ Issued", ci.get("writ_issued", "")),
            ("Report Prepared", case_data.get("report_date", datetime.now().strftime("%B %d, %Y"))),
        ]

        table_data = []
        for label, value in rows:
            table_data.append([
                Paragraph(label, S["label"]),
                Paragraph(str(value), S["value"]),
            ])

        id_table = Table(table_data, colWidths=[1.8 * inch, 4.8 * inch])
        id_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
            ("LINEBELOW", (0, 0), (-1, -2), 0.25, colors.HexColor("#e1e4e8")),
        ]))
        story.append(id_table)
        story.append(Spacer(1, 0.2 * inch))

        # Status indicator row
        status_items = case_data.get("status_indicators", [])
        if status_items:
            cols = len(status_items)
            col_w = (self.PAGE_W - 2 * self.MARGIN) / cols
            indicator_data = [[Paragraph(s, S["urgent_badge"]) for s in status_items]]
            bg_colors = [RED if i == 0 else NAVY for i in range(cols)]
            indicator_table = Table(indicator_data, colWidths=[col_w] * cols)
            ts = [
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
            for i, bg in enumerate(bg_colors):
                ts.append(("BACKGROUND", (i, 0), (i, 0), bg))
            indicator_table.setStyle(TableStyle(ts))
            story.append(indicator_table)

    # ── Executive Summary ─────────────────────────────────────────────────────

    def _build_executive_summary(self, story, S, case_data):
        story.append(self._section_header("EXECUTIVE SUMMARY / CURRENT STATUS", S))
        story.append(Spacer(1, 0.1 * inch))

        summary = case_data.get("executive_summary", "")
        if summary:
            story.append(Paragraph(summary, S["body"]))
            story.append(Spacer(1, 0.1 * inch))

        # Status bullets
        bullets = case_data.get("status_bullets", [])
        for bullet in bullets:
            color = RED if bullet.get("urgent") else NAVY
            bullet_data = [[
                Paragraph(bullet.get("icon", "•"), ParagraphStyle(
                    "b_icon", fontSize=12, textColor=color,
                    fontName="Helvetica-Bold", alignment=TA_CENTER
                )),
                Paragraph(f"<b>{bullet.get('label', '')}</b>: {bullet.get('text', '')}", S["body"]),
            ]]
            t = Table(bullet_data, colWidths=[0.25 * inch, 6.25 * inch])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
            story.append(t)

        story.append(Spacer(1, 0.15 * inch))

    # ── Timeline ──────────────────────────────────────────────────────────────

    def _build_timeline(self, story, S, events: List[Dict]):
        if not events:
            return
        story.append(self._section_header("FULL CASE TIMELINE", S))
        story.append(Spacer(1, 0.1 * inch))

        table_data = [[
            Paragraph("DATE", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("EVENT", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold")),
        ]]
        for event in events:
            phase = event.get("phase", "")
            row_bg = {
                "pre": colors.HexColor("#eaf4fb"),
                "filing": colors.HexColor("#fef9e7"),
                "judgment": colors.HexColor("#fdedec"),
                "post": colors.HexColor("#eafaf1"),
                "critical": colors.HexColor("#fdedec"),
            }.get(phase, WHITE)

            date_style = ParagraphStyle(
                "date", fontSize=8, textColor=NAVY,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=11
            )
            event_style = ParagraphStyle(
                "ev", fontSize=8, textColor=DARK_GRAY,
                fontName="Helvetica", leading=11
            )
            table_data.append([
                Paragraph(event.get("date", ""), date_style),
                Paragraph(event.get("event", ""), event_style),
            ])

        tl_table = Table(table_data, colWidths=[1.4 * inch, 5.1 * inch],
                         repeatRows=1)
        row_styles = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
            ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#e1e4e8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
        for i, event in enumerate(events, 1):
            phase = event.get("phase", "")
            bg = {
                "pre": colors.HexColor("#eaf4fb"),
                "filing": colors.HexColor("#fef9e7"),
                "judgment": colors.HexColor("#fdedec"),
                "post": colors.HexColor("#eafaf1"),
                "critical": colors.HexColor("#fff3cd"),
            }.get(phase, WHITE if i % 2 == 0 else LIGHT_GRAY)
            row_styles.append(("BACKGROUND", (0, i), (-1, i), bg))

        tl_table.setStyle(TableStyle(row_styles))
        story.append(tl_table)
        story.append(Spacer(1, 0.15 * inch))

    # ── Key Documents ─────────────────────────────────────────────────────────

    def _build_key_documents(self, story, S, documents: List[Dict]):
        if not documents:
            return
        story.append(self._section_header("KEY DOCUMENTS SUMMARY", S))
        story.append(Spacer(1, 0.1 * inch))

        table_data = [[
            Paragraph("DOCUMENT", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold")),
            Paragraph("DATE", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("STATUS", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("SIGNIFICANCE", ParagraphStyle("th", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold")),
        ]]

        for doc in documents:
            status = doc.get("status", "")
            status_color = GREEN if status == "CONFIRMED" else (
                RED if status in ("MISSING", "CRITICAL") else ORANGE
            )
            table_data.append([
                Paragraph(doc.get("name", ""), S["body_bold"]),
                Paragraph(doc.get("date", ""), S["body"]),
                Paragraph(status, ParagraphStyle(
                    "st", fontSize=8, textColor=status_color,
                    fontName="Helvetica-Bold", alignment=TA_CENTER
                )),
                Paragraph(doc.get("significance", ""), S["body"]),
            ])

        doc_table = Table(
            table_data,
            colWidths=[2.0 * inch, 0.85 * inch, 0.75 * inch, 2.9 * inch],
            repeatRows=1,
        )
        doc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
            ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#e1e4e8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(doc_table)
        story.append(Spacer(1, 0.15 * inch))

    # ── Procedural History ────────────────────────────────────────────────────

    def _build_procedural_history(self, story, S, case_data):
        history = case_data.get("procedural_history", [])
        if not history:
            return
        story.append(self._section_header("PROCEDURAL HISTORY", S))
        story.append(Spacer(1, 0.1 * inch))

        for item in history:
            keep = [
                Paragraph(f"<b>{item.get('heading', '')}</b>", S["body_bold"]),
                Paragraph(item.get("detail", ""), S["body"]),
                Spacer(1, 0.05 * inch),
            ]
            story.append(KeepTogether(keep))

        story.append(Spacer(1, 0.1 * inch))

    # ── Payment Evidence ──────────────────────────────────────────────────────

    def _build_payment_evidence(self, story, S, payment: Dict):
        if not payment:
            return
        story.append(self._section_header("PAYMENT EVIDENCE", S))
        story.append(Spacer(1, 0.1 * inch))

        # Amount comparison highlight
        judgment_amt = payment.get("judgment_amount", "")
        tendered_amt = payment.get("tendered_amount", "")
        delta = payment.get("delta", "")

        if judgment_amt and tendered_amt:
            comp_data = [
                [
                    Paragraph("JUDGMENT AMOUNT", ParagraphStyle(
                        "cl", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                    Paragraph("AMOUNT TENDERED", ParagraphStyle(
                        "cl", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                    Paragraph("OVERPAYMENT", ParagraphStyle(
                        "cl", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                ],
                [
                    Paragraph(judgment_amt, ParagraphStyle(
                        "cv", fontSize=16, textColor=NAVY, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                    Paragraph(tendered_amt, ParagraphStyle(
                        "cv", fontSize=16, textColor=GREEN, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                    Paragraph(delta, ParagraphStyle(
                        "cv", fontSize=16, textColor=GOLD, fontName="Helvetica-Bold",
                        alignment=TA_CENTER
                    )),
                ],
            ]
            col_w = (self.PAGE_W - 2 * self.MARGIN) / 3
            comp_table = Table(comp_data, colWidths=[col_w] * 3)
            comp_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
                ("LINEAFTER", (0, 0), (1, -1), 0.5, colors.HexColor("#d0d7de")),
            ]))
            story.append(comp_table)
            story.append(Spacer(1, 0.1 * inch))

        # Evidence items
        items = payment.get("evidence_items", [])
        for item in items:
            tag = item.get("tag", "")
            tag_color = RED if tag == "SMOKING GUN" else (GREEN if tag == "CONFIRMED" else ORANGE)
            row = [
                Paragraph(tag, ParagraphStyle(
                    "tag", fontSize=7, textColor=WHITE, fontName="Helvetica-Bold",
                    alignment=TA_CENTER
                )),
                Paragraph(f"<b>{item.get('title', '')}</b>: {item.get('detail', '')}", S["body"]),
            ]
            t = Table([row], colWidths=[0.9 * inch, 5.6 * inch])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), tag_color),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#e1e4e8")),
            ]))
            story.append(t)

        story.append(Spacer(1, 0.15 * inch))

    # ── Next Steps ────────────────────────────────────────────────────────────

    def _build_next_steps(self, story, S, steps: List[Dict]):
        if not steps:
            return
        story.append(self._section_header("RECOMMENDED NEXT STEPS", S))
        story.append(Spacer(1, 0.1 * inch))

        for i, step in enumerate(steps, 1):
            urgency = step.get("urgency", "")
            urg_color = RED if urgency == "IMMEDIATE" else (
                ORANGE if urgency == "URGENT" else NAVY
            )
            header_row = [[
                Paragraph(str(i), ParagraphStyle(
                    "sn", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                    alignment=TA_CENTER
                )),
                Paragraph(step.get("title", ""), ParagraphStyle(
                    "st", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold"
                )),
                Paragraph(urgency, ParagraphStyle(
                    "su", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold",
                    alignment=TA_RIGHT
                )),
            ]]
            h_table = Table(header_row, colWidths=[0.3 * inch, 5.4 * inch, 0.8 * inch])
            h_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), urg_color),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))

            detail = Paragraph(step.get("detail", ""), S["step"])

            story.append(KeepTogether([h_table, detail, Spacer(1, 0.1 * inch)]))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section_header(self, title: str, S) -> Table:
        data = [[Paragraph(title, S["section_head"])]]
        t = Table(data, colWidths=[self.PAGE_W - 2 * self.MARGIN])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        return t

    def _header_footer(self, canvas, doc, case_id: str):
        canvas.saveState()
        w, h = letter

        # Top rule
        canvas.setStrokeColor(NAVY)
        canvas.setLineWidth(1.5)
        canvas.line(self.MARGIN, h - self.MARGIN + 4, w - self.MARGIN, h - self.MARGIN + 4)

        # Footer
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(self.MARGIN, self.MARGIN - 14,
                          f"Case No. {case_id}  |  ConstruX Legal Intelligence  |  CONFIDENTIAL — FOR LEGAL USE ONLY")
        canvas.drawRightString(w - self.MARGIN, self.MARGIN - 14,
                               f"Page {doc.page}")

        canvas.restoreState()
