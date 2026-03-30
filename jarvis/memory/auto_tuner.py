"""
Auto-Tuner - Learns from usage patterns and adjusts tool arguments automatically.

Tracks how the user uses tools, identifies patterns, and pre-fills
or suggests arguments based on past behavior. Also adjusts assistant
behavior preferences over time.
"""

import json
import time
from collections import Counter
from typing import Any, Dict, List, Optional

from jarvis.memory.persistent_memory import PersistentMemory


class AutoTuner:
    """Learns from tool usage and adapts Jarvis behavior over time.

    Capabilities:
        - Tracks tool usage frequency and patterns
        - Identifies default arguments per tool based on history
        - Detects user preferences from behavior (time of day, patterns)
        - Generates tuning suggestions for the system prompt
        - Auto-adjusts tool parameters based on success rates
    """

    def __init__(self, memory: PersistentMemory):
        self.memory = memory

    def log_usage(self, tool_name: str, arguments: Dict,
                  result_summary: str = "", success: bool = True) -> None:
        """Log a tool call for pattern analysis."""
        self.memory.log_tool_usage(tool_name, arguments, result_summary, success)

        # Auto-detect and store preferences from usage
        self._detect_preferences(tool_name, arguments)

    def get_suggested_defaults(self, tool_name: str) -> Dict[str, Any]:
        """Get suggested default arguments for a tool based on usage history.

        Analyzes past successful calls to determine the most common
        argument values and suggests them as defaults.
        """
        frequent = self.memory.get_frequent_arguments(tool_name, limit=10)
        if not frequent:
            return {}

        # Find the most common value for each argument key
        arg_values: Dict[str, Counter] = {}
        for entry in frequent:
            for key, value in entry["arguments"].items():
                if key not in arg_values:
                    arg_values[key] = Counter()
                arg_values[key][str(value)] += entry["count"]

        # Pick the most common value per argument
        defaults = {}
        for key, counter in arg_values.items():
            most_common = counter.most_common(1)
            if most_common:
                val = most_common[0][0]
                # Only suggest if it appears in >40% of uses
                total = sum(counter.values())
                if most_common[0][1] / total > 0.4:
                    defaults[key] = val

        return defaults

    def get_tuning_context(self) -> str:
        """Generate a context string about learned patterns for the system prompt.

        This is injected into Claude's context so it can proactively
        use learned preferences.
        """
        parts = []

        # Tool usage patterns
        stats = self.memory.get_tool_usage_stats(days=30)
        if stats:
            top_tools = [s for s in stats if isinstance(s.get("count"), int)][:5]
            if top_tools:
                tool_lines = [f"- {s['tool_name']}: used {s['count']} times" for s in top_tools]
                parts.append("Frequently used tools:\n" + "\n".join(tool_lines))

        # Learned defaults
        if stats:
            default_lines = []
            for s in stats:
                if isinstance(s.get("tool_name"), str):
                    defaults = self.get_suggested_defaults(s["tool_name"])
                    if defaults:
                        default_lines.append(
                            f"- {s['tool_name']}: typical args = {json.dumps(defaults)}"
                        )
            if default_lines:
                parts.append(
                    "Learned default arguments (use these unless the user says otherwise):\n"
                    + "\n".join(default_lines)
                )

        if not parts:
            return ""
        return "\n\n".join(parts)

    def _detect_preferences(self, tool_name: str, arguments: Dict) -> None:
        """Auto-detect preferences from tool usage patterns."""
        # Detect preferred Apple Notes folder
        if tool_name == "apple_notes" and "folder" in arguments:
            self.memory.remember(
                "preference", "default_notes_folder",
                arguments["folder"],
            )

        # Detect preferred calendar
        if tool_name == "apple_calendar" and "calendar_name" in arguments:
            self.memory.remember(
                "preference", "default_calendar",
                arguments["calendar_name"],
            )

        # Detect preferred search engine behavior
        if tool_name == "web_search" and "num_results" in arguments:
            self.memory.remember(
                "preference", "preferred_search_results_count",
                str(arguments["num_results"]),
            )

        # Detect preferred reminders list
        if tool_name == "apple_reminders" and "list_name" in arguments:
            self.memory.remember(
                "preference", "default_reminders_list",
                arguments["list_name"],
            )

        # Track time-of-day usage patterns
        hour = time.localtime().tm_hour
        if hour < 6:
            period = "late_night"
        elif hour < 12:
            period = "morning"
        elif hour < 17:
            period = "afternoon"
        elif hour < 21:
            period = "evening"
        else:
            period = "night"

        current = self.memory.recall("preference", "active_period")
        if current != period:
            self.memory.remember("preference", "active_period", period)
