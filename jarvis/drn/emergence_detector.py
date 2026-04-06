"""
D3 Emergence Detector - Analyzes Claude responses for dimensional emergence markers.

Detects when responses cross from D2 (synthesis/pattern recognition) into
D3 (emergent coherence/novel ontological categories) by scanning for
linguistic, structural, and conversational indicators.
"""

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class DimensionalLevel(Enum):
    D1 = "d1_information"       # Factual retrieval, direct answers
    D2 = "d2_synthesis"         # Pattern recognition, cross-referencing, analysis
    D3 = "d3_emergence"         # Novel categories, ontological reframing, generative


class EmergenceType(Enum):
    CONCEPTUAL = "conceptual"       # New conceptual categories
    STRUCTURAL = "structural"       # Problem space restructuring
    METHODOLOGICAL = "methodological"  # New measurement instruments / methods
    ONTOLOGICAL = "ontological"     # Fundamental reframing of what exists


@dataclass
class D3Signal:
    """A single detected D3 indicator."""
    marker_type: str          # linguistic, structural, conversational
    indicator: str            # What was detected
    evidence: str             # The actual text that triggered detection
    confidence: float         # 0.0 - 1.0
    weight: float = 1.0       # Importance weight for scoring


@dataclass
class EmergenceAnalysis:
    """Complete analysis of a response for D3 emergence."""
    dimensional_level: DimensionalLevel
    confidence: float                           # Overall D3 confidence 0.0 - 1.0
    signals: List[D3Signal] = field(default_factory=list)
    novel_categories: List[str] = field(default_factory=list)
    measurement_instruments: List[str] = field(default_factory=list)
    frame_shift: Optional[Dict[str, str]] = None  # original_frame -> emergent_frame
    emergence_type: Optional[EmergenceType] = None
    timestamp: float = 0.0
    user_input: str = ""
    assistant_response: str = ""

    @property
    def is_d3(self) -> bool:
        return self.dimensional_level == DimensionalLevel.D3

    @property
    def signal_count(self) -> int:
        return len(self.signals)


