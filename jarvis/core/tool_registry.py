"""
Tool Registry - Discovers, registers, and routes tools for the orchestrator.
"""

from typing import Any, Dict, List, Optional
from jarvis.tools.base_tool import BaseTool


class ToolRegistry:
    """Manages all available tools for the Jarvis orchestrator.

    Tools are registered at startup. The registry provides:
    - Schema generation for Claude API tool_use calls
    - Routing tool calls to the correct tool's execute() method
    - Confirmation handling for destructive actions
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        if not tool.name:
            raise ValueError(f"Tool {tool.__class__.__name__} must define a 'name'")
        self._tools[tool.name] = tool

    def register_many(self, tools: List[BaseTool]) -> None:
        """Register multiple tools at once."""
        for tool in tools:
            self.register(tool)

    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Generate the tools array for Claude API calls."""
        return [tool.get_schema() for tool in self._tools.values()]

    def execute(self, tool_name: str, **kwargs) -> str:
        """Route a tool call to the correct tool and return the result.

        Args:
            tool_name: The name of the tool to execute.
            **kwargs: Parameters from Claude's tool_use block.

        Returns:
            String result from the tool execution.

        Raises:
            KeyError: If the tool is not registered.
        """
        tool = self._tools.get(tool_name)
        if tool is None:
            return f"Error: Unknown tool '{tool_name}'. Available tools: {list(self._tools.keys())}"

        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return f"Error executing {tool_name}: {e}"

    def needs_confirmation(self, tool_name: str, **kwargs) -> bool:
        """Check if a tool call requires user confirmation."""
        tool = self._tools.get(tool_name)
        if tool is None:
            return False
        return tool.requires_confirmation(**kwargs)

    def get_confirmation_message(self, tool_name: str, **kwargs) -> str:
        """Get the confirmation prompt for a tool call."""
        tool = self._tools.get(tool_name)
        if tool is None:
            return ""
        return tool.confirmation_message(**kwargs)

    @property
    def tool_names(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    @property
    def tool_count(self) -> int:
        return len(self._tools)
