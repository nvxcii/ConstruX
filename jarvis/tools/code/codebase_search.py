"""
Codebase Search Tool - Search and read files in local code repositories.
"""

import glob
import os
import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class CodebaseSearchTool(BaseTool):
    name = "codebase_search"
    description = (
        "Search and read files in local code repositories. Use this to find code, "
        "read source files, list project structure, or search for patterns in code."
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
                        "enum": ["search", "read", "tree", "grep"],
                        "description": (
                            "'search' to find files by name pattern, "
                            "'read' to read a file's contents, "
                            "'tree' to show project structure, "
                            "'grep' to search for text patterns in code."
                        ),
                    },
                    "path": {
                        "type": "string",
                        "description": "File path (for read) or directory path (for search/tree/grep).",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern: filename glob (for search) or text pattern (for grep).",
                    },
                    "file_type": {
                        "type": "string",
                        "description": "File extension filter, e.g. 'py', 'js', 'ts' (for grep/search).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "search":
            return self._search_files(
                kwargs.get("pattern", "*"),
                kwargs.get("path", "."),
                kwargs.get("file_type"),
            )
        elif action == "read":
            return self._read_file(kwargs.get("path", ""))
        elif action == "tree":
            return self._show_tree(kwargs.get("path", "."))
        elif action == "grep":
            return self._grep(
                kwargs.get("pattern", ""),
                kwargs.get("path", "."),
                kwargs.get("file_type"),
            )
        else:
            return f"Unknown action: {action}"

    def _search_files(self, pattern: str, directory: str, file_type: str = None) -> str:
        directory = os.path.expanduser(directory)
        if file_type:
            pattern = f"**/*.{file_type}"
        elif not ("*" in pattern or "?" in pattern):
            pattern = f"**/*{pattern}*"

        full_pattern = os.path.join(directory, pattern)
        matches = sorted(glob.glob(full_pattern, recursive=True))[:30]

        if not matches:
            return f"No files found matching '{pattern}' in {directory}"
        return "\n".join(matches)

    def _read_file(self, path: str) -> str:
        if not path:
            return "Error: Please provide a file path."
        path = os.path.expanduser(path)
        if not os.path.isfile(path):
            return f"Error: File not found: {path}"

        try:
            with open(path, "r", errors="replace") as f:
                content = f.read()
            # Limit output size
            if len(content) > 10000:
                content = content[:10000] + "\n\n[File truncated at 10000 characters...]"
            return f"File: {path}\n{'='*60}\n{content}"
        except Exception as e:
            return f"Error reading file: {e}"

    def _show_tree(self, directory: str) -> str:
        directory = os.path.expanduser(directory)
        if not os.path.isdir(directory):
            return f"Error: Not a directory: {directory}"

        lines = []
        count = 0
        max_items = 100

        for root, dirs, files in os.walk(directory):
            # Skip hidden and common non-essential directories
            dirs[:] = [d for d in sorted(dirs)
                       if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git")]

            level = root.replace(directory, "").count(os.sep)
            indent = "  " * level
            lines.append(f"{indent}{os.path.basename(root)}/")
            count += 1

            sub_indent = "  " * (level + 1)
            for f in sorted(files):
                if not f.startswith("."):
                    lines.append(f"{sub_indent}{f}")
                    count += 1
                    if count >= max_items:
                        lines.append(f"\n[Truncated at {max_items} items...]")
                        return "\n".join(lines)

        return "\n".join(lines) if lines else "Empty directory."

    def _grep(self, pattern: str, directory: str, file_type: str = None) -> str:
        if not pattern:
            return "Error: Please provide a search pattern."
        directory = os.path.expanduser(directory)

        cmd = ["grep", "-rn", "--include"]
        if file_type:
            cmd.append(f"*.{file_type}")
        else:
            cmd.append("*.*")
        cmd.extend(["-l", pattern, directory])

        try:
            # First find matching files
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            files = [f for f in result.stdout.strip().split("\n") if f][:20]

            if not files:
                return f"No matches for '{pattern}' in {directory}"

            # Then get context lines
            cmd2 = ["grep", "-rn", "--include"]
            if file_type:
                cmd2.append(f"*.{file_type}")
            else:
                cmd2.append("*.*")
            cmd2.extend(["-C", "2", pattern, directory])

            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=10)
            output = result2.stdout.strip()

            if len(output) > 5000:
                output = output[:5000] + "\n\n[Results truncated...]"

            return f"Found in {len(files)} file(s):\n\n{output}"

        except subprocess.TimeoutExpired:
            return "Error: Search timed out."
        except Exception as e:
            return f"Error searching: {e}"
