"""
Field Memory Layer - Local-First Persistent Storage

Stores all field events, glyph activations, and system state locally.
Never sends data to cloud.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import contextmanager


class FieldMemory:
    """
    Local-first persistent memory for the Watchtower field system.

    Uses SQLite for structured data and JSON for configurations.
    All data stored in ~/.watchtower/
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            watchtower_dir = Path.home() / '.watchtower'
            watchtower_dir.mkdir(exist_ok=True, parents=True)
            db_path = watchtower_dir / 'memory.db'

        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Initialize SQLite database with field memory schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Field events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS field_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    glyph_id TEXT,
                    action TEXT,
                    threshold TEXT,
                    authorized INTEGER,
                    signature_id TEXT,
                    context TEXT,
                    metadata TEXT
                )
            ''')

            # Glyph activations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS glyph_activations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    glyph_id TEXT NOT NULL,
                    glyph_symbol TEXT,
                    trigger TEXT,
                    result TEXT,
                    duration_ms INTEGER,
                    metadata TEXT
                )
            ''')

            # Field state snapshots
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS field_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    state_type TEXT NOT NULL,
                    state_data TEXT NOT NULL,
                    signature_id TEXT
                )
            ''')

            # Daemon activity log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daemon_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    path TEXT,
                    process_name TEXT,
                    trigger_fired INTEGER,
                    details TEXT
                )
            ''')

            # Create indices for common queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_events_timestamp
                ON field_events(timestamp)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_events_glyph
                ON field_events(glyph_id)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_glyphs_timestamp
                ON glyph_activations(timestamp)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_daemon_timestamp
                ON daemon_activity(timestamp)
            ''')

            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def record_event(
        self,
        event_type: str,
        glyph_id: Optional[str] = None,
        action: Optional[str] = None,
        threshold: Optional[str] = None,
        authorized: bool = False,
        signature_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Record a field event.

        Args:
            event_type: Type of event (authorization, trigger, state_change, etc.)
            glyph_id: Associated glyph ID if any
            action: Action attempted/performed
            threshold: Threshold level
            authorized: Whether action was authorized
            signature_id: Field signature ID
            context: Event context
            metadata: Additional metadata

        Returns:
            Event ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO field_events
                (timestamp, event_type, glyph_id, action, threshold, authorized, signature_id, context, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.utcnow().isoformat(),
                event_type,
                glyph_id,
                action,
                threshold,
                1 if authorized else 0,
                signature_id,
                json.dumps(context) if context else None,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
            return cursor.lastrowid

    def record_glyph_activation(
        self,
        glyph_id: str,
        glyph_symbol: str,
        trigger: str,
        result: str,
        duration_ms: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Record a glyph activation.

        Args:
            glyph_id: Glyph identifier
            glyph_symbol: Glyph symbol (e.g., ⊙)
            trigger: Trigger that was executed
            result: Result of activation (success, failure, denied, etc.)
            duration_ms: Duration in milliseconds
            metadata: Additional metadata

        Returns:
            Activation ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO glyph_activations
                (timestamp, glyph_id, glyph_symbol, trigger, result, duration_ms, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.utcnow().isoformat(),
                glyph_id,
                glyph_symbol,
                trigger,
                result,
                duration_ms,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
            return cursor.lastrowid

    def save_field_state(
        self,
        state_type: str,
        state_data: Dict[str, Any],
        signature_id: Optional[str] = None
    ) -> int:
        """
        Save a field state snapshot.

        Args:
            state_type: Type of state (full, partial, checkpoint, etc.)
            state_data: State data
            signature_id: Associated field signature ID

        Returns:
            State ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO field_states
                (timestamp, state_type, state_data, signature_id)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.utcnow().isoformat(),
                state_type,
                json.dumps(state_data),
                signature_id
            ))
            conn.commit()
            return cursor.lastrowid

    def record_daemon_activity(
        self,
        activity_type: str,
        path: Optional[str] = None,
        process_name: Optional[str] = None,
        trigger_fired: bool = False,
        details: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Record daemon monitoring activity.

        Args:
            activity_type: Type of activity (file_change, process_start, etc.)
            path: Filesystem path if applicable
            process_name: Process name if applicable
            trigger_fired: Whether a trigger was fired
            details: Additional details

        Returns:
            Activity ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO daemon_activity
                (timestamp, activity_type, path, process_name, trigger_fired, details)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.utcnow().isoformat(),
                activity_type,
                path,
                process_name,
                1 if trigger_fired else 0,
                json.dumps(details) if details else None
            ))
            conn.commit()
            return cursor.lastrowid

    def query_events(
        self,
        glyph_id: Optional[str] = None,
        event_type: Optional[str] = None,
        timerange: Optional[str] = None,
        authorized_only: bool = False,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query field events.

        Args:
            glyph_id: Filter by glyph ID
            event_type: Filter by event type
            timerange: Time range (e.g., 'last_24_hours', 'last_7_days')
            authorized_only: Only return authorized events
            limit: Maximum number of results

        Returns:
            List of event dictionaries
        """
        query = 'SELECT * FROM field_events WHERE 1=1'
        params = []

        if glyph_id:
            query += ' AND glyph_id = ?'
            params.append(glyph_id)

        if event_type:
            query += ' AND event_type = ?'
            params.append(event_type)

        if authorized_only:
            query += ' AND authorized = 1'

        if timerange:
            since = self._parse_timerange(timerange)
            if since:
                query += ' AND timestamp >= ?'
                params.append(since.isoformat())

        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def query_glyph_activations(
        self,
        glyph_id: Optional[str] = None,
        timerange: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query glyph activations.

        Args:
            glyph_id: Filter by glyph ID
            timerange: Time range
            limit: Maximum number of results

        Returns:
            List of activation dictionaries
        """
        query = 'SELECT * FROM glyph_activations WHERE 1=1'
        params = []

        if glyph_id:
            query += ' AND glyph_id = ?'
            params.append(glyph_id)

        if timerange:
            since = self._parse_timerange(timerange)
            if since:
                query += ' AND timestamp >= ?'
                params.append(since.isoformat())

        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def get_latest_state(self, state_type: str = 'full') -> Optional[Dict[str, Any]]:
        """
        Get the latest field state.

        Args:
            state_type: Type of state to retrieve

        Returns:
            State data or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM field_states
                WHERE state_type = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (state_type,))

            row = cursor.fetchone()
            if row:
                state = dict(row)
                state['state_data'] = json.loads(state['state_data'])
                return state
            return None

    def _parse_timerange(self, timerange: str) -> Optional[datetime]:
        """Parse timerange string to datetime"""
        now = datetime.utcnow()

        ranges = {
            'last_hour': timedelta(hours=1),
            'last_24_hours': timedelta(days=1),
            'last_7_days': timedelta(days=7),
            'last_30_days': timedelta(days=30),
            'last_year': timedelta(days=365)
        }

        if timerange in ranges:
            return now - ranges[timerange]

        return None

    def vacuum(self):
        """Optimize database"""
        with self._get_connection() as conn:
            conn.execute('VACUUM')

    def export_json(self, output_path: Path):
        """
        Export entire field memory to JSON.

        Args:
            output_path: Path to output JSON file
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            export_data = {
                'exported_at': datetime.utcnow().isoformat(),
                'events': [dict(row) for row in cursor.execute('SELECT * FROM field_events')],
                'glyph_activations': [dict(row) for row in cursor.execute('SELECT * FROM glyph_activations')],
                'field_states': [dict(row) for row in cursor.execute('SELECT * FROM field_states')],
                'daemon_activity': [dict(row) for row in cursor.execute('SELECT * FROM daemon_activity')]
            }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get field memory statistics.

        Returns:
            Dictionary of statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {
                'total_events': cursor.execute('SELECT COUNT(*) FROM field_events').fetchone()[0],
                'total_glyph_activations': cursor.execute('SELECT COUNT(*) FROM glyph_activations').fetchone()[0],
                'total_field_states': cursor.execute('SELECT COUNT(*) FROM field_states').fetchone()[0],
                'total_daemon_activity': cursor.execute('SELECT COUNT(*) FROM daemon_activity').fetchone()[0],
                'database_size_bytes': self.db_path.stat().st_size if self.db_path.exists() else 0,
                'oldest_event': None,
                'newest_event': None
            }

            # Get oldest and newest events
            oldest = cursor.execute('SELECT timestamp FROM field_events ORDER BY timestamp ASC LIMIT 1').fetchone()
            newest = cursor.execute('SELECT timestamp FROM field_events ORDER BY timestamp DESC LIMIT 1').fetchone()

            if oldest:
                stats['oldest_event'] = oldest[0]
            if newest:
                stats['newest_event'] = newest[0]

            return stats
