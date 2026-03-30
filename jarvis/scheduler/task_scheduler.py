"""
Task Scheduler - Schedule deferred and recurring tasks for Jarvis.

Supports:
    - One-time deferred tasks ("remind me in 2 hours")
    - Recurring tasks ("check my email every morning")
    - Persistent across sessions (stored in SQLite)
    - Background execution via threading
"""

import json
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class TaskScheduler:
    """Persistent task scheduler with support for deferred and recurring tasks."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._default_path()
        self._conn = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._task_handler: Optional[Callable] = None
        self._init_db()

    def _default_path(self) -> str:
        data_dir = Path.home() / ".jarvis" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir / "scheduler.db")

    def _init_db(self) -> None:
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                task_type TEXT NOT NULL,
                action TEXT NOT NULL,
                arguments TEXT DEFAULT '{}',
                run_at REAL NOT NULL,
                recurrence_seconds REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at REAL NOT NULL,
                last_run_at REAL DEFAULT 0,
                run_count INTEGER DEFAULT 0,
                max_runs INTEGER DEFAULT 0,
                result TEXT DEFAULT ''
            );

            CREATE INDEX IF NOT EXISTS idx_tasks_status ON scheduled_tasks(status);
            CREATE INDEX IF NOT EXISTS idx_tasks_run_at ON scheduled_tasks(run_at);
        """)
        self._conn.commit()

    # ── Task creation ───────────────────────────────────────────

    def schedule_once(self, name: str, action: str, arguments: Dict = None,
                      delay_seconds: float = 0, run_at: float = 0,
                      description: str = "") -> int:
        """Schedule a one-time task.

        Args:
            name: Human-readable task name.
            action: The action to perform (tool name or command).
            arguments: Arguments for the action.
            delay_seconds: Seconds from now to run (alternative to run_at).
            run_at: Unix timestamp to run at (overrides delay_seconds).
            description: Optional description.

        Returns:
            Task ID.
        """
        if not run_at:
            run_at = time.time() + delay_seconds

        cursor = self._conn.execute("""
            INSERT INTO scheduled_tasks
            (name, description, task_type, action, arguments, run_at, created_at)
            VALUES (?, ?, 'once', ?, ?, ?, ?)
        """, (name, description, action, json.dumps(arguments or {}), run_at, time.time()))
        self._conn.commit()
        return cursor.lastrowid

    def schedule_recurring(self, name: str, action: str, arguments: Dict = None,
                           interval_seconds: float = 3600, max_runs: int = 0,
                           description: str = "") -> int:
        """Schedule a recurring task.

        Args:
            name: Human-readable task name.
            action: The action to perform.
            arguments: Arguments for the action.
            interval_seconds: Seconds between runs.
            max_runs: Maximum number of runs (0 = unlimited).
            description: Optional description.

        Returns:
            Task ID.
        """
        run_at = time.time() + interval_seconds

        cursor = self._conn.execute("""
            INSERT INTO scheduled_tasks
            (name, description, task_type, action, arguments, run_at,
             recurrence_seconds, max_runs, created_at)
            VALUES (?, ?, 'recurring', ?, ?, ?, ?, ?, ?)
        """, (name, description, action, json.dumps(arguments or {}),
              run_at, interval_seconds, max_runs, time.time()))
        self._conn.commit()
        return cursor.lastrowid

    # ── Task management ─────────────────────────────────────────

    def cancel_task(self, task_id: int) -> bool:
        """Cancel a scheduled task."""
        cursor = self._conn.execute(
            "UPDATE scheduled_tasks SET status = 'cancelled' WHERE id = ? AND status = 'pending'",
            (task_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def list_tasks(self, status: str = "pending") -> List[Dict[str, Any]]:
        """List tasks by status."""
        rows = self._conn.execute("""
            SELECT id, name, description, task_type, action, arguments,
                   run_at, recurrence_seconds, status, run_count, max_runs
            FROM scheduled_tasks WHERE status = ?
            ORDER BY run_at ASC
        """, (status,)).fetchall()

        return [
            {
                "id": r["id"],
                "name": r["name"],
                "description": r["description"],
                "type": r["task_type"],
                "action": r["action"],
                "arguments": json.loads(r["arguments"]),
                "run_at": r["run_at"],
                "run_at_human": datetime.fromtimestamp(r["run_at"]).strftime("%Y-%m-%d %H:%M:%S"),
                "interval": r["recurrence_seconds"],
                "status": r["status"],
                "run_count": r["run_count"],
                "max_runs": r["max_runs"],
            }
            for r in rows
        ]

    def get_due_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks that are due to run now."""
        now = time.time()
        rows = self._conn.execute("""
            SELECT id, name, action, arguments, task_type, recurrence_seconds, max_runs, run_count
            FROM scheduled_tasks WHERE status = 'pending' AND run_at <= ?
            ORDER BY run_at ASC
        """, (now,)).fetchall()

        return [dict(r) for r in rows]

    def mark_completed(self, task_id: int, result: str = "") -> None:
        """Mark a task run as completed."""
        row = self._conn.execute(
            "SELECT task_type, recurrence_seconds, max_runs, run_count FROM scheduled_tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if not row:
            return

        new_count = row["run_count"] + 1

        if row["task_type"] == "recurring":
            # Check if max_runs reached
            if row["max_runs"] > 0 and new_count >= row["max_runs"]:
                new_status = "completed"
                next_run = 0
            else:
                new_status = "pending"
                next_run = time.time() + row["recurrence_seconds"]

            self._conn.execute("""
                UPDATE scheduled_tasks
                SET run_count = ?, last_run_at = ?, result = ?, status = ?, run_at = ?
                WHERE id = ?
            """, (new_count, time.time(), result, new_status,
                  next_run if new_status == "pending" else 0, task_id))
        else:
            self._conn.execute("""
                UPDATE scheduled_tasks
                SET run_count = ?, last_run_at = ?, result = ?, status = 'completed'
                WHERE id = ?
            """, (new_count, time.time(), result, task_id))

        self._conn.commit()

    # ── Background runner ───────────────────────────────────────

    def start(self, task_handler: Callable) -> None:
        """Start the background scheduler.

        Args:
            task_handler: Function called with (action, arguments) for each due task.
                          Should return a result string.
        """
        if self._running:
            return
        self._task_handler = task_handler
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the background scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None

    def _run_loop(self) -> None:
        """Main scheduler loop - checks for due tasks every 30 seconds."""
        while self._running:
            try:
                due = self.get_due_tasks()
                for task in due:
                    try:
                        args = json.loads(task["arguments"]) if isinstance(task["arguments"], str) else task["arguments"]
                        result = self._task_handler(task["action"], args)
                        self.mark_completed(task["id"], str(result)[:500])
                    except Exception as e:
                        self.mark_completed(task["id"], f"Error: {e}")
            except Exception:
                pass
            time.sleep(30)

    # ── Helpers ──────────────────────────────────────────────────

    @staticmethod
    def parse_delay(text: str) -> float:
        """Parse human-readable delay into seconds.

        Examples: '5m', '2h', '1d', '30s', '3 weeks', '2 hours 30 minutes'
        """
        import re

        text = text.lower().strip()

        units = {
            "s": 1, "sec": 1, "second": 1, "seconds": 1,
            "m": 60, "min": 60, "minute": 60, "minutes": 60,
            "h": 3600, "hr": 3600, "hour": 3600, "hours": 3600,
            "d": 86400, "day": 86400, "days": 86400,
            "w": 604800, "week": 604800, "weeks": 604800,
        }

        total = 0.0
        for match in re.finditer(r"(\d+\.?\d*)\s*([a-z]+)", text):
            num = float(match.group(1))
            unit = match.group(2)
            if unit in units:
                total += num * units[unit]

        return total

    def close(self) -> None:
        self.stop()
        if self._conn:
            self._conn.close()
