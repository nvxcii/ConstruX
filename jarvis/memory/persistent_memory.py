"""
Persistent Memory - SQLite-backed long-term memory for Jarvis.

Stores facts, preferences, conversation summaries, and context
that persists across sessions permanently.
"""

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class PersistentMemory:
    """SQLite-backed memory that persists across Jarvis sessions.

    Memory types:
        - facts: Things Jarvis learns about the user ("User prefers dark mode")
        - preferences: Tool/behavior preferences ("User likes concise responses")
        - context: Conversation summaries and recurring topics
        - history: Tool usage history for auto-tuning
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._default_path()
        self._conn = None
        self._init_db()

    def _default_path(self) -> str:
        data_dir = Path.home() / ".jarvis" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir / "memory.db")

    def _init_db(self) -> None:
        """Initialize the database schema."""
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")

        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                UNIQUE(category, key)
            );

            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                arguments TEXT NOT NULL,
                result_summary TEXT,
                success INTEGER DEFAULT 1,
                timestamp REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT NOT NULL,
                topics TEXT DEFAULT '[]',
                timestamp REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
            CREATE INDEX IF NOT EXISTS idx_memories_key ON memories(category, key);
            CREATE INDEX IF NOT EXISTS idx_tool_usage_name ON tool_usage(tool_name);
            CREATE INDEX IF NOT EXISTS idx_tool_usage_time ON tool_usage(timestamp);
        """)
        self._conn.commit()

    # ── Core memory operations ──────────────────────────────────

    def remember(self, category: str, key: str, value: str,
                 metadata: Optional[Dict] = None) -> None:
        """Store or update a memory."""
        now = time.time()
        meta_json = json.dumps(metadata or {})
        self._conn.execute("""
            INSERT INTO memories (category, key, value, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(category, key) DO UPDATE SET
                value = excluded.value,
                metadata = excluded.metadata,
                updated_at = excluded.updated_at
        """, (category, key, value, meta_json, now, now))
        self._conn.commit()

    def recall(self, category: str, key: str) -> Optional[str]:
        """Recall a specific memory. Returns None if not found."""
        row = self._conn.execute("""
            SELECT value FROM memories WHERE category = ? AND key = ?
        """, (category, key)).fetchone()

        if row:
            self._conn.execute("""
                UPDATE memories SET access_count = access_count + 1
                WHERE category = ? AND key = ?
            """, (category, key))
            self._conn.commit()
            return row["value"]
        return None

    def recall_category(self, category: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Recall all memories in a category."""
        rows = self._conn.execute("""
            SELECT key, value, metadata, updated_at, access_count
            FROM memories WHERE category = ?
            ORDER BY updated_at DESC LIMIT ?
        """, (category, limit)).fetchall()

        return [
            {
                "key": r["key"],
                "value": r["value"],
                "metadata": json.loads(r["metadata"]),
                "updated_at": r["updated_at"],
                "access_count": r["access_count"],
            }
            for r in rows
        ]

    def search(self, query: str, category: Optional[str] = None,
               limit: int = 20) -> List[Dict[str, Any]]:
        """Search memories by keyword across keys and values."""
        pattern = f"%{query}%"
        if category:
            rows = self._conn.execute("""
                SELECT category, key, value, updated_at FROM memories
                WHERE category = ? AND (key LIKE ? OR value LIKE ?)
                ORDER BY updated_at DESC LIMIT ?
            """, (category, pattern, pattern, limit)).fetchall()
        else:
            rows = self._conn.execute("""
                SELECT category, key, value, updated_at FROM memories
                WHERE key LIKE ? OR value LIKE ?
                ORDER BY updated_at DESC LIMIT ?
            """, (pattern, pattern, limit)).fetchall()

        return [
            {"category": r["category"], "key": r["key"],
             "value": r["value"], "updated_at": r["updated_at"]}
            for r in rows
        ]

    def forget(self, category: str, key: str) -> bool:
        """Remove a specific memory."""
        cursor = self._conn.execute(
            "DELETE FROM memories WHERE category = ? AND key = ?",
            (category, key)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    # ── Tool usage tracking ─────────────────────────────────────

    def log_tool_usage(self, tool_name: str, arguments: Dict,
                       result_summary: str = "", success: bool = True) -> None:
        """Log a tool invocation for pattern learning."""
        self._conn.execute("""
            INSERT INTO tool_usage (tool_name, arguments, result_summary, success, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (tool_name, json.dumps(arguments), result_summary, int(success), time.time()))
        self._conn.commit()

    def get_tool_usage_stats(self, tool_name: Optional[str] = None,
                              days: int = 30) -> List[Dict[str, Any]]:
        """Get tool usage statistics for auto-tuning."""
        cutoff = time.time() - (days * 86400)

        if tool_name:
            rows = self._conn.execute("""
                SELECT tool_name, arguments, success, timestamp
                FROM tool_usage WHERE tool_name = ? AND timestamp > ?
                ORDER BY timestamp DESC
            """, (tool_name, cutoff)).fetchall()
        else:
            rows = self._conn.execute("""
                SELECT tool_name, COUNT(*) as count,
                       SUM(success) as successes,
                       MAX(timestamp) as last_used
                FROM tool_usage WHERE timestamp > ?
                GROUP BY tool_name ORDER BY count DESC
            """, (cutoff,)).fetchall()

        return [dict(r) for r in rows]

    def get_frequent_arguments(self, tool_name: str, limit: int = 5) -> List[Dict]:
        """Get most frequently used arguments for a tool."""
        rows = self._conn.execute("""
            SELECT arguments, COUNT(*) as count
            FROM tool_usage WHERE tool_name = ? AND success = 1
            GROUP BY arguments ORDER BY count DESC LIMIT ?
        """, (tool_name, limit)).fetchall()

        return [{"arguments": json.loads(r["arguments"]), "count": r["count"]} for r in rows]

    # ── Conversation summaries ──────────────────────────────────

    def save_conversation_summary(self, summary: str, topics: List[str]) -> None:
        """Save a conversation summary for long-term context."""
        self._conn.execute("""
            INSERT INTO conversation_summaries (summary, topics, timestamp)
            VALUES (?, ?, ?)
        """, (summary, json.dumps(topics), time.time()))
        self._conn.commit()

    def get_recent_summaries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation summaries."""
        rows = self._conn.execute("""
            SELECT summary, topics, timestamp
            FROM conversation_summaries ORDER BY timestamp DESC LIMIT ?
        """, (limit,)).fetchall()

        return [
            {"summary": r["summary"], "topics": json.loads(r["topics"]),
             "timestamp": r["timestamp"]}
            for r in rows
        ]

    # ── Context injection ───────────────────────────────────────

    def get_context_for_prompt(self) -> str:
        """Generate a context string to inject into the system prompt.

        Pulls key facts, preferences, and recent context so Claude
        has persistent awareness across sessions.
        """
        parts = []

        # User facts
        facts = self.recall_category("fact", limit=20)
        if facts:
            fact_lines = [f"- {f['key']}: {f['value']}" for f in facts]
            parts.append("Known facts about the user:\n" + "\n".join(fact_lines))

        # User preferences
        prefs = self.recall_category("preference", limit=15)
        if prefs:
            pref_lines = [f"- {p['key']}: {p['value']}" for p in prefs]
            parts.append("User preferences:\n" + "\n".join(pref_lines))

        # Recent conversation context
        summaries = self.get_recent_summaries(limit=3)
        if summaries:
            summary_lines = [s["summary"] for s in summaries]
            parts.append("Recent conversation context:\n" + "\n".join(summary_lines))

        if not parts:
            return ""
        return "\n\n".join(parts)

    # ── Lifecycle ───────────────────────────────────────────────

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def __del__(self):
        self.close()