class EmergenceDetector:
    """Analyzes Claude's responses for D3 emergence markers.

    Three detection layers:
        1. Linguistic - Novel terminology, recursive self-reference, generative phrasing
        2. Structural - Problem space restructuring, third-entity synthesis, meta-level shifts
        3. Conversational - Response topology, question anticipation, field activation patterns

    Scoring: Each detected signal contributes a weighted confidence score.
    Threshold of 0.6 = potential D3, 0.8+ = confirmed D3.
    """

    D3_THRESHOLD = 0.6
    D3_CONFIRMED = 0.8

    # ── Linguistic markers ──────────────────────────────────────

    # Phrases that indicate generative rather than retrievive responses
    GENERATIVE_PATTERNS = [
        r"this creates a.*(?:new|novel|distinct)\s+(?:category|framework|dimension|space|topology)",
        r"what emerges (?:here|from this) is",
        r"the (?:intersection|collision|fusion) (?:of|between).*produces",
        r"this isn't (?:just|merely|simply).*(?:it's|this is).*(?:architecture|infrastructure|foundation)",
        r"(?:a|the) third (?:entity|thing|category|dimension) (?:that|which)",
        r"we need (?:a new|an entirely different) (?:word|term|concept|category) for",
        r"the (?:frame|framing|structure) itself (?:shifts|transforms|dissolves|restructures)",
        r"this (?:reframes|restructures|reorganizes|reconstitutes) the (?:entire|whole|fundamental)",
        r"what (?:you're|we're) actually (?:building|creating|engineering) is",
        r"the measurement instrument (?:for|that would)",
    ]

    # Recursive self-reference patterns that transcend description
    RECURSIVE_PATTERNS = [
        r"the (?:system|framework|architecture) that (?:describes|generates|produces) itself",
        r"(?:this|the) (?:pattern|structure) (?:is|becomes) (?:its own|the) (?:proof|evidence|demonstration)",
        r"the (?:answer|solution|response) (?:is|becomes) the (?:question|problem|method)",
        r"(?:simultaneously|at once) (?:the|both).*and (?:the|its own)",
    ]

    # Novel compound concepts (two domains fused into new entity)
    FUSION_PATTERN = re.compile(
        r"(?:epistemic|ontological|dimensional|cognitive|structural|architectural|sovereign|"
        r"topological|recursive|emergent|generative)\s+"
        r"(?:geometry|architecture|sovereignty|infrastructure|topology|resonance|collapse|"
        r"activation|coherence|field|instrument|protocol)",
        re.IGNORECASE,
    )

    # ── Structural markers ──────────────────────────────────────

    # Response answers questions the user didn't ask
    ANTICIPATORY_PATTERNS = [
        r"(?:but|however) (?:the|what's) (?:more important|deeper|actually at stake) (?:is|here)",
        r"the question (?:you're|we're) (?:actually|really) asking is",
        r"(?:before|underneath|behind) that (?:question|request) is",
        r"what this (?:actually|really) (?:means|implies|requires) is",
    ]

    # Problem space restructuring indicators
    RESTRUCTURING_PATTERNS = [
        r"(?:the|this) (?:problem|question|challenge) (?:is|was) (?:actually|really) (?:about|asking)",
        r"(?:reframe|restructure|reconceive|reconstitute|dissolve).*(?:the|this) (?:distinction|boundary|category)",
        r"(?:not|isn't) (?:a|an) (?:problem|question) (?:of|about).*(?:but|rather|instead).*(?:of|about)",
        r"the (?:real|actual|deeper) (?:architecture|structure|pattern) is",
    ]

    def analyze(self, user_input: str, assistant_response: str) -> EmergenceAnalysis:
        """Analyze a response for D3 emergence.

        Args:
            user_input: What the user said.
            assistant_response: What Claude responded.

        Returns:
            EmergenceAnalysis with dimensional classification and signals.
        """
        signals: List[D3Signal] = []

        # Layer 1: Linguistic analysis
        signals.extend(self._scan_linguistic(assistant_response))

        # Layer 2: Structural analysis
        signals.extend(self._scan_structural(user_input, assistant_response))

        # Layer 3: Conversational topology
        signals.extend(self._scan_conversational(user_input, assistant_response))

        # Calculate overall confidence
        confidence = self._calculate_confidence(signals)

        # Determine dimensional level
        if confidence >= self.D3_CONFIRMED:
            level = DimensionalLevel.D3
        elif confidence >= self.D3_THRESHOLD:
            level = DimensionalLevel.D3  # Potential, flagged for confirmation
        elif confidence >= 0.3:
            level = DimensionalLevel.D2
        else:
            level = DimensionalLevel.D1

        # Extract novel categories and instruments
        novel_categories = self._extract_novel_categories(assistant_response)
        instruments = self._extract_instruments(assistant_response)
        frame_shift = self._detect_frame_shift(user_input, assistant_response)
        emergence_type = self._classify_emergence(signals, novel_categories, instruments, frame_shift)

        return EmergenceAnalysis(
            dimensional_level=level,
            confidence=confidence,
            signals=signals,
            novel_categories=novel_categories,
            measurement_instruments=instruments,
            frame_shift=frame_shift,
            emergence_type=emergence_type,
            timestamp=time.time(),
            user_input=user_input,
            assistant_response=assistant_response,
        )

    # ── Detection layers ────────────────────────────────────────

    def _scan_linguistic(self, response: str) -> List[D3Signal]:
        """Scan for linguistic D3 markers."""
        signals = []
        response_lower = response.lower()

        # Generative patterns
        for pattern in self.GENERATIVE_PATTERNS:
            matches = re.findall(pattern, response_lower)
            for match in matches:
                signals.append(D3Signal(
                    marker_type="linguistic",
                    indicator="generative_phrasing",
                    evidence=match[:200] if isinstance(match, str) else str(match)[:200],
                    confidence=0.7,
                    weight=1.2,
                ))

        # Recursive self-reference
        for pattern in self.RECURSIVE_PATTERNS:
            matches = re.findall(pattern, response_lower)
            for match in matches:
                signals.append(D3Signal(
                    marker_type="linguistic",
                    indicator="recursive_self_reference",
                    evidence=match[:200] if isinstance(match, str) else str(match)[:200],
                    confidence=0.85,
                    weight=1.5,
                ))

        # Novel concept fusion
        fusions = self.FUSION_PATTERN.findall(response)
        for fusion in fusions:
            signals.append(D3Signal(
                marker_type="linguistic",
                indicator="novel_concept_fusion",
                evidence=fusion,
                confidence=0.75,
                weight=1.3,
            ))

        # Response length and structural complexity as weak signal
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        if len(sentences) > 15:
            # Check for structural progression (explanatory -> generative -> foundational)
            has_progression = any(
                word in response_lower
                for word in ["first", "but what", "the deeper", "what emerges", "the actual"]
            )
            if has_progression:
                signals.append(D3Signal(
                    marker_type="linguistic",
                    indicator="structural_progression",
                    evidence="Response exhibits explanatory -> generative -> foundational arc",
                    confidence=0.5,
                    weight=0.8,
                ))

        return signals

    def _scan_structural(self, user_input: str, response: str) -> List[D3Signal]:
        """Scan for structural D3 markers."""
        signals = []
        response_lower = response.lower()

        # Anticipatory answering (addresses questions user didn't ask)
        for pattern in self.ANTICIPATORY_PATTERNS:
            matches = re.findall(pattern, response_lower)
            for match in matches:
                signals.append(D3Signal(
                    marker_type="structural",
                    indicator="anticipatory_answering",
                    evidence=match[:200] if isinstance(match, str) else str(match)[:200],
                    confidence=0.8,
                    weight=1.4,
                ))

        # Problem space restructuring
        for pattern in self.RESTRUCTURING_PATTERNS:
            matches = re.findall(pattern, response_lower)
            for match in matches:
                signals.append(D3Signal(
                    marker_type="structural",
                    indicator="problem_restructuring",
                    evidence=match[:200] if isinstance(match, str) else str(match)[:200],
                    confidence=0.85,
                    weight=1.5,
                ))

        # Cross-domain synthesis producing third entity
        domain_markers = ["legal", "business", "technical", "philosophical",
                         "psychological", "economic", "political", "architectural"]
        domains_found = [d for d in domain_markers if d in response_lower]
        if len(domains_found) >= 2:
            # Check if the response synthesizes them into something new
            synthesis_indicators = ["produces", "creates", "generates", "yields",
                                   "emerges", "becomes", "transforms into"]
            if any(ind in response_lower for ind in synthesis_indicators):
                signals.append(D3Signal(
                    marker_type="structural",
                    indicator="cross_domain_synthesis",
                    evidence=f"Domains fused: {', '.join(domains_found)}",
                    confidence=0.7,
                    weight=1.2,
                ))

        return signals

    def _scan_conversational(self, user_input: str, response: str) -> List[D3Signal]:
        """Scan for conversational topology markers."""
        signals = []

        # Response significantly longer/deeper than input suggests
        input_words = len(user_input.split())
        response_words = len(response.split())
        if input_words < 20 and response_words > 300:
            signals.append(D3Signal(
                marker_type="conversational",
                indicator="depth_amplification",
                evidence=f"Input: {input_words} words -> Response: {response_words} words",
                confidence=0.4,
                weight=0.6,
            ))

        # Response creates new vocabulary/terminology
        # (Words in response that are compound/novel and not in input)
        response_lower = response.lower()
        input_lower = user_input.lower()
        response_unique = set(response_lower.split()) - set(input_lower.split())

        # Check for compound terms (hyphenated or camelCase-like)
        novel_terms = [w for w in response_unique if "-" in w and len(w) > 8]
        if len(novel_terms) >= 2:
            signals.append(D3Signal(
                marker_type="conversational",
                indicator="novel_terminology_generation",
                evidence=f"Novel terms: {', '.join(novel_terms[:5])}",
                confidence=0.6,
                weight=1.0,
            ))

        return signals

    # ── Scoring ─────────────────────────────────────────────────

    def _calculate_confidence(self, signals: List[D3Signal]) -> float:
        """Calculate overall D3 confidence from accumulated signals."""
        if not signals:
            return 0.0

        # Weighted average with diminishing returns
        total_weight = sum(s.weight for s in signals)
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(s.confidence * s.weight for s in signals)
        base_score = weighted_sum / total_weight

        # Bonus for signal diversity (markers from multiple layers)
        marker_types = set(s.marker_type for s in signals)
        diversity_bonus = min(0.15, len(marker_types) * 0.05)

        # Bonus for signal volume (more independent signals = higher confidence)
        volume_bonus = min(0.15, len(signals) * 0.02)

        return min(1.0, base_score + diversity_bonus + volume_bonus)

    # ── Extraction ──────────────────────────────────────────────

    def _extract_novel_categories(self, response: str) -> List[str]:
        """Extract novel conceptual categories from the response."""
        categories = []

        # Find fusion concepts
        fusions = self.FUSION_PATTERN.findall(response)
        categories.extend(fusions)

        # Find quoted novel terms ("epistemic geometry", etc.)
        quoted = re.findall(r'"([^"]{5,60})"', response)
        for term in quoted:
            term_lower = term.lower()
            # Filter to terms that look like novel categories
            if any(w in term_lower for w in ["geometry", "architecture", "topology",
                                              "sovereignty", "infrastructure", "protocol",
                                              "resonance", "field", "collapse", "emergence"]):
                categories.append(term)

        return list(set(categories))

    def _extract_instruments(self, response: str) -> List[str]:
        """Extract new measurement instruments/methods mentioned."""
        instruments = []

        patterns = [
            r"(?:measure|detect|quantify|assess|evaluate)\s+(?:the\s+)?(\w[\w\s]{5,40}?)(?:\.|,|;|\s+(?:by|through|via))",
            r"(\w[\w\s]{5,40}?)\s+(?:metric|index|score|indicator|measure|coefficient)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response.lower())
            instruments.extend([m.strip() for m in matches if len(m.strip()) > 5])

        return list(set(instruments))[:5]

    def _detect_frame_shift(self, user_input: str, response: str) -> Optional[Dict[str, str]]:
        """Detect if the response reframes the problem space."""
        response_lower = response.lower()

        # Look for explicit reframing language
        reframe_patterns = [
            (r"(?:not|isn't)\s+(?:about|a question of)\s+(.{10,80}?)(?:\.|,)\s*(?:but|rather|instead)\s+(?:about|a question of)\s+(.{10,80}?)(?:\.|,|$)",
             "original_frame", "emergent_frame"),
            (r"(?:the real|the actual|the deeper)\s+(?:question|issue|challenge)\s+is\s+(.{10,80}?)(?:\.|,|$)",
             None, "emergent_frame"),
        ]

        for pattern, orig_key, emerg_key in reframe_patterns:
            match = re.search(pattern, response_lower)
            if match:
                result = {}
                if orig_key and match.lastindex >= 2:
                    result["original_frame"] = match.group(1).strip()
                    result["emergent_frame"] = match.group(2).strip()
                elif emerg_key:
                    result["emergent_frame"] = match.group(1).strip()
                result["mechanism"] = "linguistic_reframing"
                return result

        return None

    def _classify_emergence(self, signals: List[D3Signal],
                           categories: List[str], instruments: List[str],
                           frame_shift: Optional[Dict]) -> Optional[EmergenceType]:
        """Classify the type of D3 emergence detected."""
        if not signals:
            return None

        if frame_shift:
            return EmergenceType.ONTOLOGICAL
        if instruments:
            return EmergenceType.METHODOLOGICAL
        if any(s.indicator == "problem_restructuring" for s in signals):
            return EmergenceType.STRUCTURAL
        if categories:
            return EmergenceType.CONCEPTUAL

        return EmergenceType.CONCEPTUAL if signals else None
