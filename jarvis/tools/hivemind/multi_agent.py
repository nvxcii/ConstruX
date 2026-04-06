"""
Hivemind Tool - Wraps the existing multi_ai_framework for multi-model parallel tasks.

When Claude (the brain) determines a task would benefit from multiple AI perspectives,
it invokes this tool to dispatch work across Claude, Gemini, DeepSeek, and ChatGPT
in parallel, then synthesizes results.
"""

import os
import sys
from typing import Any, Dict, List

from jarvis.tools.base_tool import BaseTool

# Add parent path so we can import multi_ai_framework
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _root not in sys.path:
    sys.path.insert(0, _root)


class HivemindTool(BaseTool):
    name = "hivemind"
    description = (
        "Dispatch a complex task to multiple AI models (Claude, Gemini, DeepSeek, ChatGPT) "
        "in parallel and synthesize their responses. Use this for tasks that benefit from "
        "multiple perspectives, deep research, or cross-validation of results."
    )

    def __init__(self, settings=None):
        self._settings = settings
        self._coordinator = None

    def _get_coordinator(self):
        """Lazy-load the AIJusticeLeague coordinator."""
        if self._coordinator is None:
            from multi_ai_framework.core.ai_coordinator import AIJusticeLeague
            from multi_ai_framework.config.config_manager import ConfigManager

            config_mgr = ConfigManager()
            config = config_mgr.get_framework_config()
            self._coordinator = AIJusticeLeague(config=config)
        return self._coordinator

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task or question to distribute across AI models.",
                    },
                    "models": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Which models to use. Options: 'claude', 'gemini', 'deepseek', 'chatgpt'. "
                            "Defaults to all available models."
                        ),
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["research", "analyze", "compare"],
                        "description": (
                            "'research': each model researches the topic independently. "
                            "'analyze': each model analyzes from its strengths. "
                            "'compare': each model provides its perspective for comparison."
                        ),
                    },
                },
                "required": ["task"],
            },
        }

    def execute(self, task: str, models: List[str] = None, mode: str = "research", **kwargs) -> str:
        try:
            coordinator = self._get_coordinator()
        except Exception as e:
            return f"Error initializing hivemind: {e}. Ensure API keys are configured."

        available_models = list(coordinator.models.keys())
        selected = models or available_models
        selected = [m for m in selected if m in available_models]

        if not selected:
            return f"Error: No valid models selected. Available: {available_models}"

        # Build task prompts based on mode
        tasks = {}
        for model_name in selected:
            prompt = self._build_prompt(task, model_name, mode)
            tasks[model_name] = {
                "prompt": prompt,
                "model": self._get_model_id(model_name),
            }

        # Distribute tasks in parallel
        try:
            results = coordinator.distributor.distribute_tasks(tasks, coordinator.models)
        except Exception as e:
            return f"Error running hivemind tasks: {e}"

        # Synthesize results
        return self._format_results(results, task)

    def _build_prompt(self, task: str, model_name: str, mode: str) -> str:
        if mode == "research":
            return f"Research the following topic thoroughly:\n\n{task}\n\nProvide detailed findings."
        elif mode == "analyze":
            strengths = {
                "claude": "strategic reasoning and narrative development",
                "gemini": "real-time research and data synthesis",
                "deepseek": "advanced modeling and quantitative analysis",
                "chatgpt": "communication optimization and procedural guidance",
            }
            strength = strengths.get(model_name, "general analysis")
            return (
                f"Analyze the following from the perspective of {strength}:\n\n{task}\n\n"
                f"Provide your expert analysis."
            )
        else:  # compare
            return (
                f"Provide your perspective on the following:\n\n{task}\n\n"
                f"Be specific and opinionated in your analysis."
            )

    def _get_model_id(self, model_name: str) -> str:
        model_ids = {
            "claude": "claude-sonnet-4-5-20250929",
            "gemini": "gemini-2.0-flash-exp",
            "deepseek": "deepseek-chat",
            "chatgpt": "gpt-4",
        }
        return model_ids.get(model_name, model_name)

    def _format_results(self, results: dict, task: str) -> str:
        parts = [f"Hivemind Results for: {task}\n{'='*60}"]

        for model_name, result in results.items():
            parts.append(f"\n--- {model_name.upper()} ---")
            if result.success:
                content = result.response.content
                if len(content) > 2000:
                    content = content[:2000] + "\n[Truncated...]"
                parts.append(content)
            else:
                parts.append(f"[Error: {result.error}]")

        successful = sum(1 for r in results.values() if r.success)
        parts.append(f"\n{'='*60}")
        parts.append(f"Models queried: {len(results)} | Successful: {successful}")

        return "\n".join(parts)
