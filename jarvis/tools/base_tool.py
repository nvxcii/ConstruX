"""
Base Tool Interface for Jarvis Assistant
All tools must extend this class to be discoverable by the orchestrator.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all Jarvis tools.

    Each tool defines its name, description, and input schema for Claude's
    tool_use API, plus an execute() method that performs the actual work.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Return the Claude tool_use schema for this tool.

        Returns:
            Dict matching Anthropic's tool schema format:
            {
                "name": "tool_name",
                "description": "What the tool does",
                "input_schema": { JSON Schema for parameters }
            }
        """
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with the given parameters.

        Args:
            **kwargs: Parameters matching the input_schema.

        Returns:
            A string result to send back to Claude as a tool_result.
        """
        pass

    def get_base_schema(self) -> Dict[str, Any]:
        """Helper to build schema with name and description pre-filled."""
        return {
            "name": self.name,
            "description": self.description,
        }

    def requires_confirmation(self, **kwargs) -> bool:
        """Override to require user confirmation for destructive actions.

        Returns:
            True if this invocation should prompt the user before executing.
        """
        return False

    def confirmation_message(self, **kwargs) -> str:
        """Message to show when requesting confirmation."""
        return f"Allow {self.name} to proceed?"
