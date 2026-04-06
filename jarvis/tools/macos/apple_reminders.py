"""
Apple Reminders Tool - Create and list reminders via AppleScript.
"""

import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class AppleRemindersTool(BaseTool):
    name = "apple_reminders"
    description = (
        "Create and list reminders in Apple Reminders. "
        "Use this to set tasks, to-dos, and time-based reminders."
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
                        "enum": ["create", "list", "complete"],
                        "description": "The action to perform.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the reminder.",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in 'YYYY-MM-DD HH:MM' format (optional).",
                    },
                    "list_name": {
                        "type": "string",
                        "description": "Reminders list name. Defaults to 'Reminders'.",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional notes for the reminder.",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "create":
            return self._create_reminder(
                kwargs.get("title", "Untitled"),
                kwargs.get("due_date"),
                kwargs.get("list_name", "Reminders"),
                kwargs.get("notes"),
            )
        elif action == "list":
            return self._list_reminders(kwargs.get("list_name", "Reminders"))
        elif action == "complete":
            return self._complete_reminder(kwargs.get("title", ""))
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

    def _create_reminder(self, title: str, due_date: str = None,
                         list_name: str = "Reminders", notes: str = None) -> str:
        title_esc = title.replace('"', '\\"')
        list_esc = list_name.replace('"', '\\"')

        props = f'name:"{title_esc}"'
        if notes:
            notes_esc = notes.replace('"', '\\"')
            props += f', body:"{notes_esc}"'

        if due_date:
            # Parse date and add due date property
            script = f'''
tell application "Reminders"
    tell list "{list_esc}"
        set newReminder to make new reminder with properties {{{props}}}
        set due date of newReminder to date "{due_date}"
    end tell
end tell
'''
        else:
            script = f'''
tell application "Reminders"
    tell list "{list_esc}"
        make new reminder with properties {{{props}}}
    end tell
end tell
'''
        result = self._run_applescript(script)
        if "error" in result.lower():
            return result
        return f"Reminder '{title}' created in '{list_name}'."

    def _list_reminders(self, list_name: str) -> str:
        list_esc = list_name.replace('"', '\\"')
        script = f'''
tell application "Reminders"
    set reminderList to ""
    tell list "{list_esc}"
        repeat with r in (reminders whose completed is false)
            set reminderList to reminderList & (name of r) & "\\n"
        end repeat
    end tell
    if reminderList is "" then
        return "No incomplete reminders in: {list_esc}"
    end if
    return reminderList
end tell
'''
        return self._run_applescript(script)

    def _complete_reminder(self, title: str) -> str:
        if not title:
            return "Error: Please provide a reminder title to complete."
        title_esc = title.replace('"', '\\"')
        script = f'''
tell application "Reminders"
    set matchedReminders to reminders whose name is "{title_esc}" and completed is false
    if (count of matchedReminders) > 0 then
        set completed of item 1 of matchedReminders to true
        return "Reminder '{title_esc}' marked as complete."
    else
        return "No incomplete reminder found: {title_esc}"
    end if
end tell
'''
        return self._run_applescript(script)
