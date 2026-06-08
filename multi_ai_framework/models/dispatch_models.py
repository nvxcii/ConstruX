"""
Dispatch Document Data Models
Dataclasses for CoworkDispatch — structured case handoff packages for multi-matter legal cases.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CaseActor:
    role: str            # plaintiff, defendant, attorney, witness, judge, etc.
    name: str
    contact: str
    organization: str = ""
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "name": self.name,
            "contact": self.contact,
            "organization": self.organization,
            "notes": self.notes,
        }


@dataclass
class EvidenceLayer:
    layer_number: int
    title: str
    description: str
    strength: int          # 1–5 (5 = strongest / most decisive)
    evidence_type: str     # document, testimony, digital, physical, conduct
    holder: str            # who currently holds or controls this evidence
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "layer_number": self.layer_number,
            "title": self.title,
            "description": self.description,
            "strength": self.strength,
            "evidence_type": self.evidence_type,
            "holder": self.holder,
            "notes": self.notes,
        }


@dataclass
class LegalDefect:
    level: str             # notice, complaint, judgment, post_judgment
    description: str
    statute_implicated: str = ""

    def to_dict(self) -> Dict:
        return {
            "level": self.level,
            "description": self.description,
            "statute_implicated": self.statute_implicated,
        }


@dataclass
class StatuteRef:
    citation: str
    description: str
    relevance: str

    def to_dict(self) -> Dict:
        return {
            "citation": self.citation,
            "description": self.description,
            "relevance": self.relevance,
        }


@dataclass
class TaskPriority:
    priority_number: int
    matter: str            # HOUSING, EMPLOYMENT, BOTH
    urgency: str           # IMMEDIATE, URGENT, ONGOING, PARALLEL
    title: str
    description: str
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "priority_number": self.priority_number,
            "matter": self.matter,
            "urgency": self.urgency,
            "title": self.title,
            "description": self.description,
            "dependencies": self.dependencies,
        }


@dataclass
class ImmediateAction:
    action_type: str       # motion, letter, call, filing, document_request
    title: str
    description: str
    deadline: str
    filing_location: str = ""
    filing_method: str = ""
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "action_type": self.action_type,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "filing_location": self.filing_location,
            "filing_method": self.filing_method,
            "notes": self.notes,
        }


@dataclass
class SettlementTarget:
    primary_goal: str
    proposed_terms: List[str] = field(default_factory=list)
    walkaway_conditions: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "primary_goal": self.primary_goal,
            "proposed_terms": self.proposed_terms,
            "walkaway_conditions": self.walkaway_conditions,
            "notes": self.notes,
        }


@dataclass
class LegalMatter:
    matter_id: str                              # e.g. HOUSING, EMPLOYMENT
    title: str
    urgency: str                                # IMMEDIATE, URGENT, ACTIVE, PARALLEL
    status: str                                 # e.g. "Active writ issued. No sheriff posting yet."
    case_identity: Dict[str, str]               # case number, court, judge, parties, etc.
    actors: List[CaseActor]
    timeline: List[Dict[str, str]]              # [{"date": ..., "event": ...}]
    evidence_layers: List[EvidenceLayer]
    legal_defects: List[LegalDefect]
    statutes: List[StatuteRef]
    immediate_actions: List[ImmediateAction]
    settlement_target: Optional[SettlementTarget]
    resources: List[Dict[str, str]]             # [{"name": ..., "phone": ..., "notes": ...}]
    background_notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "matter_id": self.matter_id,
            "title": self.title,
            "urgency": self.urgency,
            "status": self.status,
            "case_identity": self.case_identity,
            "actors": [a.to_dict() for a in self.actors],
            "timeline": self.timeline,
            "evidence_layers": [e.to_dict() for e in self.evidence_layers],
            "legal_defects": [d.to_dict() for d in self.legal_defects],
            "statutes": [s.to_dict() for s in self.statutes],
            "immediate_actions": [a.to_dict() for a in self.immediate_actions],
            "settlement_target": self.settlement_target.to_dict() if self.settlement_target else None,
            "resources": self.resources,
            "background_notes": self.background_notes,
        }


@dataclass
class DispatchDocument:
    case_name: str
    case_id: str
    prepared_date: str
    classification: str
    dispatch_instructions: str
    primary_operator: Dict[str, str]            # name, phone, email, location, address
    matters: List[LegalMatter]
    task_priorities: List[TaskPriority]
    critical_documents: List[Dict[str, str]]    # [{"name": ..., "holder": ..., "notes": ...}]
    opening_prompt: str
    field_state: str = "Λ = {C, I, L} | ψ = INTACT"

    def to_dict(self) -> Dict:
        return {
            "case_name": self.case_name,
            "case_id": self.case_id,
            "prepared_date": self.prepared_date,
            "classification": self.classification,
            "dispatch_instructions": self.dispatch_instructions,
            "primary_operator": self.primary_operator,
            "matters": [m.to_dict() for m in self.matters],
            "task_priorities": [t.to_dict() for t in self.task_priorities],
            "critical_documents": self.critical_documents,
            "opening_prompt": self.opening_prompt,
            "field_state": self.field_state,
        }
