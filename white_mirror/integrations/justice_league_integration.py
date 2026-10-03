"""
Justice League Integration - Multi-AI Framework Connector

Integrates White Mirror constitutional framework with the
Multi-AI Justice League coordination system.

This integration ensures that all AI-coordinated operations
are subject to constitutional compliance checking.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from multi_ai_framework.core.ai_coordinator import AIJusticeLeague
    from multi_ai_framework.analysis.strategic_analyzer import StrategicAnalyzer
    JUSTICE_LEAGUE_AVAILABLE = True
except ImportError:
    JUSTICE_LEAGUE_AVAILABLE = False

from ..orchestrator import WhiteMirrorOrchestrator


@dataclass
class ConstitutionalMissionResult:
    """Result of a constitutionally-verified mission"""
    mission_id: str
    constitutional_compliance: bool
    compliance_score: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    original_result: Dict[str, Any]
    timestamp: datetime


class JusticeLeagueIntegration:
    """
    Integrates White Mirror with Multi-AI Justice League

    Provides constitutional compliance layer for all AI-coordinated
    operations, ensuring that multi-AI campaigns adhere to
    constitutional principles.
    """

    def __init__(self, orchestrator: Optional[WhiteMirrorOrchestrator] = None):
        self.orchestrator = orchestrator or WhiteMirrorOrchestrator()
        self.justice_league_available = JUSTICE_LEAGUE_AVAILABLE
        self._mission_history: List[ConstitutionalMissionResult] = []

    def verify_mission_constitutional_compliance(
        self,
        mission_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify that a mission configuration complies with constitutional principles.

        Args:
            mission_config: Mission configuration to verify

        Returns:
            Compliance verification result
        """
        # Extract key elements from mission config
        action = {
            "type": "mission_execution",
            "description": mission_config.get("mission_name", "Unknown Mission"),
            "actor": "multi_ai_justice_league",
            "target": mission_config.get("target", {}).get("name", "Unknown Target"),
            "context": mission_config
        }

        # Check for specific constitutional concerns

        # 1. Check speech-related actions
        if self._involves_speech_actions(mission_config):
            action["speech_related"] = True

        # 2. Check truth verification requirements
        claims = self._extract_claims(mission_config)
        if claims:
            action["claims"] = claims

        # 3. Check autonomy considerations
        if self._involves_autonomy_actions(mission_config):
            action["autonomy_related"] = True
            action["consent"] = mission_config.get("consent_obtained", False)

        # Run unified evaluation
        result = self.orchestrator.evaluate(
            action=action,
            context={"mission_type": "justice_league"},
            include_symbolic=True,
            include_economic=True
        )

        # Generate mission-specific guidance
        guidance = self._generate_mission_guidance(result, mission_config)

        return {
            "mission_name": mission_config.get("mission_name"),
            "constitutional_compliance": result.get("compliant", False),
            "compliance_score": result.get("aggregate_score", 0),
            "evaluation_details": result,
            "guidance": guidance,
            "proceed_recommendation": result.get("compliant", False),
            "required_modifications": self._get_required_modifications(result)
        }

    def _involves_speech_actions(self, config: Dict[str, Any]) -> bool:
        """Check if mission involves speech-related actions"""
        speech_keywords = ["media", "press", "statement", "report", "publish", "expose"]
        config_str = str(config).lower()
        return any(kw in config_str for kw in speech_keywords)

    def _extract_claims(self, config: Dict[str, Any]) -> List[str]:
        """Extract claims from mission configuration"""
        claims = []
        # Look for evidence, violations, or assertions
        if "violations" in config:
            for v in config.get("violations", []):
                if isinstance(v, dict):
                    claims.append(v.get("description", str(v)))
                else:
                    claims.append(str(v))
        if "evidence" in config:
            for e in config.get("evidence", []):
                if isinstance(e, dict):
                    claims.append(e.get("description", str(e)))
        return claims

    def _involves_autonomy_actions(self, config: Dict[str, Any]) -> bool:
        """Check if mission involves autonomy-related actions"""
        autonomy_keywords = ["negotiation", "settlement", "demand", "pressure"]
        config_str = str(config).lower()
        return any(kw in config_str for kw in autonomy_keywords)

    def _generate_mission_guidance(
        self,
        result: Dict[str, Any],
        config: Dict[str, Any]
    ) -> List[str]:
        """Generate mission-specific constitutional guidance"""
        guidance = []

        # Get symbolic guidance if available
        symbolic = result.get("results", {}).get("symbolic", {})
        if symbolic and "error" not in symbolic:
            invocation = symbolic.get("invocation", "")
            if invocation:
                guidance.append(f"Guiding principle: {invocation}")

        # Add compliance-specific guidance
        if not result.get("compliant", True):
            guidance.append("Mission requires modifications before proceeding")
            guidance.extend(result.get("recommendations", []))
        else:
            guidance.append("Mission cleared for constitutional compliance")
            guidance.append("Maintain documentation for Rights Ledger")

        return guidance

    def _get_required_modifications(
        self, result: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Get required modifications for compliance"""
        modifications = []

        violations = result.get("results", {}).get("constitutional", {}).get("violations", [])

        for v in violations:
            modifications.append({
                "area": v.get("axiom", "constitutional"),
                "issue": v.get("explanation", "Compliance issue detected"),
                "required_action": "Review and modify to address violation"
            })

        return modifications

    def wrap_justice_league_operation(
        self,
        operation_func,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Wrap a Justice League operation with constitutional compliance.

        This decorator-style wrapper ensures any operation is checked
        before and after execution.

        Args:
            operation_func: The Justice League function to wrap
            *args, **kwargs: Arguments to pass to the function

        Returns:
            Result with constitutional compliance verification
        """
        # Pre-execution check
        pre_check_action = {
            "type": "operation_pre_check",
            "description": f"Pre-execution check for {operation_func.__name__}",
            "operation": operation_func.__name__,
            "args_summary": str(args)[:200]
        }

        pre_result = self.orchestrator.evaluate(pre_check_action)

        if not pre_result.get("compliant", True):
            return {
                "blocked": True,
                "reason": "Pre-execution constitutional check failed",
                "compliance_result": pre_result
            }

        # Execute operation
        try:
            operation_result = operation_func(*args, **kwargs)
        except Exception as e:
            return {
                "error": True,
                "exception": str(e),
                "pre_check_passed": True
            }

        # Post-execution check
        post_check_action = {
            "type": "operation_post_check",
            "description": f"Post-execution check for {operation_func.__name__}",
            "operation": operation_func.__name__,
            "result_summary": str(operation_result)[:500]
        }

        post_result = self.orchestrator.evaluate(post_check_action)

        return {
            "operation_result": operation_result,
            "pre_check": {"compliant": pre_result.get("compliant", True)},
            "post_check": {"compliant": post_result.get("compliant", True)},
            "constitutional_verified": True
        }

    def create_constitutional_campaign(
        self,
        campaign_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a constitutionally-verified campaign.

        This is the primary interface for creating campaigns that
        are guaranteed to comply with White Mirror principles.

        Args:
            campaign_config: Campaign configuration

        Returns:
            Constitutional campaign setup
        """
        # Verify compliance
        compliance = self.verify_mission_constitutional_compliance(campaign_config)

        if not compliance.get("constitutional_compliance", False):
            return {
                "created": False,
                "reason": "Campaign does not meet constitutional requirements",
                "compliance_result": compliance,
                "required_modifications": compliance.get("required_modifications", [])
            }

        # Record in Rights Ledger
        self.orchestrator.ledger.add_entry(
            entry_type="system_event",
            data={
                "event_type": "campaign_created",
                "campaign_name": campaign_config.get("mission_name"),
                "compliance_score": compliance.get("compliance_score"),
                "verified_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "created": True,
            "campaign_name": campaign_config.get("mission_name"),
            "constitutional_verification": compliance,
            "ledger_recorded": True,
            "guidance": compliance.get("guidance", [])
        }

    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of the Justice League integration"""
        return {
            "justice_league_available": self.justice_league_available,
            "orchestrator_active": True,
            "missions_processed": len(self._mission_history),
            "ledger_entries": self.orchestrator.ledger.entry_count,
            "system_state": self.orchestrator.get_system_state()
        }
