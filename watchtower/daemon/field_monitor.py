"""
Field Monitor - Filesystem and Process Event Monitoring

Monitors designated paths and processes for field-significant events.
"""

import os
import time
import fnmatch
from pathlib import Path
from typing import List, Callable, Optional, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FieldEventHandler(FileSystemEventHandler):
    """
    Handles filesystem events for field monitoring.
    """

    def __init__(
        self,
        patterns: List[str],
        on_event_callback: Callable,
        field_memory=None
    ):
        self.patterns = patterns
        self.on_event_callback = on_event_callback
        self.field_memory = field_memory

    def _matches_pattern(self, path: str) -> bool:
        """Check if path matches any trigger pattern"""
        for pattern in self.patterns:
            if fnmatch.fnmatch(path, f"*{pattern}"):
                return True
        return False

    def on_created(self, event: FileSystemEvent):
        """Handle file creation events"""
        if not event.is_directory and self._matches_pattern(event.src_path):
            self._handle_event('created', event)

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events"""
        if not event.is_directory and self._matches_pattern(event.src_path):
            self._handle_event('modified', event)

    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion events"""
        if not event.is_directory and self._matches_pattern(event.src_path):
            self._handle_event('deleted', event)

    def on_moved(self, event: FileSystemEvent):
        """Handle file move events"""
        if not event.is_directory:
            if self._matches_pattern(event.src_path) or self._matches_pattern(event.dest_path):
                self._handle_event('moved', event)

    def _handle_event(self, event_type: str, event: FileSystemEvent):
        """
        Handle a filesystem event.

        Args:
            event_type: Type of event (created, modified, deleted, moved)
            event: FileSystemEvent object
        """
        event_data = {
            'type': event_type,
            'path': event.src_path,
            'is_directory': event.is_directory,
            'timestamp': time.time()
        }

        if event_type == 'moved':
            event_data['dest_path'] = event.dest_path

        # Log to field memory if available
        if self.field_memory:
            self.field_memory.record_daemon_activity(
                activity_type=f'file_{event_type}',
                path=event.src_path,
                trigger_fired=True,
                details=event_data
            )

        # Trigger callback
        self.on_event_callback(event_data)


class FieldMonitor:
    """
    Monitors filesystem and process events for the field.

    Can watch multiple directories and trigger field responses
    when specific patterns are detected.
    """

    def __init__(self, field=None):
        self.field = field
        self.observers: List[Observer] = []
        self.watch_paths: List[Path] = []
        self.trigger_patterns: List[str] = []
        self.event_callbacks: List[Callable] = []
        self.running = False

    def add_watch_path(self, path: Path, recursive: bool = True):
        """
        Add a path to watch.

        Args:
            path: Path to watch
            recursive: Whether to watch subdirectories
        """
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Path does not exist: {path}")

        if path not in self.watch_paths:
            self.watch_paths.append(path)

            # If already running, start watching immediately
            if self.running:
                self._start_watching_path(path, recursive)

    def add_trigger_pattern(self, pattern: str):
        """
        Add a file pattern that should trigger events.

        Args:
            pattern: Glob pattern (e.g., '*.field', '*.glyph')
        """
        if pattern not in self.trigger_patterns:
            self.trigger_patterns.append(pattern)

    def on_event(self, callback: Callable):
        """
        Register a callback for field events.

        Args:
            callback: Function to call when event occurs
        """
        if callback not in self.event_callbacks:
            self.event_callbacks.append(callback)

    def _start_watching_path(self, path: Path, recursive: bool = True):
        """
        Start watching a specific path.

        Args:
            path: Path to watch
            recursive: Whether to watch subdirectories
        """
        observer = Observer()

        event_handler = FieldEventHandler(
            patterns=self.trigger_patterns,
            on_event_callback=self._handle_field_event,
            field_memory=self.field.memory if self.field else None
        )

        observer.schedule(event_handler, str(path), recursive=recursive)
        observer.start()

        self.observers.append(observer)

    def _handle_field_event(self, event_data: Dict[str, Any]):
        """
        Handle a field event by calling all registered callbacks.

        Args:
            event_data: Event data dictionary
        """
        for callback in self.event_callbacks:
            try:
                callback(event_data)
            except Exception as e:
                print(f"Error in event callback: {e}")

    def start(self):
        """Start monitoring"""
        if self.running:
            return

        self.running = True

        # Start watching all paths
        for path in self.watch_paths:
            self._start_watching_path(path, recursive=True)

        print(f"FieldMonitor started watching {len(self.watch_paths)} paths")

    def stop(self):
        """Stop monitoring"""
        if not self.running:
            return

        self.running = False

        # Stop all observers
        for observer in self.observers:
            observer.stop()
            observer.join()

        self.observers.clear()

        print("FieldMonitor stopped")

    def get_status(self) -> Dict[str, Any]:
        """
        Get monitor status.

        Returns:
            Status dictionary
        """
        return {
            'running': self.running,
            'watch_paths': [str(p) for p in self.watch_paths],
            'trigger_patterns': self.trigger_patterns,
            'observers_active': len(self.observers),
            'callbacks_registered': len(self.event_callbacks)
        }

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


class ProcessMonitor:
    """
    Monitors system processes for field-relevant activity.

    Can detect process starts/stops and trigger field responses.
    """

    def __init__(self, field=None):
        self.field = field
        self.monitored_processes: List[str] = []
        self.running = False
        self._monitor_thread = None

    def add_process(self, process_name: str):
        """
        Add a process to monitor.

        Args:
            process_name: Name of process to monitor
        """
        if process_name not in self.monitored_processes:
            self.monitored_processes.append(process_name)

    def start(self):
        """Start process monitoring"""
        if self.running:
            return

        self.running = True

        # In a real implementation, this would start a thread
        # that periodically checks for process activity
        print(f"ProcessMonitor started monitoring {len(self.monitored_processes)} processes")

    def stop(self):
        """Stop process monitoring"""
        if not self.running:
            return

        self.running = False
        print("ProcessMonitor stopped")

    def get_status(self) -> Dict[str, Any]:
        """
        Get monitor status.

        Returns:
            Status dictionary
        """
        return {
            'running': self.running,
            'monitored_processes': self.monitored_processes
        }
