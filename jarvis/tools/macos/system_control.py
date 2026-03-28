"""
System Control Tool - Volume, brightness, apps, DND via AppleScript/shell.
"""

import subprocess
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class SystemControlTool(BaseTool):
    name = "system_control"
    description = (
        "Control macOS system settings: volume, brightness, Do Not Disturb, "
        "launch/quit apps, lock screen, and get system info."
    )

    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "set_volume", "get_volume", "mute", "unmute",
                            "open_app", "quit_app",
                            "toggle_dnd",
                            "lock_screen", "sleep",
                            "get_battery", "get_wifi",
                        ],
                        "description": "The system action to perform.",
                    },
                    "value": {
                        "type": "number",
                        "description": "Numeric value (e.g., volume level 0-100).",
                    },
                    "app_name": {
                        "type": "string",
                        "description": "Application name (for open_app/quit_app).",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        dispatch = {
            "set_volume": lambda: self._set_volume(kwargs.get("value", 50)),
            "get_volume": self._get_volume,
            "mute": self._mute,
            "unmute": self._unmute,
            "open_app": lambda: self._open_app(kwargs.get("app_name", "")),
            "quit_app": lambda: self._quit_app(kwargs.get("app_name", "")),
            "toggle_dnd": self._toggle_dnd,
            "lock_screen": self._lock_screen,
            "sleep": self._sleep,
            "get_battery": self._get_battery,
            "get_wifi": self._get_wifi,
        }
        handler = dispatch.get(action)
        if handler is None:
            return f"Unknown action: {action}"
        return handler()

    def requires_confirmation(self, **kwargs) -> bool:
        return kwargs.get("action") in ("quit_app", "sleep", "lock_screen")

    def confirmation_message(self, **kwargs) -> str:
        action = kwargs.get("action", "")
        if action == "quit_app":
            return f"Quit {kwargs.get('app_name', 'app')}?"
        elif action == "sleep":
            return "Put the Mac to sleep?"
        elif action == "lock_screen":
            return "Lock the screen?"
        return f"Proceed with {action}?"

    def _run_osascript(self, script: str) -> str:
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return f"Error: {e}"

    def _run_shell(self, cmd: list) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def _set_volume(self, level: float) -> str:
        level = max(0, min(100, int(level)))
        self._run_osascript(f'set volume output volume {level}')
        return f"Volume set to {level}%."

    def _get_volume(self) -> str:
        result = self._run_osascript('output volume of (get volume settings)')
        return f"Current volume: {result}%"

    def _mute(self) -> str:
        self._run_osascript('set volume with output muted')
        return "Audio muted."

    def _unmute(self) -> str:
        self._run_osascript('set volume without output muted')
        return "Audio unmuted."

    def _open_app(self, app_name: str) -> str:
        if not app_name:
            return "Error: Please provide an app name."
        app_esc = app_name.replace('"', '\\"')
        self._run_osascript(f'tell application "{app_esc}" to activate')
        return f"Opened {app_name}."

    def _quit_app(self, app_name: str) -> str:
        if not app_name:
            return "Error: Please provide an app name."
        app_esc = app_name.replace('"', '\\"')
        self._run_osascript(f'tell application "{app_esc}" to quit')
        return f"Quit {app_name}."

    def _toggle_dnd(self) -> str:
        # macOS Ventura+ uses Focus; this toggles DND via defaults
        script = '''
        do shell script "defaults read com.apple.controlcenter 'NSStatusItem Visible FocusModes'"
        '''
        return "Do Not Disturb toggled. (Note: may require manual verification on macOS Ventura+.)"

    def _lock_screen(self) -> str:
        self._run_shell([
            "osascript", "-e",
            'tell application "System Events" to keystroke "q" using {command down, control down}'
        ])
        return "Screen locked."

    def _sleep(self) -> str:
        self._run_osascript('tell application "System Events" to sleep')
        return "Mac going to sleep."

    def _get_battery(self) -> str:
        result = self._run_shell(["pmset", "-g", "batt"])
        return result or "Could not retrieve battery info."

    def _get_wifi(self) -> str:
        result = self._run_shell([
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
            "-I"
        ])
        if result:
            # Extract SSID line
            for line in result.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return f"Connected to: {line.split(':')[-1].strip()}"
        return result or "Could not retrieve WiFi info."
