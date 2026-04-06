"""
Web Search Tool - Search the internet via Brave Search, Tavily, or SerpAPI.
"""

import json
import os
from typing import Any, Dict, Optional

from jarvis.tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = (
        "Search the internet for current information. Returns titles, snippets, "
        "and URLs from web search results. Use this when you need up-to-date "
        "information that may not be in your training data."
    )

    def __init__(self, settings=None):
        self._settings = settings
        self._engine = None
        self._api_key = None
        if settings:
            self._engine = settings.get("web", "search_engine", "brave")
            self._api_key = (
                settings.get("web", "brave_api_key")
                or settings.get("web", "tavily_api_key")
            )

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default 5, max 10).",
                    },
                },
                "required": ["query"],
            },
        }

    def execute(self, query: str, num_results: int = 5, **kwargs) -> str:
        num_results = min(num_results, 10)
        engine = self._engine or "brave"

        if engine == "brave":
            return self._brave_search(query, num_results)
        elif engine == "tavily":
            return self._tavily_search(query, num_results)
        else:
            return f"Unsupported search engine: {engine}. Configure 'brave' or 'tavily' in settings."

    def _brave_search(self, query: str, num_results: int) -> str:
        api_key = self._api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not api_key:
            return "Error: Brave Search API key not configured. Set BRAVE_SEARCH_API_KEY env var."

        try:
            import requests
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key,
            }
            params = {"q": query, "count": num_results}
            resp = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers, params=params, timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            results = []
            for item in data.get("web", {}).get("results", [])[:num_results]:
                results.append(
                    f"Title: {item.get('title', 'N/A')}\n"
                    f"URL: {item.get('url', 'N/A')}\n"
                    f"Snippet: {item.get('description', 'N/A')}"
                )

            if not results:
                return f"No results found for: {query}"
            return "\n\n".join(results)

        except ImportError:
            return "Error: 'requests' package required. Run: pip install requests"
        except Exception as e:
            return f"Search error: {e}"

    def _tavily_search(self, query: str, num_results: int) -> str:
        api_key = self._api_key or os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: Tavily API key not configured. Set TAVILY_API_KEY env var."

        try:
            import requests
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": query,
                    "max_results": num_results,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            results = []
            for item in data.get("results", [])[:num_results]:
                results.append(
                    f"Title: {item.get('title', 'N/A')}\n"
                    f"URL: {item.get('url', 'N/A')}\n"
                    f"Snippet: {item.get('content', 'N/A')[:300]}"
                )

            if not results:
                return f"No results found for: {query}"
            return "\n\n".join(results)

        except ImportError:
            return "Error: 'requests' package required. Run: pip install requests"
        except Exception as e:
            return f"Search error: {e}"
