"""
Apple Calendar Tool - Create and read calendar events via AppleScript.
"""

import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class AppleCalendarTool(BaseTool):
    name = "apple_calendar"
    description = (
        "Create and view events in Apple Calendar. "
        "Use this to schedule meetings, check today's agenda, or add events."
    )

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["create", "today", "list"],
                        "description": "The action: 'create' a new event, 'today' for today's events, 'list' for a specific date.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Event title (for create).",
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date/time in 'YYYY-MM-DD HH:MM' format.",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date/time in 'YYYY-MM-DD HH:MM' format.",
                    },
                    "location": {
                        "type": "string",
                        "description": "Event location (optional).",
                    },
                    "calendar_name": {
                        "type": "string",
                        "description": "Calendar name. Uses default calendar if omitted.",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date to list events for in 'YYYY-MM-DD' format (for list action).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "create":
            return self._create_event(
                kwargs.get("title", "Untitled Event"),
                kwargs.get("start_date", ""),
                kwargs.get("end_date", ""),
                kwargs.get("location"),
                kwargs.get("calendar_name"),
            )
        elif action == "today":
            return self._get_today_events()
        elif action == "list":
            return self._get_events_for_date(kwargs.get("date", ""))
        else:
            return f"Unknown action: {action}"

    def _run_applescript(self, script: str) -> str:
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode != 0:
                return f"AppleScript error: {result.stderr.strip()}"
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Error: AppleScript timed out."
        except FileNotFoundError:
            return "Error: osascript not found. This tool requires macOS."

    def _create_event(self, title: str, start_date: str, end_date: str,
                      location: str = None, calendar_name: str = None) -> str:
        if not start_date or not end_date:
            return "Error: Both start_date and end_date are required (format: 'YYYY-MM-DD HH:MM')."

        title_esc = title.replace('"', '\\"')

        props = f'summary:"{title_esc}", start date:date "{start_date}", end date:date "{end_date}"'
        if location:
            loc_esc = location.replace('"', '\\"')
            props += f', location:"{loc_esc}"'

        if calendar_name:
            cal_esc = calendar_name.replace('"', '\\"')
            cal_clause = f'tell calendar "{cal_esc}"'
        else:
            cal_clause = "tell (first calendar whose name is not missing value)"

        script = f'''
tell application "Calendar"
    {cal_clause}
        make new event with properties {{{props}}}
    end tell
end tell
'''
        result = self._run_applescript(script)
        if "error" in result.lower():
            return result
        return f"Event '{title}' created for {start_date}."

    def _get_today_events(self) -> str:
        script = '''
tell application "Calendar"
    set today to current date
    set todayStart to today - (time of today)
    set todayEnd to todayStart + (1 * days)
    set eventList to ""
    repeat with cal in calendars
        set todayEvents to (events of cal whose start date >= todayStart and start date < todayEnd)
        repeat with e in todayEvents
            set eventList to eventList & (summary of e) & " | " & time string of (start date of e) & " - " & time string of (end date of e) & "\\n"
        end repeat
    end repeat
    if eventList is "" then
        return "No events scheduled for today."
    end if
    return eventList
end tell
'''
        return self._run_applescript(script)

    def _get_events_for_date(self, date_str: str) -> str:
        if not date_str:
            return "Error: Please provide a date in 'YYYY-MM-DD' format."

        script = f'''
tell application "Calendar"
    set targetDate to date "{date_str}"
    set dayStart to targetDate - (time of targetDate)
    set dayEnd to dayStart + (1 * days)
    set eventList to ""
    repeat with cal in calendars
        set dayEvents to (events of cal whose start date >= dayStart and start date < dayEnd)
        repeat with e in dayEvents
            set eventList to eventList & (summary of e) & " | " & time string of (start date of e) & " - " & time string of (end date of e) & "\\n"
        end repeat
    end repeat
    if eventList is "" then
        return "No events found for {date_str}."
    end if
    return eventList
end tell
'''
        return self._run_applescript(script)
