"""
Ollama Client Adapter - Local LLM backend for Jarvis.

Provides the same interface as Anthropic's client so the orchestrator
can switch between Claude API and a local Ollama model seamlessly.

Requires: Ollama installed and running locally.
    macOS: brew install ollama && ollama serve
    Then:  ollama pull llama3.1  (or mistral, gemma2, etc.)

Ollama exposes an OpenAI-compatible API at http://localhost:11434.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    requests = None


# ── Response types that mirror Anthropic SDK objects ────────────────

@dataclass
class TextBlock:
    type: str = "text"
    text: str = ""


@dataclass
class ToolUseBlock:
    type: str = "tool_use"
    id: str = ""
    name: str = ""
    input: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OllamaResponse:
    """Mirrors anthropic.types.Message enough for the orchestrator."""
    content: list = field(default_factory=list)
    stop_reason: Optional[str] = None


class OllamaClient:
    """Drop-in replacement for Anthropic() that routes to a local Ollama model.

    Usage:
        client = OllamaClient(model="llama3.1")
        # Same as: client = Anthropic(api_key=...)
        # Then:    client.messages.create(...)
    """

    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        if requests is None:
            raise ImportError(
                "The 'requests' package is required for Ollama mode. "
                "Install it with: pip install requests"
            )
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.messages = self  # So client.messages.create() works

    def create(self, model: str = None, max_tokens: int = 4096,
               system: str = "", messages: list = None,
               tools: list = None, **kwargs) -> OllamaResponse:
        """Send a chat completion to Ollama and parse the response.

        Ollama supports tool calling via its /api/chat endpoint for
        compatible models. For models without native tool support,
        we inject tool descriptions into the system prompt and parse
        tool calls from the text output.
        """
        use_model = model or self.model
        messages = messages or []

        # Try native tool calling first, fall back to prompt-based
        if tools:
            try:
                return self._call_with_native_tools(
                    use_model, system, messages, tools, max_tokens
                )
            except Exception:
                # Model doesn't support native tools — use prompt injection
                return self._call_with_prompt_tools(
                    use_model, system, messages, tools, max_tokens
                )
        else:
            return self._call_plain(use_model, system, messages, max_tokens)

    # ── Native tool calling (Ollama /api/chat with tools) ──────────

    def _call_with_native_tools(self, model, system, messages, tools, max_tokens):
        """Use Ollama's native tool calling support."""
        ollama_messages = self._convert_messages(system, messages)
        ollama_tools = self._convert_tools_to_ollama(tools)

        payload = {
            "model": model,
            "messages": ollama_messages,
            "tools": ollama_tools,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }

        resp = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        return self._parse_native_response(data)

    def _convert_tools_to_ollama(self, tools):
        """Convert Anthropic tool schemas to Ollama/OpenAI function format."""
        ollama_tools = []
        for tool in tools:
            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("input_schema", {}),
                },
            })
        return ollama_tools

    def _parse_native_response(self, data):
        """Parse Ollama's native response into our response format."""
        message = data.get("message", {})
        content_blocks = []

        # Text content
        text = message.get("content", "").strip()
        if text:
            content_blocks.append(TextBlock(text=text))

        # Tool calls
        tool_calls = message.get("tool_calls", [])
        for i, tc in enumerate(tool_calls):
            func = tc.get("function", {})
            args = func.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            content_blocks.append(ToolUseBlock(
                id=f"tool_{i}_{id(tc) % 10000:04d}",
                name=func.get("name", ""),
                input=args,
            ))

        if not content_blocks:
            content_blocks.append(TextBlock(text="I couldn't generate a response."))

        return OllamaResponse(content=content_blocks)

    # ── Prompt-based tool calling (fallback) ───────────────────────

    def _call_with_prompt_tools(self, model, system, messages, tools, max_tokens):
        """Inject tool descriptions into system prompt and parse JSON tool calls from output."""
        tool_prompt = self._build_tool_prompt(tools)
        enhanced_system = system + "\n\n" + tool_prompt

        ollama_messages = self._convert_messages(enhanced_system, messages)

        payload = {
            "model": model,
            "messages": ollama_messages,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }

        resp = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        text = data.get("message", {}).get("content", "").strip()
        return self._parse_text_for_tools(text, tools)

    def _build_tool_prompt(self, tools):
        """Build a prompt section describing available tools."""
        lines = [
            "You have access to the following tools. To use a tool, respond with a JSON block:",
            '```tool_call',
            '{"tool": "tool_name", "arguments": {"arg1": "value1"}}',
            '```',
            "",
            "Available tools:",
        ]
        for tool in tools:
            lines.append(f"\n## {tool['name']}")
            lines.append(f"{tool.get('description', '')}")
            schema = tool.get("input_schema", {})
            props = schema.get("properties", {})
            required = schema.get("required", [])
            if props:
                lines.append("Parameters:")
                for pname, pinfo in props.items():
                    req = " (required)" if pname in required else ""
                    lines.append(f"  - {pname}: {pinfo.get('description', pinfo.get('type', ''))}{req}")

        lines.append("\nIf you don't need a tool, just respond normally with text.")
        return "\n".join(lines)

    def _parse_text_for_tools(self, text, tools):
        """Parse the model's text output for tool call JSON blocks."""
        content_blocks = []
        tool_names = {t["name"] for t in tools}

        # Look for ```tool_call ... ``` blocks
        pattern = r'```(?:tool_call|json)?\s*\n?(\{[^`]*?\})\s*\n?```'
        matches = list(re.finditer(pattern, text, re.DOTALL))

        if matches:
            # Extract text before first match
            pre_text = text[:matches[0].start()].strip()
            if pre_text:
                content_blocks.append(TextBlock(text=pre_text))

            for i, match in enumerate(matches):
                try:
                    call = json.loads(match.group(1))
                    tool_name = call.get("tool", call.get("name", ""))
                    args = call.get("arguments", call.get("input", call.get("args", {})))
                    if tool_name in tool_names:
                        content_blocks.append(ToolUseBlock(
                            id=f"tool_{i}_{hash(match.group(1)) % 10000:04d}",
                            name=tool_name,
                            input=args if isinstance(args, dict) else {},
                        ))
                except (json.JSONDecodeError, AttributeError):
                    continue

            # Text after last match
            post_text = text[matches[-1].end():].strip()
            if post_text:
                content_blocks.append(TextBlock(text=post_text))
        else:
            # No tool calls found — plain text response
            content_blocks.append(TextBlock(text=text))

        if not content_blocks:
            content_blocks.append(TextBlock(text=text))

        return OllamaResponse(content=content_blocks)

    # ── Plain call (no tools) ──────────────────────────────────────

    def _call_plain(self, model, system, messages, max_tokens):
        """Simple chat call without tools."""
        ollama_messages = self._convert_messages(system, messages)

        payload = {
            "model": model,
            "messages": ollama_messages,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }

        resp = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        text = data.get("message", {}).get("content", "").strip()
        if not text:
            text = "I couldn't generate a response."

        return OllamaResponse(content=[TextBlock(text=text)])

    # ── Message conversion ─────────────────────────────────────────

    def _convert_messages(self, system, messages):
        """Convert Anthropic-style messages to Ollama/OpenAI format."""
        ollama_msgs = []

        if system:
            ollama_msgs.append({"role": "system", "content": system})

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if isinstance(content, str):
                ollama_msgs.append({"role": role, "content": content})
            elif isinstance(content, list):
                # Could be tool_use blocks (assistant) or tool_result blocks (user)
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        # Tool result
                        if block.get("type") == "tool_result":
                            tool_content = block.get("content", "")
                            text_parts.append(f"[Tool result: {tool_content}]")
                        elif block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    elif hasattr(block, "type"):
                        # Anthropic SDK objects or our dataclasses
                        if block.type == "text":
                            text_parts.append(block.text)
                        elif block.type == "tool_use":
                            text_parts.append(
                                f"[Called tool: {block.name}({json.dumps(block.input)})]"
                            )
                        elif block.type == "tool_result":
                            text_parts.append(f"[Tool result: {getattr(block, 'content', '')}]")

                if text_parts:
                    ollama_msgs.append({"role": role, "content": "\n".join(text_parts)})
            else:
                ollama_msgs.append({"role": role, "content": str(content)})

        return ollama_msgs

    # ── Health check ───────────────────────────────────────────────

    def is_available(self) -> bool:
        """Check if Ollama is running and reachable."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List locally available Ollama models."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []
