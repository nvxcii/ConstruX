"""
Web Fetch Tool - Fetch and extract text content from web pages.
"""

from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class WebFetchTool(BaseTool):
    name = "web_fetch"
    description = (
        "Fetch the text content of a web page. Returns the main readable text, "
        "stripped of HTML. Use this to read articles, documentation, or any web page."
    )

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page to fetch.",
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "Maximum characters to return (default 5000).",
                    },
                },
                "required": ["url"],
            },
        }

    def execute(self, url: str, max_length: int = 5000, **kwargs) -> str:
        if not url:
            return "Error: Please provide a URL."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return "Error: 'requests' and 'beautifulsoup4' packages required. Run: pip install requests beautifulsoup4"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove script, style, nav, footer elements
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            # Try to get the main content
            main = soup.find("main") or soup.find("article") or soup.find("body")
            if main is None:
                return "Error: Could not extract content from page."

            text = main.get_text(separator="\n", strip=True)

            # Clean up excessive whitespace
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            text = "\n".join(lines)

            if len(text) > max_length:
                text = text[:max_length] + "\n\n[Content truncated...]"

            return f"Content from {url}:\n\n{text}"

        except Exception as e:
            return f"Error fetching URL: {e}"
