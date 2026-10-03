"""
C-I-L Triad: Conscience, Intuition, Logic
The foundational decision alignment framework.

Λ = {C, I, L} where:
    C (Conscience): Ethical/moral compass - "What should I do?"
    I (Intuition): Pattern recognition - "What feels right?"
    L (Logic): Analytical reasoning - "What makes sense?"

Decision Alignment = degree to which a decision honors all three dimensions.
Drift Detection = identification of systematic bias toward one dimension.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from enum import Enum
import statistics
import json
import hashlib


class DecisionDomain(Enum):
    """Domains in which decisions can be made"""
    PERSONAL = "personal"
    PROFESSIONAL = "professional"
    RELATIONAL = "relational"
    FINANCIAL = "financial"
    HEALTH = "health"
    CREATIVE = "creative"
    ETHICAL = "ethical"
    STRATEGIC = "strategic"


class AlignmentState(Enum):
    """Alignment states based on C-I-L balance"""
    ALIGNED = "aligned"           # All three in harmony
    C_DOMINANT = "c_dominant"     # Over-reliance on conscience
    I_DOMINANT = "i_dominant"     # Over-reliance on intuition
    L_DOMINANT = "l_dominant"     # Over-reliance on logic
    CI_DRIFT = "ci_drift"         # Conscience-Intuition bias (ignoring logic)
    CL_DRIFT = "cl_drift"         # Conscience-Logic bias (ignoring intuition)
    IL_DRIFT = "il_drift"         # Intuition-Logic bias (ignoring conscience)
    FRAGMENTED = "fragmented"     # All three in conflict


@dataclass
class CILScore:
    """Score for a single decision across the C-I-L dimensions"""
    conscience: float  # 0.0 to 1.0
    intuition: float   # 0.0 to 1.0
    logic: float       # 0.0 to 1.0

    def __post_init__(self):
        for name, value in [("conscience", self.conscience),
                           ("intuition", self.intuition),
                           ("logic", self.logic)]:
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")

    @property
    def alignment_score(self) -> float:
        """Calculate overall alignment (higher when balanced)"""
        values = [self.conscience, self.intuition, self.logic]
        mean = statistics.mean(values)
        variance = statistics.variance(values) if len(values) > 1 else 0
        # High alignment = high mean + low variance
        return mean * (1 - variance)

    @property
    def dominant_dimension(self) -> str:
        """Identify the dominant dimension"""
        dims = {"C": self.conscience, "I": self.intuition, "L": self.logic}
        return max(dims, key=dims.get)

    @property
    def suppressed_dimension(self) -> str:
        """Identify the most suppressed dimension"""
        dims = {"C": self.conscience, "I": self.intuition, "L": self.logic}
        return min(dims, key=dims.get)

    def to_vector(self) -> Tuple[float, float, float]:
        """Return as a vector for mathematical operations"""
        return (self.conscience, self.intuition, self.logic)


@dataclass
class Decision:
    """A single recorded decision with C-I-L analysis"""
    id: str
    timestamp: datetime
    domain: DecisionDomain
    description: str
    cil_score: CILScore
    outcome_satisfaction: Optional[float] = None  # Post-decision evaluation
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "domain": self.domain.value,
            "description": self.description,
            "cil_score": {
                "conscience": self.cil_score.conscience,
                "intuition": self.cil_score.intuition,
                "logic": self.cil_score.logic,
                "alignment": self.cil_score.alignment_score,
            },
            "outcome_satisfaction": self.outcome_satisfaction,
            "context": self.context,
            "tags": self.tags,
        }


@dataclass
class DecisionAlignment:
    """
    Tracks decision alignment over time and detects drift patterns.
    This is the core of POC1: C-I-L Decision Tracker.
    """
    decisions: List[Decision] = field(default_factory=list)
    _statistical_validity_threshold: int = 30

    def add_decision(
        self,
        description: str,
        conscience_score: float,
        intuition_score: float,
        logic_score: float,
        domain: DecisionDomain = DecisionDomain.PERSONAL,
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Decision:
        """Record a new decision"""
        cil_score = CILScore(
            conscience=conscience_score,
            intuition=intuition_score,
            logic=logic_score
        )

        decision_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{description}".encode()
        ).hexdigest()[:12]

        decision = Decision(
            id=decision_id,
            timestamp=datetime.utcnow(),
            domain=domain,
            description=description,
            cil_score=cil_score,
            context=context or {},
            tags=tags or []
        )

        self.decisions.append(decision)
        return decision

    def update_outcome(self, decision_id: str, satisfaction: float):
        """Update a decision with post-decision satisfaction score"""
        for decision in self.decisions:
            if decision.id == decision_id:
                decision.outcome_satisfaction = max(0.0, min(1.0, satisfaction))
                return True
        return False

    @property
    def is_statistically_valid(self) -> bool:
        """Check if enough decisions recorded for valid analysis"""
        return len(self.decisions) >= self._statistical_validity_threshold

    def get_aggregate_profile(self, window_days: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculate aggregate C-I-L profile.

        Args:
            window_days: If specified, only use decisions from last N days

        Returns:
            Profile with means, variances, and drift indicators
        """
        decisions = self.decisions
        if window_days:
            cutoff = datetime.utcnow().timestamp() - (window_days * 86400)
            decisions = [d for d in decisions if d.timestamp.timestamp() > cutoff]

        if not decisions:
            return {"error": "no_decisions", "message": "No decisions to analyze"}

        c_scores = [d.cil_score.conscience for d in decisions]
        i_scores = [d.cil_score.intuition for d in decisions]
        l_scores = [d.cil_score.logic for d in decisions]

        c_mean = statistics.mean(c_scores)
        i_mean = statistics.mean(i_scores)
        l_mean = statistics.mean(l_scores)

        c_std = statistics.stdev(c_scores) if len(c_scores) > 1 else 0
        i_std = statistics.stdev(i_scores) if len(i_scores) > 1 else 0
        l_std = statistics.stdev(l_scores) if len(l_scores) > 1 else 0

        # Detect alignment state
        alignment_state = self._determine_alignment_state(c_mean, i_mean, l_mean)

        return {
            "decision_count": len(decisions),
            "statistically_valid": len(decisions) >= self._statistical_validity_threshold,
            "conscience": {"mean": c_mean, "std": c_std},
            "intuition": {"mean": i_mean, "std": i_std},
            "logic": {"mean": l_mean, "std": l_std},
            "alignment_state": alignment_state.value,
            "overall_alignment": statistics.mean([
                d.cil_score.alignment_score for d in decisions
            ]),
            "recommendations": self._generate_recommendations(alignment_state, c_mean, i_mean, l_mean)
        }

    def _determine_alignment_state(
        self, c: float, i: float, l: float
    ) -> AlignmentState:
        """Determine the current alignment state from mean scores"""
        threshold = 0.15  # Difference threshold for imbalance detection
        values = [c, i, l]
        mean = statistics.mean(values)
        max_val = max(values)
        min_val = min(values)

        # Check for fragmentation (all over the place)
        if max_val - min_val > 0.4:
            return AlignmentState.FRAGMENTED

        # Check for good alignment
        if max_val - min_val < threshold:
            return AlignmentState.ALIGNED

        # Check for single dimension dominance
        if c > i + threshold and c > l + threshold:
            return AlignmentState.C_DOMINANT
        if i > c + threshold and i > l + threshold:
            return AlignmentState.I_DOMINANT
        if l > c + threshold and l > i + threshold:
            return AlignmentState.L_DOMINANT

        # Check for two-dimension drift
        if c < mean - threshold / 2:
            return AlignmentState.IL_DRIFT
        if i < mean - threshold / 2:
            return AlignmentState.CL_DRIFT
        if l < mean - threshold / 2:
            return AlignmentState.CI_DRIFT

        return AlignmentState.ALIGNED

    def _generate_recommendations(
        self, state: AlignmentState, c: float, i: float, l: float
    ) -> List[str]:
        """Generate actionable recommendations based on alignment state"""
        recommendations = []

        if state == AlignmentState.ALIGNED:
            recommendations.append("Maintain current balanced approach")
            recommendations.append("Continue tracking to detect future drift")

        elif state == AlignmentState.C_DOMINANT:
            recommendations.append("Balance ethical considerations with practical analysis")
            recommendations.append("Practice scenarios requiring logical optimization")
            recommendations.append("Trust intuitive insights more in low-stakes decisions")

        elif state == AlignmentState.I_DOMINANT:
            recommendations.append("Validate intuitive choices with logical analysis")
            recommendations.append("Consider ethical implications before acting on gut feelings")
            recommendations.append("Document reasoning to improve conscious decision-making")

        elif state == AlignmentState.L_DOMINANT:
            recommendations.append("Acknowledge emotional and ethical dimensions")
            recommendations.append("Practice intuition-based rapid decisions")
            recommendations.append("Consider impact on values, not just outcomes")

        elif state == AlignmentState.CI_DRIFT:
            recommendations.append("Incorporate more analytical rigor")
            recommendations.append("Create decision frameworks with explicit criteria")
            recommendations.append("Seek data to validate ethical intuitions")

        elif state == AlignmentState.CL_DRIFT:
            recommendations.append("Trust your instincts more in uncertain situations")
            recommendations.append("Practice rapid pattern recognition exercises")
            recommendations.append("Balance analysis with intuitive synthesis")

        elif state == AlignmentState.IL_DRIFT:
            recommendations.append("Reconnect with core values and principles")
            recommendations.append("Evaluate decisions against ethical frameworks")
            recommendations.append("Consider long-term moral implications")

        elif state == AlignmentState.FRAGMENTED:
            recommendations.append("Establish clearer decision-making principles")
            recommendations.append("Create integration rituals (meditation, reflection)")
            recommendations.append("Seek external perspective on major decisions")
            recommendations.append("Consider whether internal conflict reflects unresolved values")

        return recommendations

    def detect_temporal_drift(self, window_days: int = 30) -> Dict[str, Any]:
        """
        Detect drift over time by comparing recent decisions to historical baseline.
        """
        if len(self.decisions) < self._statistical_validity_threshold:
            return {
                "error": "insufficient_data",
                "message": f"Need {self._statistical_validity_threshold} decisions, have {len(self.decisions)}"
            }

        # Split into historical and recent
        cutoff = datetime.utcnow().timestamp() - (window_days * 86400)
        historical = [d for d in self.decisions if d.timestamp.timestamp() <= cutoff]
        recent = [d for d in self.decisions if d.timestamp.timestamp() > cutoff]

        if len(historical) < 10 or len(recent) < 5:
            return {
                "error": "insufficient_comparison_data",
                "message": "Not enough data in both periods for drift analysis"
            }

        # Calculate drift for each dimension
        def calculate_drift(dimension: str):
            hist_scores = [getattr(d.cil_score, dimension) for d in historical]
            recent_scores = [getattr(d.cil_score, dimension) for d in recent]
            hist_mean = statistics.mean(hist_scores)
            recent_mean = statistics.mean(recent_scores)
            return {
                "historical_mean": hist_mean,
                "recent_mean": recent_mean,
                "drift": recent_mean - hist_mean,
                "drift_direction": "increasing" if recent_mean > hist_mean else "decreasing"
            }

        return {
            "analysis_window_days": window_days,
            "historical_decisions": len(historical),
            "recent_decisions": len(recent),
            "conscience_drift": calculate_drift("conscience"),
            "intuition_drift": calculate_drift("intuition"),
            "logic_drift": calculate_drift("logic"),
            "significant_drift": any(
                abs(calculate_drift(d)["drift"]) > 0.1
                for d in ["conscience", "intuition", "logic"]
            )
        }

    def get_domain_analysis(self) -> Dict[str, Dict[str, Any]]:
        """Analyze C-I-L patterns by decision domain"""
        domain_decisions: Dict[DecisionDomain, List[Decision]] = {}

        for decision in self.decisions:
            if decision.domain not in domain_decisions:
                domain_decisions[decision.domain] = []
            domain_decisions[decision.domain].append(decision)

        analysis = {}
        for domain, decisions in domain_decisions.items():
            if decisions:
                c_scores = [d.cil_score.conscience for d in decisions]
                i_scores = [d.cil_score.intuition for d in decisions]
                l_scores = [d.cil_score.logic for d in decisions]

                analysis[domain.value] = {
                    "decision_count": len(decisions),
                    "conscience_mean": statistics.mean(c_scores),
                    "intuition_mean": statistics.mean(i_scores),
                    "logic_mean": statistics.mean(l_scores),
                    "dominant_dimension": max(
                        [("C", statistics.mean(c_scores)),
                         ("I", statistics.mean(i_scores)),
                         ("L", statistics.mean(l_scores))],
                        key=lambda x: x[1]
                    )[0]
                }

        return analysis

    def export_for_research(self) -> Dict[str, Any]:
        """Export data in format suitable for research analysis"""
        return {
            "metadata": {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_decisions": len(self.decisions),
                "statistically_valid": self.is_statistically_valid,
                "framework_version": "POC1_v1.0"
            },
            "aggregate_profile": self.get_aggregate_profile(),
            "domain_analysis": self.get_domain_analysis(),
            "decisions": [d.to_dict() for d in self.decisions]
        }


