"""
URCE Tracker - Unified Recursive Consciousness Engine (Personal)

The URCE Tracker is the personal implementation of the White Mirror
framework. It tracks individual consciousness alignment through:
    - C-I-L decision tracking (POC1)
    - Personal precommitment protocols
    - Drift detection and correction
    - Consciousness optimization recommendations

This is the individual-scale instantiation of the collective
White Mirror architecture.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json
import statistics


class ConsciousnessState(Enum):
    """States of consciousness alignment"""
    INTEGRATED = "integrated"       # All systems aligned
    DRIFTING = "drifting"          # Beginning to lose alignment
    FRAGMENTED = "fragmented"       # Significant misalignment
    RECOVERING = "recovering"       # In process of realignment
    OPTIMIZING = "optimizing"       # Actively improving


class DriftType(Enum):
    """Types of consciousness drift"""
    CONSCIENCE_NEGLECT = "conscience_neglect"  # Ignoring ethical dimension
    INTUITION_OVERRIDE = "intuition_override"  # Over-relying on gut
    LOGIC_DOMINANCE = "logic_dominance"        # Pure rationalism
    TEMPORAL_MYOPIA = "temporal_myopia"        # Short-term focus
    VALUE_EROSION = "value_erosion"            # Core values weakening


@dataclass
class ConsciousnessSnapshot:
    """A snapshot of consciousness state at a moment in time"""
    timestamp: datetime
    cil_balance: Tuple[float, float, float]  # (C, I, L)
    alignment_score: float
    active_precommitments: int
    recent_decision_count: int
    drift_indicators: List[str]
    state: ConsciousnessState

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "cil_balance": {
                "conscience": self.cil_balance[0],
                "intuition": self.cil_balance[1],
                "logic": self.cil_balance[2]
            },
            "alignment_score": self.alignment_score,
            "active_precommitments": self.active_precommitments,
            "recent_decision_count": self.recent_decision_count,
            "drift_indicators": self.drift_indicators,
            "state": self.state.value
        }


@dataclass
class URCEPrecommitment:
    """A precommitment in the URCE system"""
    id: str
    principle: str
    trigger_condition: str
    intended_response: str
    cil_weights: Tuple[float, float, float]
    created_at: datetime
    last_invoked: Optional[datetime] = None
    invocation_count: int = 0
    success_rate: float = 1.0
    active: bool = True


@dataclass
class OptimizationRecommendation:
    """A recommendation for consciousness optimization"""
    id: str
    category: str
    recommendation: str
    priority: float  # 0-1
    estimated_impact: float  # 0-1
    implementation_steps: List[str]
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "recommendation": self.recommendation,
            "priority": self.priority,
            "estimated_impact": self.estimated_impact,
            "implementation_steps": self.implementation_steps,
            "timestamp": self.timestamp.isoformat()
        }


class URCETracker:
    """
    URCE (Unified Recursive Consciousness Engine) Personal Tracker

    The individual-scale implementation of White Mirror for personal
    consciousness optimization and alignment tracking.
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self._decisions: List[Dict[str, Any]] = []
        self._precommitments: Dict[str, URCEPrecommitment] = {}
        self._snapshots: List[ConsciousnessSnapshot] = []
        self._recommendations: List[OptimizationRecommendation] = []
        self._current_state = ConsciousnessState.INTEGRATED

        # Configuration
        self._statistical_validity_threshold = 30
        self._snapshot_interval_hours = 24
        self._drift_threshold = 0.15

    def record_decision(
        self,
        description: str,
        conscience_weight: float,
        intuition_weight: float,
        logic_weight: float,
        domain: str = "personal",
        outcome: Optional[str] = None,
        satisfaction: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Record a decision with C-I-L analysis.

        Args:
            description: What the decision was about
            conscience_weight: How much ethics influenced (0-1)
            intuition_weight: How much intuition influenced (0-1)
            logic_weight: How much logic influenced (0-1)
            domain: Decision domain
            outcome: Optional outcome description
            satisfaction: Optional satisfaction score (0-1)

        Returns:
            Decision record with analysis
        """
        # Normalize weights
        total = conscience_weight + intuition_weight + logic_weight
        if total > 0:
            c, i, l = conscience_weight/total, intuition_weight/total, logic_weight/total
        else:
            c, i, l = 0.33, 0.33, 0.34

        decision_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{description}".encode()
        ).hexdigest()[:12]

        decision = {
            "id": decision_id,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description,
            "cil_weights": {"C": c, "I": i, "L": l},
            "domain": domain,
            "outcome": outcome,
            "satisfaction": satisfaction
        }

        self._decisions.append(decision)

        # Check precommitments
        triggered_precommitments = self._check_precommitments(description)

        # Calculate alignment
        alignment = self._calculate_decision_alignment(c, i, l)

        # Update state if needed
        self._update_state()

        return {
            "decision_id": decision_id,
            "recorded": True,
            "cil_normalized": {"C": c, "I": i, "L": l},
            "alignment_score": alignment,
            "triggered_precommitments": triggered_precommitments,
            "current_state": self._current_state.value,
            "decisions_until_valid": max(0, self._statistical_validity_threshold - len(self._decisions))
        }

    def add_precommitment(
        self,
        principle: str,
        trigger_condition: str,
        intended_response: str,
        conscience_weight: float = 0.4,
        intuition_weight: float = 0.3,
        logic_weight: float = 0.3
    ) -> URCEPrecommitment:
        """
        Add a precommitment to the URCE system.

        Precommitments are decisions made in advance for future scenarios,
        helping maintain alignment under pressure.
        """
        precommitment_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{principle}".encode()
        ).hexdigest()[:12]

        # Normalize weights
        total = conscience_weight + intuition_weight + logic_weight
        c, i, l = conscience_weight/total, intuition_weight/total, logic_weight/total

        precommitment = URCEPrecommitment(
            id=precommitment_id,
            principle=principle,
            trigger_condition=trigger_condition,
            intended_response=intended_response,
            cil_weights=(c, i, l),
            created_at=datetime.utcnow()
        )

        self._precommitments[precommitment_id] = precommitment
        return precommitment

    def _check_precommitments(self, context: str) -> List[Dict[str, Any]]:
        """Check if any precommitments are triggered by current context"""
        triggered = []
        context_lower = context.lower()

        for precommitment in self._precommitments.values():
            if not precommitment.active:
                continue

            trigger_lower = precommitment.trigger_condition.lower()
            # Simple keyword matching
            trigger_words = set(trigger_lower.split())
            context_words = set(context_lower.split())

            if trigger_words & context_words:
                precommitment.last_invoked = datetime.utcnow()
                precommitment.invocation_count += 1
                triggered.append({
                    "id": precommitment.id,
                    "principle": precommitment.principle,
                    "intended_response": precommitment.intended_response
                })

        return triggered

    def _calculate_decision_alignment(self, c: float, i: float, l: float) -> float:
        """Calculate alignment score for a decision's C-I-L weights"""
        # Perfect alignment = balanced weights
        # Score decreases with imbalance
        mean = (c + i + l) / 3
        variance = ((c - mean)**2 + (i - mean)**2 + (l - mean)**2) / 3
        return 1.0 - min(1.0, variance * 3)

    def _update_state(self):
        """Update consciousness state based on recent patterns"""
        if len(self._decisions) < 5:
            return

        recent = self._decisions[-10:]
        c_vals = [d["cil_weights"]["C"] for d in recent]
        i_vals = [d["cil_weights"]["I"] for d in recent]
        l_vals = [d["cil_weights"]["L"] for d in recent]

        c_mean, i_mean, l_mean = statistics.mean(c_vals), statistics.mean(i_vals), statistics.mean(l_vals)

        # Check for drift
        max_val = max(c_mean, i_mean, l_mean)
        min_val = min(c_mean, i_mean, l_mean)

        if max_val - min_val > 0.3:
            self._current_state = ConsciousnessState.FRAGMENTED
        elif max_val - min_val > self._drift_threshold:
            self._current_state = ConsciousnessState.DRIFTING
        else:
            if self._current_state in [ConsciousnessState.FRAGMENTED, ConsciousnessState.DRIFTING]:
                self._current_state = ConsciousnessState.RECOVERING
            else:
                self._current_state = ConsciousnessState.INTEGRATED

    def take_snapshot(self) -> ConsciousnessSnapshot:
        """Take a snapshot of current consciousness state"""
        recent_window = timedelta(days=7)
        cutoff = datetime.utcnow() - recent_window

        recent_decisions = [
            d for d in self._decisions
            if datetime.fromisoformat(d["timestamp"]) > cutoff
        ]

        if not recent_decisions:
            cil_balance = (0.33, 0.33, 0.34)
            alignment = 0.5
        else:
            c_vals = [d["cil_weights"]["C"] for d in recent_decisions]
            i_vals = [d["cil_weights"]["I"] for d in recent_decisions]
            l_vals = [d["cil_weights"]["L"] for d in recent_decisions]

            cil_balance = (
                statistics.mean(c_vals),
                statistics.mean(i_vals),
                statistics.mean(l_vals)
            )
            alignment = self._calculate_decision_alignment(*cil_balance)

        # Detect drift indicators
        drift_indicators = self._detect_drift_indicators(cil_balance)

        snapshot = ConsciousnessSnapshot(
            timestamp=datetime.utcnow(),
            cil_balance=cil_balance,
            alignment_score=alignment,
            active_precommitments=sum(1 for p in self._precommitments.values() if p.active),
            recent_decision_count=len(recent_decisions),
            drift_indicators=drift_indicators,
            state=self._current_state
        )

        self._snapshots.append(snapshot)
        return snapshot

    def _detect_drift_indicators(self, cil_balance: Tuple[float, float, float]) -> List[str]:
        """Detect drift indicators from C-I-L balance"""
        c, i, l = cil_balance
        indicators = []

        if c < 0.25:
            indicators.append(DriftType.CONSCIENCE_NEGLECT.value)
        if i > 0.5:
            indicators.append(DriftType.INTUITION_OVERRIDE.value)
        if l > 0.5:
            indicators.append(DriftType.LOGIC_DOMINANCE.value)

        return indicators

    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations based on current state"""
        recommendations = []

        if len(self._decisions) < self._statistical_validity_threshold:
            recommendations.append(self._create_recommendation(
                category="data_collection",
                recommendation=f"Record {self._statistical_validity_threshold - len(self._decisions)} more decisions for statistically valid analysis",
                priority=0.9,
                estimated_impact=0.8,
                steps=["Continue tracking decisions across different domains", "Include both major and minor decisions"]
            ))
            return [r.to_dict() for r in recommendations]

        # Analyze patterns
        snapshot = self.take_snapshot() if not self._snapshots else self._snapshots[-1]

        # State-based recommendations
        if self._current_state == ConsciousnessState.FRAGMENTED:
            recommendations.append(self._create_recommendation(
                category="integration",
                recommendation="Focus on reintegrating C-I-L dimensions through reflective practices",
                priority=0.95,
                estimated_impact=0.9,
                steps=[
                    "Set aside 15 minutes daily for decision reflection",
                    "Review recent decisions and identify imbalances",
                    "Practice decisions that honor all three dimensions"
                ]
            ))

        elif self._current_state == ConsciousnessState.DRIFTING:
            # Specific recommendations based on drift type
            for indicator in snapshot.drift_indicators:
                if indicator == DriftType.CONSCIENCE_NEGLECT.value:
                    recommendations.append(self._create_recommendation(
                        category="conscience",
                        recommendation="Strengthen conscience dimension in decision-making",
                        priority=0.85,
                        estimated_impact=0.7,
                        steps=[
                            "Before decisions, ask 'What would my best self do?'",
                            "Consider long-term ethical implications",
                            "Reconnect with core values through journaling"
                        ]
                    ))
                elif indicator == DriftType.LOGIC_DOMINANCE.value:
                    recommendations.append(self._create_recommendation(
                        category="balance",
                        recommendation="Balance analytical thinking with other dimensions",
                        priority=0.8,
                        estimated_impact=0.6,
                        steps=[
                            "Practice trusting intuition in low-stakes decisions",
                            "Notice when over-analysis leads to paralysis",
                            "Set time limits on analytical deliberation"
                        ]
                    ))

        # Precommitment recommendations
        if len(self._precommitments) < 3:
            recommendations.append(self._create_recommendation(
                category="precommitment",
                recommendation="Establish more precommitments for challenging scenarios",
                priority=0.7,
                estimated_impact=0.65,
                steps=[
                    "Identify recurring decision challenges",
                    "Define clear principles for each challenge type",
                    "Create precommitments with specific trigger conditions"
                ]
            ))

        self._recommendations = recommendations
        return [r.to_dict() for r in recommendations]

    def _create_recommendation(
        self,
        category: str,
        recommendation: str,
        priority: float,
        estimated_impact: float,
        steps: List[str]
    ) -> OptimizationRecommendation:
        """Create an optimization recommendation"""
        rec_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{recommendation}".encode()
        ).hexdigest()[:12]

        return OptimizationRecommendation(
            id=rec_id,
            category=category,
            recommendation=recommendation,
            priority=priority,
            estimated_impact=estimated_impact,
            implementation_steps=steps,
            timestamp=datetime.utcnow()
        )

    def get_profile_report(self) -> Dict[str, Any]:
        """Generate comprehensive URCE profile report"""
        if not self._decisions:
            return {
                "user_id": self.user_id,
                "status": "insufficient_data",
                "decisions_recorded": 0,
                "decisions_needed": self._statistical_validity_threshold
            }

        c_vals = [d["cil_weights"]["C"] for d in self._decisions]
        i_vals = [d["cil_weights"]["I"] for d in self._decisions]
        l_vals = [d["cil_weights"]["L"] for d in self._decisions]

        # Domain analysis
        domains = {}
        for d in self._decisions:
            domain = d.get("domain", "unknown")
            if domain not in domains:
                domains[domain] = {"count": 0, "C": [], "I": [], "L": []}
            domains[domain]["count"] += 1
            domains[domain]["C"].append(d["cil_weights"]["C"])
            domains[domain]["I"].append(d["cil_weights"]["I"])
            domains[domain]["L"].append(d["cil_weights"]["L"])

        domain_profiles = {}
        for domain, data in domains.items():
            domain_profiles[domain] = {
                "decision_count": data["count"],
                "cil_means": {
                    "C": statistics.mean(data["C"]),
                    "I": statistics.mean(data["I"]),
                    "L": statistics.mean(data["L"])
                }
            }

        return {
            "user_id": self.user_id,
            "status": "valid" if len(self._decisions) >= self._statistical_validity_threshold else "building",
            "total_decisions": len(self._decisions),
            "statistically_valid": len(self._decisions) >= self._statistical_validity_threshold,
            "current_state": self._current_state.value,
            "cil_profile": {
                "conscience": {
                    "mean": statistics.mean(c_vals),
                    "std": statistics.stdev(c_vals) if len(c_vals) > 1 else 0
                },
                "intuition": {
                    "mean": statistics.mean(i_vals),
                    "std": statistics.stdev(i_vals) if len(i_vals) > 1 else 0
                },
                "logic": {
                    "mean": statistics.mean(l_vals),
                    "std": statistics.stdev(l_vals) if len(l_vals) > 1 else 0
                }
            },
            "domain_profiles": domain_profiles,
            "active_precommitments": sum(1 for p in self._precommitments.values() if p.active),
            "snapshots_taken": len(self._snapshots),
            "optimization_available": len(self._decisions) >= self._statistical_validity_threshold
        }

    def export_data(self) -> Dict[str, Any]:
        """Export all URCE data"""
        return {
            "metadata": {
                "user_id": self.user_id,
                "export_timestamp": datetime.utcnow().isoformat(),
                "framework_version": "URCE_v1.0"
            },
            "profile": self.get_profile_report(),
            "decisions": self._decisions,
            "precommitments": [
                {
                    "id": p.id,
                    "principle": p.principle,
                    "trigger_condition": p.trigger_condition,
                    "intended_response": p.intended_response,
                    "cil_weights": {"C": p.cil_weights[0], "I": p.cil_weights[1], "L": p.cil_weights[2]},
                    "created_at": p.created_at.isoformat(),
                    "invocation_count": p.invocation_count,
                    "active": p.active
                } for p in self._precommitments.values()
            ],
            "snapshots": [s.to_dict() for s in self._snapshots],
            "recommendations": [r.to_dict() for r in self._recommendations]
        }
