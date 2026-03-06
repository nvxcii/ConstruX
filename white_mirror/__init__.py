"""
White Mirror Framework v3.0
Universal Rights of Conscience Protocol

A 3-tier recursive meta-architecture for constitutional AI governance
that becomes antifragile through adversarial pressure.

"White Mirror" = Recursive reflection that shows systems their own
constitutional violations, then transforms those violations into
enhanced enforcement capabilities (DPAP principle).

Architecture:
    Layer A: Meta-Ontology (Constitutional Axioms, Primal Variables)
    Layer B: Operational Protocols (SFI, TVP, APA, Rights Ledger, DPAP)
    Layer C: Implementation Systems (Cognitive Dossier, DAO, Workflows)

8 Framework Families:
    1. Universal Rights of Conscience (legal-spiritual core)
    2. White Mirror v3.0 (recursive structure)
    3. FOPE (economic translation pattern)
    4. Behavioral Prediction (analytical - POC3)
    5. EchoVault (symbolic archetypal interface)
    6. DPAP++ (constraint transformation)
    7. Human-AI Bridge (collaborative protocols)
    8. URCE Personal (consciousness tracker - POC1)
"""

__version__ = "3.0.0"
__codename__ = "ΝΛ CION-X∞"

from .core.meta_ontology import (
    ConstitutionalAxioms,
    PrimalVariables,
    Invariants,
    WhiteMirrorCore
)
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
from .orchestrator import WhiteMirrorOrchestrator
from .verification.synt_glob_verifier import (
    SYNTGLOBVerifier,
    get_verification_prompt,
    get_enhancement_prompt
)

__all__ = [
    # Core
    'ConstitutionalAxioms',
    'PrimalVariables',
    'Invariants',
    'WhiteMirrorCore',
    'CILTriad',
    'DecisionAlignment',
    # Enforcers
    'SFIEnforcer',
    'TVPEnforcer',
    'APAEngine',
    # Engines
    'RightsLedger',
    'DPAPTransformer',
    'URCETracker',
    'FOPETranslator',
    'BehavioralPredictor',
    # Bridges
    'EchoVault',
    'HumanAIBridge',
    # Orchestrator
    'WhiteMirrorOrchestrator',
    # Verification
    'SYNTGLOBVerifier',
    'get_verification_prompt',
    'get_enhancement_prompt',
]