class CILTriad:
    """
    The C-I-L Triad engine for decision alignment.
    Provides the interface for the consciousness operating system's
    decision-making framework.
    """

    def __init__(self):
        self.alignment_tracker = DecisionAlignment()
        self._precommitments: List[Dict[str, Any]] = []

    def record_decision(
        self,
        description: str,
        conscience: float,
        intuition: float,
        logic: float,
        domain: str = "personal",
        context: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Record a decision with C-I-L scores.

        Args:
            description: What the decision was about
            conscience: How much ethical/moral considerations influenced (0-1)
            intuition: How much gut feeling/pattern recognition influenced (0-1)
            logic: How much analytical reasoning influenced (0-1)
            domain: Decision domain (personal, professional, etc.)
            context: Additional context
            tags: Tags for categorization

        Returns:
            Decision record with analysis
        """
        try:
            domain_enum = DecisionDomain(domain.lower())
        except ValueError:
            domain_enum = DecisionDomain.PERSONAL

        decision = self.alignment_tracker.add_decision(
            description=description,
            conscience_score=conscience,
            intuition_score=intuition,
            logic_score=logic,
            domain=domain_enum,
            context=context,
            tags=tags
        )

        return {
            "decision_id": decision.id,
            "recorded": True,
            "cil_score": decision.cil_score.to_vector(),
            "alignment_score": decision.cil_score.alignment_score,
            "current_profile": self.alignment_tracker.get_aggregate_profile()
        }

    def add_precommitment(
        self,
        principle: str,
        trigger_condition: str,
        intended_response: str,
        cil_weights: Tuple[float, float, float]
    ) -> Dict[str, Any]:
        """
        Add a precommitment - a decision made in advance for future scenarios.
        This is a key feature for maintaining constitutional alignment under pressure.
        """
        precommitment = {
            "id": hashlib.sha256(
                f"{datetime.utcnow().isoformat()}:{principle}".encode()
            ).hexdigest()[:12],
            "principle": principle,
            "trigger_condition": trigger_condition,
            "intended_response": intended_response,
            "cil_weights": {
                "conscience": cil_weights[0],
                "intuition": cil_weights[1],
                "logic": cil_weights[2]
            },
            "created_at": datetime.utcnow().isoformat(),
            "invocation_count": 0
        }

        self._precommitments.append(precommitment)
        return precommitment

    def check_precommitments(self, current_context: str) -> List[Dict[str, Any]]:
        """Check if any precommitments are relevant to current context"""
        # Simple keyword matching - in production, this would use semantic similarity
        relevant = []
        context_lower = current_context.lower()

        for precommitment in self._precommitments:
            trigger_lower = precommitment["trigger_condition"].lower()
            # Check for keyword overlap
            trigger_words = set(trigger_lower.split())
            context_words = set(context_lower.split())
            if trigger_words & context_words:
                relevant.append(precommitment)

        return relevant

    def get_alignment_report(self) -> Dict[str, Any]:
        """Generate comprehensive alignment report"""
        return {
            "profile": self.alignment_tracker.get_aggregate_profile(),
            "domain_patterns": self.alignment_tracker.get_domain_analysis(),
            "precommitments": len(self._precommitments),
            "statistically_valid": self.alignment_tracker.is_statistically_valid,
            "decisions_until_valid": max(
                0,
                self.alignment_tracker._statistical_validity_threshold - len(self.alignment_tracker.decisions)
            )
        }

    def export_data(self) -> Dict[str, Any]:
        """Export all data for backup or research"""
        return {
            "decisions": self.alignment_tracker.export_for_research(),
            "precommitments": self._precommitments,
            "export_timestamp": datetime.utcnow().isoformat()
        }
