"""
Scheduler Tool - Allows Claude to schedule deferred and recurring tasks.
"""

import time
from datetime import datetime
from typing import Any, Dict

from jarvis.scheduler.task_scheduler import TaskScheduler
from jarvis.tools.base_tool import BaseTool


class SchedulerTool(BaseTool):
    name = "scheduler"
    description = (
        "Schedule tasks for later execution. Supports one-time deferred tasks "
        "(e.g., 'remind me in 2 hours') and recurring tasks (e.g., 'check weather "
        "every morning'). Tasks persist across sessions."
    )

    def __init__(self, scheduler: TaskScheduler = None):
        self._scheduler = scheduler or TaskScheduler()

    @property
    def scheduler(self) -> TaskScheduler:
        return self._scheduler

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["schedule_once", "schedule_recurring", "list", "cancel"],
                        "description": (
                            "'schedule_once': one-time task at a future time. "
                            "'schedule_recurring': repeating task on an interval. "
                            "'list': show scheduled tasks. "
                            "'cancel': cancel a task by ID."
                        ),
                    },
                    "name": {
                        "type": "string",
                        "description": "Human-readable name for the task.",
                    },
                    "task_action": {
                        "type": "string",
                        "description": (
                            "The tool to invoke when the task runs (e.g., 'apple_reminders', "
                            "'web_search', 'memory'). Or 'notify' to just display a message."
                        ),
                    },
                    "task_arguments": {
                        "type": "object",
                        "description": "Arguments to pass to the tool when the task runs.",
                    },
                    "delay": {
                        "type": "string",
                        "description": (
                            "How long from now to run (for schedule_once). "
                            "Examples: '5m', '2h', '1d', '3 weeks'."
                        ),
                    },
                    "interval": {
                        "type": "string",
                        "description": (
                            "How often to repeat (for schedule_recurring). "
                            "Examples: '1h', '24h', '7d'."
                        ),
                    },
                    "max_runs": {
                        "type": "integer",
                        "description": "Maximum number of times to run (0 = unlimited). For recurring tasks.",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID (for cancel action).",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of what the task does.",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if action == "schedule_once":
            return self._schedule_once(kwargs)
        elif action == "schedule_recurring":
            return self._schedule_recurring(kwargs)
        elif action == "list":
            return self._list_tasks()
        elif action == "cancel":
            return self._cancel_task(kwargs.get("task_id", 0))
        else:
            return f"Unknown action: {action}"

    def _schedule_once(self, kwargs: dict) -> str:
        name = kwargs.get("name", "Unnamed task")
        task_action = kwargs.get("task_action", "notify")
        arguments = kwargs.get("task_arguments", {})
        delay_str = kwargs.get("delay", "")
        description = kwargs.get("description", "")

        if not delay_str:
            return "Error: 'delay' is required (e.g., '5m', '2h', '1d')."

        delay_secs = TaskScheduler.parse_delay(delay_str)
        if delay_secs <= 0:
            return f"Error: Could not parse delay '{delay_str}'. Try '5m', '2h', '1d', etc."

        task_id = self._scheduler.schedule_once(
            name=name,
            action=task_action,
            arguments=arguments,
            delay_seconds=delay_secs,
            description=description,
        )

        run_time = datetime.fromtimestamp(time.time() + delay_secs)
        return (
            f"Task #{task_id} '{name}' scheduled.\n"
            f"Will run at: {run_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"({delay_str} from now).\n"
            f"Action: {task_action}"
        )

    def _schedule_recurring(self, kwargs: dict) -> str:
        name = kwargs.get("name", "Unnamed recurring task")
        task_action = kwargs.get("task_action", "notify")
        arguments = kwargs.get("task_arguments", {})
        interval_str = kwargs.get("interval", "")
        max_runs = kwargs.get("max_runs", 0)
        description = kwargs.get("description", "")

        if not interval_str:
            return "Error: 'interval' is required (e.g., '1h', '24h', '7d')."

        interval_secs = TaskScheduler.parse_delay(interval_str)
        if interval_secs <= 0:
            return f"Error: Could not parse interval '{interval_str}'."

        task_id = self._scheduler.schedule_recurring(
            name=name,
            action=task_action,
            arguments=arguments,
            interval_seconds=interval_secs,
            max_runs=max_runs,
            description=description,
        )

        runs_text = f", max {max_runs} runs" if max_runs else ", unlimited runs"
        return (
            f"Recurring task #{task_id} '{name}' scheduled.\n"
            f"Runs every {interval_str}{runs_text}.\n"
            f"Action: {task_action}"
        )

    def _list_tasks(self) -> str:
        tasks = self._scheduler.list_tasks("pending")
        if not tasks:
            return "No scheduled tasks."

        lines = []
        for t in tasks:
            if t["type"] == "recurring":
                interval_h = t["interval"] / 3600
                max_str = f"/{t['max_runs']}" if t['max_runs'] else ""
                lines.append(
                    f"#{t['id']} [{t['type']}] {t['name']}\n"
                    f"   Every {interval_h:.1f}h | Runs: {t['run_count']}"
                    f"{max_str} | Next: {t['run_at_human']}"
                )
            else:
                lines.append(
                    f"#{t['id']} [{t['type']}] {t['name']}\n"
                    f"   Runs at: {t['run_at_human']} | Action: {t['action']}"
                )

        return f"Scheduled tasks ({len(tasks)}):\n\n" + "\n\n".join(lines)

    def _cancel_task(self, task_id: int) -> str:
        if not task_id:
            return "Error: 'task_id' is required."
        if self._scheduler.cancel_task(task_id):
            return f"Task #{task_id} cancelled."
        return f"Could not cancel task #{task_id} (not found or already completed)."
