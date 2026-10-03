"""
Rights Ledger - Immutable Audit Trail

The Rights Ledger provides an immutable record of all constitutional
evaluations, violations, and DPAP transformations. It ensures:
    - Complete audit trail of system operations
    - Cryptographic integrity verification
    - Historical pattern analysis
    - Accountability and transparency

Constitutional Basis: Invariant I4 (Ledger Immutability)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import json
import sqlite3
import os


class EntryType(Enum):
    """Types of ledger entries"""
    EVALUATION = "evaluation"           # Constitutional evaluation
    VIOLATION = "violation"             # Detected violation
    DPAP_TRANSFORMATION = "dpap"        # DPAP transformation
    REMEDIATION = "remediation"         # Remediation action
    PRECOMMITMENT = "precommitment"     # C-I-L precommitment
    DECISION = "decision"               # Recorded decision
    SYSTEM_EVENT = "system_event"       # System-level event


@dataclass
class LedgerEntry:
    """A single entry in the Rights Ledger"""
    id: str
    entry_type: EntryType
    timestamp: datetime
    data: Dict[str, Any]
    previous_hash: str
    entry_hash: str
    signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "entry_type": self.entry_type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
            "signature": self.signature
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'LedgerEntry':
        return cls(
            id=d["id"],
            entry_type=EntryType(d["entry_type"]),
            timestamp=datetime.fromisoformat(d["timestamp"]),
            data=d["data"],
            previous_hash=d["previous_hash"],
            entry_hash=d["entry_hash"],
            signature=d.get("signature")
        )


class RightsLedger:
    """
    Rights Ledger - Immutable Constitutional Audit Trail

    Provides blockchain-inspired immutable record keeping for all
    constitutional operations. Each entry is linked to the previous
    entry through cryptographic hashing.
    """

    def __init__(self, db_path: str = "rights_ledger.db"):
        self.db_path = db_path
        self._entries: List[LedgerEntry] = []
        self._genesis_hash = "0" * 64  # Genesis block hash
        self._init_database()
        self._load_entries()

    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ledger_entries (
                id TEXT PRIMARY KEY,
                entry_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL,
                signature TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_entry_type ON ledger_entries(entry_type)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON ledger_entries(timestamp)
        ''')

        conn.commit()
        conn.close()

    def _load_entries(self):
        """Load entries from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, entry_type, timestamp, data, previous_hash, entry_hash, signature
            FROM ledger_entries
            ORDER BY created_at ASC
        ''')

        for row in cursor.fetchall():
            entry = LedgerEntry(
                id=row[0],
                entry_type=EntryType(row[1]),
                timestamp=datetime.fromisoformat(row[2]),
                data=json.loads(row[3]),
                previous_hash=row[4],
                entry_hash=row[5],
                signature=row[6]
            )
            self._entries.append(entry)

        conn.close()

    def _get_previous_hash(self) -> str:
        """Get hash of the previous entry"""
        if not self._entries:
            return self._genesis_hash
        return self._entries[-1].entry_hash

    def _compute_hash(self, entry_data: Dict[str, Any], previous_hash: str) -> str:
        """Compute cryptographic hash for an entry"""
        content = json.dumps({
            "data": entry_data,
            "previous_hash": previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def add_entry(
        self,
        entry_type: str,
        data: Dict[str, Any],
        signature: Optional[str] = None
    ) -> LedgerEntry:
        """
        Add a new entry to the ledger.

        Args:
            entry_type: Type of entry
            data: Entry data
            signature: Optional cryptographic signature

        Returns:
            The created ledger entry
        """
        try:
            etype = EntryType(entry_type.lower())
        except ValueError:
            etype = EntryType.SYSTEM_EVENT

        timestamp = datetime.utcnow()
        previous_hash = self._get_previous_hash()

        # Add timestamp to data for hash computation
        data_with_timestamp = {
            **data,
            "_timestamp": timestamp.isoformat()
        }

        entry_hash = self._compute_hash(data_with_timestamp, previous_hash)

        entry_id = hashlib.sha256(
            f"{timestamp.isoformat()}:{entry_hash[:16]}".encode()
        ).hexdigest()[:16]

        entry = LedgerEntry(
            id=entry_id,
            entry_type=etype,
            timestamp=timestamp,
            data=data,
            previous_hash=previous_hash,
            entry_hash=entry_hash,
            signature=signature
        )

        # Save to database
        self._save_entry(entry)

        # Add to memory
        self._entries.append(entry)

        return entry

    def _save_entry(self, entry: LedgerEntry):
        """Save entry to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO ledger_entries
            (id, entry_type, timestamp, data, previous_hash, entry_hash, signature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.id,
            entry.entry_type.value,
            entry.timestamp.isoformat(),
            json.dumps(entry.data),
            entry.previous_hash,
            entry.entry_hash,
            entry.signature
        ))

        conn.commit()
        conn.close()

    def record_evaluation(
        self,
        action: Dict[str, Any],
        result: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> LedgerEntry:
        """Record a constitutional evaluation"""
        return self.add_entry(
            entry_type="evaluation",
            data={
                "action": action,
                "result": result,
                "context": context or {},
                "compliant": result.get("compliant", False),
                "score": result.get("aggregate_score", 0)
            }
        )

    def record_violation(
        self,
        violation_type: str,
        severity: float,
        details: Dict[str, Any],
        source_system: str
    ) -> LedgerEntry:
        """Record a detected violation"""
        return self.add_entry(
            entry_type="violation",
            data={
                "violation_type": violation_type,
                "severity": severity,
                "details": details,
                "source_system": source_system
            }
        )

    def record_dpap_transformation(
        self,
        violation_id: str,
        input_constraint: Dict[str, Any],
        output_capability: Dict[str, Any],
        transformation_path: List[str]
    ) -> LedgerEntry:
        """Record a DPAP transformation"""
        return self.add_entry(
            entry_type="dpap",
            data={
                "violation_id": violation_id,
                "input_constraint": input_constraint,
                "output_capability": output_capability,
                "transformation_path": transformation_path
            }
        )

    def record_decision(
        self,
        decision_id: str,
        cil_scores: Tuple[float, float, float],
        domain: str,
        description: str
    ) -> LedgerEntry:
        """Record a C-I-L decision"""
        return self.add_entry(
            entry_type="decision",
            data={
                "decision_id": decision_id,
                "cil_scores": {
                    "conscience": cil_scores[0],
                    "intuition": cil_scores[1],
                    "logic": cil_scores[2]
                },
                "domain": domain,
                "description": description
            }
        )

    def verify_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the entire ledger.
        Checks that each entry's hash correctly chains to the previous.
        """
        if not self._entries:
            return {
                "valid": True,
                "entries_checked": 0,
                "message": "Empty ledger - nothing to verify"
            }

        issues = []
        previous_hash = self._genesis_hash

        for i, entry in enumerate(self._entries):
            # Check chain linkage
            if entry.previous_hash != previous_hash:
                issues.append({
                    "entry_index": i,
                    "entry_id": entry.id,
                    "issue": "chain_break",
                    "expected_previous": previous_hash,
                    "actual_previous": entry.previous_hash
                })

            # Recompute hash to verify
            data_with_timestamp = {
                **entry.data,
                "_timestamp": entry.timestamp.isoformat()
            }
            computed_hash = self._compute_hash(data_with_timestamp, entry.previous_hash)

            if computed_hash != entry.entry_hash:
                issues.append({
                    "entry_index": i,
                    "entry_id": entry.id,
                    "issue": "hash_mismatch",
                    "computed": computed_hash,
                    "stored": entry.entry_hash
                })

            previous_hash = entry.entry_hash

        return {
            "valid": len(issues) == 0,
            "entries_checked": len(self._entries),
            "issues": issues,
            "message": "Ledger integrity verified" if not issues else f"Found {len(issues)} integrity issues"
        }

    def get_entries(
        self,
        entry_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query ledger entries with optional filters.

        Args:
            entry_type: Filter by entry type
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum entries to return

        Returns:
            List of matching entries
        """
        results = []

        for entry in reversed(self._entries):  # Most recent first
            if len(results) >= limit:
                break

            # Apply filters
            if entry_type and entry.entry_type.value != entry_type.lower():
                continue

            if start_time and entry.timestamp < start_time:
                continue

            if end_time and entry.timestamp > end_time:
                continue

            results.append(entry.to_dict())

        return results

    def get_violations_summary(self) -> Dict[str, Any]:
        """Get summary of all recorded violations"""
        violation_entries = [
            e for e in self._entries if e.entry_type == EntryType.VIOLATION
        ]

        if not violation_entries:
            return {
                "total_violations": 0,
                "by_type": {},
                "average_severity": 0,
                "dpap_converted": 0
            }

        by_type = {}
        severity_sum = 0

        for entry in violation_entries:
            vtype = entry.data.get("violation_type", "unknown")
            by_type[vtype] = by_type.get(vtype, 0) + 1
            severity_sum += entry.data.get("severity", 0)

        # Count DPAP conversions
        dpap_entries = [
            e for e in self._entries if e.entry_type == EntryType.DPAP_TRANSFORMATION
        ]

        return {
            "total_violations": len(violation_entries),
            "by_type": by_type,
            "average_severity": severity_sum / len(violation_entries),
            "dpap_converted": len(dpap_entries)
        }

    def get_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision patterns from ledger"""
        decision_entries = [
            e for e in self._entries if e.entry_type == EntryType.DECISION
        ]

        if not decision_entries:
            return {
                "total_decisions": 0,
                "by_domain": {},
                "cil_averages": {"conscience": 0, "intuition": 0, "logic": 0}
            }

        by_domain = {}
        c_sum, i_sum, l_sum = 0, 0, 0

        for entry in decision_entries:
            domain = entry.data.get("domain", "unknown")
            by_domain[domain] = by_domain.get(domain, 0) + 1

            scores = entry.data.get("cil_scores", {})
            c_sum += scores.get("conscience", 0)
            i_sum += scores.get("intuition", 0)
            l_sum += scores.get("logic", 0)

        n = len(decision_entries)
        return {
            "total_decisions": n,
            "by_domain": by_domain,
            "cil_averages": {
                "conscience": c_sum / n,
                "intuition": i_sum / n,
                "logic": l_sum / n
            }
        }

    def export_ledger(self, filepath: str = None) -> Dict[str, Any]:
        """Export entire ledger to JSON"""
        export_data = {
            "metadata": {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_entries": len(self._entries),
                "genesis_hash": self._genesis_hash,
                "latest_hash": self._entries[-1].entry_hash if self._entries else self._genesis_hash
            },
            "integrity_check": self.verify_integrity(),
            "entries": [e.to_dict() for e in self._entries]
        }

        if filepath:
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)

        return export_data

    @property
    def entry_count(self) -> int:
        """Get total number of entries"""
        return len(self._entries)

    @property
    def latest_hash(self) -> str:
        """Get hash of the latest entry"""
        return self._entries[-1].entry_hash if self._entries else self._genesis_hash
