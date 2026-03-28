"""
Apple Notes Tool - Create, read, and search notes via AppleScript.
"""

import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class AppleNotesTool(BaseTool):
    name = "apple_notes"
    description = (
        "Create, read, and search Apple Notes. "
        "Use this to save information, create summaries, or retrieve existing notes."
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
                        "enum": ["create", "read", "search", "list"],
                        "description": "The action to perform on Apple Notes.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the note (for create/read).",
                    },
                    "body": {
                        "type": "string",
                        "description": "Body content of the note (for create).",
                    },
                    "folder": {
                        "type": "string",
                        "description": "Notes folder name. Defaults to 'Notes'.",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for search action).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "create":
            return self._create_note(
                kwargs.get("title", "Untitled"),
                kwargs.get("body", ""),
                kwargs.get("folder", "Notes"),
            )
        elif action == "read":
            return self._read_note(kwargs.get("title", ""))
        elif action == "search":
            return self._search_notes(kwargs.get("query", ""))
        elif action == "list":
            return self._list_notes(kwargs.get("folder", "Notes"))
        else:
            return f"Unknown action: {action}"

    def _run_applescript(self, script: str) -> str:
        """Execute an AppleScript and return the output."""
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                return f"AppleScript error: {result.stderr.strip()}"
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Error: AppleScript timed out."
        except FileNotFoundError:
            return "Error: osascript not found. This tool requires macOS."

    def _create_note(self, title: str, body: str, folder: str) -> str:
        # Escape quotes for AppleScript
        title_esc = title.replace('"', '\\"')
        body_esc = body.replace('"', '\\"').replace("\n", "\\n")
        folder_esc = folder.replace('"', '\\"')

        script = f'''
tell application "Notes"
    tell folder "{folder_esc}"
        make new note with properties {{name:"{title_esc}", body:"{body_esc}"}}
    end tell
end tell
'''
        result = self._run_applescript(script)
        if "error" in result.lower():
            return result
        return f"Note '{title}' created in folder '{folder}'."

    def _read_note(self, title: str) -> str:
        if not title:
            return "Error: Please provide a note title to read."

        title_esc = title.replace('"', '\\"')
        script = f'''
tell application "Notes"
    set matchedNotes to notes whose name is "{title_esc}"
    if (count of matchedNotes) > 0 then
        set theNote to item 1 of matchedNotes
        return (name of theNote) & "\\n---\\n" & (plaintext of theNote)
    else
        return "No note found with title: {title_esc}"
    end if
end tell
'''
        return self._run_applescript(script)

    def _search_notes(self, query: str) -> str:
        if not query:
            return "Error: Please provide a search query."

        query_esc = query.replace('"', '\\"')
        script = f'''
tell application "Notes"
    set results to ""
    repeat with aNote in notes
        if (name of aNote) contains "{query_esc}" or (plaintext of aNote) contains "{query_esc}" then
            set results to results & (name of aNote) & "\\n"
        end if
    end repeat
    if results is "" then
        return "No notes found matching: {query_esc}"
    end if
    return results
end tell
'''
        return self._run_applescript(script)

    def _list_notes(self, folder: str) -> str:
        folder_esc = folder.replace('"', '\\"')
        script = f'''
tell application "Notes"
    set noteList to ""
    tell folder "{folder_esc}"
        repeat with aNote in notes
            set noteList to noteList & (name of aNote) & "\\n"
        end repeat
    end tell
    if noteList is "" then
        return "No notes found in folder: {folder_esc}"
    end if
    return noteList
end tell
'''
        return self._run_applescript(script)
