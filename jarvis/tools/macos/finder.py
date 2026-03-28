"""
Finder Tool - File system operations via macOS Finder and shell commands.
"""

import glob
import os
import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class FinderTool(BaseTool):
    name = "finder"
    description = (
        "Interact with the macOS file system: open files/folders in Finder, "
        "search for files, list directory contents, and get file info."
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
                        "enum": ["open", "list", "search", "info"],
                        "description": "The action: open a file/folder, list directory, search files, or get file info.",
                    },
                    "path": {
                        "type": "string",
                        "description": "File or directory path.",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query or glob pattern (for search action).",
                    },
                    "directory": {
                        "type": "string",
                        "description": "Directory to search in (defaults to home directory).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "open":
            return self._open_path(kwargs.get("path", ""))
        elif action == "list":
            return self._list_directory(kwargs.get("path", ""))
        elif action == "search":
            return self._search_files(
                kwargs.get("query", ""),
                kwargs.get("directory", os.path.expanduser("~")),
            )
        elif action == "info":
            return self._file_info(kwargs.get("path", ""))
        else:
            return f"Unknown action: {action}"

    def _open_path(self, path: str) -> str:
        if not path:
            return "Error: Please provide a file or folder path."
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Error: Path does not exist: {path}"
        try:
            subprocess.run(["open", path], check=True, timeout=5)
            return f"Opened: {path}"
        except Exception as e:
            return f"Error opening path: {e}"

    def _list_directory(self, path: str) -> str:
        path = os.path.expanduser(path) if path else os.path.expanduser("~")
        if not os.path.isdir(path):
            return f"Error: Not a directory: {path}"
        try:
            entries = sorted(os.listdir(path))
            if not entries:
                return f"Directory is empty: {path}"
            items = []
            for entry in entries[:50]:  # Limit output
                full = os.path.join(path, entry)
                prefix = "[DIR] " if os.path.isdir(full) else "      "
                items.append(f"{prefix}{entry}")
            result = "\n".join(items)
            if len(entries) > 50:
                result += f"\n... and {len(entries) - 50} more items"
            return result
        except PermissionError:
            return f"Error: Permission denied for {path}"

    def _search_files(self, query: str, directory: str) -> str:
        if not query:
            return "Error: Please provide a search query."
        directory = os.path.expanduser(directory)

        # Use mdfind (Spotlight) for fast macOS search
        try:
            result = subprocess.run(
                ["mdfind", "-onlyin", directory, query],
                capture_output=True, text=True, timeout=10,
            )
            files = result.stdout.strip().split("\n")
            files = [f for f in files if f][:20]  # Limit to 20 results
            if not files:
                return f"No files found matching '{query}' in {directory}"
            return "\n".join(files)
        except Exception:
            # Fallback to glob
            pattern = os.path.join(directory, "**", f"*{query}*")
            matches = glob.glob(pattern, recursive=True)[:20]
            if not matches:
                return f"No files found matching '{query}' in {directory}"
            return "\n".join(matches)

    def _file_info(self, path: str) -> str:
        if not path:
            return "Error: Please provide a file path."
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Error: Path does not exist: {path}"
        try:
            stat = os.stat(path)
            size = stat.st_size
            if size > 1_000_000:
                size_str = f"{size / 1_000_000:.1f} MB"
            elif size > 1_000:
                size_str = f"{size / 1_000:.1f} KB"
            else:
                size_str = f"{size} bytes"

            import datetime
            modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            file_type = "Directory" if os.path.isdir(path) else "File"

            return f"Path: {path}\nType: {file_type}\nSize: {size_str}\nModified: {modified}"
        except Exception as e:
            return f"Error getting file info: {e}"
