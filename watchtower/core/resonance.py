"""
Resonance Engine - Field Coherence and Synchronization

Manages the flow and resonance between different field components.
Ensures coherence across the multi-layer field architecture.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ResonanceEngine:
    """
    Manages field resonance and coherence.

    Ensures that changes in one field layer properly propagate
    to other layers, maintaining system-wide coherence.
    """

    def __init__(self, field):
        self.field = field
        self.resonance_patterns: Dict[str, Dict[str, Any]] = {}
        self.coherence_score = 1.0

    def register_pattern(
        self,
        pattern_id: str,
        source_layer: str,
        target_layers: List[str],
        propagation_rule: str = 'immediate'
    ):
        """
        Register a resonance pattern.

        Args:
            pattern_id: Unique pattern identifier
            source_layer: Layer where resonance originates
            target_layers: Layers that should resonate
            propagation_rule: How resonance propagates (immediate, delayed, conditional)
        """
        self.resonance_patterns[pattern_id] = {
            'source_layer': source_layer,
            'target_layers': target_layers,
            'propagation_rule': propagation_rule,
            'created_at': datetime.utcnow().isoformat()
        }

    def propagate(
        self,
        pattern_id: str,
        source_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Propagate resonance through the field.

        Args:
            pattern_id: Pattern to activate
            source_data: Data from source layer
            context: Additional context

        Returns:
            Propagation results
        """
        if pattern_id not in self.resonance_patterns:
            return {'status': 'error', 'reason': 'pattern_not_found'}

        pattern = self.resonance_patterns[pattern_id]
        context = context or {}

        results = {
            'pattern_id': pattern_id,
            'source_layer': pattern['source_layer'],
            'target_layers': pattern['target_layers'],
            'propagation_rule': pattern['propagation_rule'],
            'timestamp': datetime.utcnow().isoformat(),
            'target_results': {}
        }

        # Propagate to each target layer
        for target_layer in pattern['target_layers']:
            target_result = self._propagate_to_layer(
                target_layer,
                source_data,
                pattern['propagation_rule'],
                context
            )
            results['target_results'][target_layer] = target_result

        # Update coherence score
        self._update_coherence(results)

        return results

    def _propagate_to_layer(
        self,
        target_layer: str,
        data: Dict[str, Any],
        rule: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Propagate resonance to a specific layer.

        Args:
            target_layer: Target layer name
            data: Data to propagate
            rule: Propagation rule
            context: Context

        Returns:
            Layer result
        """
        # In a real implementation, this would interface with actual field layers
        # For now, we simulate the propagation

        if rule == 'immediate':
            return {
                'status': 'propagated',
                'layer': target_layer,
                'data_received': True,
                'timestamp': datetime.utcnow().isoformat()
            }
        elif rule == 'delayed':
            return {
                'status': 'queued',
                'layer': target_layer,
                'scheduled_for': 'next_cycle',
                'timestamp': datetime.utcnow().isoformat()
            }
        elif rule == 'conditional':
            # Check if conditions are met
            condition_met = context.get('condition_met', True)
            if condition_met:
                return {
                    'status': 'propagated',
                    'layer': target_layer,
                    'condition': 'met',
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'status': 'blocked',
                    'layer': target_layer,
                    'condition': 'not_met',
                    'timestamp': datetime.utcnow().isoformat()
                }

        return {'status': 'unknown_rule', 'layer': target_layer}

    def _update_coherence(self, propagation_results: Dict[str, Any]):
        """
        Update field coherence score based on propagation results.

        Args:
            propagation_results: Results from propagation
        """
        successful = sum(
            1 for result in propagation_results['target_results'].values()
            if result.get('status') in ['propagated', 'queued']
        )
        total = len(propagation_results['target_results'])

        if total > 0:
            new_score = successful / total
            # Exponential moving average
            self.coherence_score = 0.7 * self.coherence_score + 0.3 * new_score

    def get_coherence_score(self) -> float:
        """
        Get current field coherence score.

        Returns:
            Coherence score (0.0 to 1.0)
        """
        return self.coherence_score

    def sync_all_layers(self) -> Dict[str, Any]:
        """
        Force synchronization of all field layers.

        Returns:
            Sync results
        """
        # Trigger field state save
        self.field.save_state()

        # Record sync event
        self.field.memory.record_event(
            event_type='resonance_sync',
            action='sync_all_layers',
            authorized=True,
            signature_id=self.field.signature.signature_id if self.field.signature else None,
            metadata={
                'coherence_score': self.coherence_score,
                'patterns_active': len(self.resonance_patterns)
            }
        )

        return {
            'status': 'synced',
            'coherence_score': self.coherence_score,
            'timestamp': datetime.utcnow().isoformat()
        }

    def diagnose_incoherence(self) -> List[Dict[str, Any]]:
        """
        Diagnose sources of field incoherence.

        Returns:
            List of diagnostic findings
        """
        findings = []

        if self.coherence_score < 0.8:
            findings.append({
                'severity': 'warning',
                'issue': 'low_coherence',
                'score': self.coherence_score,
                'recommendation': 'Run sync_all_layers() to restore coherence'
            })

        # Check for failed propagations in recent history
        recent_events = self.field.memory.query_events(
            event_type='resonance_sync',
            timerange='last_24_hours',
            limit=50
        )

        failed_count = sum(
            1 for event in recent_events
            if not event.get('authorized')
        )

        if failed_count > 5:
            findings.append({
                'severity': 'warning',
                'issue': 'frequent_propagation_failures',
                'count': failed_count,
                'recommendation': 'Check field signature and authorization settings'
            })

        return findings
