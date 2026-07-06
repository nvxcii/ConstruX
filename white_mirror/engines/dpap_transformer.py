"""
DPAP++ Transformer - Constraint to Capability Converter

The DPAP (Dynamic Principle-Aligned Protocol) Transformer converts
constitutional violations into enhanced enforcement capabilities.
This is the antifragile core of the White Mirror system.

Principle: Every constraint reveals capability. Every violation
           strengthens the system.

"What doesn't kill me makes me stronger" - Nietzsche (antifragility)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime
from enum import Enum
import hashlib
import json


class TransformationType(Enum):
    """Types of DPAP transformations"""
    VIOLATION_TO_DETECTION = "violation_to_detection"     # Learn to detect similar violations
    CONSTRAINT_TO_PROTOCOL = "constraint_to_protocol"     # Convert constraint to protocol
    FAILURE_TO_RESILIENCE = "failure_to_resilience"       # Build resilience from failure
    ATTACK_TO_DEFENSE = "attack_to_defense"               # Convert attack pattern to defense
    WEAKNESS_TO_STRENGTH = "weakness_to_strength"         # Transform weakness into strength
    PATTERN_TO_PREDICTION = "pattern_to_prediction"       # Learn predictive patterns


class TransformationStatus(Enum):
    """Status of a transformation"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    INTEGRATED = "integrated"  # Fully integrated into system


@dataclass
class Constraint:
    """A constraint or violation to be transformed"""
    id: str
    constraint_type: str
    source: str  # Which system detected it (SFI, TVP, APA, etc.)
    severity: float
    description: str
    patterns: List[str]  # Patterns associated with this constraint
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Capability:
    """A capability generated from transformation"""
    id: str
    capability_type: str
    description: str
    detection_patterns: List[str]
    enforcement_rules: List[Dict[str, Any]]
    effectiveness_score: float
    source_constraints: List[str]  # IDs of source constraints
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "capability_type": self.capability_type,
            "description": self.description,
            "detection_patterns": self.detection_patterns,
            "enforcement_rules": self.enforcement_rules,
            "effectiveness_score": self.effectiveness_score,
            "source_constraints": self.source_constraints,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Transformation:
    """A complete transformation record"""
    id: str
    transformation_type: TransformationType
    input_constraint: Constraint
    output_capability: Capability
    transformation_path: List[str]
    status: TransformationStatus
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "transformation_type": self.transformation_type.value,
            "input_constraint_id": self.input_constraint.id,
            "output_capability": self.output_capability.to_dict(),
            "transformation_path": self.transformation_path,
            "status": self.status.value,
            "metadata": self.metadata
        }


