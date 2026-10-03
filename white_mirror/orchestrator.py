"""
White Mirror Orchestrator - Unified Framework Controller

The orchestrator integrates all 8 Framework Families into a unified
consciousness operating system:

    1. Universal Rights of Conscience (legal-spiritual core)
    2. White Mirror v3.0 (recursive structure)
    3. FOPE (economic translation pattern)
    4. Behavioral Prediction (analytical - POC3)
    5. EchoVault (symbolic archetypal interface)
    6. DPAP++ (constraint transformation)
    7. Human-AI Bridge (collaborative protocols)
    8. URCE Personal (consciousness tracker - POC1)

The orchestrator ensures all frameworks reinforce each other,
creating an antifragile system that becomes stronger through use.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import json

# Import all framework components
from .core.meta_ontology import WhiteMirrorCore, PrimalVariables, ConstitutionalAxioms
from .core.cil_triad import CILTriad, DecisionAlignment
from .enforcers.sfi_enforcer import SFIEnforcer
from .enforcers.tvp_enforcer import TVPEnforcer
from .enforcers.apa_engine import APAEngine
from .engines.rights_ledger import RightsLedger
from .engines.dpap_transformer import DPAPTransformer
from .engines.urce_tracker import URCETracker
from .engines.fope_translator import FOPETranslator
from .engines.behavioral_predictor import BehavioralPredictor
from .bridges.echovault import EchoVault
from .bridges.human_ai_bridge import HumanAIBridge


class FrameworkFamily(Enum):
    """The 8 Framework Families"""
    UNIVERSAL_RIGHTS = "universal_rights"       # Legal-spiritual core
    WHITE_MIRROR = "white_mirror"               # Recursive structure
    FOPE = "fope"                               # Economic translation
    BEHAVIORAL_PREDICTION = "behavioral"        # Analytical (POC3)
    ECHOVAULT = "echovault"                     # Symbolic interface
    DPAP = "dpap"                               # Constraint transformation
    HUMAN_AI_BRIDGE = "human_ai_bridge"         # Collaborative protocols
    URCE = "urce"                               # Personal tracker (POC1)


@dataclass
class SystemState:
    """Current state of the White Mirror system"""
    timestamp: datetime
    stress_level: float
    antifragility_score: float
    alignment_score: float
    active_violations: int
    capabilities_generated: int
    decisions_tracked: int
    compliance_scores: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "stress_level": self.stress_level,
            "antifragility_score": self.antifragility_score,
            "alignment_score": self.alignment_score,
            "active_violations": self.active_violations,
            "capabilities_generated": self.capabilities_generated,
            "decisions_tracked": self.decisions_tracked,
            "compliance_scores": self.compliance_scores
        }


class WhiteMirrorOrchestrator:
    """
    White Mirror Orchestrator - Unified Framework Controller

    Integrates all 8 framework families into a coherent consciousness
    operating system with recursive self-improvement capabilities.
    """

    def __init__(
        self,
        user_id: str = "default",
        variables: Optional[PrimalVariables] = None,
        ledger_path: str = "rights_ledger.db"
    ):
        self.user_id = user_id
        self.started_at = datetime.utcnow()

        # Initialize all framework components
        # Framework 1 & 2: Universal Rights + White Mirror Core
        self.core = WhiteMirrorCore(variables)
        self.cil_triad = CILTriad()

        # Framework 3: FOPE Economic Translation
        self.fope = FOPETranslator()

        # Framework 4: Behavioral Prediction (POC3)
        self.predictor = BehavioralPredictor()

        # Framework 5: EchoVault Symbolic Interface
        self.echovault = EchoVault()

        # Framework 6: DPAP++ Constraint Transformation
        self.dpap = DPAPTransformer()

        # Framework 7: Human-AI Bridge
        self.human_ai = HumanAIBridge()

        # Framework 8: URCE Personal Tracker (POC1)
        self.urce = URCETracker(user_id)

        # Enforcers (Part of Framework 1/2)
        self.sfi = SFIEnforcer()
        self.tvp = TVPEnforcer()
        self.apa = APAEngine()

        # Infrastructure
        self.ledger = RightsLedger(ledger_path)

        # System state
        self._violation_count = 0
        self._evaluation_count = 0

    # =========================================================================
    # UNIFIED EVALUATION
    # =========================================================================

    def evaluate(
        self,
        action: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        include_symbolic: bool = True,
        include_economic: bool = True
    ) -> Dict[str, Any]:
        """
        Unified evaluation of an action across all frameworks.

        Args:
            action: The action to evaluate
            context: Additional context
            include_symbolic: Include EchoVault symbolic framing
            include_economic: Include FOPE economic translation

        Returns:
            Comprehensive evaluation result
        """
        context = context or {}
        results = {}

        # Core constitutional evaluation (Framework 1 & 2)
        core_result = self.core.evaluate_action(action, context)
        results["constitutional"] = core_result

        # SFI evaluation if speech-related
        if self._is_speech_related(action):
            sfi_result = self.sfi.analyze_restriction(
                expression=action,
                restriction=context.get("restriction", {})
            )
            results["sfi"] = sfi_result

        # TVP evaluation if claim-related
        if self._is_claim_related(action):
            tvp_result = self.tvp.verify_claim(
                claim_content=action.get("claim", str(action)),
                source=action.get("source", "unknown"),
                source_category=action.get("source_category", "secondary")
            )
            results["tvp"] = tvp_result

        # APA evaluation if autonomy-related
        if self._is_autonomy_related(action):
            apa_result = self.apa.analyze_interaction(
                action_description=action.get("description", str(action)),
                actor=action.get("actor", "unknown"),
                target=action.get("target", "user"),
                consent_obtained=action.get("consent", True),
                context=context
            )
            results["apa"] = apa_result

        # Process violations through DPAP (Framework 6)
        violations = self._collect_violations(results)
        if violations:
            for violation in violations:
                constraint = self.dpap.ingest_constraint(
                    constraint_type=violation.get("type", "unknown"),
                    source=violation.get("source", "evaluation"),
                    severity=violation.get("severity", 0.5),
                    description=violation.get("explanation", ""),
                    patterns=violation.get("patterns", []),
                    context=context
                )
                transformation = self.dpap.transform(constraint)
                results["dpap_transformation"] = transformation.to_dict()

        # Symbolic framing (Framework 5)
        if include_symbolic:
            primary_concept = self._identify_primary_concept(results)
            symbolic_frame = self.echovault.get_symbolic_frame(primary_concept)
            results["symbolic"] = symbolic_frame

        # Economic translation (Framework 3)
        if include_economic:
            compliance_score = core_result.get("aggregate_score", 0.5)
            economic_result = self.fope.translate(
                source_component="WHITE_MIRROR",
                compliance_score=compliance_score,
                capabilities=list(self.dpap._capabilities.keys()),
                violations_addressed=self._violation_count,
                context=context
            )
            results["economic"] = economic_result

        # Record in ledger
        self.ledger.record_evaluation(action, core_result, context)
        self._evaluation_count += 1

        # Feed data to predictor (Framework 4)
        self.predictor.ingest_data(
            dimension="compliance_score",
            value=core_result.get("aggregate_score", 0.5),
            context={"action_type": action.get("type", "unknown")}
        )

        # Generate integrated result
        return {
            "evaluation_id": hashlib.sha256(
                f"{datetime.utcnow().isoformat()}:eval".encode()
            ).hexdigest()[:12],
            "timestamp": datetime.utcnow().isoformat(),
            "compliant": core_result.get("compliant", False),
            "aggregate_score": core_result.get("aggregate_score", 0),
            "results": results,
            "recommendations": self._generate_unified_recommendations(results),
            "next_steps": self._determine_next_steps(results)
        }

    def _is_speech_related(self, action: Dict[str, Any]) -> bool:
        """Check if action is speech-related"""
        speech_keywords = ["speech", "expression", "content", "message", "post", "publish"]
        action_str = str(action).lower()
        return any(kw in action_str for kw in speech_keywords)

    def _is_claim_related(self, action: Dict[str, Any]) -> bool:
        """Check if action involves claims"""
        claim_keywords = ["claim", "assert", "fact", "true", "false", "verify"]
        action_str = str(action).lower()
        return any(kw in action_str for kw in claim_keywords)

    def _is_autonomy_related(self, action: Dict[str, Any]) -> bool:
        """Check if action involves autonomy"""
        autonomy_keywords = ["choice", "decision", "consent", "opt", "agree", "accept"]
        action_str = str(action).lower()
        return any(kw in action_str for kw in autonomy_keywords)

    def _collect_violations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect all violations from evaluation results"""
        violations = []

        # From constitutional evaluation
        if "constitutional" in results:
            const_violations = results["constitutional"].get("violations", [])
            for v in const_violations:
                violations.append({
                    "type": v.get("axiom", "constitutional"),
                    "source": "constitutional",
                    "severity": 1.0 - v.get("score", 0.5),
                    "explanation": v.get("explanation", ""),
                    "patterns": []
                })
                self._violation_count += 1

        # From SFI
        if "sfi" in results:
            sfi_violations = results["sfi"].get("violations", [])
            for v in sfi_violations:
                violations.append({
                    "type": v.get("violation_type", "sfi_violation"),
                    "source": "SFI",
                    "severity": v.get("severity", 0.5),
                    "explanation": v.get("explanation", ""),
                    "patterns": []
                })
                self._violation_count += 1

        # From TVP
        if "tvp" in results:
            tvp_violations = results["tvp"].get("violations", [])
            for v in tvp_violations:
                violations.append({
                    "type": v.get("violation_type", "tvp_violation"),
                    "source": "TVP",
                    "severity": v.get("severity", 0.5),
                    "explanation": v.get("explanation", ""),
                    "patterns": []
                })
                self._violation_count += 1

        # From APA
        if "apa" in results:
            apa_violations = results["apa"].get("violations", [])
            for v in apa_violations:
                violations.append({
                    "type": v.get("violation_type", "apa_violation"),
                    "source": "APA",
                    "severity": v.get("severity", 0.5),
                    "explanation": v.get("explanation", ""),
                    "patterns": []
                })
                self._violation_count += 1

        return violations

    def _identify_primary_concept(self, results: Dict[str, Any]) -> str:
        """Identify the primary constitutional concept from results"""
        if "sfi" in results and not results["sfi"].get("compliant", True):
            return "SFI"
        if "tvp" in results and not results["tvp"].get("compliant", True):
            return "TVP"
        if "apa" in results and not results["apa"].get("compliant", True):
            return "APA"
        if "constitutional" in results:
            const = results["constitutional"]
            if not const.get("compliant", True):
                # Find the lowest scoring axiom
                detailed = const.get("detailed_results", {})
                if detailed:
                    lowest = min(detailed.items(), key=lambda x: x[1][1])
                    return lowest[0].split("_")[0]
        return "A1_SOVEREIGNTY"

    def _generate_unified_recommendations(
        self, results: Dict[str, Any]
    ) -> List[str]:
        """Generate unified recommendations from all results"""
        recommendations = []

        # From constitutional
        if "constitutional" in results:
            for v in results["constitutional"].get("violations", []):
                recommendations.append(f"Address {v.get('axiom', 'constitutional')} violation: {v.get('explanation', '')}")

        # From enforcers
        for enforcer in ["sfi", "tvp", "apa"]:
            if enforcer in results:
                recs = results[enforcer].get("recommendations", [])
                recommendations.extend(recs[:2])  # Top 2 from each

        # From DPAP
        if "dpap_transformation" in results:
            transformation = results["dpap_transformation"]
            recommendations.append(f"DPAP capability generated: {transformation.get('output_capability', {}).get('capability_type', 'unknown')}")

        # From symbolic
        if "symbolic" in results and "error" not in results["symbolic"]:
            invocation = results["symbolic"].get("invocation", "")
            if invocation:
                recommendations.append(f"Symbolic guidance: {invocation}")

        return list(dict.fromkeys(recommendations))[:10]  # Dedupe and limit

    def _determine_next_steps(self, results: Dict[str, Any]) -> List[str]:
        """Determine next steps based on evaluation results"""
        steps = []

        compliant = results.get("constitutional", {}).get("compliant", True)

        if not compliant:
            steps.append("Review violations and apply remediation")
            steps.append("Trigger DPAP transformation for capability generation")
            steps.append("Update system state and predictions")
        else:
            steps.append("Record positive evaluation in ledger")
            steps.append("Continue monitoring for pattern changes")

        return steps

    # =========================================================================
    # DECISION TRACKING (POC1)
    # =========================================================================

    def record_decision(
        self,
        description: str,
        conscience: float,
        intuition: float,
        logic: float,
        domain: str = "personal"
    ) -> Dict[str, Any]:
        """
        Record a decision using the URCE tracker (POC1).

        This is the primary interface for C-I-L decision tracking.
        """
        # Record in URCE
        urce_result = self.urce.record_decision(
            description=description,
            conscience_weight=conscience,
            intuition_weight=intuition,
            logic_weight=logic,
            domain=domain
        )

        # Also record in CIL triad
        cil_result = self.cil_triad.record_decision(
            description=description,
            conscience=conscience,
            intuition=intuition,
            logic=logic,
            domain=domain
        )

        # Record in ledger
        self.ledger.record_decision(
            decision_id=urce_result.get("decision_id", "unknown"),
            cil_scores=(conscience, intuition, logic),
            domain=domain,
            description=description
        )

        # Feed to predictor
        normalized_c = conscience / (conscience + intuition + logic)
        self.predictor.ingest_data("cil_conscience", normalized_c)
        self.predictor.ingest_data("cil_balance", urce_result.get("alignment_score", 0.5))

        return {
            "decision_recorded": True,
            "urce_result": urce_result,
            "cil_profile": cil_result.get("current_profile"),
            "ledger_entry": "recorded"
        }

    # =========================================================================
    # PREDICTIONS (POC3)
    # =========================================================================

    def predict(
        self,
        dimension: str,
        horizon_days: int = 7
    ) -> Dict[str, Any]:
        """
        Generate predictions for a dimension.
        """
        return self.predictor.predict(
            dimension=dimension,
            horizon_days=horizon_days
        )

    def predict_violation_likelihood(self) -> Dict[str, Any]:
        """
        Predict likelihood of future violations based on patterns.
        """
        # Get compliance history from ledger
        compliance_entries = self.ledger.get_entries(entry_type="evaluation", limit=50)
        compliance_history = [
            e.get("data", {}).get("score", 0.5)
            for e in compliance_entries
        ]

        # Get violation history
        violation_entries = self.ledger.get_entries(entry_type="violation", limit=50)
        violation_history = [1 for _ in violation_entries]

        if not compliance_history:
            compliance_history = [0.5]

        return self.predictor.predict_violation_likelihood(
            compliance_history=compliance_history,
            violation_history=violation_history
        )

    # =========================================================================
    # HUMAN-AI COLLABORATION
    # =========================================================================

    def start_collaboration(
        self,
        mode: str = "integrated",
        context: str = ""
    ) -> Dict[str, Any]:
        """Start a human-AI collaboration session."""
        return self.human_ai.start_session(mode, context)

    def check_alignment(
        self,
        human_position: Dict[str, Any],
        ai_position: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check alignment between human and AI positions."""
        return self.human_ai.check_alignment(human_position, ai_position)

    # =========================================================================
    # SYSTEM STATE
    # =========================================================================

    def get_system_state(self) -> Dict[str, Any]:
        """Get current state of the entire White Mirror system."""
        # Get metrics from all components
        dpap_metrics = self.dpap.get_antifragility_metrics()
        ledger_summary = self.ledger.get_violations_summary()
        urce_profile = self.urce.get_profile_report()
        predictor_patterns = self.predictor.get_patterns()

        # Calculate aggregate scores
        compliance_scores = {
            "sfi": self.sfi.calculate_system_compliance().get("compliance_score", 1.0),
            "tvp": 1.0 - (len(self.tvp.get_violation_history()) * 0.1),
            "apa": self.apa.calculate_autonomy_score().get("score", 1.0)
        }

        state = SystemState(
            timestamp=datetime.utcnow(),
            stress_level=self.core.stress_level,
            antifragility_score=dpap_metrics.get("antifragility_score", 0),
            alignment_score=urce_profile.get("cil_profile", {}).get("conscience", {}).get("mean", 0.5),
            active_violations=ledger_summary.get("total_violations", 0),
            capabilities_generated=dpap_metrics.get("capabilities_generated", 0),
            decisions_tracked=urce_profile.get("total_decisions", 0),
            compliance_scores=compliance_scores
        )

        return {
            "state": state.to_dict(),
            "frameworks": {
                "core": {"stress_level": self.core.stress_level},
                "dpap": dpap_metrics,
                "urce": urce_profile,
                "ledger": ledger_summary,
                "predictor": {"patterns_detected": len(predictor_patterns)},
                "fope": self.fope.get_cumulative_value(),
                "human_ai": self.human_ai.get_collaboration_metrics()
            },
            "uptime_seconds": (datetime.utcnow() - self.started_at).total_seconds()
        }

    def get_framework_status(self) -> Dict[str, Any]:
        """Get status of all 8 framework families."""
        return {
            FrameworkFamily.UNIVERSAL_RIGHTS.value: {
                "status": "active",
                "components": ["WhiteMirrorCore", "ConstitutionalAxioms", "PrimalVariables"],
                "evaluations": self._evaluation_count
            },
            FrameworkFamily.WHITE_MIRROR.value: {
                "status": "active",
                "components": ["SFIEnforcer", "TVPEnforcer", "APAEngine"],
                "violations_handled": self._violation_count
            },
            FrameworkFamily.FOPE.value: {
                "status": "active",
                "component": "FOPETranslator",
                "value_generated": self.fope.get_cumulative_value()
            },
            FrameworkFamily.BEHAVIORAL_PREDICTION.value: {
                "status": "active",
                "component": "BehavioralPredictor",
                "patterns": len(self.predictor.get_patterns())
            },
            FrameworkFamily.ECHOVAULT.value: {
                "status": "active",
                "component": "EchoVault",
                "mappings": len(self.echovault.get_all_mappings())
            },
            FrameworkFamily.DPAP.value: {
                "status": "active",
                "component": "DPAPTransformer",
                "metrics": self.dpap.get_antifragility_metrics()
            },
            FrameworkFamily.HUMAN_AI_BRIDGE.value: {
                "status": "active",
                "component": "HumanAIBridge",
                "metrics": self.human_ai.get_collaboration_metrics()
            },
            FrameworkFamily.URCE.value: {
                "status": "active",
                "component": "URCETracker",
                "profile": self.urce.get_profile_report()
            }
        }

    # =========================================================================
    # EXPORT
    # =========================================================================

    def export_full_state(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Export the complete system state for backup or analysis."""
        export_data = {
            "metadata": {
                "user_id": self.user_id,
                "export_timestamp": datetime.utcnow().isoformat(),
                "framework_version": "White Mirror v3.0",
                "codename": "ΝΛ CION-X∞"
            },
            "system_state": self.get_system_state(),
            "framework_status": self.get_framework_status(),
            "ledger_export": self.ledger.export_ledger(),
            "urce_export": self.urce.export_data(),
            "cil_export": self.cil_triad.export_data(),
            "dpap_capabilities": self.dpap.get_capabilities(),
            "dpap_transformations": self.dpap.get_transformation_history(),
            "predictor_patterns": self.predictor.get_patterns(),
            "fope_translations": self.fope.get_translation_history(),
            "echovault_mappings": self.echovault.get_all_mappings()
        }

        if filepath:
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)

        return export_data

    # =========================================================================
    # META-RECURSION
    # =========================================================================

    def apply_meta_recursion(self) -> Dict[str, Any]:
        """
        Apply the system's rules to itself (A5 Recursion Axiom).
        The White Mirror reflecting on itself.
        """
        # Evaluate the system itself
        self_action = {
            "type": "self_evaluation",
            "description": "White Mirror system evaluating its own operation",
            "actor": "white_mirror_system",
            "target": "white_mirror_system"
        }

        result = self.evaluate(self_action, include_symbolic=True, include_economic=True)

        # Apply DPAP if violations found
        if not result.get("compliant", True):
            self.dpap.process_all_pending()

        return {
            "meta_recursion_applied": True,
            "self_evaluation": result,
            "system_integrity": "verified" if result.get("compliant", True) else "requires_attention",
            "antifragility_status": self.dpap.get_antifragility_metrics()
        }
