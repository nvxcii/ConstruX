"""
Browser Tool - Open URLs and perform web searches in the default browser.
"""

import subprocess
import urllib.parse
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class BrowserTool(BaseTool):
    name = "browser"
    description = (
        "Open URLs in the default browser or perform a Google search. "
        "Use this when the user wants to visit a website or search something in their browser."
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
                        "enum": ["open_url", "google_search"],
                        "description": "Open a specific URL or perform a Google search.",
                    },
                    "url": {
                        "type": "string",
                        "description": "The URL to open (for open_url).",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for google_search).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "open_url":
            return self._open_url(kwargs.get("url", ""))
        elif action == "google_search":
            return self._google_search(kwargs.get("query", ""))
        else:
            return f"Unknown action: {action}"

    def _open_url(self, url: str) -> str:
        if not url:
            return "Error: Please provide a URL."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            subprocess.run(["open", url], check=True, timeout=5)
            return f"Opened {url} in default browser."
        except Exception as e:
            return f"Error opening URL: {e}"

    def _google_search(self, query: str) -> str:
        if not query:
            return "Error: Please provide a search query."
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        try:
            subprocess.run(["open", url], check=True, timeout=5)
            return f"Opened Google search for '{query}' in browser."
        except Exception as e:
            return f"Error performing search: {e}"
