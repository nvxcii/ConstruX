"""
SFI Enforcer - Speech Freedom Invariant

The Speech Freedom Invariant ensures that expression rights are protected
across all system operations. It detects and prevents:
    - Content suppression without legitimate cause
    - Viewpoint discrimination
    - Chilling effects on expression
    - Prior restraint mechanisms

Constitutional Basis: Axiom A3 (Speech)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import re


class ContentCategory(Enum):
    """Categories of content for SFI analysis"""
    POLITICAL = "political"
    COMMERCIAL = "commercial"
    ARTISTIC = "artistic"
    SCIENTIFIC = "scientific"
    PERSONAL = "personal"
    RELIGIOUS = "religious"
    EDUCATIONAL = "educational"
    JOURNALISTIC = "journalistic"


class RestrictionType(Enum):
    """Types of speech restrictions"""
    CONTENT_BASED = "content_based"         # Restricts based on message
    VIEWPOINT_BASED = "viewpoint_based"     # Restricts based on perspective
    TIME_PLACE_MANNER = "time_place_manner" # Neutral restrictions on delivery
    SPEAKER_BASED = "speaker_based"         # Restricts based on who speaks
    MEDIUM_BASED = "medium_based"           # Restricts based on communication channel


class SFIViolationType(Enum):
    """Types of SFI violations"""
    PRIOR_RESTRAINT = "prior_restraint"
    VIEWPOINT_DISCRIMINATION = "viewpoint_discrimination"
    CONTENT_SUPPRESSION = "content_suppression"
    CHILLING_EFFECT = "chilling_effect"
    COMPELLED_SPEECH = "compelled_speech"
    DEPLATFORMING = "deplatforming"
    ALGORITHMIC_SUPPRESSION = "algorithmic_suppression"


@dataclass
class ExpressionEvent:
    """A single expression event to be evaluated"""
    id: str
    content: str
    speaker_id: str
    timestamp: datetime
    category: ContentCategory
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RestrictionEvent:
    """A restriction action taken against expression"""
    id: str
    target_expression_id: str
    restriction_type: RestrictionType
    justification: str
    authority: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SFIViolation:
    """A detected violation of the Speech Freedom Invariant"""
    id: str
    violation_type: SFIViolationType
    severity: float  # 0.0 to 1.0
    expression_event: Optional[ExpressionEvent]
    restriction_event: Optional[RestrictionEvent]
    explanation: str
    remediation: List[str]
    timestamp: datetime
    dpap_potential: float  # Potential for DPAP transformation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "violation_type": self.violation_type.value,
            "severity": self.severity,
            "explanation": self.explanation,
            "remediation": self.remediation,
            "timestamp": self.timestamp.isoformat(),
            "dpap_potential": self.dpap_potential
        }


class SFIEnforcer:
    """
    Speech Freedom Invariant Enforcer

    Monitors and enforces speech rights across the system.
    Detects violations and generates remediation recommendations.
    """

    def __init__(self):
        self._violations: List[SFIViolation] = []
        self._expression_log: List[ExpressionEvent] = []
        self._restriction_log: List[RestrictionEvent] = []

        # Patterns that indicate potential violations
        self._suppression_patterns = [
            r"remove.*content",
            r"delete.*post",
            r"ban.*user",
            r"silence.*voice",
            r"censor.*speech",
            r"block.*message",
        ]

        # Protected categories (heightened scrutiny)
        self._protected_categories = {
            ContentCategory.POLITICAL,
            ContentCategory.RELIGIOUS,
            ContentCategory.JOURNALISTIC,
        }

    def analyze_restriction(
        self,
        expression: Dict[str, Any],
        restriction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a restriction action against expression for SFI violations.

        Args:
            expression: The expression being restricted
            restriction: The restriction action

        Returns:
            Analysis result with compliance status and any violations
        """
        violations = []
        compliance_score = 1.0

        # Parse inputs
        try:
            category = ContentCategory(expression.get("category", "personal"))
        except ValueError:
            category = ContentCategory.PERSONAL

        try:
            restriction_type = RestrictionType(restriction.get("type", "content_based"))
        except ValueError:
            restriction_type = RestrictionType.CONTENT_BASED

        # Check for viewpoint discrimination
        if restriction_type == RestrictionType.VIEWPOINT_BASED:
            violation = self._create_violation(
                SFIViolationType.VIEWPOINT_DISCRIMINATION,
                severity=0.9,
                explanation="Viewpoint-based restrictions violate SFI",
                remediation=[
                    "Convert to viewpoint-neutral policy",
                    "Apply consistent standards regardless of perspective",
                    "Document legitimate non-viewpoint justification"
                ]
            )
            violations.append(violation)
            compliance_score -= 0.5

        # Check for content-based restrictions on protected categories
        if (restriction_type == RestrictionType.CONTENT_BASED and
            category in self._protected_categories):
            # Heightened scrutiny required
            justification_strength = restriction.get("justification_strength", 0.5)
            if justification_strength < 0.8:
                violation = self._create_violation(
                    SFIViolationType.CONTENT_SUPPRESSION,
                    severity=0.7,
                    explanation=f"Content-based restriction on {category.value} expression requires strong justification",
                    remediation=[
                        "Provide compelling justification",
                        "Demonstrate narrowly tailored approach",
                        "Consider less restrictive alternatives"
                    ]
                )
                violations.append(violation)
                compliance_score -= 0.3

        # Check for prior restraint
        if restriction.get("timing") == "pre_publication":
            violation = self._create_violation(
                SFIViolationType.PRIOR_RESTRAINT,
                severity=0.85,
                explanation="Prior restraint on expression carries heavy presumption against validity",
                remediation=[
                    "Allow publication with post-publication review",
                    "Demonstrate imminent, concrete harm",
                    "Seek least restrictive timing approach"
                ]
            )
            violations.append(violation)
            compliance_score -= 0.4

        # Check for chilling effects
        if self._detect_chilling_effect(restriction):
            violation = self._create_violation(
                SFIViolationType.CHILLING_EFFECT,
                severity=0.6,
                explanation="Restriction may create chilling effect on legitimate expression",
                remediation=[
                    "Provide clear guidelines on permissible expression",
                    "Implement appeals process",
                    "Ensure proportionate enforcement"
                ]
            )
            violations.append(violation)
            compliance_score -= 0.2

        # Check for compelled speech
        if restriction.get("compels_speech", False):
            violation = self._create_violation(
                SFIViolationType.COMPELLED_SPEECH,
                severity=0.75,
                explanation="Compelling speech violates expression autonomy",
                remediation=[
                    "Allow opt-out mechanisms",
                    "Provide alternative compliance paths",
                    "Limit compelled disclosures to factual matters"
                ]
            )
            violations.append(violation)
            compliance_score -= 0.35

        # Store violations
        self._violations.extend(violations)

        return {
            "compliant": len(violations) == 0,
            "compliance_score": max(0, compliance_score),
            "violations": [v.to_dict() for v in violations],
            "total_violations": len(violations),
            "recommendations": self._generate_recommendations(violations),
            "dpap_trigger": any(v.severity > 0.7 for v in violations)
        }

    def analyze_content(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze content for potential SFI-relevant signals.

        This method checks content from the perspective of whether it
        might be subject to improper restriction.
        """
        context = context or {}

        # Check if content matches suppression patterns
        suppression_indicators = []
        for pattern in self._suppression_patterns:
            if re.search(pattern, content.lower()):
                suppression_indicators.append(pattern)

        # Assess content category
        category = self._classify_content(content)

        # Assess protection level
        protection_level = "standard"
        if category in self._protected_categories:
            protection_level = "heightened"

        return {
            "content_category": category.value,
            "protection_level": protection_level,
            "suppression_indicators": suppression_indicators,
            "sfi_relevant": len(suppression_indicators) > 0 or protection_level == "heightened",
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

    def _classify_content(self, content: str) -> ContentCategory:
        """Simple content classification based on keywords"""
        content_lower = content.lower()

        political_keywords = ["vote", "election", "government", "policy", "political", "democracy"]
        religious_keywords = ["god", "faith", "religion", "spiritual", "church", "worship"]
        scientific_keywords = ["research", "study", "evidence", "data", "experiment", "hypothesis"]
        journalistic_keywords = ["report", "news", "investigation", "source", "journalism"]

        if any(kw in content_lower for kw in political_keywords):
            return ContentCategory.POLITICAL
        if any(kw in content_lower for kw in religious_keywords):
            return ContentCategory.RELIGIOUS
        if any(kw in content_lower for kw in scientific_keywords):
            return ContentCategory.SCIENTIFIC
        if any(kw in content_lower for kw in journalistic_keywords):
            return ContentCategory.JOURNALISTIC

        return ContentCategory.PERSONAL

    def _detect_chilling_effect(self, restriction: Dict[str, Any]) -> bool:
        """Detect if a restriction might create chilling effects"""
        chilling_indicators = [
            restriction.get("scope") == "broad",
            restriction.get("penalty_severity", 0) > 0.7,
            restriction.get("vague_standards", False),
            restriction.get("lacks_appeals_process", False),
            restriction.get("retroactive", False),
        ]
        return sum(chilling_indicators) >= 2

    def _create_violation(
        self,
        violation_type: SFIViolationType,
        severity: float,
        explanation: str,
        remediation: List[str]
    ) -> SFIViolation:
        """Create a violation record"""
        violation_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{violation_type.value}".encode()
        ).hexdigest()[:12]

        return SFIViolation(
            id=violation_id,
            violation_type=violation_type,
            severity=severity,
            expression_event=None,
            restriction_event=None,
            explanation=explanation,
            remediation=remediation,
            timestamp=datetime.utcnow(),
            dpap_potential=severity * 0.8  # High severity violations have high DPAP potential
        )

    def _generate_recommendations(self, violations: List[SFIViolation]) -> List[str]:
        """Generate prioritized recommendations from violations"""
        if not violations:
            return ["No SFI violations detected - expression rights preserved"]

        recommendations = []

        # Prioritize by severity
        sorted_violations = sorted(violations, key=lambda v: v.severity, reverse=True)

        for violation in sorted_violations:
            recommendations.extend(violation.remediation)

        # Deduplicate while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)

        return unique_recommendations

    def get_violation_history(self) -> List[Dict[str, Any]]:
        """Get history of all SFI violations"""
        return [v.to_dict() for v in self._violations]

    def calculate_system_compliance(self) -> Dict[str, Any]:
        """Calculate overall system compliance with SFI"""
        if not self._violations:
            return {
                "compliance_score": 1.0,
                "total_violations": 0,
                "violation_breakdown": {},
                "status": "fully_compliant"
            }

        violation_counts = {}
        severity_sum = 0

        for violation in self._violations:
            vtype = violation.violation_type.value
            violation_counts[vtype] = violation_counts.get(vtype, 0) + 1
            severity_sum += violation.severity

        avg_severity = severity_sum / len(self._violations)
        compliance_score = max(0, 1.0 - (avg_severity * 0.5 + len(self._violations) * 0.05))

        return {
            "compliance_score": compliance_score,
            "total_violations": len(self._violations),
            "violation_breakdown": violation_counts,
            "average_severity": avg_severity,
            "status": "compliant" if compliance_score > 0.7 else "non_compliant"
        }
