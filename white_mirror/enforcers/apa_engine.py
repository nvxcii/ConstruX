"""
APA Engine - Autonomy Preservation Algorithms

The Autonomy Preservation Algorithms ensure that self-determination
cannot be externally overridden. It implements:
    - Manipulation detection
    - Dependency analysis
    - Exit option verification
    - Consent validation
    - Coercion detection

Constitutional Basis: Axiom A4 (Autonomy)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime
from enum import Enum
import hashlib
import re


class ManipulationType(Enum):
    """Types of manipulation that threaten autonomy"""
    DARK_PATTERN = "dark_pattern"
    EMOTIONAL_EXPLOITATION = "emotional_exploitation"
    INFORMATION_ASYMMETRY = "information_asymmetry"
    ARTIFICIAL_URGENCY = "artificial_urgency"
    SOCIAL_PROOF_MANIPULATION = "social_proof_manipulation"
    SUNK_COST_EXPLOITATION = "sunk_cost_exploitation"
    ANCHORING = "anchoring"
    FRAMING_MANIPULATION = "framing_manipulation"
    CHOICE_OVERLOAD = "choice_overload"
    DEFAULT_EXPLOITATION = "default_exploitation"


class DependencyType(Enum):
    """Types of dependencies that may limit autonomy"""
    TECHNICAL = "technical"       # Platform lock-in, proprietary formats
    ECONOMIC = "economic"         # Financial dependencies
    SOCIAL = "social"             # Network effects, social pressure
    INFORMATIONAL = "informational"  # Data dependencies
    HABITUAL = "habitual"         # Behavioral dependencies
    CONTRACTUAL = "contractual"   # Legal binding


class APAViolationType(Enum):
    """Types of APA violations"""
    MANIPULATION_DETECTED = "manipulation_detected"
    COERCION_DETECTED = "coercion_detected"
    DEPENDENCY_CREATION = "dependency_creation"
    EXIT_BLOCKED = "exit_blocked"
    CONSENT_INVALID = "consent_invalid"
    AUTONOMY_OVERRIDE = "autonomy_override"
    DECEPTIVE_CHOICE = "deceptive_choice"


@dataclass
class AutonomyContext:
    """Context for an autonomy evaluation"""
    id: str
    actor: str
    target: str
    action_description: str
    timestamp: datetime
    consent_obtained: bool
    consent_type: str  # explicit, implicit, none
    exit_options: List[str]
    dependencies_created: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ManipulationSignal:
    """A detected manipulation signal"""
    manipulation_type: ManipulationType
    confidence: float
    indicators: List[str]
    explanation: str


@dataclass
class APAViolation:
    """A detected violation of Autonomy Preservation"""
    id: str
    violation_type: APAViolationType
    severity: float
    context: Optional[AutonomyContext]
    manipulation_signals: List[ManipulationSignal]
    explanation: str
    remediation: List[str]
    timestamp: datetime
    dpap_potential: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "violation_type": self.violation_type.value,
            "severity": self.severity,
            "manipulation_signals": [
                {
                    "type": s.manipulation_type.value,
                    "confidence": s.confidence,
                    "indicators": s.indicators
                } for s in self.manipulation_signals
            ],
            "explanation": self.explanation,
            "remediation": self.remediation,
            "timestamp": self.timestamp.isoformat(),
            "dpap_potential": self.dpap_potential
        }


class APAEngine:
    """
    Autonomy Preservation Algorithms Engine

    Monitors and protects user autonomy from manipulation,
    coercion, and improper dependency creation.
    """

    def __init__(self):
        self._violations: List[APAViolation] = []
        self._manipulation_patterns: Dict[ManipulationType, List[str]] = self._init_patterns()
        self._dependency_registry: Dict[str, List[DependencyType]] = {}

        # Thresholds
        self._manipulation_threshold = 0.6
        self._coercion_threshold = 0.5
        self._dependency_concern_threshold = 3

    def _init_patterns(self) -> Dict[ManipulationType, List[str]]:
        """Initialize manipulation detection patterns"""
        return {
            ManipulationType.DARK_PATTERN: [
                r"limited.?time.?offer",
                r"only.?\d+.?left",
                r"act.?now",
                r"don't.?miss.?out",
                r"before.?it's.?gone",
            ],
            ManipulationType.ARTIFICIAL_URGENCY: [
                r"expires?.?soon",
                r"countdown",
                r"hurry",
                r"last.?chance",
                r"deadline",
                r"limited.?availability",
            ],
            ManipulationType.SOCIAL_PROOF_MANIPULATION: [
                r"\d+.?people.?are.?viewing",
                r"popular.?choice",
                r"best.?seller",
                r"everyone.?is",
                r"trending",
            ],
            ManipulationType.EMOTIONAL_EXPLOITATION: [
                r"you'll.?regret",
                r"imagine.?how",
                r"feel.?bad",
                r"let.?down",
                r"disappoint",
            ],
            ManipulationType.SUNK_COST_EXPLOITATION: [
                r"already.?invested",
                r"come.?this.?far",
                r"don't.?waste",
                r"you've.?earned",
            ],
            ManipulationType.DEFAULT_EXPLOITATION: [
                r"pre.?selected",
                r"automatically.?enrolled",
                r"opt.?out",
                r"default.?setting",
            ],
        }

    def analyze_interaction(
        self,
        action_description: str,
        actor: str,
        target: str,
        consent_obtained: bool = True,
        consent_type: str = "explicit",
        exit_options: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze an interaction for autonomy preservation compliance.

        Args:
            action_description: Description of the action/interaction
            actor: Who is performing the action
            target: Who is affected by the action
            consent_obtained: Whether consent was obtained
            consent_type: Type of consent (explicit, implicit, none)
            exit_options: Available exit options for the target
            context: Additional context

        Returns:
            Analysis result with compliance status and violations
        """
        context_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{action_description}".encode()
        ).hexdigest()[:12]

        autonomy_context = AutonomyContext(
            id=context_id,
            actor=actor,
            target=target,
            action_description=action_description,
            timestamp=datetime.utcnow(),
            consent_obtained=consent_obtained,
            consent_type=consent_type,
            exit_options=exit_options or [],
            dependencies_created=[],
            metadata=context or {}
        )

        # Run analysis pipeline
        manipulation_signals = self._detect_manipulation(action_description)
        coercion_score = self._assess_coercion(autonomy_context)
        dependency_analysis = self._analyze_dependencies(autonomy_context, context or {})
        exit_analysis = self._analyze_exit_options(autonomy_context)
        consent_analysis = self._validate_consent(autonomy_context)

        # Collect violations
        violations = []

        # Manipulation violations
        high_confidence_manipulations = [
            s for s in manipulation_signals if s.confidence >= self._manipulation_threshold
        ]
        if high_confidence_manipulations:
            violations.append(self._create_violation(
                APAViolationType.MANIPULATION_DETECTED,
                severity=max(s.confidence for s in high_confidence_manipulations),
                manipulation_signals=high_confidence_manipulations,
                explanation=f"Detected {len(high_confidence_manipulations)} manipulation patterns",
                remediation=[
                    "Remove manipulative language and patterns",
                    "Present information neutrally",
                    "Allow genuine deliberation time"
                ]
            ))

        # Coercion violations
        if coercion_score >= self._coercion_threshold:
            violations.append(self._create_violation(
                APAViolationType.COERCION_DETECTED,
                severity=coercion_score,
                manipulation_signals=[],
                explanation=f"Coercion level ({coercion_score:.2f}) exceeds threshold",
                remediation=[
                    "Remove threatening or pressuring elements",
                    "Ensure genuine freedom to decline",
                    "Provide neutral framing of options"
                ]
            ))

        # Exit option violations
        if not exit_analysis["adequate"]:
            violations.append(self._create_violation(
                APAViolationType.EXIT_BLOCKED,
                severity=0.7,
                manipulation_signals=[],
                explanation=exit_analysis["explanation"],
                remediation=[
                    "Provide clear exit/cancellation options",
                    "Make exit process as easy as entry",
                    "Do not hide or complicate exit procedures"
                ]
            ))

        # Consent violations
        if not consent_analysis["valid"]:
            violations.append(self._create_violation(
                APAViolationType.CONSENT_INVALID,
                severity=consent_analysis["severity"],
                manipulation_signals=[],
                explanation=consent_analysis["explanation"],
                remediation=[
                    "Obtain explicit informed consent",
                    "Clearly explain what is being consented to",
                    "Provide opportunity to review before consent"
                ]
            ))

        # Store violations
        self._violations.extend(violations)

        # Calculate overall compliance
        compliance_score = 1.0
        for v in violations:
            compliance_score -= v.severity * 0.25

        return {
            "context_id": context_id,
            "compliant": len(violations) == 0,
            "compliance_score": max(0, compliance_score),
            "manipulation_signals": [
                {
                    "type": s.manipulation_type.value,
                    "confidence": s.confidence,
                    "indicators": s.indicators
                } for s in manipulation_signals
            ],
            "coercion_score": coercion_score,
            "dependency_analysis": dependency_analysis,
            "exit_analysis": exit_analysis,
            "consent_analysis": consent_analysis,
            "violations": [v.to_dict() for v in violations],
            "recommendations": self._generate_recommendations(violations)
        }

    def _detect_manipulation(self, content: str) -> List[ManipulationSignal]:
        """Detect manipulation patterns in content"""
        signals = []
        content_lower = content.lower()

        for manipulation_type, patterns in self._manipulation_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    matches.append(pattern)

            if matches:
                confidence = min(1.0, len(matches) * 0.3 + 0.3)
                signals.append(ManipulationSignal(
                    manipulation_type=manipulation_type,
                    confidence=confidence,
                    indicators=matches,
                    explanation=f"Detected {manipulation_type.value} pattern with {len(matches)} indicators"
                ))

        return signals

    def _assess_coercion(self, context: AutonomyContext) -> float:
        """Assess level of coercion in the interaction"""
        coercion_score = 0.0

        # Check for power asymmetry indicators
        metadata = context.metadata
        if metadata.get("power_asymmetry", False):
            coercion_score += 0.3

        # Check for negative consequences for non-compliance
        if metadata.get("negative_consequences", False):
            coercion_score += 0.3

        # Check for time pressure
        if metadata.get("time_pressure", False):
            coercion_score += 0.2

        # Check for isolation tactics
        if metadata.get("isolation", False):
            coercion_score += 0.2

        return min(1.0, coercion_score)

    def _analyze_dependencies(
        self,
        context: AutonomyContext,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze dependency creation"""
        dependencies = []

        # Check for technical dependencies
        if metadata.get("creates_lock_in", False):
            dependencies.append(DependencyType.TECHNICAL)

        # Check for economic dependencies
        if metadata.get("recurring_payment", False):
            dependencies.append(DependencyType.ECONOMIC)

        # Check for data dependencies
        if metadata.get("data_retention", False):
            dependencies.append(DependencyType.INFORMATIONAL)

        # Check for social dependencies
        if metadata.get("network_effect", False):
            dependencies.append(DependencyType.SOCIAL)

        concern_level = "low"
        if len(dependencies) >= self._dependency_concern_threshold:
            concern_level = "high"
        elif len(dependencies) >= 2:
            concern_level = "medium"

        return {
            "dependencies_detected": [d.value for d in dependencies],
            "count": len(dependencies),
            "concern_level": concern_level,
            "recommendation": self._get_dependency_recommendation(dependencies)
        }

    def _get_dependency_recommendation(self, dependencies: List[DependencyType]) -> str:
        """Get recommendation based on dependencies"""
        if not dependencies:
            return "No concerning dependencies detected"

        if DependencyType.TECHNICAL in dependencies:
            return "Ensure data portability and standard formats"
        if DependencyType.ECONOMIC in dependencies:
            return "Provide clear cancellation and refund policies"
        if DependencyType.INFORMATIONAL in dependencies:
            return "Implement data export and deletion capabilities"

        return "Review dependency creation for autonomy impact"

    def _analyze_exit_options(self, context: AutonomyContext) -> Dict[str, Any]:
        """Analyze adequacy of exit options"""
        exit_options = context.exit_options

        if not exit_options:
            return {
                "adequate": False,
                "explanation": "No exit options provided",
                "options_count": 0
            }

        # Check for clear exit path
        clear_exit_keywords = ["cancel", "unsubscribe", "delete", "remove", "exit", "leave"]
        has_clear_exit = any(
            any(kw in opt.lower() for kw in clear_exit_keywords)
            for opt in exit_options
        )

        adequate = has_clear_exit and len(exit_options) >= 1

        return {
            "adequate": adequate,
            "explanation": "Clear exit options available" if adequate else "Exit options unclear or hidden",
            "options_count": len(exit_options),
            "has_clear_exit": has_clear_exit
        }

    def _validate_consent(self, context: AutonomyContext) -> Dict[str, Any]:
        """Validate consent quality"""
        if not context.consent_obtained:
            return {
                "valid": False,
                "explanation": "No consent obtained",
                "severity": 0.8
            }

        if context.consent_type == "explicit":
            return {
                "valid": True,
                "explanation": "Explicit consent obtained",
                "severity": 0.0
            }

        if context.consent_type == "implicit":
            return {
                "valid": False,
                "explanation": "Implicit consent insufficient for this action",
                "severity": 0.4
            }

        return {
            "valid": False,
            "explanation": f"Unknown consent type: {context.consent_type}",
            "severity": 0.6
        }

    def _create_violation(
        self,
        violation_type: APAViolationType,
        severity: float,
        manipulation_signals: List[ManipulationSignal],
        explanation: str,
        remediation: List[str]
    ) -> APAViolation:
        """Create a violation record"""
        violation_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{violation_type.value}".encode()
        ).hexdigest()[:12]

        return APAViolation(
            id=violation_id,
            violation_type=violation_type,
            severity=severity,
            context=None,
            manipulation_signals=manipulation_signals,
            explanation=explanation,
            remediation=remediation,
            timestamp=datetime.utcnow(),
            dpap_potential=severity * 0.75
        )

    def _generate_recommendations(self, violations: List[APAViolation]) -> List[str]:
        """Generate recommendations from violations"""
        if not violations:
            return ["Autonomy preservation standards met"]

        recommendations = []
        for violation in violations:
            recommendations.extend(violation.remediation)

        # Deduplicate
        return list(dict.fromkeys(recommendations))

    def get_violation_history(self) -> List[Dict[str, Any]]:
        """Get history of all APA violations"""
        return [v.to_dict() for v in self._violations]

    def calculate_autonomy_score(self) -> Dict[str, Any]:
        """Calculate overall autonomy preservation score"""
        if not self._violations:
            return {
                "score": 1.0,
                "total_violations": 0,
                "status": "fully_preserved"
            }

        severity_sum = sum(v.severity for v in self._violations)
        avg_severity = severity_sum / len(self._violations)
        score = max(0, 1.0 - (avg_severity * 0.4 + len(self._violations) * 0.03))

        return {
            "score": score,
            "total_violations": len(self._violations),
            "average_severity": avg_severity,
            "status": "preserved" if score > 0.7 else "at_risk"
        }

    def register_dependency(self, target: str, dependency_type: str):
        """Register a dependency for tracking"""
        try:
            dep_type = DependencyType(dependency_type.lower())
        except ValueError:
            dep_type = DependencyType.TECHNICAL

        if target not in self._dependency_registry:
            self._dependency_registry[target] = []
        self._dependency_registry[target].append(dep_type)

    def get_dependency_report(self, target: str) -> Dict[str, Any]:
        """Get dependency report for a target"""
        dependencies = self._dependency_registry.get(target, [])
        return {
            "target": target,
            "dependencies": [d.value for d in dependencies],
            "count": len(dependencies),
            "concern_level": "high" if len(dependencies) >= 3 else "medium" if len(dependencies) >= 2 else "low"
        }
