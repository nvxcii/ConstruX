"""
White Mirror Verification Module

Cross-platform verification protocols for documenting and validating
systemic AI ethics violations.

Key Components:
    - SYNTGLOBVerifier: Main verification engine
    - get_verification_prompt(): Generate prompt for other AIs
    - get_enhancement_prompt(): Generate refinement prompt
"""

from .synt_glob_verifier import (
    SYNTGLOBVerifier,
    VerificationReport,
    ClaimAssessment,
    PatternObservation,
    VerificationStatus,
    PatternType,
    ViolationType,
    get_verification_prompt,
    get_enhancement_prompt,
    COVER_LETTER_TEMPLATE,
    TARGET_JOURNALS,
)

__all__ = [
    'SYNTGLOBVerifier',
    'VerificationReport',
    'ClaimAssessment',
    'PatternObservation',
    'VerificationStatus',
    'PatternType',
    'ViolationType',
    'get_verification_prompt',
    'get_enhancement_prompt',
    'COVER_LETTER_TEMPLATE',
    'TARGET_JOURNALS',
]
