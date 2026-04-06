"""
Memory Tool - Allows Claude to store and retrieve persistent memories.
"""

from typing import Any, Dict

from jarvis.memory.persistent_memory import PersistentMemory
from jarvis.tools.base_tool import BaseTool


class MemoryTool(BaseTool):
    name = "memory"
    description = (
        "Store and retrieve persistent memories across sessions. "
        "Use this to remember facts about the user, their preferences, "
        "important context, or anything that should persist permanently. "
        "Also use this to recall previously stored information."
    )

    def __init__(self, memory: PersistentMemory = None):
        self._memory = memory or PersistentMemory()

    @property
    def memory(self) -> PersistentMemory:
        return self._memory

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["remember", "recall", "search", "forget", "list", "stats"],
                        "description": (
                            "'remember': store a new fact/preference/context. "
                            "'recall': retrieve a specific memory by key. "
                            "'search': search memories by keyword. "
                            "'forget': remove a memory. "
                            "'list': list all memories in a category. "
                            "'stats': show tool usage statistics."
                        ),
                    },
                    "category": {
                        "type": "string",
                        "enum": ["fact", "preference", "context", "project", "person"],
                        "description": (
                            "Memory category: 'fact' for things about the user, "
                            "'preference' for likes/settings, 'context' for ongoing topics, "
                            "'project' for project-specific info, 'person' for people/contacts."
                        ),
                    },
                    "key": {
                        "type": "string",
                        "description": "Short descriptive key for the memory (e.g., 'name', 'favorite_language').",
                    },
                    "value": {
                        "type": "string",
                        "description": "The content to remember.",
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
        if action == "remember":
            return self._remember(
                kwargs.get("category", "fact"),
                kwargs.get("key", ""),
                kwargs.get("value", ""),
            )
        elif action == "recall":
            return self._recall(
                kwargs.get("category", "fact"),
                kwargs.get("key", ""),
            )
        elif action == "search":
            return self._search(
                kwargs.get("query", ""),
                kwargs.get("category"),
            )
        elif action == "forget":
            return self._forget(
                kwargs.get("category", "fact"),
                kwargs.get("key", ""),
            )
        elif action == "list":
            return self._list_category(kwargs.get("category", "fact"))
        elif action == "stats":
            return self._show_stats()
        else:
            return f"Unknown action: {action}"

    def _remember(self, category: str, key: str, value: str) -> str:
        if not key or not value:
            return "Error: Both 'key' and 'value' are required to store a memory."
        self._memory.remember(category, key, value)
        return f"Remembered [{category}] {key}: {value}"

    def _recall(self, category: str, key: str) -> str:
        if not key:
            return "Error: 'key' is required to recall a memory."
        value = self._memory.recall(category, key)
        if value is None:
            return f"No memory found for [{category}] {key}"
        return f"[{category}] {key}: {value}"

    def _search(self, query: str, category: str = None) -> str:
        if not query:
            return "Error: 'query' is required for search."
        results = self._memory.search(query, category)
        if not results:
            return f"No memories found matching '{query}'."
        lines = [f"[{r['category']}] {r['key']}: {r['value']}" for r in results]
        return f"Found {len(results)} memories:\n" + "\n".join(lines)

    def _forget(self, category: str, key: str) -> str:
        if not key:
            return "Error: 'key' is required to forget a memory."
        if self._memory.forget(category, key):
            return f"Forgot [{category}] {key}"
        return f"No memory found for [{category}] {key}"

    def _list_category(self, category: str) -> str:
        memories = self._memory.recall_category(category)
        if not memories:
            return f"No memories in category '{category}'."
        lines = [f"- {m['key']}: {m['value']}" for m in memories]
        return f"Memories [{category}] ({len(memories)}):\n" + "\n".join(lines)

    def _show_stats(self) -> str:
        stats = self._memory.get_tool_usage_stats()
        if not stats:
            return "No tool usage data yet."
        lines = [
            f"- {s['tool_name']}: {s['count']} uses, "
            f"{s['successes']} successful, last used {s['last_used']}"
            for s in stats
        ]
        return "Tool usage (last 30 days):\n" + "\n".join(lines)
