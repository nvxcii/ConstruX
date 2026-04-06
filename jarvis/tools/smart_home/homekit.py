"""
Smart Home Tool - Control devices via Home Assistant or HomeKit.
"""

import os
from typing import Any, Dict

from jarvis.tools.base_tool import BaseTool


class SmartHomeTool(BaseTool):
    name = "smart_home"
    description = (
        "Control smart home devices: lights, thermostat, locks, switches. "
        "Supports Home Assistant integration."
    )

    def __init__(self, settings=None):
        self._base_url = ""
        self._token = ""
        if settings:
            self._base_url = (
                settings.get("smart_home", "homeassistant_url", "")
                or os.getenv("HOMEASSISTANT_URL", "")
            )
            self._token = (
                settings.get("smart_home", "homeassistant_token", "")
                or os.getenv("HOMEASSISTANT_TOKEN", "")
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
                        "enum": ["turn_on", "turn_off", "toggle", "set", "status", "list_devices"],
                        "description": "Action to perform on a device.",
                    },
                    "device": {
                        "type": "string",
                        "description": "Device name or entity_id (e.g., 'living room lights', 'light.living_room').",
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to set (e.g., brightness '80', temperature '72').",
                    },
                    "domain": {
                        "type": "string",
                        "description": "Device domain: 'light', 'switch', 'climate', 'lock', 'cover'.",
                    },
                },
                "required": ["action"],
            },
        }

    def execute(self, action: str, **kwargs) -> str:
        if not self._base_url or not self._token:
            return (
                "Error: Home Assistant not configured. "
                "Set HOMEASSISTANT_URL and HOMEASSISTANT_TOKEN env vars, "
                "or configure in ~/.jarvis/config.json under 'smart_home'."
            )

        if action == "list_devices":
            return self._list_devices(kwargs.get("domain"))
        elif action == "status":
            return self._get_status(kwargs.get("device", ""))
        elif action in ("turn_on", "turn_off", "toggle"):
            return self._call_service(action, kwargs.get("device", ""), kwargs.get("domain"))
        elif action == "set":
            return self._set_value(kwargs.get("device", ""), kwargs.get("value", ""), kwargs.get("domain"))
        else:
            return f"Unknown action: {action}"

    def requires_confirmation(self, **kwargs) -> bool:
        return kwargs.get("action") in ("turn_off",) and kwargs.get("domain") == "lock"

    def confirmation_message(self, **kwargs) -> str:
        return f"Unlock {kwargs.get('device', 'device')}?"

    def _api_call(self, method: str, endpoint: str, json_data: dict = None) -> dict:
        """Make a Home Assistant API call."""
        import requests

        url = f"{self._base_url.rstrip('/')}/api/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=10)
            else:
                resp = requests.post(url, headers=headers, json=json_data or {}, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def _list_devices(self, domain: str = None) -> str:
        data = self._api_call("GET", "states")
        if isinstance(data, dict) and "error" in data:
            return f"Error: {data['error']}"

        devices = []
        for entity in data:
            entity_id = entity.get("entity_id", "")
            if domain and not entity_id.startswith(f"{domain}."):
                continue
            friendly_name = entity.get("attributes", {}).get("friendly_name", entity_id)
            state = entity.get("state", "unknown")
            devices.append(f"{friendly_name} ({entity_id}): {state}")

        if not devices:
            return "No devices found."
        return "\n".join(devices[:30])

    def _get_status(self, device: str) -> str:
        entity_id = self._resolve_entity(device)
        if not entity_id:
            return f"Could not find device: {device}"

        data = self._api_call("GET", f"states/{entity_id}")
        if "error" in data:
            return f"Error: {data['error']}"

        name = data.get("attributes", {}).get("friendly_name", entity_id)
        state = data.get("state", "unknown")
        attrs = data.get("attributes", {})

        info = f"{name}: {state}"
        if "brightness" in attrs:
            info += f" (brightness: {attrs['brightness']})"
        if "current_temperature" in attrs:
            info += f" (temp: {attrs['current_temperature']})"
        return info

    def _call_service(self, action: str, device: str, domain: str = None) -> str:
        entity_id = self._resolve_entity(device)
        if not entity_id:
            return f"Could not find device: {device}"

        if not domain:
            domain = entity_id.split(".")[0]

        service = action  # turn_on, turn_off, toggle
        data = self._api_call("POST", f"services/{domain}/{service}", {"entity_id": entity_id})

        if isinstance(data, dict) and "error" in data:
            return f"Error: {data['error']}"
        return f"{action.replace('_', ' ').title()} {device}."

    def _set_value(self, device: str, value: str, domain: str = None) -> str:
        entity_id = self._resolve_entity(device)
        if not entity_id:
            return f"Could not find device: {device}"

        if not domain:
            domain = entity_id.split(".")[0]

        service_data = {"entity_id": entity_id}
        if domain == "light":
            service_data["brightness_pct"] = int(value)
            service = "turn_on"
        elif domain == "climate":
            service_data["temperature"] = float(value)
            service = "set_temperature"
        else:
            return f"Don't know how to set value for domain: {domain}"

        data = self._api_call("POST", f"services/{domain}/{service}", service_data)
        if isinstance(data, dict) and "error" in data:
            return f"Error: {data['error']}"
        return f"Set {device} to {value}."

    def _resolve_entity(self, device: str) -> str:
        """Resolve a friendly device name to an entity_id."""
        if "." in device:
            return device  # Already an entity_id

        # Search for matching entity
        data = self._api_call("GET", "states")
        if isinstance(data, dict) and "error" in data:
            return ""

        device_lower = device.lower()
        for entity in data:
            friendly = entity.get("attributes", {}).get("friendly_name", "").lower()
            entity_id = entity.get("entity_id", "")
            if device_lower in friendly or device_lower in entity_id:
                return entity_id
        return ""
