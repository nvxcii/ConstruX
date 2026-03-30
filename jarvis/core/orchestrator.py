"""
Jarvis Orchestrator - The Brain
Uses Claude's tool_use API to reason about user requests and dispatch tools.
Integrates persistent memory, auto-tuning, and scheduled tasks.
"""

import sys
from typing import Any, Callable, Dict, List, Optional

from anthropic import Anthropic

from jarvis.core.conversation import ConversationManager
from jarvis.core.tool_registry import ToolRegistry


class Orchestrator:
    """Central orchestrator that connects voice/text input to Claude's
    tool_use API and routes tool calls to registered tools.

    Now with:
        - Persistent memory (injected into system prompt each call)
        - Auto-tuning (logs tool usage, learns defaults)
        - Scheduled tasks (background runner for deferred actions)

    Flow:
        user input -> conversation history -> Claude API (with tools)
        -> if tool_use: execute tools, log usage, feed results back
        -> repeat until Claude returns a final text response
        -> return text to user (and optionally speak it)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None,
        on_tool_call: Optional[Callable] = None,
        memory=None,
        auto_tuner=None,
        scheduler=None,
    ):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.registry = ToolRegistry()
        self.conversation = ConversationManager(system_prompt=system_prompt)
        self.on_tool_call = on_tool_call  # Optional callback for UI updates
        self.memory = memory          # PersistentMemory instance
        self.auto_tuner = auto_tuner  # AutoTuner instance
        self.scheduler = scheduler    # TaskScheduler instance

    def register_tools(self, tools: list) -> None:
        """Register tools with the orchestrator."""
        self.registry.register_many(tools)

    def process(self, user_input: str) -> str:
        """Process a user message and return the assistant's final text response.

        This is the main entry point. It:
        1. Adds user input to conversation
        2. Calls Claude with tools
        3. If Claude wants to use tools, executes them and loops
        4. Returns the final text response

        Args:
            user_input: The user's message (text from voice or keyboard).

        Returns:
            The assistant's final text response.
        """
        self.conversation.add_user(user_input)

        while True:
            response = self._call_claude()

            # Check if Claude wants to use tools
            tool_use_blocks = [
                block for block in response.content
                if block.type == "tool_use"
            ]

            if not tool_use_blocks:
                # No tool calls - extract final text and return
                self.conversation.add_assistant(response.content)
                text_parts = [
                    block.text for block in response.content
                    if block.type == "text"
                ]
                return " ".join(text_parts) if text_parts else ""

            # Execute tool calls and collect results
            self.conversation.add_assistant(response.content)
            tool_results = self._execute_tool_calls(tool_use_blocks)
            self.conversation.add_tool_results(tool_results)

    def _call_claude(self):
        """Make a Claude API call with the current conversation and tools.

        Injects persistent memory and auto-tuning context into the
        system prompt so Claude has cross-session awareness.
        """
        # Build dynamic system prompt with memory + tuning context
        system = self.conversation.system_prompt
        extra_context = []

        if self.memory:
            mem_ctx = self.memory.get_context_for_prompt()
            if mem_ctx:
                extra_context.append(mem_ctx)

        if self.auto_tuner:
            tune_ctx = self.auto_tuner.get_tuning_context()
            if tune_ctx:
                extra_context.append(tune_ctx)

        if extra_context:
            system = system + "\n\n--- Persistent Context ---\n" + "\n\n".join(extra_context)

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system,
            "messages": self.conversation.get_messages(),
        }

        schemas = self.registry.get_all_schemas()
        if schemas:
            kwargs["tools"] = schemas

        return self.client.messages.create(**kwargs)

    def _execute_tool_calls(self, tool_use_blocks: list) -> List[Dict[str, Any]]:
        """Execute a batch of tool calls and return results for Claude."""
        results = []

        for block in tool_use_blocks:
            tool_name = block.name
            tool_input = block.input

            # Notify UI if callback registered
            if self.on_tool_call:
                self.on_tool_call(tool_name, tool_input)

            # Check if confirmation is needed
            if self.registry.needs_confirmation(tool_name, **tool_input):
                msg = self.registry.get_confirmation_message(tool_name, **tool_input)
                if not self._confirm_with_user(msg):
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": "User denied this action.",
                    })
                    continue

            # Execute the tool
            result = self.registry.execute(tool_name, **tool_input)

            # Log tool usage for auto-tuning
            if self.auto_tuner:
                success = not str(result).startswith("Error")
                self.auto_tuner.log_usage(
                    tool_name, tool_input,
                    result_summary=str(result)[:200],
                    success=success,
                )

            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
            })

        return results

    def _confirm_with_user(self, message: str) -> bool:
        """Ask the user for confirmation before a destructive action."""
        try:
            print(f"\n[Confirmation required] {message}")
            response = input("Proceed? (y/n): ").strip().lower()
            return response in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            return False

    def reset_conversation(self) -> None:
        """Clear conversation history for a fresh start."""
        self.conversation.clear()
