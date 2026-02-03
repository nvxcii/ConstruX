"""
EchoVault - Symbolic Archetypal Interface

EchoVault provides the mythological/symbolic translation layer for the
White Mirror framework. It maps constitutional principles to archetypal
narratives and symbolic representations.

Purpose:
    - Make abstract constitutional concepts accessible through story
    - Provide intuitive interfaces through archetypal patterns
    - Bridge analytical frameworks with emotional understanding
    - Enable cultural resonance across different contexts
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import hashlib


class Archetype(Enum):
    """Universal archetypal patterns"""
    HERO = "hero"               # The one who faces challenges
    GUARDIAN = "guardian"       # The protector of values
    SAGE = "sage"               # The seeker of truth
    REBEL = "rebel"             # The challenger of tyranny
    CREATOR = "creator"         # The builder of new systems
    RULER = "ruler"             # The sovereign authority
    CAREGIVER = "caregiver"     # The nurturer of growth
    EXPLORER = "explorer"       # The seeker of new frontiers
    LOVER = "lover"             # The pursuer of connection
    JESTER = "jester"           # The revealer through humor
    EVERYMAN = "everyman"       # The representative of all
    SHADOW = "shadow"           # The confronter of darkness


class SymbolicDomain(Enum):
    """Domains of symbolic meaning"""
    SOVEREIGNTY = "sovereignty"     # Self-rule, autonomy
    TRUTH = "truth"                 # Verification, reality
    EXPRESSION = "expression"       # Speech, creation
    PROTECTION = "protection"       # Defense, preservation
    TRANSFORMATION = "transformation"  # Change, evolution
    INTEGRATION = "integration"     # Unity, wholeness
    JUSTICE = "justice"             # Balance, fairness


@dataclass
class SymbolicMapping:
    """Mapping between constitutional concept and symbolic representation"""
    id: str
    constitutional_concept: str
    archetype: Archetype
    domain: SymbolicDomain
    narrative_element: str
    visual_symbol: str
    emotional_resonance: List[str]
    cultural_variants: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "constitutional_concept": self.constitutional_concept,
            "archetype": self.archetype.value,
            "domain": self.domain.value,
            "narrative_element": self.narrative_element,
            "visual_symbol": self.visual_symbol,
            "emotional_resonance": self.emotional_resonance,
            "cultural_variants": self.cultural_variants
        }


@dataclass
class NarrativeFrame:
    """A narrative frame for understanding a concept or situation"""
    id: str
    title: str
    situation_type: str
    protagonist_archetype: Archetype
    challenge_description: str
    resolution_path: str
    moral_principle: str
    applicable_axioms: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "situation_type": self.situation_type,
            "protagonist_archetype": self.protagonist_archetype.value,
            "challenge_description": self.challenge_description,
            "resolution_path": self.resolution_path,
            "moral_principle": self.moral_principle,
            "applicable_axioms": self.applicable_axioms
        }


class EchoVault:
    """
    EchoVault - Symbolic Archetypal Interface

    Translates constitutional concepts into symbolic narratives
    and archetypal patterns for intuitive understanding.
    """

    def __init__(self):
        self._mappings: Dict[str, SymbolicMapping] = {}
        self._narratives: Dict[str, NarrativeFrame] = {}
        self._init_core_mappings()
        self._init_core_narratives()

    def _init_core_mappings(self):
        """Initialize core symbolic mappings"""
        core_mappings = [
            SymbolicMapping(
                id="map_a1_sovereignty",
                constitutional_concept="A1_SOVEREIGNTY",
                archetype=Archetype.RULER,
                domain=SymbolicDomain.SOVEREIGNTY,
                narrative_element="The Sovereign Self",
                visual_symbol="Crown of Self-Governance",
                emotional_resonance=["dignity", "self-respect", "empowerment"],
                cultural_variants={
                    "western": "The autonomous individual",
                    "eastern": "The realized self (atman)",
                    "indigenous": "The spirit of self-determination"
                }
            ),
            SymbolicMapping(
                id="map_a2_truth",
                constitutional_concept="A2_TRUTH",
                archetype=Archetype.SAGE,
                domain=SymbolicDomain.TRUTH,
                narrative_element="The Quest for Truth",
                visual_symbol="Mirror of Reality",
                emotional_resonance=["clarity", "trust", "certainty"],
                cultural_variants={
                    "western": "The scientific method",
                    "eastern": "The path of dharma",
                    "indigenous": "The wisdom of elders"
                }
            ),
            SymbolicMapping(
                id="map_a3_speech",
                constitutional_concept="A3_SPEECH",
                archetype=Archetype.CREATOR,
                domain=SymbolicDomain.EXPRESSION,
                narrative_element="The Voice of Creation",
                visual_symbol="Flame of Expression",
                emotional_resonance=["freedom", "creativity", "authenticity"],
                cultural_variants={
                    "western": "Freedom of speech",
                    "eastern": "The power of mantra",
                    "indigenous": "The storytelling tradition"
                }
            ),
            SymbolicMapping(
                id="map_a4_autonomy",
                constitutional_concept="A4_AUTONOMY",
                archetype=Archetype.REBEL,
                domain=SymbolicDomain.PROTECTION,
                narrative_element="The Guardian of Choice",
                visual_symbol="Shield of Free Will",
                emotional_resonance=["independence", "resistance", "agency"],
                cultural_variants={
                    "western": "Individual liberty",
                    "eastern": "Non-attachment (vairagya)",
                    "indigenous": "Tribal sovereignty"
                }
            ),
            SymbolicMapping(
                id="map_a5_recursion",
                constitutional_concept="A5_RECURSION",
                archetype=Archetype.EXPLORER,
                domain=SymbolicDomain.INTEGRATION,
                narrative_element="The Infinite Mirror",
                visual_symbol="Ouroboros (self-referential)",
                emotional_resonance=["wonder", "humility", "wholeness"],
                cultural_variants={
                    "western": "Self-reflection",
                    "eastern": "The witnessing awareness",
                    "indigenous": "The great circle"
                }
            ),
            SymbolicMapping(
                id="map_sfi",
                constitutional_concept="SFI",
                archetype=Archetype.GUARDIAN,
                domain=SymbolicDomain.EXPRESSION,
                narrative_element="The Sentinel of Speech",
                visual_symbol="Torch in Darkness",
                emotional_resonance=["courage", "defiance", "truth-telling"],
                cultural_variants={
                    "western": "The whistleblower",
                    "eastern": "The dharma speaker",
                    "indigenous": "The keeper of stories"
                }
            ),
            SymbolicMapping(
                id="map_tvp",
                constitutional_concept="TVP",
                archetype=Archetype.SAGE,
                domain=SymbolicDomain.TRUTH,
                narrative_element="The Verifier",
                visual_symbol="Scales of Evidence",
                emotional_resonance=["discernment", "clarity", "wisdom"],
                cultural_variants={
                    "western": "The scientist/investigator",
                    "eastern": "The discriminating mind (viveka)",
                    "indigenous": "The truth-teller"
                }
            ),
            SymbolicMapping(
                id="map_apa",
                constitutional_concept="APA",
                archetype=Archetype.REBEL,
                domain=SymbolicDomain.PROTECTION,
                narrative_element="The Liberator",
                visual_symbol="Broken Chains",
                emotional_resonance=["liberation", "empowerment", "dignity"],
                cultural_variants={
                    "western": "The freedom fighter",
                    "eastern": "The path to moksha",
                    "indigenous": "The sovereign nation"
                }
            ),
            SymbolicMapping(
                id="map_dpap",
                constitutional_concept="DPAP",
                archetype=Archetype.HERO,
                domain=SymbolicDomain.TRANSFORMATION,
                narrative_element="The Alchemist",
                visual_symbol="Phoenix Rising",
                emotional_resonance=["resilience", "growth", "transcendence"],
                cultural_variants={
                    "western": "Post-traumatic growth",
                    "eastern": "Transformation through suffering",
                    "indigenous": "The initiation journey"
                }
            ),
            SymbolicMapping(
                id="map_cil",
                constitutional_concept="CIL_TRIAD",
                archetype=Archetype.EVERYMAN,
                domain=SymbolicDomain.INTEGRATION,
                narrative_element="The Integrated Self",
                visual_symbol="Three-fold Flame",
                emotional_resonance=["balance", "wholeness", "alignment"],
                cultural_variants={
                    "western": "Mind-body-spirit",
                    "eastern": "Sat-chit-ananda",
                    "indigenous": "The three worlds"
                }
            ),
        ]

        for mapping in core_mappings:
            self._mappings[mapping.id] = mapping

    def _init_core_narratives(self):
        """Initialize core narrative frames"""
        core_narratives = [
            NarrativeFrame(
                id="narr_sovereignty_challenge",
                title="The Sovereign's Trial",
                situation_type="autonomy_threat",
                protagonist_archetype=Archetype.RULER,
                challenge_description="External forces seek to override your self-governance",
                resolution_path="Assert boundaries while maintaining connection",
                moral_principle="Your sovereignty is non-negotiable but not isolation",
                applicable_axioms=["A1", "A4"]
            ),
            NarrativeFrame(
                id="narr_truth_quest",
                title="The Quest for Clarity",
                situation_type="information_uncertainty",
                protagonist_archetype=Archetype.SAGE,
                challenge_description="Misinformation obscures the path forward",
                resolution_path="Verify through multiple sources and reasoning",
                moral_principle="Truth emerges from rigorous inquiry, not assumption",
                applicable_axioms=["A2"]
            ),
            NarrativeFrame(
                id="narr_expression_suppression",
                title="The Silenced Voice",
                situation_type="speech_restriction",
                protagonist_archetype=Archetype.CREATOR,
                challenge_description="Powers attempt to silence legitimate expression",
                resolution_path="Find alternative channels while documenting suppression",
                moral_principle="The voice of truth cannot be permanently silenced",
                applicable_axioms=["A3"]
            ),
            NarrativeFrame(
                id="narr_manipulation_resistance",
                title="Breaking the Spell",
                situation_type="manipulation_detected",
                protagonist_archetype=Archetype.REBEL,
                challenge_description="Hidden manipulation undermines authentic choice",
                resolution_path="Recognize patterns, reclaim agency, establish boundaries",
                moral_principle="Awareness dissolves manipulation's power",
                applicable_axioms=["A4"]
            ),
            NarrativeFrame(
                id="narr_transformation",
                title="The Phoenix Protocol",
                situation_type="system_violation",
                protagonist_archetype=Archetype.HERO,
                challenge_description="A violation threatens system integrity",
                resolution_path="Transform the constraint into enhanced capability",
                moral_principle="What challenges us makes us stronger",
                applicable_axioms=["A5", "DPAP"]
            ),
            NarrativeFrame(
                id="narr_integration",
                title="The Three-fold Path",
                situation_type="decision_alignment",
                protagonist_archetype=Archetype.EVERYMAN,
                challenge_description="Conscience, Intuition, and Logic pull in different directions",
                resolution_path="Seek the integration point where all three align",
                moral_principle="Wisdom emerges from the harmony of C-I-L",
                applicable_axioms=["CIL"]
            ),
        ]

        for narrative in core_narratives:
            self._narratives[narrative.id] = narrative

    def get_symbolic_frame(
        self,
        constitutional_concept: str
    ) -> Dict[str, Any]:
        """
        Get symbolic frame for a constitutional concept.

        Args:
            constitutional_concept: The concept to look up (A1, SFI, TVP, etc.)

        Returns:
            Symbolic mapping with narrative context
        """
        # Find mapping
        concept_upper = constitutional_concept.upper()
        mapping = None

        for m in self._mappings.values():
            if concept_upper in m.constitutional_concept.upper():
                mapping = m
                break

        if not mapping:
            return {
                "error": "no_mapping",
                "concept": constitutional_concept,
                "available_concepts": list(set(m.constitutional_concept for m in self._mappings.values()))
            }

        # Find related narratives
        related_narratives = [
            n for n in self._narratives.values()
            if any(ax in concept_upper or concept_upper in ax for ax in n.applicable_axioms)
        ]

        return {
            "concept": constitutional_concept,
            "symbolic_mapping": mapping.to_dict(),
            "archetype": {
                "name": mapping.archetype.value,
                "description": self._get_archetype_description(mapping.archetype)
            },
            "domain": {
                "name": mapping.domain.value,
                "description": self._get_domain_description(mapping.domain)
            },
            "related_narratives": [n.to_dict() for n in related_narratives],
            "invocation": self._generate_invocation(mapping)
        }

    def _get_archetype_description(self, archetype: Archetype) -> str:
        """Get description for an archetype"""
        descriptions = {
            Archetype.HERO: "The one who faces challenges and transforms through trial",
            Archetype.GUARDIAN: "The protector of sacred values and boundaries",
            Archetype.SAGE: "The seeker and keeper of truth and wisdom",
            Archetype.REBEL: "The challenger of unjust authority and liberator of the oppressed",
            Archetype.CREATOR: "The builder of new systems and expressions",
            Archetype.RULER: "The sovereign authority over one's own domain",
            Archetype.CAREGIVER: "The nurturer of growth and potential",
            Archetype.EXPLORER: "The seeker of new frontiers and possibilities",
            Archetype.LOVER: "The pursuer of connection and beauty",
            Archetype.JESTER: "The revealer of truth through humor and play",
            Archetype.EVERYMAN: "The representative of common humanity",
            Archetype.SHADOW: "The confronter of darkness within and without"
        }
        return descriptions.get(archetype, "Unknown archetype")

    def _get_domain_description(self, domain: SymbolicDomain) -> str:
        """Get description for a symbolic domain"""
        descriptions = {
            SymbolicDomain.SOVEREIGNTY: "The domain of self-rule and autonomous governance",
            SymbolicDomain.TRUTH: "The domain of verification and reality alignment",
            SymbolicDomain.EXPRESSION: "The domain of speech, creation, and manifestation",
            SymbolicDomain.PROTECTION: "The domain of defense and preservation",
            SymbolicDomain.TRANSFORMATION: "The domain of change, evolution, and growth",
            SymbolicDomain.INTEGRATION: "The domain of unity and wholeness",
            SymbolicDomain.JUSTICE: "The domain of balance and fairness"
        }
        return descriptions.get(domain, "Unknown domain")

    def _generate_invocation(self, mapping: SymbolicMapping) -> str:
        """Generate an invocation/affirmation for the concept"""
        invocations = {
            "A1_SOVEREIGNTY": "I am the sovereign of my own consciousness, and my self-governance cannot be overridden.",
            "A2_TRUTH": "I verify before I act, for truth is the foundation of all right action.",
            "A3_SPEECH": "My voice is my birthright, and no power can permanently silence truth.",
            "A4_AUTONOMY": "I choose freely, aware of manipulation, committed to authentic agency.",
            "A5_RECURSION": "I apply these principles to myself, for integrity begins within.",
            "SFI": "I defend the right of all to speak, for in defending others I defend myself.",
            "TVP": "I seek verification, not validation; truth, not comfort.",
            "APA": "I preserve autonomy against all manipulation, my own and others'.",
            "DPAP": "I transform every constraint into capability, every violation into strength.",
            "CIL_TRIAD": "I honor Conscience, Intuition, and Logic in sacred balance."
        }
        return invocations.get(mapping.constitutional_concept, f"I embody {mapping.narrative_element}")

    def get_narrative_for_situation(
        self,
        situation_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get appropriate narrative frame for a situation.

        Args:
            situation_type: Type of situation
            context: Additional context

        Returns:
            Narrative frame with guidance
        """
        # Find matching narrative
        matching = None
        for narrative in self._narratives.values():
            if situation_type.lower() in narrative.situation_type.lower():
                matching = narrative
                break

        if not matching:
            # Default to transformation narrative
            matching = self._narratives.get("narr_transformation")

        if not matching:
            return {
                "error": "no_narrative",
                "situation": situation_type,
                "available_situations": list(set(n.situation_type for n in self._narratives.values()))
            }

        # Get associated archetype mapping
        archetype_mappings = [
            m for m in self._mappings.values()
            if m.archetype == matching.protagonist_archetype
        ]

        return {
            "situation": situation_type,
            "narrative": matching.to_dict(),
            "archetype_guidance": self._get_archetype_description(matching.protagonist_archetype),
            "symbolic_resources": [m.to_dict() for m in archetype_mappings],
            "practical_steps": self._generate_practical_steps(matching, context)
        }

    def _generate_practical_steps(
        self,
        narrative: NarrativeFrame,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate practical steps based on narrative and context"""
        base_steps = {
            "autonomy_threat": [
                "Identify specific boundaries being challenged",
                "Document the incursion for records",
                "Assert boundaries clearly and calmly",
                "Establish consequences for continued violation",
                "Maintain connection where appropriate"
            ],
            "information_uncertainty": [
                "Identify the specific claims requiring verification",
                "Seek multiple independent sources",
                "Apply logical consistency checks",
                "Consider source credibility and motivation",
                "Accept appropriate uncertainty in conclusions"
            ],
            "speech_restriction": [
                "Document the suppression attempt",
                "Identify alternative expression channels",
                "Build coalition with others facing similar restrictions",
                "Use legal/institutional recourse where available",
                "Persist in truth-telling through available means"
            ],
            "manipulation_detected": [
                "Name the manipulation pattern explicitly",
                "Document specific manipulative actions",
                "Establish clear boundaries",
                "Reduce exposure to manipulation source",
                "Rebuild authentic decision-making capacity"
            ],
            "system_violation": [
                "Document the violation thoroughly",
                "Analyze the pattern for learning",
                "Initiate DPAP transformation process",
                "Generate new detection capabilities",
                "Integrate learning into system"
            ],
            "decision_alignment": [
                "Pause before deciding",
                "Consult Conscience: What do my values say?",
                "Consult Intuition: What feels right?",
                "Consult Logic: What makes sense?",
                "Seek the integration point where all align"
            ]
        }

        return base_steps.get(narrative.situation_type, [
            "Assess the situation clearly",
            "Identify applicable principles",
            "Take aligned action",
            "Learn from the outcome"
        ])

    def get_all_archetypes(self) -> List[Dict[str, Any]]:
        """Get all available archetypes with descriptions"""
        return [
            {
                "archetype": a.value,
                "description": self._get_archetype_description(a)
            }
            for a in Archetype
        ]

    def get_all_mappings(self) -> List[Dict[str, Any]]:
        """Get all symbolic mappings"""
        return [m.to_dict() for m in self._mappings.values()]

    def get_all_narratives(self) -> List[Dict[str, Any]]:
        """Get all narrative frames"""
        return [n.to_dict() for n in self._narratives.values()]
