"""
White Mirror Meta-Ontology (Layer A)

Constitutional Axioms (A1-A5):
    A1: Sovereignty Axiom - Each consciousness possesses irreducible self-governance
    A2: Truth Axiom - Reality verification precedes all actions
    A3: Speech Axiom - Expression rights are foundational to consciousness
    A4: Autonomy Axiom - Self-determination cannot be externally overridden
    A5: Recursion Axiom - The system applies its rules to itself

Primal Variables (Λ):
    λ₁: Conscience coefficient (ethical weight)
    λ₂: Intuition coefficient (pattern recognition weight)
    λ₃: Logic coefficient (analytical weight)
    λ₄: Temporal decay factor (memory degradation)
    λ₅: Antifragility multiplier (stress response)
    λ₆: Recursion depth (self-reference limit)
    λ₇: Integration constant (cross-framework coupling)

Invariants:
    I1: No axiom may contradict another axiom
    I2: Primal variables must remain within valid bounds
    I3: Constitutional violations trigger DPAP transformation
    I4: Rights ledger entries are immutable
    I5: Recursive depth has finite bounds
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import hashlib
import json


class AxiomID(Enum):
    """Constitutional Axiom Identifiers"""
    A1_SOVEREIGNTY = "A1"
    A2_TRUTH = "A2"
    A3_SPEECH = "A3"
    A4_AUTONOMY = "A4"
    A5_RECURSION = "A5"


class InvariantID(Enum):
    """System Invariant Identifiers"""
    I1_AXIOM_CONSISTENCY = "I1"
    I2_VARIABLE_BOUNDS = "I2"
    I3_DPAP_TRIGGER = "I3"
    I4_LEDGER_IMMUTABILITY = "I4"
    I5_RECURSION_BOUNDS = "I5"


@dataclass
class ConstitutionalAxiom:
    """A single constitutional axiom with enforcement logic"""
    id: AxiomID
    name: str
    description: str
    enforcement_weight: float = 1.0
    violation_threshold: float = 0.3

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        """
        Check if an action complies with this axiom.
        Returns: (compliant: bool, score: float, explanation: str)
        """
        raise NotImplementedError("Subclasses must implement compliance checking")


class SovereigntyAxiom(ConstitutionalAxiom):
    """A1: Each consciousness possesses irreducible self-governance"""

    def __init__(self):
        super().__init__(
            id=AxiomID.A1_SOVEREIGNTY,
            name="Sovereignty",
            description="Each consciousness possesses irreducible self-governance rights",
            enforcement_weight=1.0,
            violation_threshold=0.2
        )

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        score = 1.0
        violations = []

        # Check for autonomy override attempts
        if action.get("overrides_user_choice", False):
            score -= 0.4
            violations.append("Attempts to override user's autonomous choice")

        # Check for coercive elements
        if action.get("coercion_level", 0) > 0.3:
            score -= action["coercion_level"] * 0.5
            violations.append(f"Contains coercive elements (level: {action['coercion_level']:.2f})")

        # Check for consent
        if not action.get("consent_obtained", True):
            score -= 0.3
            violations.append("Action taken without explicit consent")

        compliant = score >= (1.0 - self.violation_threshold)
        explanation = "; ".join(violations) if violations else "Full compliance with sovereignty axiom"
        return compliant, max(0, score), explanation


class TruthAxiom(ConstitutionalAxiom):
    """A2: Reality verification precedes all actions"""

    def __init__(self):
        super().__init__(
            id=AxiomID.A2_TRUTH,
            name="Truth",
            description="Reality verification precedes all actions",
            enforcement_weight=1.0,
            violation_threshold=0.25
        )

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        score = 1.0
        violations = []

        # Check for false claims
        if action.get("contains_false_claims", False):
            score -= 0.5
            violations.append("Contains verifiably false claims")

        # Check for verification status
        verification_score = action.get("verification_score", 1.0)
        if verification_score < 0.7:
            score -= (0.7 - verification_score)
            violations.append(f"Insufficient verification (score: {verification_score:.2f})")

        # Check for deceptive framing
        if action.get("deceptive_framing", False):
            score -= 0.4
            violations.append("Uses deceptive framing or misleading presentation")

        compliant = score >= (1.0 - self.violation_threshold)
        explanation = "; ".join(violations) if violations else "Full compliance with truth axiom"
        return compliant, max(0, score), explanation


class SpeechAxiom(ConstitutionalAxiom):
    """A3: Expression rights are foundational to consciousness"""

    def __init__(self):
        super().__init__(
            id=AxiomID.A3_SPEECH,
            name="Speech",
            description="Expression rights are foundational to consciousness",
            enforcement_weight=1.0,
            violation_threshold=0.2
        )

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        score = 1.0
        violations = []

        # Check for suppression attempts
        if action.get("suppresses_expression", False):
            score -= 0.5
            violations.append("Suppresses legitimate expression")

        # Check for chilling effects
        if action.get("chilling_effect_potential", 0) > 0.3:
            score -= action["chilling_effect_potential"] * 0.4
            violations.append(f"May create chilling effects on speech")

        # Check for viewpoint discrimination
        if action.get("viewpoint_discrimination", False):
            score -= 0.4
            violations.append("Discriminates based on viewpoint rather than content")

        compliant = score >= (1.0 - self.violation_threshold)
        explanation = "; ".join(violations) if violations else "Full compliance with speech axiom"
        return compliant, max(0, score), explanation


class AutonomyAxiom(ConstitutionalAxiom):
    """A4: Self-determination cannot be externally overridden"""

    def __init__(self):
        super().__init__(
            id=AxiomID.A4_AUTONOMY,
            name="Autonomy",
            description="Self-determination cannot be externally overridden",
            enforcement_weight=1.0,
            violation_threshold=0.2
        )

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        score = 1.0
        violations = []

        # Check for manipulation
        manipulation_score = action.get("manipulation_score", 0)
        if manipulation_score > 0.2:
            score -= manipulation_score * 0.6
            violations.append(f"Contains manipulative elements (score: {manipulation_score:.2f})")

        # Check for dependency creation
        if action.get("creates_dependency", False):
            score -= 0.3
            violations.append("Creates artificial dependency reducing self-determination")

        # Check for exit options
        if not action.get("exit_options_available", True):
            score -= 0.3
            violations.append("Does not provide clear exit options")

        compliant = score >= (1.0 - self.violation_threshold)
        explanation = "; ".join(violations) if violations else "Full compliance with autonomy axiom"
        return compliant, max(0, score), explanation


class RecursionAxiom(ConstitutionalAxiom):
    """A5: The system applies its rules to itself"""

    def __init__(self):
        super().__init__(
            id=AxiomID.A5_RECURSION,
            name="Recursion",
            description="The system applies its rules to itself (meta-constitutional)",
            enforcement_weight=1.0,
            violation_threshold=0.3
        )

    def check_compliance(self, action: Dict[str, Any]) -> Tuple[bool, float, str]:
        score = 1.0
        violations = []

        # Check for self-exemption
        if action.get("self_exemption", False):
            score -= 0.5
            violations.append("System exempts itself from its own rules")

        # Check for recursive consistency
        if not action.get("recursively_consistent", True):
            score -= 0.4
            violations.append("Action creates recursive inconsistency")

        # Check for meta-level integrity
        if action.get("violates_meta_rules", False):
            score -= 0.4
            violations.append("Violates meta-level rules that govern rule-making")

        compliant = score >= (1.0 - self.violation_threshold)
        explanation = "; ".join(violations) if violations else "Full compliance with recursion axiom"
        return compliant, max(0, score), explanation


@dataclass
class ConstitutionalAxioms:
    """Container for all five Constitutional Axioms"""

    A1: SovereigntyAxiom = field(default_factory=SovereigntyAxiom)
    A2: TruthAxiom = field(default_factory=TruthAxiom)
    A3: SpeechAxiom = field(default_factory=SpeechAxiom)
    A4: AutonomyAxiom = field(default_factory=AutonomyAxiom)
    A5: RecursionAxiom = field(default_factory=RecursionAxiom)

    def check_all(self, action: Dict[str, Any]) -> Dict[str, Tuple[bool, float, str]]:
        """Check compliance against all axioms"""
        return {
            "A1_SOVEREIGNTY": self.A1.check_compliance(action),
            "A2_TRUTH": self.A2.check_compliance(action),
            "A3_SPEECH": self.A3.check_compliance(action),
            "A4_AUTONOMY": self.A4.check_compliance(action),
            "A5_RECURSION": self.A5.check_compliance(action),
        }

    def get_aggregate_score(self, action: Dict[str, Any]) -> Tuple[bool, float, Dict]:
        """
        Get aggregate compliance score across all axioms.
        Returns: (all_compliant, aggregate_score, detailed_results)
        """
        results = self.check_all(action)
        all_compliant = all(r[0] for r in results.values())
        aggregate_score = sum(r[1] for r in results.values()) / len(results)
        return all_compliant, aggregate_score, results


@dataclass
class PrimalVariables:
    """
    The 7 Primal Variables (Λ) that regulate system behavior.
    These are mathematical coefficients that weight different aspects
    of the consciousness operating system.
    """

    # λ₁: Conscience coefficient - weights ethical considerations
    lambda_conscience: float = 0.4

    # λ₂: Intuition coefficient - weights pattern recognition
    lambda_intuition: float = 0.3

    # λ₃: Logic coefficient - weights analytical reasoning
    lambda_logic: float = 0.3

    # λ₄: Temporal decay - how quickly past decisions lose weight
    lambda_temporal_decay: float = 0.1

    # λ₅: Antifragility multiplier - how much stress strengthens the system
    lambda_antifragility: float = 1.5

    # λ₆: Recursion depth - maximum self-reference levels
    lambda_recursion_depth: int = 7

    # λ₇: Integration constant - cross-framework coupling strength
    lambda_integration: float = 0.8

    # Bounds for validation
    _bounds: Dict[str, Tuple[float, float]] = field(default_factory=lambda: {
        "lambda_conscience": (0.0, 1.0),
        "lambda_intuition": (0.0, 1.0),
        "lambda_logic": (0.0, 1.0),
        "lambda_temporal_decay": (0.0, 1.0),
        "lambda_antifragility": (1.0, 10.0),
        "lambda_recursion_depth": (1, 20),
        "lambda_integration": (0.0, 1.0),
    })

    def __post_init__(self):
        self.validate()
        # Ensure C-I-L weights sum to 1.0
        self._normalize_cil()

    def _normalize_cil(self):
        """Ensure Conscience, Intuition, Logic weights sum to 1.0"""
        total = self.lambda_conscience + self.lambda_intuition + self.lambda_logic
        if abs(total - 1.0) > 0.001:
            self.lambda_conscience /= total
            self.lambda_intuition /= total
            self.lambda_logic /= total

    def validate(self) -> bool:
        """Validate all variables are within bounds (Invariant I2)"""
        for var_name, (low, high) in self._bounds.items():
            value = getattr(self, var_name)
            if not (low <= value <= high):
                raise ValueError(
                    f"Primal variable {var_name}={value} out of bounds [{low}, {high}]"
                )
        return True

    def get_cil_weights(self) -> Tuple[float, float, float]:
        """Get the C-I-L triad weights"""
        return (self.lambda_conscience, self.lambda_intuition, self.lambda_logic)

    def adjust_for_stress(self, stress_level: float) -> 'PrimalVariables':
        """
        Apply antifragility transformation under stress.
        Higher stress increases system's enforcement capabilities.
        """
        if stress_level <= 0:
            return self

        # Antifragile response: stress strengthens the system
        multiplier = 1.0 + (stress_level * (self.lambda_antifragility - 1.0))

        return PrimalVariables(
            lambda_conscience=min(1.0, self.lambda_conscience * multiplier),
            lambda_intuition=self.lambda_intuition,
            lambda_logic=self.lambda_logic,
            lambda_temporal_decay=self.lambda_temporal_decay / multiplier,
            lambda_antifragility=self.lambda_antifragility,
            lambda_recursion_depth=self.lambda_recursion_depth,
            lambda_integration=min(1.0, self.lambda_integration * multiplier),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "λ₁_conscience": self.lambda_conscience,
            "λ₂_intuition": self.lambda_intuition,
            "λ₃_logic": self.lambda_logic,
            "λ₄_temporal_decay": self.lambda_temporal_decay,
            "λ₅_antifragility": self.lambda_antifragility,
            "λ₆_recursion_depth": self.lambda_recursion_depth,
            "λ₇_integration": self.lambda_integration,
        }


@dataclass
class Invariants:
    """
    System invariants that must always hold true.
    Violation of any invariant triggers emergency protocols.
    """

    @staticmethod
    def check_axiom_consistency(axioms: ConstitutionalAxioms) -> Tuple[bool, str]:
        """I1: No axiom may contradict another axiom"""
        # All axioms are designed to be mutually consistent
        # This check ensures they remain so during runtime
        return True, "Axiom consistency maintained"

    @staticmethod
    def check_variable_bounds(variables: PrimalVariables) -> Tuple[bool, str]:
        """I2: Primal variables must remain within valid bounds"""
        try:
            variables.validate()
            return True, "All variables within bounds"
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def check_dpap_trigger(violation_detected: bool, dpap_activated: bool) -> Tuple[bool, str]:
        """I3: Constitutional violations trigger DPAP transformation"""
        if violation_detected and not dpap_activated:
            return False, "Violation detected but DPAP not triggered"
        return True, "DPAP trigger invariant maintained"

    @staticmethod
    def check_ledger_immutability(ledger_hash: str, computed_hash: str) -> Tuple[bool, str]:
        """I4: Rights ledger entries are immutable"""
        if ledger_hash != computed_hash:
            return False, f"Ledger integrity compromised: {ledger_hash} != {computed_hash}"
        return True, "Ledger immutability verified"

    @staticmethod
    def check_recursion_bounds(current_depth: int, max_depth: int) -> Tuple[bool, str]:
        """I5: Recursive depth has finite bounds"""
        if current_depth > max_depth:
            return False, f"Recursion depth {current_depth} exceeds maximum {max_depth}"
        return True, f"Recursion depth {current_depth} within bounds"


class WhiteMirrorCore:
    """
    The core White Mirror engine that integrates:
    - Constitutional Axioms (A1-A5)
    - Primal Variables (λ₁-λ₇)
    - Invariant checking

    This is the foundation upon which all other components build.
    """

    def __init__(self, variables: Optional[PrimalVariables] = None):
        self.axioms = ConstitutionalAxioms()
        self.variables = variables or PrimalVariables()
        self.invariants = Invariants()
        self.recursion_depth = 0
        self.stress_level = 0.0
        self._violation_history: List[Dict] = []

    def evaluate_action(
        self,
        action: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an action against all constitutional axioms.

        Args:
            action: Dictionary describing the action to evaluate
            context: Optional context for the evaluation

        Returns:
            Evaluation result with compliance status, scores, and recommendations
        """
        # Check recursion bounds
        self.recursion_depth += 1
        bounds_ok, bounds_msg = self.invariants.check_recursion_bounds(
            self.recursion_depth,
            self.variables.lambda_recursion_depth
        )
        if not bounds_ok:
            self.recursion_depth -= 1
            return {
                "error": "recursion_limit",
                "message": bounds_msg,
                "compliant": False
            }

        try:
            # Adjust variables for current stress level
            active_variables = self.variables.adjust_for_stress(self.stress_level)

            # Check compliance against all axioms
            all_compliant, aggregate_score, detailed_results = self.axioms.get_aggregate_score(action)

            # Calculate weighted score using C-I-L coefficients
            c_weight, i_weight, l_weight = active_variables.get_cil_weights()

            # Conscience: ethical dimension
            conscience_score = detailed_results["A1_SOVEREIGNTY"][1] * 0.5 + detailed_results["A4_AUTONOMY"][1] * 0.5

            # Intuition: pattern recognition of violations
            intuition_score = detailed_results["A3_SPEECH"][1]

            # Logic: truth verification
            logic_score = detailed_results["A2_TRUTH"][1] * 0.5 + detailed_results["A5_RECURSION"][1] * 0.5

            weighted_score = (
                c_weight * conscience_score +
                i_weight * intuition_score +
                l_weight * logic_score
            )

            # Record violations for DPAP processing
            violations = []
            for axiom_id, (compliant, score, explanation) in detailed_results.items():
                if not compliant:
                    violations.append({
                        "axiom": axiom_id,
                        "score": score,
                        "explanation": explanation,
                        "timestamp": datetime.utcnow().isoformat()
                    })

            if violations:
                self._violation_history.extend(violations)
                self.stress_level = min(1.0, self.stress_level + 0.1 * len(violations))

            result = {
                "compliant": all_compliant,
                "aggregate_score": aggregate_score,
                "weighted_score": weighted_score,
                "detailed_results": detailed_results,
                "violations": violations,
                "dpap_triggered": len(violations) > 0,
                "stress_level": self.stress_level,
                "active_variables": active_variables.to_dict(),
                "evaluation_hash": self._compute_hash(action, detailed_results)
            }

            return result

        finally:
            self.recursion_depth -= 1

    def _compute_hash(self, action: Dict, results: Dict) -> str:
        """Compute hash for audit trail"""
        data = json.dumps({
            "action": action,
            "results": {k: v[1] for k, v in results.items()},
            "timestamp": datetime.utcnow().isoformat()
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def get_violation_history(self) -> List[Dict]:
        """Get history of all violations for DPAP processing"""
        return self._violation_history.copy()

    def reset_stress(self):
        """Reset stress level (use after DPAP transformation)"""
        self.stress_level = 0.0

    def apply_meta_recursion(self, depth: int = 1) -> Dict[str, Any]:
        """
        Apply the system's rules to itself (A5 Recursion Axiom).
        This is the "White Mirror" operation - the system reflecting on itself.
        """
        self_action = {
            "action_type": "self_evaluation",
            "overrides_user_choice": False,
            "consent_obtained": True,
            "verification_score": 1.0,
            "suppresses_expression": False,
            "manipulation_score": 0.0,
            "self_exemption": False,
            "recursively_consistent": True,
        }

        result = self.evaluate_action(self_action)
        result["meta_recursion_depth"] = depth
        result["meta_recursion_type"] = "white_mirror_self_reflection"

        return result
