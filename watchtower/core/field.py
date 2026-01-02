"""
Field - Core Field Architecture

The Field is the central concept of Watchtower.
It represents a container of sovereignty that coordinates all field operations.
"""

from typing import Dict, Optional, Any, Callable
from pathlib import Path
from .field_signature import FieldSignature, FieldAuthorizer
from ..config.field_memory import FieldMemory
from ..config.config_manager import ConfigManager
from ..glyphs.glyph_registry import GlyphRegistry
from ..glyphs.system_glyphs import load_system_glyphs


class FieldBase:
    """
    Base class for field implementations.

    Override to create custom field behaviors.
    """

    def on_trigger(self, event: Dict[str, Any]):
        """
        Handle field trigger events.

        Args:
            event: Trigger event data
        """
        raise NotImplementedError("Subclasses must implement on_trigger")

    def on_authorization(self, action: str, authorized: bool, context: Dict[str, Any]):
        """
        Handle authorization events.

        Args:
            action: Action that was authorized/denied
            authorized: Whether it was authorized
            context: Authorization context
        """
        pass

    def on_state_change(self, old_state: Dict[str, Any], new_state: Dict[str, Any]):
        """
        Handle field state changes.

        Args:
            old_state: Previous field state
            new_state: New field state
        """
        pass


