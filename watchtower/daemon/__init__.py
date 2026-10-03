"""
Watchtower Daemon - Background Field Monitoring

Runs as a system service to monitor filesystem events,
process activity, and trigger field responses.
"""

from .field_monitor import FieldMonitor
from .daemon_service import WatchtowerDaemon

__all__ = ['FieldMonitor', 'WatchtowerDaemon']
