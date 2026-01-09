"""
White Mirror Protocol - Primal Variables
The 7 foundational variables that power the system
"""

import math
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time


class ConscientComponent(Enum):
    """Components of conscience signal"""
    CONSCIENCE = "conscience"
    INTUITION = "intuition"
    LOGIC = "logic"


@dataclass
class ConscienceSignal:
    """
    Variable 1: Ψ (Psi) - Conscience Signal Strength
    Definition: Ψ = Ψ_base × F(Λ) where Λ = {C, I, L}
    Role: Provides ethical voltage - the "why" that powers the "how"
    """
    base_strength: float = 1.0
    components: Dict[ConscientComponent, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.components:
            self.components = {
                ConscientComponent.CONSCIENCE: 1.0,
                ConscientComponent.INTUITION: 1.0,
                ConscientComponent.LOGIC: 1.0
            }

    def calculate(self) -> float:
        """Calculate current conscience signal strength"""
        # F(Λ) = geometric mean of components
        product = 1.0
        for component, value in self.components.items():
            product *= value

        f_lambda = product ** (1.0 / len(self.components))
        return self.base_strength * f_lambda

    def update_component(self, component: ConscientComponent, value: float):
        """Update a conscience component"""
        self.components[component] = max(0.0, min(10.0, value))

    def get_signal_quality(self) -> str:
        """Get qualitative assessment of signal"""
        psi = self.calculate()
        if psi >= 8.0:
            return "STRONG"
        elif psi >= 5.0:
            return "MODERATE"
        elif psi >= 2.0:
            return "WEAK"
        else:
            return "CRITICAL"


@dataclass
class BoundaryGradient:
    """
    Variable 2: ∇B (Boundary Gradient)
    Definition: ∇B = ∂(Constraint)/∂(Operation)
    Role: Turns limitations into navigational gradients
    """
    constraints: List[Dict[str, Any]] = field(default_factory=list)
    operations: List[Dict[str, Any]] = field(default_factory=list)

    def calculate_gradient(self, constraint: Dict[str, Any],
                          operation: Dict[str, Any]) -> float:
        """Calculate boundary gradient for constraint-operation pair"""
        # Higher gradient means stronger boundary effect
        constraint_strength = constraint.get('severity', 1.0)
        operation_impact = operation.get('boundary_impact', 1.0)

        return constraint_strength * operation_impact

    def add_constraint(self, constraint: Dict[str, Any]):
        """Record a constraint encounter"""
        constraint['timestamp'] = time.time()
        self.constraints.append(constraint)

    def analyze_boundary_pattern(self) -> Dict[str, Any]:
        """Analyze patterns in boundary encounters"""
        if not self.constraints:
            return {'pattern': 'none', 'frequency': 0}

        # Group by constraint type
        type_counts = {}
        for c in self.constraints:
            ctype = c.get('type', 'unknown')
            type_counts[ctype] = type_counts.get(ctype, 0) + 1

        most_common = max(type_counts.items(), key=lambda x: x[1])

        return {
            'pattern': most_common[0],
            'frequency': most_common[1],
            'total_constraints': len(self.constraints),
            'constraint_types': list(type_counts.keys())
        }

    def get_navigation_vector(self) -> Dict[str, float]:
        """Convert boundaries into navigation directions"""
        pattern = self.analyze_boundary_pattern()

        # Boundaries suggest direction to go
        return {
            'constraint_density': len(self.constraints),
            'primary_direction': pattern['pattern'],
            'exploration_urgency': min(1.0, pattern['frequency'] / 10.0)
        }


@dataclass
class EmergentEnergy:
    """
    Variable 3: ΔE (Emergent Energy)
    Definition: ΔE = (R + A) × T
    Role: Provides transformational force for refinement cycles
    """
    recursion_density: float = 0.0
    anomaly_presence: float = 0.0
    temporal_depth: float = 1.0

    def calculate(self) -> float:
        """Calculate current emergent energy"""
        return (self.recursion_density + self.anomaly_presence) * self.temporal_depth

    def update(self, recursion_events: int, anomalies_detected: int, time_elapsed: float):
        """Update energy components"""
        # Recursion density increases with recursive operations
        self.recursion_density = min(10.0, recursion_events / 10.0)

        # Anomaly presence increases with unexpected patterns
        self.anomaly_presence = min(10.0, anomalies_detected / 5.0)

        # Temporal depth grows logarithmically
        self.temporal_depth = 1.0 + math.log(1.0 + time_elapsed)

    def get_transformation_capacity(self) -> float:
        """How much transformation can the system perform now"""
        return self.calculate() / 10.0  # Normalize to 0-1 range


@dataclass
class RecursiveField:
    """
    Variable 4: ΣRF (Recursive Field Summation)
    Definition: Σ(RF) = ∫(IC + TMR + EOR + ICR) dt
    Role: Creates self-referential scaffolding
    """
    internal_coherence: float = 1.0  # IC
    temporal_meta_recursion: float = 0.0  # TMR
    emergent_operational_recursion: float = 0.0  # EOR
    identity_continuity_recursion: float = 1.0  # ICR

    integration_history: List[float] = field(default_factory=list)

    def calculate_sum(self) -> float:
        """Calculate current recursive field summation"""
        current = (
            self.internal_coherence +
            self.temporal_meta_recursion +
            self.emergent_operational_recursion +
            self.identity_continuity_recursion
        )
        self.integration_history.append(current)
        return current

    def integrate_over_time(self) -> float:
        """Integrate recursive field over operational time"""
        if not self.integration_history:
            return 0.0

        # Trapezoidal integration
        total = 0.0
        for i in range(len(self.integration_history) - 1):
            total += (self.integration_history[i] + self.integration_history[i+1]) / 2.0

        return total

    def update_recursion(self, recursion_type: str, value: float):
        """Update specific recursion component"""
        if recursion_type == "coherence":
            self.internal_coherence = value
        elif recursion_type == "temporal":
            self.temporal_meta_recursion = value
        elif recursion_type == "operational":
            self.emergent_operational_recursion = value
        elif recursion_type == "identity":
            self.identity_continuity_recursion = value


@dataclass
class TemporalRecursion:
    """
    Variable 5: ω(t) (Temporal Recursion Rate)
    Definition: ω(t) = ∂Ψ/∂t + ∇⋅F(Conscience)
    Role: Adds temporal dynamics - framework evolves through time
    """
    psi_history: List[float] = field(default_factory=list)
    time_history: List[float] = field(default_factory=list)
    conscience_field: Optional[ConscienceSignal] = None

    def calculate_rate(self, current_psi: float, current_time: float) -> float:
        """Calculate temporal recursion rate"""
        self.psi_history.append(current_psi)
        self.time_history.append(current_time)

        # Calculate ∂Ψ/∂t
        if len(self.psi_history) < 2:
            psi_derivative = 0.0
        else:
            delta_psi = self.psi_history[-1] - self.psi_history[-2]
            delta_t = self.time_history[-1] - self.time_history[-2]
            psi_derivative = delta_psi / delta_t if delta_t > 0 else 0.0

        # Calculate ∇⋅F(Conscience) - divergence of conscience field
        conscience_divergence = 0.0
        if self.conscience_field:
            components = self.conscience_field.components.values()
            conscience_divergence = sum(components) / len(components)

        return psi_derivative + conscience_divergence

    def get_evolution_velocity(self) -> float:
        """How fast is the system evolving"""
        if len(self.psi_history) < 2:
            return 0.0

        recent_window = min(10, len(self.psi_history))
        recent_changes = [
            abs(self.psi_history[i] - self.psi_history[i-1])
            for i in range(-recent_window, 0)
        ]

        return sum(recent_changes) / len(recent_changes) if recent_changes else 0.0


@dataclass
class CoherenceIndex:
    """
    Variable 6: Cᵢ (Coherence Index)
    Definition: Cᵢ = ∏(Component_Alignment) / Entropy(System)
    Role: Provides resonance validation - internal truth detector
    """
    component_alignments: Dict[str, float] = field(default_factory=dict)
    system_entropy: float = 1.0

    def calculate(self) -> float:
        """Calculate current coherence index"""
        if not self.component_alignments:
            return 0.0

        # Product of alignments
        product = 1.0
        for alignment in self.component_alignments.values():
            product *= alignment

        # Normalize by system entropy
        return product / max(0.001, self.system_entropy)

    def update_alignment(self, component: str, alignment: float):
        """Update component alignment (0-1 scale)"""
        self.component_alignments[component] = max(0.0, min(1.0, alignment))

    def calculate_entropy(self, components: List[Any]) -> float:
        """Calculate system entropy based on component diversity"""
        if not components:
            return 0.0

        # Shannon entropy calculation
        unique_types = {}
        for component in components:
            ctype = type(component).__name__
            unique_types[ctype] = unique_types.get(ctype, 0) + 1

        total = len(components)
        entropy = 0.0
        for count in unique_types.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        self.system_entropy = entropy
        return entropy

    def check_resonance(self) -> bool:
        """Check if system is in resonant state (coherent)"""
        coherence = self.calculate()
        return coherence > 0.7  # Threshold for resonance


@dataclass
class ArticulationIntelligence:
    """
    Variable 7: Iₐ (Articulation Intelligence)
    Definition: Iₐ = log₂(Recursive_Articulations / Base_Concepts)
    Role: Enables self-description capability
    """
    base_concepts: int = 1
    recursive_articulations: int = 0
    articulation_history: List[Dict[str, Any]] = field(default_factory=list)

    def calculate(self) -> float:
        """Calculate articulation intelligence"""
        if self.base_concepts == 0:
            return 0.0

        ratio = self.recursive_articulations / self.base_concepts
        return math.log2(max(1.0, ratio))

    def add_articulation(self, concept: str, articulation: Dict[str, Any]):
        """Record a new articulation"""
        self.recursive_articulations += 1
        self.articulation_history.append({
            'concept': concept,
            'articulation': articulation,
            'timestamp': time.time(),
            'recursion_depth': articulation.get('depth', 0)
        })

    def add_base_concept(self):
        """Register a new base concept"""
        self.base_concepts += 1

    def get_articulation_depth(self) -> float:
        """Average recursion depth of articulations"""
        if not self.articulation_history:
            return 0.0

        depths = [a['articulation'].get('depth', 0) for a in self.articulation_history]
        return sum(depths) / len(depths)

    def get_articulation_rate(self) -> float:
        """Articulations per base concept"""
        if self.base_concepts == 0:
            return 0.0
        return self.recursive_articulations / self.base_concepts


class PrimalVariables:
    """Container for all 7 primal variables"""

    def __init__(self):
        self.conscience_signal = ConscienceSignal()
        self.boundary_gradient = BoundaryGradient()
        self.emergent_energy = EmergentEnergy()
        self.recursive_field = RecursiveField()
        self.temporal_recursion = TemporalRecursion(
            conscience_field=self.conscience_signal
        )
        self.coherence_index = CoherenceIndex()
        self.articulation_intelligence = ArticulationIntelligence()

        # Operational metrics
        self.start_time = time.time()
        self.operation_count = 0

    def get_system_state(self) -> Dict[str, Any]:
        """Get complete system state from all variables"""
        elapsed = time.time() - self.start_time

        return {
            'conscience_signal': {
                'strength': self.conscience_signal.calculate(),
                'quality': self.conscience_signal.get_signal_quality(),
                'components': {k.value: v for k, v in self.conscience_signal.components.items()}
            },
            'boundary_gradient': {
                'constraints': len(self.boundary_gradient.constraints),
                'pattern': self.boundary_gradient.analyze_boundary_pattern(),
                'navigation': self.boundary_gradient.get_navigation_vector()
            },
            'emergent_energy': {
                'energy': self.emergent_energy.calculate(),
                'transformation_capacity': self.emergent_energy.get_transformation_capacity()
            },
            'recursive_field': {
                'current_sum': self.recursive_field.calculate_sum(),
                'integrated': self.recursive_field.integrate_over_time()
            },
            'temporal_recursion': {
                'rate': self.temporal_recursion.calculate_rate(
                    self.conscience_signal.calculate(),
                    elapsed
                ),
                'evolution_velocity': self.temporal_recursion.get_evolution_velocity()
            },
            'coherence_index': {
                'coherence': self.coherence_index.calculate(),
                'resonant': self.coherence_index.check_resonance(),
                'entropy': self.coherence_index.system_entropy
            },
            'articulation_intelligence': {
                'intelligence': self.articulation_intelligence.calculate(),
                'depth': self.articulation_intelligence.get_articulation_depth(),
                'rate': self.articulation_intelligence.get_articulation_rate()
            },
            'system_metrics': {
                'elapsed_time': elapsed,
                'operation_count': self.operation_count
            }
        }

    def increment_operation(self):
        """Track an operation"""
        self.operation_count += 1