class Field:
    """
    The Field - A Persistent Container of Sovereignty

    Coordinates all field operations:
    - Field signature authorization
    - Glyph activation and mapping
    - Memory persistence
    - State management
    - Trigger execution
    """

    def __init__(
        self,
        signature: Optional[FieldSignature] = None,
        memory: Optional[FieldMemory] = None,
        config: Optional[ConfigManager] = None,
        glyph_registry: Optional[GlyphRegistry] = None
    ):
        # Initialize components
        self.signature = signature
        self.memory = memory or FieldMemory()
        self.config = config or ConfigManager()
        self.glyph_registry = glyph_registry or GlyphRegistry()

        # Initialize authorizer if we have a signature
        self.authorizer = FieldAuthorizer(signature) if signature else None

        # Field state
        self.state: Dict[str, Any] = {
            'initialized': True,
            'active': False,
            'field_id': signature.signature_id if signature else None
        }

        # Trigger callbacks
        self._trigger_callbacks: Dict[str, Callable] = {}

        # Load system glyphs if registry is empty
        if len(self.glyph_registry.list_all()) == 0:
            load_system_glyphs(self.glyph_registry)

    @classmethod
    def create_new(cls, personal_glyph: Optional[str] = None) -> 'Field':
        """
        Create a new field with a fresh signature.

        Args:
            personal_glyph: Optional personal glyph symbol

        Returns:
            New Field instance
        """
        signature = FieldSignature.create_personal(personal_glyph)
        signature.save()

        field = cls(signature=signature)
        field.activate()

        return field

    @classmethod
    def load_personal(cls, signature_path: Optional[Path] = None) -> Optional['Field']:
        """
        Load personal field from saved signature.

        Args:
            signature_path: Optional path to signature file

        Returns:
            Field instance or None if no signature found
        """
        signature = FieldSignature.load(signature_path)
        if not signature:
            return None

        field = cls(signature=signature)
        field.load_state()

        return field

    def activate(self):
        """Activate the field"""
        old_state = self.state.copy()
        self.state['active'] = True

        self.memory.record_event(
            event_type='field_activation',
            signature_id=self.signature.signature_id if self.signature else None,
            authorized=True,
            metadata={'activation_time': self._current_timestamp()}
        )

        self.save_state()

    def deactivate(self):
        """Deactivate the field"""
        old_state = self.state.copy()
        self.state['active'] = False

        self.memory.record_event(
            event_type='field_deactivation',
            signature_id=self.signature.signature_id if self.signature else None,
            authorized=True,
            metadata={'deactivation_time': self._current_timestamp()}
        )

        self.save_state()

    def authorize(
        self,
        action: str,
        glyph: Optional[str] = None,
        threshold: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        consent_callback: Optional[Callable] = None
    ) -> bool:
        """
        Authorize a field action.

        Args:
            action: Action to authorize
            glyph: Glyph ID to use for authorization
            threshold: Override threshold level
            context: Additional context
            consent_callback: Callback for user consent

        Returns:
            True if authorized, False otherwise
        """
        if not self.authorizer:
            raise RuntimeError("Field has no signature - cannot authorize actions")

        context = context or {}

        # Look up glyph if provided
        if glyph:
            glyph_obj = self.glyph_registry.get(glyph)
            if not glyph_obj:
                return False

            # Use glyph's threshold if none specified
            if threshold is None:
                threshold = glyph_obj.threshold

            context['glyph'] = glyph
            context['glyph_symbol'] = glyph_obj.symbol

        # Use medium threshold as default
        if threshold is None:
            threshold = 'medium'

        # Authorize
        authorized = self.authorizer.authorize(
            action=action,
            threshold=threshold,
            context=context,
            consent_callback=consent_callback
        )

        # Record authorization event
        self.memory.record_event(
            event_type='authorization',
            glyph_id=glyph,
            action=action,
            threshold=threshold,
            authorized=authorized,
            signature_id=self.signature.signature_id,
            context=context
        )

        return authorized

    def activate_glyph(
        self,
        glyph_id: str,
        context: Optional[Dict[str, Any]] = None,
        consent_callback: Optional[Callable] = None
    ) -> bool:
        """
        Activate a glyph and execute its trigger.

        Args:
            glyph_id: Glyph identifier
            context: Activation context
            consent_callback: Callback for user consent

        Returns:
            True if successful, False otherwise
        """
        import time

        glyph = self.glyph_registry.get(glyph_id)
        if not glyph:
            return False

        context = context or {}
        start_time = time.time()

        # Authorize the glyph activation
        authorized = self.authorize(
            action=f"activate_glyph_{glyph_id}",
            glyph=glyph_id,
            context=context,
            consent_callback=consent_callback
        )

        if not authorized:
            self.memory.record_glyph_activation(
                glyph_id=glyph_id,
                glyph_symbol=glyph.symbol,
                trigger=glyph.trigger,
                result='denied',
                metadata={'reason': 'authorization_failed'}
            )
            return False

        # Execute trigger
        try:
            result = self._execute_trigger(glyph.trigger, context)
            duration_ms = int((time.time() - start_time) * 1000)

            self.memory.record_glyph_activation(
                glyph_id=glyph_id,
                glyph_symbol=glyph.symbol,
                trigger=glyph.trigger,
                result='success',
                duration_ms=duration_ms,
                metadata={'trigger_result': result}
            )

            return True

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)

            self.memory.record_glyph_activation(
                glyph_id=glyph_id,
                glyph_symbol=glyph.symbol,
                trigger=glyph.trigger,
                result='error',
                duration_ms=duration_ms,
                metadata={'error': str(e)}
            )

            return False

    def register_trigger(self, trigger_name: str, callback: Callable):
        """
        Register a trigger callback.

        Args:
            trigger_name: Name of the trigger
            callback: Callback function
        """
        self._trigger_callbacks[trigger_name] = callback

    def _execute_trigger(self, trigger_name: str, context: Dict[str, Any]) -> Any:
        """
        Execute a trigger.

        Args:
            trigger_name: Name of the trigger
            context: Trigger context

        Returns:
            Trigger result
        """
        if trigger_name in self._trigger_callbacks:
            return self._trigger_callbacks[trigger_name](context)

        # Default trigger implementations
        if trigger_name == 'authorize_field_action':
            return {'status': 'authorized'}
        elif trigger_name == 'sync_field_state':
            self.save_state()
            return {'status': 'synced'}
        elif trigger_name == 'persist_state':
            self.save_state()
            return {'status': 'persisted'}
        elif trigger_name == 'health_check':
            return self.get_health_status()
        else:
            return {'status': 'no_op', 'trigger': trigger_name}

    def save_state(self):
        """Save current field state to memory"""
        self.memory.save_field_state(
            state_type='full',
            state_data=self.state,
            signature_id=self.signature.signature_id if self.signature else None
        )

    def load_state(self):
        """Load field state from memory"""
        saved_state = self.memory.get_latest_state('full')
        if saved_state:
            self.state = saved_state['state_data']

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get field health status.

        Returns:
            Health status dictionary
        """
        memory_stats = self.memory.get_statistics()
        glyph_stats = self.glyph_registry.get_statistics()

        return {
            'field_active': self.state.get('active', False),
            'signature_present': self.signature is not None,
            'memory_stats': memory_stats,
            'glyph_stats': glyph_stats,
            'trigger_callbacks_registered': len(self._trigger_callbacks)
        }

    def _current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def __repr__(self) -> str:
        field_id = self.signature.signature_id[:8] if self.signature else 'no_signature'
        active_status = 'active' if self.state.get('active') else 'inactive'
        return f"Field(id={field_id}, status={active_status})"
