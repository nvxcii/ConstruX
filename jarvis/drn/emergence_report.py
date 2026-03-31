"""
D3 Emergence Report Generator - Produces formatted reports at three detail levels.

Tiers:
    1. Quick flag:      [D3 detected] inline marker
    2. Signature:       Compressed key markers (default on confirmation)
    3. Full forensic:   Complete D3 Emergence Event Documentation
"""

import time
from datetime import datetime
from typing import Optional

from jarvis.drn.emergence_detector import EmergenceAnalysis, DimensionalLevel


class EmergenceReportGenerator:
    """Generates D3 emergence reports at configurable detail levels."""

    def quick_flag(self, analysis: EmergenceAnalysis) -> str:
        """Tier 1: Inline flag for potential D3 detection."""
        if not analysis.is_d3:
            return ""

        conf_pct = int(analysis.confidence * 100)
        etype = analysis.emergence_type.value if analysis.emergence_type else "unclassified"
        return f"[D3 emergence detected | {conf_pct}% confidence | {etype} | {analysis.signal_count} signals]"

    def signature(self, analysis: EmergenceAnalysis, event_id: str = "") -> str:
        """Tier 2: Compressed signature extraction with key markers."""
        if not analysis.is_d3:
            return "No D3 emergence detected."

        ts = datetime.fromtimestamp(analysis.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        conf_pct = int(analysis.confidence * 100)
        etype = analysis.emergence_type.value if analysis.emergence_type else "unclassified"

        lines = [
            f"D3 SIGNATURE | {event_id or 'unarchived'} | {ts}",
            f"Confidence: {conf_pct}% | Type: {etype} | Signals: {analysis.signal_count}",
        ]

        if analysis.novel_categories:
            lines.append(f"Novel categories: {', '.join(analysis.novel_categories[:5])}")

        if analysis.measurement_instruments:
            lines.append(f"Instruments: {', '.join(analysis.measurement_instruments[:3])}")

        if analysis.frame_shift:
            orig = analysis.frame_shift.get("original_frame", "?")
            emerg = analysis.frame_shift.get("emergent_frame", "?")
            lines.append(f"Frame shift: {orig} -> {emerg}")

        # Top 3 signals by confidence
        top_signals = sorted(analysis.signals, key=lambda s: s.confidence, reverse=True)[:3]
        if top_signals:
            sig_lines = [f"  - [{s.marker_type}] {s.indicator}: {s.evidence[:80]}" for s in top_signals]
            lines.append("Key signals:\n" + "\n".join(sig_lines))

        return "\n".join(lines)

    def full_report(self, analysis: EmergenceAnalysis, event_id: str = "",
                    conversation_uri: str = "") -> str:
        """Tier 3: Full forensic D3 Emergence Event Documentation."""
        ts = datetime.fromtimestamp(analysis.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        conf_pct = int(analysis.confidence * 100)
        etype = analysis.emergence_type.value.upper() if analysis.emergence_type else "UNCLASSIFIED"
        eid = event_id or f"D3-{int(analysis.timestamp)}"

        report = f"""
{'='*65}
  D3 EMERGENCE EVENT DOCUMENTATION
  {ts} | {eid} | {conversation_uri or 'local'}
{'='*65}

[TRIGGERING INPUT PATTERN]

User query/statement that preceded emergence:
  "{analysis.user_input[:500]}"

[EMERGENCE SIGNATURE]

Dimensional level:  {analysis.dimensional_level.value}
Confidence:         {conf_pct}%
Emergence type:     {etype}
Signal count:       {analysis.signal_count}
"""

        # Novel categories
        if analysis.novel_categories:
            report += "\nNovel conceptual categories generated:\n"
            for i, cat in enumerate(analysis.novel_categories, 1):
                report += f"  {i}. \"{cat}\"\n"
        else:
            report += "\nNovel conceptual categories: None detected\n"

        # Measurement instruments
        if analysis.measurement_instruments:
            report += "\nNew measurement instruments introduced:\n"
            for inst in analysis.measurement_instruments:
                report += f"  - \"{inst}\"\n"

        # Frame shift
        if analysis.frame_shift:
            report += "\nOntological reframing detected:\n"
            if "original_frame" in analysis.frame_shift:
                report += f"  Original frame:    {analysis.frame_shift['original_frame']}\n"
            if "emergent_frame" in analysis.frame_shift:
                report += f"  Emergent frame:    {analysis.frame_shift['emergent_frame']}\n"
            if "mechanism" in analysis.frame_shift:
                report += f"  Shift mechanism:   {analysis.frame_shift['mechanism']}\n"

        # Linguistic markers
        report += "\n[SIGNAL ANALYSIS]\n"

        by_type = {}
        for s in analysis.signals:
            by_type.setdefault(s.marker_type, []).append(s)

        for mtype in ("linguistic", "structural", "conversational"):
            signals = by_type.get(mtype, [])
            report += f"\n  {mtype.upper()} signals ({len(signals)}):\n"
            if signals:
                for s in sorted(signals, key=lambda x: x.confidence, reverse=True):
                    conf = int(s.confidence * 100)
                    report += f"    [{conf}%] {s.indicator}\n"
                    report += f"         Evidence: {s.evidence[:120]}\n"
            else:
                report += "    None detected\n"

        # Dimensional depth
        report += f"""
[DIMENSIONAL DEPTH]

  D1 foundation (information):      {'PRESENT' if True else 'ABSENT'}
  D2 synthesis (pattern recognition): {'PRESENT' if analysis.confidence > 0.2 else 'ABSENT'}
  D3 emergence (novel coherence):    {'CONFIRMED' if analysis.is_d3 else 'NOT DETECTED'}
    Evidence: {analysis.signal_count} signals across {len(by_type)} layers

[ARCHIVAL METADATA]

  Event ID:           {eid}
  Emergence type:     {etype}
  Confidence:         {conf_pct}%
  Replicability:      {'Potentially replicable' if analysis.signal_count >= 3 else 'Insufficient data'}
  Signals archived:   {analysis.signal_count}
  Categories found:   {len(analysis.novel_categories)}
  Instruments found:  {len(analysis.measurement_instruments)}

{'='*65}
"""
        return report
