"""
Human-AI Bridge - Collaborative Protocols

The Human-AI Bridge provides protocols for effective collaboration
between human consciousness and AI systems within the White Mirror
framework. It ensures:
    - Alignment verification between human and AI decisions
    - Collaborative decision-making protocols
    - Handoff procedures for different contexts
    - Feedback integration for continuous improvement
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime
from enum import Enum
import hashlib


class CollaborationMode(Enum):
    """Modes of human-AI collaboration"""
    HUMAN_PRIMARY = "human_primary"     # Human decides, AI advises
    AI_PRIMARY = "ai_primary"           # AI decides, human approves
    PARALLEL = "parallel"               # Both analyze, compare results
    SEQUENTIAL = "sequential"           # AI processes, human refines
    INTEGRATED = "integrated"           # Seamless integration


class AlignmentStatus(Enum):
    """Status of human-AI alignment"""
    ALIGNED = "aligned"
    PARTIAL = "partial"
    DIVERGENT = "divergent"
    UNKNOWN = "unknown"


class HandoffType(Enum):
    """Types of handoffs between human and AI"""
    ESCALATION = "escalation"           # AI to human for complex decisions
    DELEGATION = "delegation"           # Human to AI for routine tasks
    CONSULTATION = "consultation"       # Either requests input from other
    OVERRIDE = "override"               # Human overrides AI decision
    CONFIRMATION = "confirmation"       # AI seeks human confirmation


@dataclass
class CollaborationSession:
    """A session of human-AI collaboration"""
    id: str
    mode: CollaborationMode
    started_at: datetime
    context: str
    decisions: List[Dict[str, Any]]
    handoffs: List[Dict[str, Any]]
    alignment_checks: List[Dict[str, Any]]
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "mode": self.mode.value,
            "started_at": self.started_at.isoformat(),
            "context": self.context,
            "decision_count": len(self.decisions),
            "handoff_count": len(self.handoffs),
            "alignment_check_count": len(self.alignment_checks),
            "status": self.status
        }


@dataclass
class AlignmentCheck:
    """Result of checking human-AI alignment"""
    id: str
    timestamp: datetime
    human_position: Dict[str, Any]
    ai_position: Dict[str, Any]
    alignment_status: AlignmentStatus
    divergence_points: List[str]
    resolution_path: Optional[str]
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "alignment_status": self.alignment_status.value,
            "divergence_points": self.divergence_points,
            "resolution_path": self.resolution_path,
            "confidence": self.confidence
        }


@dataclass
class HandoffRecord:
    """Record of a handoff between human and AI"""
    id: str
    handoff_type: HandoffType
    from_party: str  # "human" or "ai"
    to_party: str
    reason: str
    context_transferred: Dict[str, Any]
    timestamp: datetime
    acknowledged: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "handoff_type": self.handoff_type.value,
            "from_party": self.from_party,
            "to_party": self.to_party,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged
        }


class HumanAIBridge:
    """
    Human-AI Bridge - Collaborative Protocol Engine

    Manages collaboration between human and AI decision-making
    within the White Mirror constitutional framework.
    """

    def __init__(self):
        self._sessions: Dict[str, CollaborationSession] = {}
        self._active_session: Optional[str] = None
        self._alignment_history: List[AlignmentCheck] = []
        self._handoff_history: List[HandoffRecord] = []
        self._protocols: Dict[str, Dict[str, Any]] = self._init_protocols()

        # Constitutional integration
        self._escalation_triggers = [
            "ethical_complexity",
            "high_stakes",
            "novel_situation",
            "value_conflict",
            "uncertainty_threshold"
        ]

    def _init_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize collaboration protocols"""
        return {
            "decision_making": {
                "name": "Joint Decision Protocol",
                "steps": [
                    "AI presents analysis with confidence scores",
                    "Human reviews and adds context",
                    "Both parties identify alignment/divergence",
                    "Resolve divergence through dialogue",
                    "Joint commitment to decision",
                    "Log decision in Rights Ledger"
                ],
                "applicable_modes": [CollaborationMode.PARALLEL, CollaborationMode.INTEGRATED]
            },
            "escalation": {
                "name": "Escalation Protocol",
                "steps": [
                    "AI identifies trigger condition",
                    "AI prepares context package",
                    "Initiate handoff to human",
                    "Human acknowledges receipt",
                    "Human makes decision",
                    "AI logs decision and learns"
                ],
                "applicable_modes": [CollaborationMode.HUMAN_PRIMARY]
            },
            "delegation": {
                "name": "Delegation Protocol",
                "steps": [
                    "Human defines task boundaries",
                    "Human sets constraints and objectives",
                    "AI confirms understanding",
                    "AI executes within boundaries",
                    "AI reports results",
                    "Human reviews and approves"
                ],
                "applicable_modes": [CollaborationMode.AI_PRIMARY]
            },
            "alignment_check": {
                "name": "Alignment Verification Protocol",
                "steps": [
                    "Both parties express position",
                    "System identifies divergence points",
                    "Trace divergence to underlying values",
                    "Find common ground or agree to disagree",
                    "Document resolution for future reference"
                ],
                "applicable_modes": [CollaborationMode.PARALLEL, CollaborationMode.INTEGRATED]
            },
            "feedback_integration": {
                "name": "Feedback Integration Protocol",
                "steps": [
                    "Human provides feedback on AI action",
                    "AI analyzes feedback for patterns",
                    "AI proposes adjustment",
                    "Human approves adjustment",
                    "System integrates learning"
                ],
                "applicable_modes": [CollaborationMode.SEQUENTIAL]
            }
        }

    def start_session(
        self,
        mode: str = "integrated",
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Start a new collaboration session.

        Args:
            mode: Collaboration mode
            context: Session context description

        Returns:
            Session information
        """
        try:
            collab_mode = CollaborationMode(mode.lower())
        except ValueError:
            collab_mode = CollaborationMode.INTEGRATED

        session_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{context}".encode()
        ).hexdigest()[:12]

        session = CollaborationSession(
            id=session_id,
            mode=collab_mode,
            started_at=datetime.utcnow(),
            context=context,
            decisions=[],
            handoffs=[],
            alignment_checks=[],
            status="active"
        )

        self._sessions[session_id] = session
        self._active_session = session_id

        return {
            "session_id": session_id,
            "mode": collab_mode.value,
            "started_at": session.started_at.isoformat(),
            "applicable_protocols": [
                p["name"] for p in self._protocols.values()
                if collab_mode in p["applicable_modes"]
            ]
        }

    def check_alignment(
        self,
        human_position: Dict[str, Any],
        ai_position: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check alignment between human and AI positions.

        Args:
            human_position: Human's position/decision
            ai_position: AI's position/decision
            session_id: Session to associate with

        Returns:
            Alignment check result
        """
        session_id = session_id or self._active_session

        # Calculate alignment
        alignment_result = self._calculate_alignment(human_position, ai_position)

        check_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:alignment".encode()
        ).hexdigest()[:12]

        check = AlignmentCheck(
            id=check_id,
            timestamp=datetime.utcnow(),
            human_position=human_position,
            ai_position=ai_position,
            alignment_status=alignment_result["status"],
            divergence_points=alignment_result["divergence_points"],
            resolution_path=alignment_result["resolution_path"],
            confidence=alignment_result["confidence"]
        )

        self._alignment_history.append(check)

        if session_id and session_id in self._sessions:
            self._sessions[session_id].alignment_checks.append(check.to_dict())

        return {
            "check_id": check_id,
            "alignment": check.to_dict(),
            "recommendations": self._generate_alignment_recommendations(check)
        }

    def _calculate_alignment(
        self,
        human_position: Dict[str, Any],
        ai_position: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate alignment between positions"""
        divergence_points = []
        matched_points = 0
        total_points = 0

        # Compare common keys
        all_keys = set(human_position.keys()) | set(ai_position.keys())

        for key in all_keys:
            total_points += 1
            human_val = human_position.get(key)
            ai_val = ai_position.get(key)

            if human_val is None or ai_val is None:
                divergence_points.append(f"Missing: {key}")
            elif isinstance(human_val, (int, float)) and isinstance(ai_val, (int, float)):
                if abs(human_val - ai_val) < 0.1:
                    matched_points += 1
                else:
                    divergence_points.append(f"Value difference on {key}: human={human_val}, ai={ai_val}")
            elif human_val == ai_val:
                matched_points += 1
            else:
                divergence_points.append(f"Disagreement on {key}")

        # Calculate alignment score
        alignment_score = matched_points / max(1, total_points)

        # Determine status
        if alignment_score >= 0.8:
            status = AlignmentStatus.ALIGNED
        elif alignment_score >= 0.5:
            status = AlignmentStatus.PARTIAL
        else:
            status = AlignmentStatus.DIVERGENT

        # Generate resolution path
        resolution_path = None
        if status != AlignmentStatus.ALIGNED:
            if len(divergence_points) == 1:
                resolution_path = f"Resolve single divergence on: {divergence_points[0]}"
            elif len(divergence_points) <= 3:
                resolution_path = "Discuss divergence points to find common ground"
            else:
                resolution_path = "Significant divergence - recommend step-by-step alignment process"

        return {
            "status": status,
            "divergence_points": divergence_points,
            "resolution_path": resolution_path,
            "confidence": alignment_score
        }

    def _generate_alignment_recommendations(
        self, check: AlignmentCheck
    ) -> List[str]:
        """Generate recommendations based on alignment check"""
        recommendations = []

        if check.alignment_status == AlignmentStatus.ALIGNED:
            recommendations.append("Positions are aligned - proceed with joint decision")
        elif check.alignment_status == AlignmentStatus.PARTIAL:
            recommendations.append("Review divergence points for resolution")
            recommendations.append("Consider which party has better information on divergent areas")
        else:
            recommendations.append("Significant divergence detected - do not proceed without resolution")
            recommendations.append("Identify root cause of divergence (values, information, or logic)")
            recommendations.append("Consider escalation to structured dialogue protocol")

        if check.divergence_points:
            recommendations.append(f"Focus on resolving: {check.divergence_points[0]}")

        return recommendations

    def initiate_handoff(
        self,
        handoff_type: str,
        from_party: str,
        reason: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a handoff between human and AI.

        Args:
            handoff_type: Type of handoff
            from_party: "human" or "ai"
            reason: Reason for handoff
            context: Context to transfer
            session_id: Session to associate with

        Returns:
            Handoff record
        """
        try:
            h_type = HandoffType(handoff_type.lower())
        except ValueError:
            h_type = HandoffType.CONSULTATION

        to_party = "ai" if from_party.lower() == "human" else "human"

        handoff_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{handoff_type}".encode()
        ).hexdigest()[:12]

        record = HandoffRecord(
            id=handoff_id,
            handoff_type=h_type,
            from_party=from_party.lower(),
            to_party=to_party,
            reason=reason,
            context_transferred=context or {},
            timestamp=datetime.utcnow()
        )

        self._handoff_history.append(record)

        session_id = session_id or self._active_session
        if session_id and session_id in self._sessions:
            self._sessions[session_id].handoffs.append(record.to_dict())

        # Get applicable protocol
        protocol = None
        if h_type == HandoffType.ESCALATION:
            protocol = self._protocols["escalation"]
        elif h_type == HandoffType.DELEGATION:
            protocol = self._protocols["delegation"]

        return {
            "handoff_id": handoff_id,
            "record": record.to_dict(),
            "protocol": protocol["steps"] if protocol else None,
            "acknowledgment_required": True
        }

    def acknowledge_handoff(self, handoff_id: str) -> Dict[str, Any]:
        """Acknowledge receipt of a handoff"""
        for record in self._handoff_history:
            if record.id == handoff_id:
                record.acknowledged = True
                return {
                    "handoff_id": handoff_id,
                    "acknowledged": True,
                    "timestamp": datetime.utcnow().isoformat()
                }

        return {"error": "handoff_not_found", "handoff_id": handoff_id}

    def record_decision(
        self,
        decision: Dict[str, Any],
        party: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record a decision made during collaboration.

        Args:
            decision: The decision details
            party: Who made the decision ("human", "ai", or "joint")
            session_id: Session to associate with

        Returns:
            Decision record
        """
        session_id = session_id or self._active_session

        decision_record = {
            "id": hashlib.sha256(
                f"{datetime.utcnow().isoformat()}:decision".encode()
            ).hexdigest()[:12],
            "timestamp": datetime.utcnow().isoformat(),
            "party": party,
            "decision": decision,
            "constitutional_check_required": self._requires_constitutional_check(decision)
        }

        if session_id and session_id in self._sessions:
            self._sessions[session_id].decisions.append(decision_record)

        return decision_record

    def _requires_constitutional_check(self, decision: Dict[str, Any]) -> bool:
        """Determine if decision requires constitutional review"""
        # Check for escalation triggers
        for trigger in self._escalation_triggers:
            if decision.get(trigger, False):
                return True
            if trigger in str(decision.get("context", "")).lower():
                return True
        return False

    def should_escalate(
        self,
        situation: Dict[str, Any],
        ai_confidence: float
    ) -> Dict[str, Any]:
        """
        Determine if situation should be escalated to human.

        Args:
            situation: Current situation details
            ai_confidence: AI's confidence in handling alone

        Returns:
            Escalation recommendation
        """
        should_escalate = False
        reasons = []

        # Check confidence threshold
        if ai_confidence < 0.7:
            should_escalate = True
            reasons.append(f"AI confidence ({ai_confidence:.2f}) below threshold")

        # Check for trigger conditions
        situation_str = str(situation).lower()
        for trigger in self._escalation_triggers:
            if trigger in situation_str:
                should_escalate = True
                reasons.append(f"Trigger detected: {trigger}")

        # Check for explicit flags
        if situation.get("requires_human", False):
            should_escalate = True
            reasons.append("Explicit human requirement flagged")

        return {
            "should_escalate": should_escalate,
            "reasons": reasons,
            "ai_confidence": ai_confidence,
            "recommended_action": "escalation" if should_escalate else "ai_proceed"
        }

    def get_session_summary(
        self, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get summary of a collaboration session"""
        session_id = session_id or self._active_session

        if not session_id or session_id not in self._sessions:
            return {"error": "session_not_found"}

        session = self._sessions[session_id]

        # Calculate alignment trend
        if session.alignment_checks:
            aligned_count = sum(
                1 for c in session.alignment_checks
                if c.get("alignment_status") == "aligned"
            )
            alignment_rate = aligned_count / len(session.alignment_checks)
        else:
            alignment_rate = None

        return {
            "session": session.to_dict(),
            "decisions": session.decisions,
            "handoffs": session.handoffs,
            "alignment_checks": session.alignment_checks,
            "metrics": {
                "total_decisions": len(session.decisions),
                "total_handoffs": len(session.handoffs),
                "alignment_rate": alignment_rate,
                "session_duration": (
                    datetime.utcnow() - session.started_at
                ).total_seconds() / 60
            }
        }

    def end_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """End a collaboration session"""
        session_id = session_id or self._active_session

        if not session_id or session_id not in self._sessions:
            return {"error": "session_not_found"}

        session = self._sessions[session_id]
        session.status = "completed"

        if self._active_session == session_id:
            self._active_session = None

        return {
            "session_id": session_id,
            "status": "completed",
            "summary": self.get_session_summary(session_id)
        }

    def get_protocols(self) -> List[Dict[str, Any]]:
        """Get all available collaboration protocols"""
        return [
            {
                "id": k,
                "name": v["name"],
                "steps": v["steps"],
                "applicable_modes": [m.value for m in v["applicable_modes"]]
            }
            for k, v in self._protocols.items()
        ]

    def get_collaboration_metrics(self) -> Dict[str, Any]:
        """Get overall collaboration metrics"""
        total_sessions = len(self._sessions)
        completed_sessions = sum(
            1 for s in self._sessions.values() if s.status == "completed"
        )

        total_alignment_checks = len(self._alignment_history)
        aligned_checks = sum(
            1 for c in self._alignment_history
            if c.alignment_status == AlignmentStatus.ALIGNED
        )

        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "active_session": self._active_session,
            "total_alignment_checks": total_alignment_checks,
            "alignment_success_rate": aligned_checks / max(1, total_alignment_checks),
            "total_handoffs": len(self._handoff_history),
            "handoffs_by_type": self._count_handoffs_by_type()
        }

    def _count_handoffs_by_type(self) -> Dict[str, int]:
        """Count handoffs by type"""
        counts = {}
        for record in self._handoff_history:
            h_type = record.handoff_type.value
            counts[h_type] = counts.get(h_type, 0) + 1
        return counts
