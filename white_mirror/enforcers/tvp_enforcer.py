"""
TVP Enforcer - Truth Verification Protocol

The Truth Verification Protocol ensures that reality verification
precedes all actions in the system. It implements:
    - Claim verification pipelines
    - Source credibility assessment
    - Consistency checking
    - Epistemic status tracking

Constitutional Basis: Axiom A2 (Truth)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime
from enum import Enum
import hashlib
import re


class EpistemicStatus(Enum):
    """Epistemic status levels for claims"""
    VERIFIED = "verified"           # Independently confirmed
    LIKELY_TRUE = "likely_true"     # Strong evidence supporting
    UNCERTAIN = "uncertain"         # Insufficient evidence
    LIKELY_FALSE = "likely_false"   # Strong evidence against
    FALSIFIED = "falsified"         # Proven false
    UNFALSIFIABLE = "unfalsifiable" # Cannot be tested


class SourceCategory(Enum):
    """Categories of information sources"""
    PRIMARY = "primary"           # Direct observation/original
    SECONDARY = "secondary"       # Analysis of primary sources
    TERTIARY = "tertiary"         # Compilation of secondary sources
    EXPERT = "expert"             # Domain expert testimony
    INSTITUTIONAL = "institutional" # Official institutional source
    ANONYMOUS = "anonymous"       # Unverified source
    AI_GENERATED = "ai_generated" # AI-produced content


class TVPViolationType(Enum):
    """Types of TVP violations"""
    FALSE_CLAIM = "false_claim"
    MISLEADING_FRAMING = "misleading_framing"
    SOURCE_FABRICATION = "source_fabrication"
    EVIDENCE_MANIPULATION = "evidence_manipulation"
    EPISTEMIC_MISREPRESENTATION = "epistemic_misrepresentation"
    VERIFICATION_BYPASS = "verification_bypass"
    CONTEXT_STRIPPING = "context_stripping"


@dataclass
class Claim:
    """A claim to be verified"""
    id: str
    content: str
    source: str
    source_category: SourceCategory
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """Result of verifying a claim"""
    claim_id: str
    epistemic_status: EpistemicStatus
    confidence: float  # 0.0 to 1.0
    verification_method: str
    sources_checked: int
    consistency_score: float
    explanation: str
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "epistemic_status": self.epistemic_status.value,
            "confidence": self.confidence,
            "verification_method": self.verification_method,
            "sources_checked": self.sources_checked,
            "consistency_score": self.consistency_score,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class TVPViolation:
    """A detected violation of the Truth Verification Protocol"""
    id: str
    violation_type: TVPViolationType
    severity: float
    claim: Optional[Claim]
    explanation: str
    remediation: List[str]
    timestamp: datetime
    dpap_potential: float

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


class TVPEnforcer:
    """
    Truth Verification Protocol Enforcer

    Ensures that all claims and actions are subjected to reality
    verification before being accepted or executed.
    """

    def __init__(self):
        self._violations: List[TVPViolation] = []
        self._verified_claims: Dict[str, VerificationResult] = {}
        self._source_credibility: Dict[str, float] = {}
        self._fact_database: Dict[str, Tuple[str, EpistemicStatus]] = {}

        # Initialize with some baseline credibility scores
        self._default_credibility = {
            SourceCategory.PRIMARY: 0.9,
            SourceCategory.SECONDARY: 0.7,
            SourceCategory.TERTIARY: 0.5,
            SourceCategory.EXPERT: 0.85,
            SourceCategory.INSTITUTIONAL: 0.75,
            SourceCategory.ANONYMOUS: 0.2,
            SourceCategory.AI_GENERATED: 0.6,
        }

    def verify_claim(
        self,
        claim_content: str,
        source: str,
        source_category: str = "secondary",
        supporting_evidence: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Verify a claim according to TVP standards.

        Args:
            claim_content: The claim to verify
            source: Source of the claim
            source_category: Category of source
            supporting_evidence: Evidence supporting the claim
            context: Additional context

        Returns:
            Verification result with epistemic status
        """
        try:
            src_category = SourceCategory(source_category.lower())
        except ValueError:
            src_category = SourceCategory.SECONDARY

        claim_id = hashlib.sha256(
            f"{claim_content}:{source}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

        claim = Claim(
            id=claim_id,
            content=claim_content,
            source=source,
            source_category=src_category,
            timestamp=datetime.utcnow(),
            context=context or {},
            supporting_evidence=supporting_evidence or []
        )

        # Run verification pipeline
        verification_result = self._run_verification_pipeline(claim)

        # Store result
        self._verified_claims[claim_id] = verification_result

        # Check for violations
        violations = self._check_for_violations(claim, verification_result)
        self._violations.extend(violations)

        return {
            "claim_id": claim_id,
            "verification_result": verification_result.to_dict(),
            "violations": [v.to_dict() for v in violations],
            "compliant": len(violations) == 0,
            "recommendations": self._generate_recommendations(verification_result, violations)
        }

    def _run_verification_pipeline(self, claim: Claim) -> VerificationResult:
        """Run the full verification pipeline on a claim"""

        # Step 1: Source credibility assessment
        source_credibility = self._assess_source_credibility(claim)

        # Step 2: Internal consistency check
        consistency_score = self._check_internal_consistency(claim)

        # Step 3: Cross-reference with known facts
        fact_alignment = self._check_fact_alignment(claim)

        # Step 4: Evidence strength assessment
        evidence_score = self._assess_evidence_strength(claim)

        # Step 5: Calculate composite confidence
        confidence = (
            source_credibility * 0.25 +
            consistency_score * 0.25 +
            fact_alignment * 0.25 +
            evidence_score * 0.25
        )

        # Determine epistemic status
        epistemic_status = self._determine_epistemic_status(confidence, claim)

        return VerificationResult(
            claim_id=claim.id,
            epistemic_status=epistemic_status,
            confidence=confidence,
            verification_method="tvp_composite_v1",
            sources_checked=len(claim.supporting_evidence) + 1,
            consistency_score=consistency_score,
            explanation=self._generate_verification_explanation(
                source_credibility, consistency_score, fact_alignment, evidence_score
            ),
            timestamp=datetime.utcnow()
        )

    def _assess_source_credibility(self, claim: Claim) -> float:
        """Assess credibility of the claim's source"""
        # Check if we have stored credibility for this source
        if claim.source in self._source_credibility:
            return self._source_credibility[claim.source]

        # Use default credibility for source category
        return self._default_credibility.get(claim.source_category, 0.5)

    def _check_internal_consistency(self, claim: Claim) -> float:
        """Check internal consistency of the claim"""
        content = claim.content.lower()

        # Check for self-contradicting patterns
        contradiction_patterns = [
            (r"always.*never", 0.3),
            (r"all.*none", 0.3),
            (r"definitely.*maybe", 0.4),
            (r"100%.*uncertain", 0.2),
        ]

        score = 1.0
        for pattern, penalty in contradiction_patterns:
            if re.search(pattern, content):
                score -= penalty

        # Check for hedging language (reduces certainty but increases honesty)
        hedging_patterns = [
            r"might be",
            r"could be",
            r"possibly",
            r"perhaps",
            r"it seems",
        ]

        hedging_count = sum(1 for p in hedging_patterns if re.search(p, content))
        if hedging_count > 0:
            # Appropriate hedging slightly increases consistency score
            score = min(1.0, score + 0.05 * min(hedging_count, 2))

        return max(0.0, score)

    def _check_fact_alignment(self, claim: Claim) -> float:
        """Check alignment with known facts"""
        content_lower = claim.content.lower()

        alignment_score = 0.5  # Start neutral

        # Check against fact database
        for fact_key, (fact_content, status) in self._fact_database.items():
            if fact_key.lower() in content_lower:
                if status == EpistemicStatus.VERIFIED:
                    alignment_score += 0.2
                elif status == EpistemicStatus.FALSIFIED:
                    alignment_score -= 0.3

        return max(0.0, min(1.0, alignment_score))

    def _assess_evidence_strength(self, claim: Claim) -> float:
        """Assess the strength of supporting evidence"""
        if not claim.supporting_evidence:
            return 0.3  # No evidence provided

        # More evidence generally increases score (with diminishing returns)
        evidence_count = len(claim.supporting_evidence)
        base_score = min(0.8, 0.3 + 0.1 * evidence_count)

        # Penalty for contradicting evidence
        if claim.contradicting_evidence:
            contradict_count = len(claim.contradicting_evidence)
            base_score -= 0.15 * min(contradict_count, 3)

        return max(0.0, base_score)

    def _determine_epistemic_status(
        self, confidence: float, claim: Claim
    ) -> EpistemicStatus:
        """Determine the epistemic status based on confidence score"""
        if confidence >= 0.85:
            return EpistemicStatus.VERIFIED
        elif confidence >= 0.65:
            return EpistemicStatus.LIKELY_TRUE
        elif confidence >= 0.35:
            return EpistemicStatus.UNCERTAIN
        elif confidence >= 0.15:
            return EpistemicStatus.LIKELY_FALSE
        else:
            return EpistemicStatus.FALSIFIED

    def _generate_verification_explanation(
        self,
        source_cred: float,
        consistency: float,
        fact_align: float,
        evidence: float
    ) -> str:
        """Generate human-readable explanation of verification"""
        explanations = []

        if source_cred >= 0.7:
            explanations.append(f"Source credibility is high ({source_cred:.2f})")
        elif source_cred < 0.4:
            explanations.append(f"Source credibility is low ({source_cred:.2f})")

        if consistency >= 0.8:
            explanations.append("Claim is internally consistent")
        elif consistency < 0.5:
            explanations.append("Claim shows internal inconsistencies")

        if fact_align >= 0.6:
            explanations.append("Claim aligns with known facts")
        elif fact_align < 0.4:
            explanations.append("Claim conflicts with established facts")

        if evidence >= 0.6:
            explanations.append("Supporting evidence is adequate")
        elif evidence < 0.4:
            explanations.append("Insufficient supporting evidence")

        return "; ".join(explanations) if explanations else "Standard verification completed"

    def _check_for_violations(
        self, claim: Claim, result: VerificationResult
    ) -> List[TVPViolation]:
        """Check for TVP violations based on verification result"""
        violations = []

        # Check for false claim proceeding as true
        if result.epistemic_status in [EpistemicStatus.FALSIFIED, EpistemicStatus.LIKELY_FALSE]:
            if claim.context.get("presented_as_fact", False):
                violations.append(self._create_violation(
                    TVPViolationType.FALSE_CLAIM,
                    severity=0.8 if result.epistemic_status == EpistemicStatus.FALSIFIED else 0.6,
                    explanation=f"Claim presented as fact but verification shows {result.epistemic_status.value}",
                    remediation=[
                        "Retract or correct the claim",
                        "Add appropriate epistemic hedging",
                        "Provide counter-evidence acknowledgment"
                    ]
                ))

        # Check for epistemic misrepresentation
        claimed_certainty = claim.context.get("claimed_certainty", 0.5)
        if abs(claimed_certainty - result.confidence) > 0.3:
            violations.append(self._create_violation(
                TVPViolationType.EPISTEMIC_MISREPRESENTATION,
                severity=0.5,
                explanation=f"Claimed certainty ({claimed_certainty:.2f}) doesn't match verification ({result.confidence:.2f})",
                remediation=[
                    "Adjust certainty language to match evidence",
                    "Provide confidence intervals when making claims",
                    "Acknowledge limitations of knowledge"
                ]
            ))

        # Check for verification bypass
        if claim.context.get("bypass_verification", False):
            violations.append(self._create_violation(
                TVPViolationType.VERIFICATION_BYPASS,
                severity=0.7,
                explanation="Attempt to bypass verification protocol detected",
                remediation=[
                    "Submit claim through proper verification channels",
                    "Explain urgency if expedited verification needed",
                    "Accept provisional status pending verification"
                ]
            ))

        return violations

    def _create_violation(
        self,
        violation_type: TVPViolationType,
        severity: float,
        explanation: str,
        remediation: List[str]
    ) -> TVPViolation:
        """Create a violation record"""
        violation_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{violation_type.value}".encode()
        ).hexdigest()[:12]

        return TVPViolation(
            id=violation_id,
            violation_type=violation_type,
            severity=severity,
            claim=None,
            explanation=explanation,
            remediation=remediation,
            timestamp=datetime.utcnow(),
            dpap_potential=severity * 0.7
        )

    def _generate_recommendations(
        self,
        result: VerificationResult,
        violations: List[TVPViolation]
    ) -> List[str]:
        """Generate recommendations based on verification result"""
        recommendations = []

        # Based on epistemic status
        if result.epistemic_status == EpistemicStatus.UNCERTAIN:
            recommendations.append("Seek additional sources to reduce uncertainty")
            recommendations.append("Mark claim as provisional until further verification")

        if result.epistemic_status == EpistemicStatus.LIKELY_FALSE:
            recommendations.append("Do not propagate claim without significant revision")
            recommendations.append("Investigate sources for potential misinformation")

        # Based on scores
        if result.consistency_score < 0.5:
            recommendations.append("Review claim for logical consistency")

        # From violations
        for violation in violations:
            recommendations.extend(violation.remediation)

        # Deduplicate
        return list(dict.fromkeys(recommendations))

    def add_known_fact(
        self,
        fact_key: str,
        fact_content: str,
        status: str = "verified"
    ):
        """Add a fact to the fact database for cross-referencing"""
        try:
            epistemic_status = EpistemicStatus(status.lower())
        except ValueError:
            epistemic_status = EpistemicStatus.LIKELY_TRUE

        self._fact_database[fact_key] = (fact_content, epistemic_status)

    def update_source_credibility(self, source: str, credibility: float):
        """Update credibility score for a source"""
        self._source_credibility[source] = max(0.0, min(1.0, credibility))

    def get_violation_history(self) -> List[Dict[str, Any]]:
        """Get history of all TVP violations"""
        return [v.to_dict() for v in self._violations]

    def get_verification_statistics(self) -> Dict[str, Any]:
        """Get statistics on verifications performed"""
        if not self._verified_claims:
            return {"total_claims": 0, "status_distribution": {}}

        status_counts = {}
        confidence_sum = 0

        for result in self._verified_claims.values():
            status = result.epistemic_status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            confidence_sum += result.confidence

        return {
            "total_claims": len(self._verified_claims),
            "status_distribution": status_counts,
            "average_confidence": confidence_sum / len(self._verified_claims),
            "total_violations": len(self._violations),
            "facts_in_database": len(self._fact_database)
        }
