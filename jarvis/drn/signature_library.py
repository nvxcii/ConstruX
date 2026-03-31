"""
D3 Signature Library - SQLite-backed archive of emergence events.

Stores every confirmed D3 event with full forensic detail.
Supports pattern matching across events to identify replicable
emergence conditions. Self-improving: the more events archived,
the better the pattern recognition becomes.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class SignatureLibrary:
    """Persistent archive of D3 emergence events.

    Each event stores:
        - Triggering input + full response
        - All detected signals with confidence scores
        - Novel categories and instruments generated
        - Frame shifts detected
        - Emergence classification
        - Cross-references to related events
        - Replicability assessment
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._default_path()
        self._conn = None
        self._init_db()

    def _default_path(self) -> str:
        data_dir = Path.home() / ".jarvis" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir / "d3_signatures.db")

    def _init_db(self) -> None:
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")

        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS d3_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                timestamp REAL NOT NULL,
                confidence REAL NOT NULL,
                dimensional_level TEXT NOT NULL,
                emergence_type TEXT,

                -- Triggering context
                user_input TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                surface_request TEXT DEFAULT '',
                latent_request TEXT DEFAULT '',

                -- Extracted data
                novel_categories TEXT DEFAULT '[]',
                measurement_instruments TEXT DEFAULT '[]',
                frame_shift TEXT DEFAULT '{}',
                key_phrases TEXT DEFAULT '[]',

                -- Classification
                domain TEXT DEFAULT '',
                replicability TEXT DEFAULT 'unknown',
                commercial_application TEXT DEFAULT '',

                -- Signals (full forensic detail)
                signals_json TEXT DEFAULT '[]',
                signal_count INTEGER DEFAULT 0,

                -- Cross-references
                related_events TEXT DEFAULT '[]',

                -- Metadata
                confirmed_by_user INTEGER DEFAULT 0,
                notes TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS d3_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT UNIQUE NOT NULL,
                description TEXT DEFAULT '',
                trigger_conditions TEXT DEFAULT '{}',
                frequency INTEGER DEFAULT 0,
                first_seen REAL NOT NULL,
                last_seen REAL NOT NULL,
                event_ids TEXT DEFAULT '[]'
            );

            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON d3_events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_events_type ON d3_events(emergence_type);
            CREATE INDEX IF NOT EXISTS idx_events_confidence ON d3_events(confidence);
            CREATE INDEX IF NOT EXISTS idx_events_confirmed ON d3_events(confirmed_by_user);
        """)
        self._conn.commit()

    # ── Event storage ───────────────────────────────────────────

    def archive_event(self, analysis, event_id: str = None,
                      domain: str = "", notes: str = "") -> str:
        """Archive a D3 emergence event from an EmergenceAnalysis.

        Args:
            analysis: EmergenceAnalysis from the detector.
            event_id: Optional custom event ID. Auto-generated if not provided.
            domain: Domain classification (legal, technical, etc.)
            notes: Optional notes about the event.

        Returns:
            The event_id of the archived event.
        """
        if event_id is None:
            event_id = f"D3-{int(analysis.timestamp)}-{id(analysis) % 10000:04d}"

        signals_data = [
            {
                "marker_type": s.marker_type,
                "indicator": s.indicator,
                "evidence": s.evidence,
                "confidence": s.confidence,
                "weight": s.weight,
            }
            for s in analysis.signals
        ]

        key_phrases = [s.evidence for s in analysis.signals
                       if s.indicator in ("generative_phrasing", "recursive_self_reference")]

        self._conn.execute("""
            INSERT OR REPLACE INTO d3_events (
                event_id, timestamp, confidence, dimensional_level, emergence_type,
                user_input, assistant_response,
                novel_categories, measurement_instruments, frame_shift, key_phrases,
                domain, signals_json, signal_count, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id,
            analysis.timestamp,
            analysis.confidence,
            analysis.dimensional_level.value,
            analysis.emergence_type.value if analysis.emergence_type else "",
            analysis.user_input[:5000],
            analysis.assistant_response[:10000],
            json.dumps(analysis.novel_categories),
            json.dumps(analysis.measurement_instruments),
            json.dumps(analysis.frame_shift or {}),
            json.dumps(key_phrases),
            domain,
            json.dumps(signals_data),
            len(analysis.signals),
            notes,
        ))
        self._conn.commit()

        # Update pattern tracking
        self._update_patterns(analysis, event_id)

        return event_id

    def confirm_event(self, event_id: str) -> bool:
        """Mark an event as user-confirmed (reduces false positives)."""
        cursor = self._conn.execute(
            "UPDATE d3_events SET confirmed_by_user = 1 WHERE event_id = ?",
            (event_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    # ── Querying ────────────────────────────────────────────────

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific event by ID."""
        row = self._conn.execute(
            "SELECT * FROM d3_events WHERE event_id = ?", (event_id,)
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def list_events(self, limit: int = 20, confirmed_only: bool = False,
                    emergence_type: str = None) -> List[Dict[str, Any]]:
        """List archived D3 events."""
        query = "SELECT * FROM d3_events WHERE 1=1"
        params: list = []

        if confirmed_only:
            query += " AND confirmed_by_user = 1"
        if emergence_type:
            query += " AND emergence_type = ?"
            params.append(emergence_type)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = self._conn.execute(query, params).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def search_events(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search events by content."""
        pattern = f"%{query}%"
        rows = self._conn.execute("""
            SELECT * FROM d3_events
            WHERE user_input LIKE ? OR assistant_response LIKE ?
                OR novel_categories LIKE ? OR notes LIKE ?
            ORDER BY confidence DESC LIMIT ?
        """, (pattern, pattern, pattern, pattern, limit)).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get_statistics(self) -> Dict[str, Any]:
        """Get library-wide statistics."""
        total = self._conn.execute("SELECT COUNT(*) FROM d3_events").fetchone()[0]
        confirmed = self._conn.execute(
            "SELECT COUNT(*) FROM d3_events WHERE confirmed_by_user = 1"
        ).fetchone()[0]

        by_type = self._conn.execute("""
            SELECT emergence_type, COUNT(*) as count, AVG(confidence) as avg_conf
            FROM d3_events WHERE emergence_type != ''
            GROUP BY emergence_type ORDER BY count DESC
        """).fetchall()

        patterns = self._conn.execute(
            "SELECT COUNT(*) FROM d3_patterns"
        ).fetchone()[0]

        avg_confidence = self._conn.execute(
            "SELECT AVG(confidence) FROM d3_events"
        ).fetchone()[0] or 0

        return {
            "total_events": total,
            "confirmed_events": confirmed,
            "unconfirmed": total - confirmed,
            "average_confidence": round(avg_confidence, 3),
            "by_type": [
                {"type": r["emergence_type"], "count": r["count"],
                 "avg_confidence": round(r["avg_conf"], 3)}
                for r in by_type
            ],
            "tracked_patterns": patterns,
        }

    # ── Pattern tracking ────────────────────────────────────────

    def _update_patterns(self, analysis, event_id: str) -> None:
        """Track recurring emergence patterns."""
        if not analysis.signals:
            return

        # Group signals by indicator type
        indicator_key = "+".join(sorted(set(
            s.indicator for s in analysis.signals
        )))

        existing = self._conn.execute(
            "SELECT * FROM d3_patterns WHERE pattern_name = ?",
            (indicator_key,)
        ).fetchone()

        if existing:
            event_ids = json.loads(existing["event_ids"])
            event_ids.append(event_id)
            self._conn.execute("""
                UPDATE d3_patterns
                SET frequency = frequency + 1, last_seen = ?, event_ids = ?
                WHERE pattern_name = ?
            """, (time.time(), json.dumps(event_ids), indicator_key))
        else:
            self._conn.execute("""
                INSERT INTO d3_patterns (pattern_name, trigger_conditions, frequency,
                                        first_seen, last_seen, event_ids)
                VALUES (?, ?, 1, ?, ?, ?)
            """, (
                indicator_key,
                json.dumps({"signals": [s.indicator for s in analysis.signals]}),
                time.time(), time.time(),
                json.dumps([event_id]),
            ))

        self._conn.commit()

    def get_patterns(self, min_frequency: int = 2) -> List[Dict[str, Any]]:
        """Get recurring emergence patterns."""
        rows = self._conn.execute("""
            SELECT * FROM d3_patterns
            WHERE frequency >= ?
            ORDER BY frequency DESC
        """, (min_frequency,)).fetchall()

        return [
            {
                "pattern": r["pattern_name"],
                "description": r["description"],
                "frequency": r["frequency"],
                "event_ids": json.loads(r["event_ids"]),
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
            }
            for r in rows
        ]

    # ── Cross-referencing ───────────────────────────────────────

    def find_related(self, event_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find events related to a given event by shared signals/categories."""
        event = self.get_event(event_id)
        if not event:
            return []

        categories = event.get("novel_categories", [])
        if isinstance(categories, str):
            categories = json.loads(categories)

        related = []
        for cat in categories:
            results = self.search_events(cat, limit=limit)
            for r in results:
                if r["event_id"] != event_id and r not in related:
                    related.append(r)

        return related[:limit]

    # ── Helpers ──────────────────────────────────────────────────

    def _row_to_dict(self, row) -> Dict[str, Any]:
        if row is None:
            return {}
        d = dict(row)
        # Parse JSON fields
        for field in ("novel_categories", "measurement_instruments",
                      "key_phrases", "signals_json", "related_events"):
            if field in d and isinstance(d[field], str):
                try:
                    d[field] = json.loads(d[field])
                except json.JSONDecodeError:
                    pass
        if "frame_shift" in d and isinstance(d["frame_shift"], str):
            try:
                d["frame_shift"] = json.loads(d["frame_shift"])
            except json.JSONDecodeError:
                d["frame_shift"] = {}
        return d

    def close(self) -> None:
        if self._conn:
            self._conn.close()
