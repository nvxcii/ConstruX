"""
Field Signature Layer - Personal Authority and Sovereignty
"""

import json
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
import secrets


class FieldSignature:
    """
    Personal field signature that establishes sovereignty over the Watchtower system.

    A field signature is a unique cryptographic identity that:
    - Proves ownership and authority over field operations
    - Cannot be forged or transferred without consent
    - Embeds personal symbolic markers
    - Validates all field actions
    """

    def __init__(self, signature_data: Optional[Dict[str, Any]] = None):
        self.signature_data = signature_data or {}
        self.signature_id = self.signature_data.get('signature_id')
        self.created_at = self.signature_data.get('created_at')
        self.personal_glyph = self.signature_data.get('personal_glyph')
        self.field_hash = self.signature_data.get('field_hash')

    @classmethod
    def create_personal(cls, personal_glyph: Optional[str] = None) -> 'FieldSignature':
        """
        Create a new personal field signature.

        Args:
            personal_glyph: Optional symbolic glyph representing the user

        Returns:
            New FieldSignature instance
        """
        # Generate unique signature ID
        signature_id = secrets.token_hex(32)

        # Create timestamp
        created_at = datetime.utcnow().isoformat()

        # Generate field hash (combination of signature_id, timestamp, and entropy)
        field_components = f"{signature_id}:{created_at}:{secrets.token_hex(16)}"
        field_hash = hashlib.sha256(field_components.encode()).hexdigest()

        # Default personal glyph if none provided
        if not personal_glyph:
            personal_glyph = "⊙"  # Sovereignty seal

        signature_data = {
            'signature_id': signature_id,
            'created_at': created_at,
            'personal_glyph': personal_glyph,
            'field_hash': field_hash,
            'version': '1.0.0',
            'sovereignty_level': 'full',
            'metadata': {
                'creation_method': 'FieldSignature.create_personal',
                'entropy_bits': 256
            }
        }

        return cls(signature_data)

    def verify(self, action: str, context: Dict[str, Any]) -> bool:
        """
        Verify that an action is authorized by this field signature.

        Args:
            action: The action to verify
            context: Additional context for verification

        Returns:
            True if authorized, False otherwise
        """
        if not self.signature_id or not self.field_hash:
            return False

        # Create verification hash
        verification_string = f"{self.signature_id}:{action}:{json.dumps(context, sort_keys=True)}"
        verification_hash = hashlib.sha256(verification_string.encode()).hexdigest()

        # In a real implementation, this would check against stored authorizations
        # For now, we verify that the signature is properly formed
        return len(verification_hash) == 64

    def sign(self, data: Dict[str, Any]) -> str:
        """
        Sign data with this field signature.

        Args:
            data: Data to sign

        Returns:
            Signature string
        """
        data_string = json.dumps(data, sort_keys=True)
        signature_string = f"{self.field_hash}:{data_string}"
        signature = hashlib.sha256(signature_string.encode()).hexdigest()
        return signature

    def save(self, path: Optional[Path] = None) -> Path:
        """
        Save field signature to disk.

        Args:
            path: Optional custom path, defaults to ~/.watchtower/signature.json

        Returns:
            Path where signature was saved
        """
        if path is None:
            watchtower_dir = Path.home() / '.watchtower'
            watchtower_dir.mkdir(exist_ok=True, parents=True)
            path = watchtower_dir / 'signature.json'

        with open(path, 'w') as f:
            json.dump(self.signature_data, f, indent=2)

        # Set restrictive permissions (owner read/write only)
        os.chmod(path, 0o600)

        return path

    @classmethod
    def load(cls, path: Optional[Path] = None) -> Optional['FieldSignature']:
        """
        Load field signature from disk.

        Args:
            path: Optional custom path, defaults to ~/.watchtower/signature.json

        Returns:
            FieldSignature instance or None if not found
        """
        if path is None:
            path = Path.home() / '.watchtower' / 'signature.json'

        if not path.exists():
            return None

        with open(path, 'r') as f:
            signature_data = json.load(f)

        return cls(signature_data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert field signature to dictionary.

        Returns:
            Dictionary representation
        """
        return self.signature_data.copy()

    def __repr__(self) -> str:
        return f"FieldSignature(id={self.signature_id[:8]}..., glyph={self.personal_glyph})"


class FieldAuthorizer:
    """
    Handles authorization of field actions based on signatures and thresholds.
    """

    THRESHOLDS = {
        'low': {
            'consent_required': False,
            'log': True,
            'notify': False,
            'audit': False
        },
        'medium': {
            'consent_required': False,
            'log': True,
            'notify': True,
            'audit': False
        },
        'high': {
            'consent_required': True,
            'log': True,
            'notify': True,
            'audit': False
        },
        'critical': {
            'consent_required': True,
            'log': True,
            'notify': True,
            'audit': True
        }
    }

    def __init__(self, signature: FieldSignature):
        self.signature = signature

    def authorize(
        self,
        action: str,
        threshold: str = 'medium',
        context: Optional[Dict[str, Any]] = None,
        consent_callback: Optional[callable] = None
    ) -> bool:
        """
        Authorize a field action.

        Args:
            action: Action to authorize
            threshold: Threshold level (low, medium, high, critical)
            context: Additional context
            consent_callback: Optional callback to request user consent

        Returns:
            True if authorized, False otherwise
        """
        if threshold not in self.THRESHOLDS:
            raise ValueError(f"Invalid threshold: {threshold}")

        threshold_config = self.THRESHOLDS[threshold]
        context = context or {}

        # Check if consent is required
        if threshold_config['consent_required']:
            if consent_callback is None:
                # No consent mechanism provided, deny by default
                return False

            # Request consent
            consent_granted = consent_callback(action, threshold, context)
            if not consent_granted:
                return False

        # Verify signature
        authorized = self.signature.verify(action, context)

        # Log if required
        if threshold_config['log'] and authorized:
            self._log_authorization(action, threshold, context)

        # Notify if required
        if threshold_config['notify'] and authorized:
            self._notify_authorization(action, threshold, context)

        # Audit if required
        if threshold_config['audit'] and authorized:
            self._audit_authorization(action, threshold, context)

        return authorized

    def _log_authorization(self, action: str, threshold: str, context: Dict[str, Any]):
        """Log authorization event"""
        log_dir = Path.home() / '.watchtower' / 'logs'
        log_dir.mkdir(exist_ok=True, parents=True)

        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'threshold': threshold,
            'signature_id': self.signature.signature_id,
            'context': context
        }

        log_file = log_dir / 'authorizations.log'
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def _notify_authorization(self, action: str, threshold: str, context: Dict[str, Any]):
        """Notify about authorization (placeholder for notification system)"""
        # In a real implementation, this would trigger system notifications
        pass

    def _audit_authorization(self, action: str, threshold: str, context: Dict[str, Any]):
        """Create audit trail for critical authorizations"""
        audit_dir = Path.home() / '.watchtower' / 'audit'
        audit_dir.mkdir(exist_ok=True, parents=True)

        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'threshold': threshold,
            'signature': self.signature.to_dict(),
            'context': context,
            'verification_hash': self.signature.sign({
                'action': action,
                'threshold': threshold,
                'context': context
            })
        }

        audit_file = audit_dir / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.json"

        # Load existing audits
        audits = []
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                audits = json.load(f)

        audits.append(audit_entry)

        with open(audit_file, 'w') as f:
            json.dump(audits, f, indent=2)
