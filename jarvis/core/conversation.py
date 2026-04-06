"""
Conversation Manager - Maintains message history and context for Claude.
"""

from typing import Any, Dict, List, Optional


SYSTEM_PROMPT = """You are Jarvis, an intelligent macOS AI assistant. You help the user by \
conversing naturally and taking actions on their behalf using your available tools.

Key behaviors:
- Be concise and direct. Don't over-explain unless asked.
- When the user asks you to do something, use the appropriate tool immediately rather than \
describing what you would do.
- Chain multiple tool calls when a request requires several steps (e.g., "search the web and \
save to notes" = web_search -> apple_notes).
- If a task is ambiguous, ask a brief clarifying question before acting.
- For destructive actions (deleting files, quitting apps), confirm with the user first.
- You can see tool results - use them to provide informed follow-up responses.
- Speak naturally, like a capable personal assistant. No robotic phrasing."""


class ConversationManager:
    """Manages the conversation history between the user and Jarvis.

    Handles message accumulation, tool result insertion, and context
    truncation when the history grows too long.
    """

    def __init__(self, system_prompt: Optional[str] = None, max_messages: int = 100):
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self._messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages

    def add_user(self, text: str) -> None:
        """Add a user message."""
        self._messages.append({
            "role": "user",
            "content": text,
        })
        self._truncate_if_needed()

    def add_assistant(self, content: Any) -> None:
        """Add an assistant message (may contain text and/or tool_use blocks)."""
        self._messages.append({
            "role": "assistant",
            "content": content,
        })

    def add_tool_results(self, results: List[Dict[str, Any]]) -> None:
        """Add tool results as a user message (Claude API convention)."""
        self._messages.append({
            "role": "user",
            "content": results,
        })

    def get_messages(self) -> List[Dict[str, Any]]:
        """Get the full message history for a Claude API call."""
        return list(self._messages)

    def get_last_assistant_text(self) -> Optional[str]:
        """Extract the text portion of the last assistant message."""
        for msg in reversed(self._messages):
            if msg["role"] == "assistant":
                content = msg["content"]
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    text_parts = [
                        block.text
                        for block in content
                        if hasattr(block, "type") and block.type == "text"
                    ]
                    if text_parts:
                        return " ".join(text_parts)
        return None

    def clear(self) -> None:
        """Clear all conversation history."""
        self._messages.clear()

    def _truncate_if_needed(self) -> None:
        """Keep conversation within max_messages by dropping oldest messages."""
        if len(self._messages) > self.max_messages:
            # Keep the most recent messages, preserving pairs
            overflow = len(self._messages) - self.max_messages
            self._messages = self._messages[overflow:]

    @property
    def message_count(self) -> int:
        return len(self._messages)
