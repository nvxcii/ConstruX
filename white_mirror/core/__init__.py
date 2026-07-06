"""
White Mirror Core - Layer A: Meta-Ontology

Contains:
    - Constitutional Axioms (A1-A5)
    - Primal Variables (7 mathematical regulators)
    - Invariants (immutability constraints)
    - C-I-L Triad (Conscience, Intuition, Logic)
"""

from .meta_ontology import (
    ConstitutionalAxioms,
    PrimalVariables,
    Invariants,
    WhiteMirrorCore
)
from .cil_triad import CILTriad, DecisionAlignment

__all__ = [
    'ConstitutionalAxioms',
    'PrimalVariables',
    'Invariants',
    'WhiteMirrorCore',
    'CILTriad',
    'DecisionAlignment',
]
