"""
Universal Analytical Framework (UNAF) v1.0
A content-agnostic, value-aligned framework for traceable, transparent,
balanced analysis resistant to cherry-picking and contextual drift.

Core values: Evidence-based, Transparent, Balanced, Proportionate, Self-correcting.
Seven structural principles: P1–P7 (see UNAFFramework docstring).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import textwrap


class ConfidenceLevel(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class EvidenceWeight(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


ABSOLUTE_LANGUAGE_FLAGS = [
    "void", "invalid", "unenforceable", "fatal", "catastrophic",
    "impossible", "always", "never", "proves", "definitively",
    "conclusively", "obviously", "clearly", "undoubtedly",
]

PROPORTIONATE_REPLACEMENTS = {
    "void": "may be unenforceable",
    "invalid": "may not be valid",
    "fatal": "may be significant",
    "impossible": "unlikely",
    "always": "often",
    "never": "rarely",
    "proves": "suggests",
    "definitively": "on balance",
    "conclusively": "tends to indicate",
    "obviously": "the evidence shows",
    "clearly": "the evidence suggests",
}


@dataclass
class Layer0Entry:
    """Single evidence entry — verbatim only, no interpretation."""
    source: str
    verbatim_text: str
    timestamp: str
    entry_type: str  # claim / fact / quote / data
    item_number: int = 0


@dataclass
class Layer1Assumption:
    assumption: str
    why_unproven: str
    counter_evidence: str


@dataclass
class Layer4Interpretation:
    claim: str
    favorable_to_source: str
    alternative: str
    neutral_technical: str
    evidence_for_favorable: str
    evidence_for_alternative: str
    confidence: ConfidenceLevel


@dataclass
class Layer5EvidenceItem:
    description: str
    weight: EvidenceWeight
    rationale: str
    would_change_mind_if_disproven: bool


@dataclass
class UNAFAnalysis:
    """
    Complete UNAF analysis container.
    Populate each layer in order; call validate() before finalising.

    Structural Principles:
      P1 – Separate observation from interpretation
      P2 – Exhaustive forced documentation
      P3 – Built-in adversarial testing (Skeptic's Challenge)
      P4 – Layered independence
      P5 – Proportionate claiming (no absolute language)
      P6 – Uncertainty acknowledgment
      P7 – Actionable output with fallback
    """

    # Metadata
    analyst: str = ""
    date: str = ""
    topic: str = ""
    purpose: str = ""

    # Layer 0 – Exact Capture (P1)
    evidence: list[Layer0Entry] = field(default_factory=list)
    not_said: str = ""
    layer0_verified: bool = False

    # Layer 1 – Hidden Assumptions (P2)
    assumptions: list[Layer1Assumption] = field(default_factory=list)
    source_assumptions: str = ""
    credibility_assumptions: str = ""
    layer1_verified: bool = False

    # Layer 2 – Question Behind the Question (P1 + P6)
    surface_question: str = ""
    unstated_goal: str = ""
    actual_need: str = ""
    reframed_issue: str = ""  # "At bottom, this is about X vs. Y"
    source_fear: str = ""
    my_fear: str = ""
    power_dynamics: str = ""
    layer2_verified: bool = False

    # Layer 3 – Structural Patterns (P4)
    sequence: list[str] = field(default_factory=list)
    repeating_pattern: str = ""
    inconsistency: str = ""
    gap: str = ""
    framing_device: str = ""
    emphasized: str = ""
    minimized: str = ""
    layer3_verified: bool = False

    # Layer 4 – Alternative Interpretations + Skeptic's Challenge (P3 + P5)
    interpretations: list[Layer4Interpretation] = field(default_factory=list)
    most_parsimonious: str = ""
    skeptics_challenge: str = ""          # strongest counter-argument
    evidence_to_defeat_challenge: str = ""
    preferred_survives_without_it: str = ""
    absolute_language_found: list[str] = field(default_factory=list)
    layer4_verified: bool = False

    # Layer 5 – Evidence Weighting & Fallacy Check (P5)
    weighted_evidence: list[Layer5EvidenceItem] = field(default_factory=list)
    # Keys are every bias/fallacy the analyst *reviewed* (present or absent).
    # Value is the mitigation note, or "" / "N/A" when the bias was not found.
    # The self-audit checks len(keys) >= 5, not the presence of mitigations.
    fallacies_identified: dict[str, str] = field(default_factory=dict)
    layer5_verified: bool = False

    # Layer 6 – Decision & Response (P7 + P6)
    strongest_claim: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    specific_action: str = ""
    responsible_party: str = ""
    deadline: str = ""
    uncertainty_statement: str = ""
    evidence_to_resolve: str = ""
    fallback_position: str = ""
    minimum_acceptable: str = ""
    walk_away_threshold: str = ""
    layer6_verified: bool = False

    # Layer 7 – Summary Generator (plain language)
    narrative_summary: str = ""      # 4–6 sentences, no jargon
    executive_brief: str = ""        # max 75 words
    action_sheet: list[dict] = field(default_factory=list)  # [{what, by_when, if_blocked}]
    most_important_action: str = ""
    potential_derailer: str = ""
    who_else_needs_to_know: str = ""
    layer7_verified: bool = False


class UNAFFramework:
    """
    Validates a UNAFAnalysis instance against all seven structural principles.
    Use render_template() to produce a filled Markdown document.
    Use validate() to run the 18-point self-audit checklist.
    """

    ABSOLUTE_TERMS = ABSOLUTE_LANGUAGE_FLAGS

    def validate(self, analysis: UNAFAnalysis) -> dict:
        """
        Run the 18-point self-audit. Returns {check: pass/fail, ...} and overall score.
        """
        checks = {}

        # 1–5: Layers 0–2
        checks["L0: no interpretation in evidence"] = analysis.layer0_verified
        checks["L1: 3+ assumptions listed"] = len(analysis.assumptions) >= 3
        checks["L1: each assumption has counter-evidence"] = all(
            bool((a.counter_evidence or "").strip()) for a in analysis.assumptions
        )
        checks["L2: issue reframed as interests"] = (
            "vs." in (analysis.reframed_issue or "")
            or "versus" in (analysis.reframed_issue or "").lower()
        )
        checks["L3: pattern + inconsistency + gap identified"] = all([
            bool((analysis.repeating_pattern or "").strip()) or len(analysis.sequence) >= 2,
            bool((analysis.inconsistency or "").strip()),
            bool((analysis.gap or "").strip()),
        ])

        # 6–8: Layer 4
        checks["L4: 1+ alternative interpretation"] = len(analysis.interpretations) >= 1
        checks["L4: skeptic's challenge written"] = bool((analysis.skeptics_challenge or "").strip())
        checks["L4: absolute language checked/replaced"] = analysis.layer4_verified

        # 9–11: Layer 5
        checks["L5: key evidence weighted"] = len(analysis.weighted_evidence) >= 1
        # The checklist requires 5+ biases *checked* (not necessarily present/mitigated).
        # fallacies_identified keys represent every bias the analyst reviewed, whether
        # present or not (value may be "N/A" or empty string for absent biases).
        checks["L5: 5+ biases/fallacies checked"] = len(analysis.fallacies_identified) >= 5
        checks["L5: conclusion does not exceed evidence"] = analysis.layer5_verified

        # 12–15: Layer 6
        checks["L6: uncertainty stated"] = bool((analysis.uncertainty_statement or "").strip())
        checks["L6: resolving evidence identified"] = bool((analysis.evidence_to_resolve or "").strip())
        checks["L6: action is specific with deadline"] = (
            bool((analysis.specific_action or "").strip()) and bool((analysis.deadline or "").strip())
        )
        checks["L6: fallback position exists"] = bool((analysis.fallback_position or "").strip())

        # 16–18: Layer 7
        brief = analysis.executive_brief or ""
        word_count = len(brief.split())
        checks["L7: narrative summary (plain language)"] = bool((analysis.narrative_summary or "").strip())
        checks["L7: executive brief ≤75 words"] = bool(brief.strip()) and word_count <= 75
        checks["L7: action sheet with contingencies"] = (
            len(analysis.action_sheet) >= 1
            and all("if_blocked" in step for step in analysis.action_sheet)
        )

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        return {
            "checks": checks,
            "passed": passed,
            "total": total,
            "score": f"{passed}/{total}",
            "all_pass": passed == total,
        }

    def scan_absolute_language(self, text: str) -> list[str]:
        """Return list of flagged absolute terms found in text."""
        lower = text.lower()
        return [term for term in self.ABSOLUTE_TERMS if term in lower]

    def render_template(self, analysis: UNAFAnalysis) -> str:
        """Render the analysis as a filled Markdown document."""
        lines = []

        def h(level: int, title: str):
            lines.append(f"\n{'#' * level} {title}\n")

        def field_line(label: str, value: str):
            lines.append(f"**{label}:** {value or '_________________'}")

        def table(headers: list[str], rows: list[list[str]]):
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(c) or "_" for c in row) + " |")

        h(1, "Universal Analytical Framework (UNAF) — Analysis Document")
        h(2, "Metadata")
        for label, val in [
            ("Analyst", analysis.analyst),
            ("Date", analysis.date),
            ("Topic / Source Material", analysis.topic),
            ("Purpose", analysis.purpose),
        ]:
            field_line(label, val)

        # Layer 0
        h(2, "Layer 0 — Exact Capture")
        if analysis.evidence:
            table(
                ["#", "Source", "Verbatim Text", "Timestamp", "Type"],
                [[str(e.item_number), e.source, e.verbatim_text, e.timestamp, e.entry_type]
                 for e in analysis.evidence],
            )
        field_line("What was NOT said", analysis.not_said)
        lines.append(f"\n_Verified: {analysis.layer0_verified}_")

        # Layer 1
        h(2, "Layer 1 — Hidden Assumptions")
        if analysis.assumptions:
            table(
                ["#", "Assumption", "Why Unproven", "Counter-Evidence"],
                [[str(i + 1), a.assumption, a.why_unproven, a.counter_evidence]
                 for i, a in enumerate(analysis.assumptions)],
            )
        field_line("Source assumptions", analysis.source_assumptions)
        field_line("Credibility assumptions", analysis.credibility_assumptions)
        lines.append(f"\n_Verified: {analysis.layer1_verified}_")

        # Layer 2
        h(2, "Layer 2 — Question Behind the Question")
        for label, val in [
            ("Surface question", analysis.surface_question),
            ("Unstated goal", analysis.unstated_goal),
            ("Actual need", analysis.actual_need),
            ("Reframed issue", analysis.reframed_issue),
            ("Source fear", analysis.source_fear),
            ("My fear", analysis.my_fear),
            ("Power dynamics", analysis.power_dynamics),
        ]:
            field_line(label, val)
        lines.append(f"\n_Verified: {analysis.layer2_verified}_")

        # Layer 3
        h(2, "Layer 3 — Structural Patterns")
        seq = " → ".join(analysis.sequence) if analysis.sequence else "_________________"
        field_line("Sequence", seq)
        for label, val in [
            ("Repeating pattern", analysis.repeating_pattern),
            ("Inconsistency", analysis.inconsistency),
            ("Gap", analysis.gap),
            ("Framing device", analysis.framing_device),
            ("Emphasized", analysis.emphasized),
            ("Minimized / omitted", analysis.minimized),
        ]:
            field_line(label, val)
        lines.append(f"\n_Verified: {analysis.layer3_verified}_")

        # Layer 4
        h(2, "Layer 4 — Alternative Interpretations + Skeptic's Challenge")
        if analysis.interpretations:
            table(
                ["Claim", "Favorable", "Alternative", "Neutral", "Confidence"],
                [[i.claim, i.favorable_to_source, i.alternative,
                  i.neutral_technical, i.confidence.value]
                 for i in analysis.interpretations],
            )
        field_line("Most parsimonious", analysis.most_parsimonious)
        h(3, "Skeptic's Challenge (Mandatory)")
        lines.append(analysis.skeptics_challenge or "_________________")
        field_line("Evidence needed to defeat challenge", analysis.evidence_to_defeat_challenge)
        field_line("Preferred interpretation survives?", analysis.preferred_survives_without_it)
        if analysis.absolute_language_found:
            lines.append(f"\n**Absolute language flagged:** {', '.join(analysis.absolute_language_found)}")
        lines.append(f"\n_Verified: {analysis.layer4_verified}_")

        # Layer 5
        h(2, "Layer 5 — Evidence Weighting & Fallacy Check")
        if analysis.weighted_evidence:
            table(
                ["Evidence", "Weight", "Rationale", "Would Change Mind?"],
                [[e.description, e.weight.value, e.rationale,
                  "Yes" if e.would_change_mind_if_disproven else "No"]
                 for e in analysis.weighted_evidence],
            )
        if analysis.fallacies_identified:
            h(3, "Fallacy / Bias Check")
            table(
                ["Bias / Fallacy", "Mitigation"],
                [[k, v] for k, v in analysis.fallacies_identified.items()],
            )
        lines.append(f"\n_Verified: {analysis.layer5_verified}_")

        # Layer 6
        h(2, "Layer 6 — Decision & Response")
        for label, val in [
            ("Strongest supportable claim", analysis.strongest_claim),
            ("Confidence", analysis.confidence.value),
            ("Specific action requested", analysis.specific_action),
            ("Responsible party", analysis.responsible_party),
            ("Deadline", analysis.deadline),
        ]:
            field_line(label, val)
        h(3, "Uncertainty Statement (Mandatory)")
        field_line("What I do not know", analysis.uncertainty_statement)
        field_line("Evidence to resolve", analysis.evidence_to_resolve)
        h(3, "Fallback Position (Mandatory)")
        field_line("Fallback", analysis.fallback_position)
        field_line("Minimum acceptable", analysis.minimum_acceptable)
        field_line("Walk-away threshold", analysis.walk_away_threshold)
        lines.append(f"\n_Verified: {analysis.layer6_verified}_")

        # Layer 7
        h(2, "Layer 7 — Summary Generator")
        h(3, "7A — Narrative Summary")
        lines.append(analysis.narrative_summary or "_________________")
        h(3, "7B — Executive Brief")
        word_count = len(analysis.executive_brief.split()) if analysis.executive_brief else 0
        lines.append(analysis.executive_brief or "_________________")
        lines.append(f"\n_Word count: {word_count} / 75_")
        h(3, "7C — Action Sheet")
        if analysis.action_sheet:
            table(
                ["#", "What I will do", "By when", "If blocked"],
                [[str(i + 1), s.get("what", ""), s.get("by_when", ""), s.get("if_blocked", "")]
                 for i, s in enumerate(analysis.action_sheet)],
            )
        field_line("Most important action", analysis.most_important_action)
        field_line("Potential derailer", analysis.potential_derailer)
        field_line("Who else needs to know", analysis.who_else_needs_to_know)
        lines.append(f"\n_Verified: {analysis.layer7_verified}_")

        return "\n".join(lines)

    def check_action_threshold(self, analysis: UNAFAnalysis) -> dict:
        """
        Escalation / threshold check — determines whether evidence is strong
        enough to act at all, or whether more evidence should be gathered first.
        Returns a recommendation: 'act', 'gather_more', or 'do_not_act'.
        """
        high_weight_count = sum(
            1 for e in analysis.weighted_evidence
            if e.weight == EvidenceWeight.HIGH
        )
        total_evidence = len(analysis.evidence)
        has_fallback = bool((analysis.fallback_position or "").strip())
        confidence_ok = analysis.confidence in (ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM)

        if high_weight_count >= 2 and confidence_ok and has_fallback:
            recommendation = "act"
            rationale = (
                f"{high_weight_count} high-weight evidence items support action at "
                f"{analysis.confidence.value} confidence with a documented fallback."
            )
        elif total_evidence >= 1 and confidence_ok:
            recommendation = "gather_more"
            rationale = (
                "Evidence exists but high-weight items are insufficient for proportionate action. "
                "Gather additional primary sources before proceeding."
            )
        else:
            recommendation = "do_not_act"
            rationale = (
                "Evidence base is too thin or confidence is Low. "
                "Acting now risks overclaiming and undermining credibility."
            )

        return {
            "recommendation": recommendation,
            "rationale": rationale,
            "high_weight_count": high_weight_count,
            "total_evidence": total_evidence,
            "confidence": analysis.confidence.value,
        }
