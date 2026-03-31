"""
DRN Tool - Allows Claude to query, search, and manage D3 emergence events.
"""

from typing import Any, Dict

from jarvis.drn.signature_library import SignatureLibrary
from jarvis.drn.emergence_report import EmergenceReportGenerator
from jarvis.tools.base_tool import BaseTool


class DRNTool(BaseTool):
    name = "drn"
    description = (
        "Query and manage the D3 Emergence Signature Library. "
        "Search past D3 events, view full reports, find patterns, "
        "confirm events, and get emergence statistics. "
        "Use this to study what conditions produce D3 emergence."
    )

    def __init__(self, library: SignatureLibrary = None):
        self._library = library or SignatureLibrary()
        self._reporter = EmergenceReportGenerator()

    @property
    def library(self) -> SignatureLibrary:
        return self._library

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "list", "search", "view", "confirm",
                            "patterns", "stats", "related",
                        ],
                        "description": (
                            "'list': list recent D3 events. "
                            "'search': search events by keyword. "
                            "'view': view full report for an event. "
                            "'confirm': mark an event as user-confirmed. "
                            "'patterns': show recurring emergence patterns. "
                            "'stats': show library statistics. "
                            "'related': find events related to a given event."
                        ),
                    },
                    "event_id": {
                        "type": "string",
                        "description": "Event ID (for view/confirm/related).",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for search action).",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default 10).",
                    },
                    "confirmed_only": {
                        "type": "boolean",
                        "description": "Only show user-confirmed events (for list).",
                    },
                    "emergence_type": {
                        "type": "string",
                        "enum": ["conceptual", "structural", "methodological", "ontological"],
                        "description": "Filter by emergence type (for list).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "list":
            return self._list_events(
                kwargs.get("limit", 10),
                kwargs.get("confirmed_only", False),
                kwargs.get("emergence_type"),
            )
        elif action == "search":
            return self._search(kwargs.get("query", ""), kwargs.get("limit", 10))
        elif action == "view":
            return self._view_event(kwargs.get("event_id", ""))
        elif action == "confirm":
            return self._confirm_event(kwargs.get("event_id", ""))
        elif action == "patterns":
            return self._show_patterns()
        elif action == "stats":
            return self._show_stats()
        elif action == "related":
            return self._find_related(kwargs.get("event_id", ""))
        else:
            return f"Unknown action: {action}"

    def _list_events(self, limit: int, confirmed_only: bool,
                     emergence_type: str = None) -> str:
        events = self._library.list_events(
            limit=limit,
            confirmed_only=confirmed_only,
            emergence_type=emergence_type,
        )
        if not events:
            return "No D3 events in the library."

        lines = []
        for e in events:
            conf = int(e.get("confidence", 0) * 100)
            etype = e.get("emergence_type", "?")
            confirmed = " [CONFIRMED]" if e.get("confirmed_by_user") else ""
            categories = e.get("novel_categories", [])
            if isinstance(categories, str):
                import json
                categories = json.loads(categories)
            cat_str = f" | Categories: {', '.join(categories[:3])}" if categories else ""
            lines.append(
                f"  {e['event_id']} | {conf}% | {etype}{confirmed}{cat_str}"
            )

        return f"D3 Events ({len(events)}):\n" + "\n".join(lines)

    def _search(self, query: str, limit: int) -> str:
        if not query:
            return "Error: 'query' is required for search."
        events = self._library.search_events(query, limit)
        if not events:
            return f"No events found matching '{query}'."

        lines = []
        for e in events:
            conf = int(e.get("confidence", 0) * 100)
            lines.append(f"  {e['event_id']} | {conf}% | {e.get('emergence_type', '?')}")

        return f"Search results for '{query}' ({len(events)}):\n" + "\n".join(lines)

    def _view_event(self, event_id: str) -> str:
        if not event_id:
            return "Error: 'event_id' is required."
        event = self._library.get_event(event_id)
        if not event:
            return f"Event not found: {event_id}"

        # Reconstruct a minimal analysis for the report generator
        from jarvis.drn.emergence_detector import (
            EmergenceAnalysis, DimensionalLevel, EmergenceType, D3Signal
        )

        signals = []
        for s in event.get("signals_json", []):
            if isinstance(s, dict):
                signals.append(D3Signal(
                    marker_type=s.get("marker_type", ""),
                    indicator=s.get("indicator", ""),
                    evidence=s.get("evidence", ""),
                    confidence=s.get("confidence", 0),
                    weight=s.get("weight", 1.0),
                ))

        level_map = {v.value: v for v in DimensionalLevel}
        type_map = {v.value: v for v in EmergenceType}

        analysis = EmergenceAnalysis(
            dimensional_level=level_map.get(
                event.get("dimensional_level", ""), DimensionalLevel.D3
            ),
            confidence=event.get("confidence", 0),
            signals=signals,
            novel_categories=event.get("novel_categories", []),
            measurement_instruments=event.get("measurement_instruments", []),
            frame_shift=event.get("frame_shift"),
            emergence_type=type_map.get(event.get("emergence_type", ""), None),
            timestamp=event.get("timestamp", 0),
            user_input=event.get("user_input", ""),
            assistant_response=event.get("assistant_response", "")[:2000],
        )

        return self._reporter.full_report(analysis, event_id=event_id)

    def _confirm_event(self, event_id: str) -> str:
        if not event_id:
            return "Error: 'event_id' is required."
        if self._library.confirm_event(event_id):
            return f"Event {event_id} confirmed."
        return f"Could not confirm {event_id} (not found)."

    def _show_patterns(self) -> str:
        patterns = self._library.get_patterns(min_frequency=1)
        if not patterns:
            return "No recurring patterns detected yet. More D3 events needed."

        lines = []
        for p in patterns:
            lines.append(
                f"  Pattern: {p['pattern']}\n"
                f"    Frequency: {p['frequency']} | "
                f"Events: {len(p['event_ids'])}"
            )

        return f"Emergence Patterns ({len(patterns)}):\n\n" + "\n\n".join(lines)

    def _show_stats(self) -> str:
        stats = self._library.get_statistics()
        lines = [
            f"D3 Signature Library Statistics",
            f"  Total events:     {stats['total_events']}",
            f"  Confirmed:        {stats['confirmed_events']}",
            f"  Unconfirmed:      {stats['unconfirmed']}",
            f"  Avg confidence:   {stats['average_confidence']*100:.1f}%",
            f"  Tracked patterns: {stats['tracked_patterns']}",
        ]

        if stats["by_type"]:
            lines.append("\n  By emergence type:")
            for t in stats["by_type"]:
                lines.append(
                    f"    {t['type']}: {t['count']} events "
                    f"(avg {t['avg_confidence']*100:.1f}%)"
                )

        return "\n".join(lines)

    def _find_related(self, event_id: str) -> str:
        if not event_id:
            return "Error: 'event_id' is required."
        related = self._library.find_related(event_id)
        if not related:
            return f"No related events found for {event_id}."

        lines = [f"  {e['event_id']} | {int(e['confidence']*100)}%" for e in related]
        return f"Events related to {event_id}:\n" + "\n".join(lines)