class DPAPTransformer:
    """
    DPAP++ Transformer Engine

    Converts constraints and violations into enhanced capabilities.
    This is the antifragile mechanism that makes the system stronger
    through adversarial pressure.
    """

    def __init__(self):
        self._transformations: List[Transformation] = []
        self._capabilities: Dict[str, Capability] = {}
        self._pending_constraints: List[Constraint] = []
        self._transformation_strategies: Dict[str, Callable] = self._init_strategies()

        # Antifragility metrics
        self._stress_absorbed = 0.0
        self._capabilities_generated = 0
        self._system_strength = 1.0

    def _init_strategies(self) -> Dict[str, Callable]:
        """Initialize transformation strategies"""
        return {
            "sfi_violation": self._transform_sfi_violation,
            "tvp_violation": self._transform_tvp_violation,
            "apa_violation": self._transform_apa_violation,
            "axiom_violation": self._transform_axiom_violation,
            "generic": self._transform_generic,
        }

    def ingest_constraint(
        self,
        constraint_type: str,
        source: str,
        severity: float,
        description: str,
        patterns: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Constraint:
        """
        Ingest a new constraint for transformation.

        Args:
            constraint_type: Type of constraint (e.g., "speech_suppression")
            source: Source system (SFI, TVP, APA, etc.)
            severity: Severity score 0-1
            description: Human-readable description
            patterns: Associated patterns
            context: Additional context

        Returns:
            The created constraint object
        """
        constraint_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{constraint_type}:{description}".encode()
        ).hexdigest()[:12]

        constraint = Constraint(
            id=constraint_id,
            constraint_type=constraint_type,
            source=source,
            severity=severity,
            description=description,
            patterns=patterns or [],
            context=context or {}
        )

        self._pending_constraints.append(constraint)
        self._stress_absorbed += severity

        return constraint

    def transform(self, constraint: Constraint) -> Transformation:
        """
        Transform a constraint into a capability.

        This is the core DPAP operation - converting adversarial
        pressure into system strength.
        """
        # Select transformation strategy
        strategy_key = self._select_strategy(constraint)
        strategy = self._transformation_strategies.get(strategy_key, self._transform_generic)

        # Execute transformation
        capability, transformation_path = strategy(constraint)

        # Create transformation record
        transformation_id = hashlib.sha256(
            f"{constraint.id}:{capability.id}".encode()
        ).hexdigest()[:12]

        transformation = Transformation(
            id=transformation_id,
            transformation_type=self._get_transformation_type(constraint),
            input_constraint=constraint,
            output_capability=capability,
            transformation_path=transformation_path,
            status=TransformationStatus.COMPLETED,
            metadata={
                "strategy_used": strategy_key,
                "stress_level": constraint.severity,
                "transformation_timestamp": datetime.utcnow().isoformat()
            }
        )

        # Store results
        self._transformations.append(transformation)
        self._capabilities[capability.id] = capability
        self._capabilities_generated += 1

        # Update system strength (antifragile response)
        self._update_system_strength(constraint.severity)

        # Remove from pending
        if constraint in self._pending_constraints:
            self._pending_constraints.remove(constraint)

        return transformation

    def _select_strategy(self, constraint: Constraint) -> str:
        """Select the appropriate transformation strategy"""
        source_lower = constraint.source.lower()

        if "sfi" in source_lower:
            return "sfi_violation"
        elif "tvp" in source_lower:
            return "tvp_violation"
        elif "apa" in source_lower:
            return "apa_violation"
        elif "axiom" in source_lower:
            return "axiom_violation"
        else:
            return "generic"

    def _get_transformation_type(self, constraint: Constraint) -> TransformationType:
        """Determine transformation type based on constraint"""
        if "violation" in constraint.constraint_type.lower():
            return TransformationType.VIOLATION_TO_DETECTION
        elif "attack" in constraint.constraint_type.lower():
            return TransformationType.ATTACK_TO_DEFENSE
        elif "failure" in constraint.constraint_type.lower():
            return TransformationType.FAILURE_TO_RESILIENCE
        else:
            return TransformationType.CONSTRAINT_TO_PROTOCOL

    def _transform_sfi_violation(
        self, constraint: Constraint
    ) -> Tuple[Capability, List[str]]:
        """Transform SFI violation into enhanced speech protection"""
        transformation_path = [
            "analyze_violation_pattern",
            "extract_suppression_indicators",
            "generate_detection_rules",
            "create_protective_protocol",
            "integrate_capability"
        ]

        # Generate detection patterns from the violation
        detection_patterns = constraint.patterns.copy()
        detection_patterns.extend([
            f"similar_to:{constraint.constraint_type}",
            f"source_pattern:{constraint.source}"
        ])

        # Generate enforcement rules
        enforcement_rules = [
            {
                "trigger": constraint.constraint_type,
                "action": "flag_and_review",
                "severity_threshold": max(0.3, constraint.severity - 0.2)
            },
            {
                "trigger": "pattern_match",
                "patterns": constraint.patterns,
                "action": "heightened_scrutiny"
            }
        ]

        capability = self._create_capability(
            capability_type="speech_protection_enhanced",
            description=f"Enhanced protection against {constraint.constraint_type}",
            detection_patterns=detection_patterns,
            enforcement_rules=enforcement_rules,
            effectiveness_score=min(1.0, 0.5 + constraint.severity * 0.5),
            source_constraints=[constraint.id]
        )

        return capability, transformation_path

    def _transform_tvp_violation(
        self, constraint: Constraint
    ) -> Tuple[Capability, List[str]]:
        """Transform TVP violation into enhanced truth verification"""
        transformation_path = [
            "analyze_misinformation_pattern",
            "identify_credibility_gaps",
            "strengthen_verification_pipeline",
            "add_detection_layer",
            "integrate_capability"
        ]

        detection_patterns = [
            f"tvp_pattern:{p}" for p in constraint.patterns
        ]
        detection_patterns.append(f"source_category:{constraint.context.get('source_category', 'unknown')}")

        enforcement_rules = [
            {
                "trigger": "low_verification_score",
                "threshold": 0.5,
                "action": "require_additional_sources"
            },
            {
                "trigger": "pattern_match",
                "patterns": constraint.patterns,
                "action": "enhanced_verification"
            }
        ]

        capability = self._create_capability(
            capability_type="truth_verification_enhanced",
            description=f"Enhanced verification against {constraint.constraint_type}",
            detection_patterns=detection_patterns,
            enforcement_rules=enforcement_rules,
            effectiveness_score=min(1.0, 0.6 + constraint.severity * 0.4),
            source_constraints=[constraint.id]
        )

        return capability, transformation_path

    def _transform_apa_violation(
        self, constraint: Constraint
    ) -> Tuple[Capability, List[str]]:
        """Transform APA violation into enhanced autonomy protection"""
        transformation_path = [
            "analyze_manipulation_pattern",
            "map_coercion_indicators",
            "build_detection_matrix",
            "create_intervention_protocol",
            "integrate_capability"
        ]

        detection_patterns = [
            f"manipulation:{p}" for p in constraint.patterns
        ]

        enforcement_rules = [
            {
                "trigger": "manipulation_score_high",
                "threshold": 0.6,
                "action": "block_and_alert"
            },
            {
                "trigger": "dependency_creation",
                "action": "require_exit_option"
            }
        ]

        capability = self._create_capability(
            capability_type="autonomy_protection_enhanced",
            description=f"Enhanced autonomy protection against {constraint.constraint_type}",
            detection_patterns=detection_patterns,
            enforcement_rules=enforcement_rules,
            effectiveness_score=min(1.0, 0.55 + constraint.severity * 0.45),
            source_constraints=[constraint.id]
        )

        return capability, transformation_path

    def _transform_axiom_violation(
        self, constraint: Constraint
    ) -> Tuple[Capability, List[str]]:
        """Transform axiom violation into constitutional enforcement"""
        transformation_path = [
            "identify_violated_axiom",
            "analyze_violation_vector",
            "generate_constitutional_response",
            "strengthen_axiom_enforcement",
            "integrate_capability"
        ]

        detection_patterns = constraint.patterns.copy()
        detection_patterns.append(f"axiom_violation:{constraint.constraint_type}")

        enforcement_rules = [
            {
                "trigger": "axiom_threat",
                "axiom": constraint.context.get("axiom", "unknown"),
                "action": "constitutional_review"
            }
        ]

        capability = self._create_capability(
            capability_type="constitutional_enforcement_enhanced",
            description=f"Enhanced constitutional enforcement for {constraint.constraint_type}",
            detection_patterns=detection_patterns,
            enforcement_rules=enforcement_rules,
            effectiveness_score=min(1.0, 0.7 + constraint.severity * 0.3),
            source_constraints=[constraint.id]
        )

        return capability, transformation_path

    def _transform_generic(
        self, constraint: Constraint
    ) -> Tuple[Capability, List[str]]:
        """Generic transformation for unclassified constraints"""
        transformation_path = [
            "analyze_constraint",
            "extract_patterns",
            "generate_response",
            "integrate_capability"
        ]

        capability = self._create_capability(
            capability_type="generic_enhancement",
            description=f"Enhanced detection for {constraint.constraint_type}",
            detection_patterns=constraint.patterns,
            enforcement_rules=[{
                "trigger": constraint.constraint_type,
                "action": "log_and_review"
            }],
            effectiveness_score=0.5 + constraint.severity * 0.3,
            source_constraints=[constraint.id]
        )

        return capability, transformation_path

    def _create_capability(
        self,
        capability_type: str,
        description: str,
        detection_patterns: List[str],
        enforcement_rules: List[Dict[str, Any]],
        effectiveness_score: float,
        source_constraints: List[str]
    ) -> Capability:
        """Create a new capability"""
        capability_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{capability_type}:{description}".encode()
        ).hexdigest()[:12]

        return Capability(
            id=capability_id,
            capability_type=capability_type,
            description=description,
            detection_patterns=detection_patterns,
            enforcement_rules=enforcement_rules,
            effectiveness_score=effectiveness_score,
            source_constraints=source_constraints
        )

    def _update_system_strength(self, stress: float):
        """Update system strength based on absorbed stress (antifragility)"""
        # Antifragile response: stress increases strength (with diminishing returns)
        strength_gain = stress * 0.1 * (1 - (self._system_strength - 1) / 2)
        self._system_strength = min(2.0, self._system_strength + strength_gain)

    def process_all_pending(self) -> List[Transformation]:
        """Process all pending constraints"""
        results = []
        for constraint in list(self._pending_constraints):
            transformation = self.transform(constraint)
            results.append(transformation)
        return results

    def get_capabilities(self) -> List[Dict[str, Any]]:
        """Get all generated capabilities"""
        return [cap.to_dict() for cap in self._capabilities.values()]

    def get_capability_by_type(self, capability_type: str) -> List[Capability]:
        """Get capabilities of a specific type"""
        return [
            cap for cap in self._capabilities.values()
            if cap.capability_type == capability_type
        ]

    def get_transformation_history(self) -> List[Dict[str, Any]]:
        """Get history of all transformations"""
        return [t.to_dict() for t in self._transformations]

    def get_antifragility_metrics(self) -> Dict[str, Any]:
        """Get antifragility metrics for the system"""
        return {
            "stress_absorbed": self._stress_absorbed,
            "capabilities_generated": self._capabilities_generated,
            "system_strength": self._system_strength,
            "pending_constraints": len(self._pending_constraints),
            "transformation_efficiency": (
                self._capabilities_generated / max(1, len(self._transformations))
            ),
            "antifragility_score": min(1.0, self._system_strength - 1 + self._capabilities_generated * 0.05)
        }

    def apply_capability(self, capability_id: str, target: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a capability to evaluate a target.

        Args:
            capability_id: ID of capability to apply
            target: Target to evaluate

        Returns:
            Evaluation result
        """
        capability = self._capabilities.get(capability_id)
        if not capability:
            return {"error": "capability_not_found", "capability_id": capability_id}

        # Check detection patterns
        target_str = json.dumps(target).lower()
        matches = []
        for pattern in capability.detection_patterns:
            if pattern.lower() in target_str:
                matches.append(pattern)

        # Apply enforcement rules
        triggered_rules = []
        for rule in capability.enforcement_rules:
            if rule.get("trigger", "").lower() in target_str:
                triggered_rules.append(rule)

        return {
            "capability_id": capability_id,
            "capability_type": capability.capability_type,
            "pattern_matches": matches,
            "rules_triggered": triggered_rules,
            "detection_score": len(matches) / max(1, len(capability.detection_patterns)),
            "action_required": len(triggered_rules) > 0
        }
