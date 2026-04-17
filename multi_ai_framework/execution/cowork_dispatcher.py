"""
CoworkDispatcher — generates structured case handoff documents (CoworkDispatch)
from a case config dictionary. Produces both human-readable text and JSON exports.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from ..models.dispatch_models import (
    CaseActor,
    DispatchDocument,
    EvidenceLayer,
    ImmediateAction,
    LegalDefect,
    LegalMatter,
    SettlementTarget,
    StatuteRef,
    TaskPriority,
)


class CoworkDispatcher:
    """Builds and exports CoworkDispatch documents from structured case data."""

    # ------------------------------------------------------------------ #
    #  Public entry point                                                  #
    # ------------------------------------------------------------------ #

    def generate_dispatch(self, case_data: Dict) -> DispatchDocument:
        matters = [
            self._compile_matter(m) for m in case_data.get("matters", [])
        ]
        task_priorities = self._build_task_priorities(
            case_data.get("task_priorities", [])
        )
        opening_prompt = case_data.get(
            "opening_prompt",
            self._default_opening_prompt(case_data, matters),
        )

        return DispatchDocument(
            case_name=case_data["case_name"],
            case_id=case_data["case_id"],
            prepared_date=case_data.get(
                "prepared_date", datetime.now().strftime("%B %d, %Y")
            ),
            classification=case_data.get(
                "classification", "Urgent — Active Legal Proceedings"
            ),
            dispatch_instructions=case_data.get("dispatch_instructions", ""),
            primary_operator=case_data.get("primary_operator", {}),
            matters=matters,
            task_priorities=task_priorities,
            critical_documents=case_data.get("critical_documents", []),
            opening_prompt=opening_prompt,
            field_state=case_data.get(
                "field_state", "Λ = {C, I, L} | ψ = INTACT"
            ),
        )

    # ------------------------------------------------------------------ #
    #  Matter compilation                                                  #
    # ------------------------------------------------------------------ #

    def _compile_matter(self, matter_data: Dict) -> LegalMatter:
        actors = [
            CaseActor(
                role=a.get("role", ""),
                name=a.get("name", ""),
                contact=a.get("contact", ""),
                organization=a.get("organization", ""),
                notes=a.get("notes", ""),
            )
            for a in matter_data.get("actors", [])
        ]

        evidence_layers = [
            EvidenceLayer(
                layer_number=e.get("layer_number", i + 1),
                title=e.get("title", ""),
                description=e.get("description", ""),
                strength=e.get("strength", 3),
                evidence_type=e.get("evidence_type", "document"),
                holder=e.get("holder", ""),
                notes=e.get("notes", ""),
            )
            for i, e in enumerate(matter_data.get("evidence_layers", []))
        ]

        legal_defects = [
            LegalDefect(
                level=d.get("level", ""),
                description=d.get("description", ""),
                statute_implicated=d.get("statute_implicated", ""),
            )
            for d in matter_data.get("legal_defects", [])
        ]

        statutes = [
            StatuteRef(
                citation=s.get("citation", ""),
                description=s.get("description", ""),
                relevance=s.get("relevance", ""),
            )
            for s in matter_data.get("statutes", [])
        ]

        immediate_actions = [
            ImmediateAction(
                action_type=a.get("action_type", ""),
                title=a.get("title", ""),
                description=a.get("description", ""),
                deadline=a.get("deadline", ""),
                filing_location=a.get("filing_location", ""),
                filing_method=a.get("filing_method", ""),
                notes=a.get("notes", ""),
            )
            for a in matter_data.get("immediate_actions", [])
        ]

        st_data = matter_data.get("settlement_target")
        settlement_target = (
            SettlementTarget(
                primary_goal=st_data.get("primary_goal", ""),
                proposed_terms=st_data.get("proposed_terms", []),
                walkaway_conditions=st_data.get("walkaway_conditions", []),
                notes=st_data.get("notes", ""),
            )
            if st_data
            else None
        )

        return LegalMatter(
            matter_id=matter_data["matter_id"],
            title=matter_data.get("title", ""),
            urgency=matter_data.get("urgency", "URGENT"),
            status=matter_data.get("status", ""),
            case_identity=matter_data.get("case_identity", {}),
            actors=actors,
            timeline=matter_data.get("timeline", []),
            evidence_layers=evidence_layers,
            legal_defects=legal_defects,
            statutes=statutes,
            immediate_actions=immediate_actions,
            settlement_target=settlement_target,
            resources=matter_data.get("resources", []),
            background_notes=matter_data.get("background_notes", ""),
        )

    # ------------------------------------------------------------------ #
    #  Task priorities                                                     #
    # ------------------------------------------------------------------ #

    def _build_task_priorities(
        self, priorities_data: List[Dict]
    ) -> List[TaskPriority]:
        return [
            TaskPriority(
                priority_number=p.get("priority_number", i + 1),
                matter=p.get("matter", "BOTH"),
                urgency=p.get("urgency", "URGENT"),
                title=p.get("title", ""),
                description=p.get("description", ""),
                dependencies=p.get("dependencies", []),
            )
            for i, p in enumerate(priorities_data)
        ]

    # ------------------------------------------------------------------ #
    #  Default opening prompt fallback                                     #
    # ------------------------------------------------------------------ #

    def _default_opening_prompt(
        self, case_data: Dict, matters: List[LegalMatter]
    ) -> str:
        op = case_data.get("primary_operator", {})
        matter_ids = ", ".join(m.matter_id for m in matters)
        return (
            f"Continuing case file for {op.get('name', 'client')}, "
            f"case {case_data.get('case_id', '')}. "
            f"Active matters: {matter_ids}. "
            f"Full context in dispatch document. What is the first task you need to execute?"
        )

    # ------------------------------------------------------------------ #
    #  Text export                                                         #
    # ------------------------------------------------------------------ #

    def export_to_text(self, doc: DispatchDocument) -> str:
        lines: List[str] = []
        sep = "=" * 72
        thin = "-" * 72

        def h(text: str) -> str:
            return f"\n{sep}\n{text}\n{sep}"

        def sh(text: str) -> str:
            return f"\n{thin}\n{text}\n{thin}"

        # Header
        lines.append("COWORK DISPATCH DOCUMENT")
        lines.append(f"Case File: {doc.case_name}")
        lines.append(f"Prepared: {doc.prepared_date}")
        lines.append(f"Classification: {doc.classification}")

        # Dispatch instructions
        lines.append(h("DISPATCH INSTRUCTIONS"))
        lines.append(doc.dispatch_instructions)

        # Primary operator
        op = doc.primary_operator
        lines.append(h("PRIMARY OPERATOR"))
        for k, v in op.items():
            lines.append(f"{k.replace('_', ' ').title()}: {v}")

        # Matters
        for matter in doc.matters:
            lines.append(h(f"MATTER — {matter.matter_id}: {matter.title}"))
            lines.append(f"Urgency: {matter.urgency}")
            lines.append(f"Status: {matter.status}")

            # Case identity
            lines.append(sh("CASE IDENTITY"))
            for k, v in matter.case_identity.items():
                lines.append(f"{k.replace('_', ' ').title()}: {v}")

            # Actors
            if matter.actors:
                lines.append(sh("KEY ACTORS"))
                for a in matter.actors:
                    line = f"[{a.role.upper()}] {a.name}"
                    if a.contact:
                        line += f" | {a.contact}"
                    if a.organization:
                        line += f" | {a.organization}"
                    if a.notes:
                        line += f"\n  {a.notes}"
                    lines.append(line)

            # Timeline
            if matter.timeline:
                lines.append(sh("CHRONOLOGICAL TIMELINE"))
                for event in matter.timeline:
                    lines.append(f"{event.get('date', '')} — {event.get('event', '')}")

            # Evidence layers
            if matter.evidence_layers:
                lines.append(sh("EVIDENTIARY ARCHITECTURE"))
                for layer in sorted(
                    matter.evidence_layers, key=lambda x: x.layer_number
                ):
                    strength_bar = "★" * layer.strength + "☆" * (5 - layer.strength)
                    lines.append(
                        f"\nLayer {layer.layer_number} [{strength_bar}] — {layer.title}"
                    )
                    lines.append(f"  Type: {layer.evidence_type} | Holder: {layer.holder}")
                    lines.append(f"  {layer.description}")
                    if layer.notes:
                        lines.append(f"  Note: {layer.notes}")

            # Legal defects
            if matter.legal_defects:
                lines.append(sh("DOCUMENTED LEGAL DEFECTS"))
                current_level = None
                for defect in matter.legal_defects:
                    if defect.level != current_level:
                        lines.append(f"\n{defect.level.replace('_', ' ').title()} level:")
                        current_level = defect.level
                    lines.append(f"  • {defect.description}")
                    if defect.statute_implicated:
                        lines.append(f"    [{defect.statute_implicated}]")

            # Statutes
            if matter.statutes:
                lines.append(sh("APPLICABLE LEGAL FRAMEWORK"))
                for s in matter.statutes:
                    lines.append(f"\n{s.citation}")
                    lines.append(f"  {s.description}")
                    lines.append(f"  Relevance: {s.relevance}")

            # Immediate actions
            if matter.immediate_actions:
                lines.append(sh("IMMEDIATE ACTIONS REQUIRED"))
                for action in matter.immediate_actions:
                    lines.append(f"\n[{action.action_type.upper()}] {action.title}")
                    lines.append(f"  Deadline: {action.deadline}")
                    if action.filing_location:
                        lines.append(f"  Filing location: {action.filing_location}")
                    if action.filing_method:
                        lines.append(f"  Method: {action.filing_method}")
                    lines.append(f"  {action.description}")
                    if action.notes:
                        lines.append(f"  Note: {action.notes}")

            # Settlement target
            if matter.settlement_target:
                st = matter.settlement_target
                lines.append(sh("SETTLEMENT TARGET"))
                lines.append(f"Primary Goal: {st.primary_goal}")
                if st.proposed_terms:
                    lines.append("\nProposed Terms:")
                    for term in st.proposed_terms:
                        lines.append(f"  • {term}")
                if st.walkaway_conditions:
                    lines.append("\nWalkaway Conditions:")
                    for cond in st.walkaway_conditions:
                        lines.append(f"  • {cond}")
                if st.notes:
                    lines.append(f"\n{st.notes}")

            # Resources
            if matter.resources:
                lines.append(sh("LEGAL AID RESOURCES"))
                for r in matter.resources:
                    line = f"  {r.get('name', '')}"
                    if r.get("phone"):
                        line += f" — {r['phone']}"
                    if r.get("notes"):
                        line += f" — {r['notes']}"
                    lines.append(line)

        # Task priorities
        lines.append(h("COWORK TASK PRIORITIES"))
        for task in sorted(doc.task_priorities, key=lambda x: x.priority_number):
            lines.append(
                f"\nPriority {task.priority_number} — {task.matter} — {task.urgency}"
            )
            lines.append(f"  {task.title}")
            lines.append(f"  {task.description}")
            if task.dependencies:
                lines.append(f"  Depends on: {', '.join(task.dependencies)}")

        # Critical documents
        if doc.critical_documents:
            lines.append(h("CRITICAL DOCUMENTS"))
            for doc_item in doc.critical_documents:
                line = f"  • {doc_item.get('name', '')}"
                if doc_item.get("holder"):
                    line += f" [Holder: {doc_item['holder']}]"
                if doc_item.get("notes"):
                    line += f" — {doc_item['notes']}"
                lines.append(line)

        # Opening prompt
        lines.append(h("OPENING PROMPT FOR CONTINUATION"))
        lines.append(doc.opening_prompt)

        # Field state
        lines.append(f"\n{doc.field_state}")
        lines.append("Engine: URCE / NΛCIO-X∞")
        lines.append(
            "Field held across all matters. All documentation preserved. Ready for execution."
        )
        lines.append("Legal information not legal advice. All legal aid resources remain active.")

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  JSON export                                                         #
    # ------------------------------------------------------------------ #

    def export_to_json(self, doc: DispatchDocument) -> Dict:
        return doc.to_dict()

    # ------------------------------------------------------------------ #
    #  File I/O                                                            #
    # ------------------------------------------------------------------ #

    def save(self, doc: DispatchDocument, output_dir: str) -> Dict[str, str]:
        """Write COWORK_DISPATCH.txt and cowork_dispatch.json. Returns paths written."""
        os.makedirs(output_dir, exist_ok=True)
        txt_path = os.path.join(output_dir, "COWORK_DISPATCH.txt")
        json_path = os.path.join(output_dir, "cowork_dispatch.json")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(self.export_to_text(doc))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.export_to_json(doc), f, indent=2, ensure_ascii=False)

        return {"txt": txt_path, "json": json_path}
