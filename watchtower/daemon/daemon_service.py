"""
Watchtower Daemon Service

Main daemon service that runs in the background to monitor
and manage field operations.
"""

import time
import signal
import sys
from pathlib import Path
from typing import Optional
from .field_monitor import FieldMonitor, ProcessMonitor
from ..core.field import Field


class WatchtowerDaemon:
    """
    Main Watchtower daemon service.

    Coordinates field monitoring, triggers, and responses.
    Designed to run as a system service.
    """

    def __init__(self, field: Optional[Field] = None):
        self.field = field or Field.load_personal()

        if not self.field:
            raise RuntimeError(
                "No personal field found. Run 'watchtower init' first."
            )

        self.file_monitor = FieldMonitor(field=self.field)
        self.process_monitor = ProcessMonitor(field=self.field)

        self.running = False
        self.config = self.field.config

        # Load daemon configuration
        self._load_daemon_config()

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

    def _load_daemon_config(self):
        """Load daemon configuration from field config"""
        daemon_config = self.config.get('daemon', {})

        # Add watch paths
        for path_str in daemon_config.get('watch_paths', []):
            path = Path(path_str).expanduser()
            if path.exists():
                self.file_monitor.add_watch_path(path)

        # Add trigger patterns
        for pattern in daemon_config.get('trigger_patterns', []):
            self.file_monitor.add_trigger_pattern(pattern)

        # Register default event handler
        self.file_monitor.on_event(self._handle_filesystem_event)

    def _handle_filesystem_event(self, event_data):
        """
        Handle filesystem events detected by the monitor.

        Args:
            event_data: Event data dictionary
        """
        print(f"Field event detected: {event_data['type']} - {event_data['path']}")

        # Determine appropriate glyph based on event type
        glyph_mapping = {
            'created': 'manifestation_star',
            'modified': 'resonance_wave',
            'deleted': 'dissolution_cross',
            'moved': 'resonance_wave'
        }

        glyph_id = glyph_mapping.get(event_data['type'], 'trigger_point')

        # Activate glyph (with automatic authorization for daemon events)
        self.field.activate_glyph(
            glyph_id=glyph_id,
            context=event_data,
            consent_callback=lambda action, threshold, ctx: True  # Auto-consent for daemon
        )

    def _handle_shutdown(self, signum, frame):
        """
        Handle shutdown signals.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        print("\nReceived shutdown signal. Stopping daemon...")
        self.stop()
        sys.exit(0)

    def start(self):
        """Start the daemon service"""
        if self.running:
            print("Daemon already running")
            return

        print("Starting Watchtower Daemon...")

        # Activate field
        if not self.field.state.get('active'):
            self.field.activate()

        # Start monitors
        self.file_monitor.start()
        self.process_monitor.start()

        self.running = True

        # Log daemon start
        self.field.memory.record_daemon_activity(
            activity_type='daemon_start',
            trigger_fired=False,
            details={
                'watch_paths': [str(p) for p in self.file_monitor.watch_paths],
                'trigger_patterns': self.file_monitor.trigger_patterns
            }
        )

        print("Watchtower Daemon started successfully")
        print(f"Watching {len(self.file_monitor.watch_paths)} paths")
        print("Press Ctrl+C to stop")

        # Main daemon loop
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the daemon service"""
        if not self.running:
            return

        print("Stopping Watchtower Daemon...")

        self.running = False

        # Stop monitors
        self.file_monitor.stop()
        self.process_monitor.stop()

        # Deactivate field
        self.field.deactivate()

        # Log daemon stop
        self.field.memory.record_daemon_activity(
            activity_type='daemon_stop',
            trigger_fired=False,
            details={'reason': 'user_requested'}
        )

        print("Watchtower Daemon stopped")

    def get_status(self):
        """
        Get daemon status.

        Returns:
            Status dictionary
        """
        return {
            'running': self.running,
            'field_active': self.field.state.get('active'),
            'file_monitor': self.file_monitor.get_status(),
            'process_monitor': self.process_monitor.get_status(),
            'field_health': self.field.get_health_status()
        }

    def reload_config(self):
        """Reload daemon configuration"""
        print("Reloading daemon configuration...")

        # Stop monitors
        self.file_monitor.stop()

        # Clear watch paths and patterns
        self.file_monitor.watch_paths.clear()
        self.file_monitor.trigger_patterns.clear()

        # Reload configuration
        self.field.config = type(self.field.config)()  # Fresh config
        self._load_daemon_config()

        # Restart monitors if daemon is running
        if self.running:
            self.file_monitor.start()

        print("Configuration reloaded")


def main():
    """Main entry point for daemon"""
    import argparse

    parser = argparse.ArgumentParser(description='Watchtower Daemon')
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status', 'reload'],
        help='Daemon command'
    )

    args = parser.parse_args()

    try:
        daemon = WatchtowerDaemon()

        if args.command == 'start':
            daemon.start()
        elif args.command == 'stop':
            daemon.stop()
        elif args.command == 'status':
            status = daemon.get_status()
            print(f"\nDaemon Status:")
            print(f"  Running: {status['running']}")
            print(f"  Field Active: {status['field_active']}")
            print(f"\nFile Monitor:")
            print(f"  Active: {status['file_monitor']['running']}")
            print(f"  Watching: {len(status['file_monitor']['watch_paths'])} paths")
            print(f"\nProcess Monitor:")
            print(f"  Active: {status['process_monitor']['running']}")
        elif args.command == 'reload':
            daemon.reload_config()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
