"""
Menu Bar App - macOS system tray app using rumps for quick access to Jarvis.
"""

import threading
from typing import Optional


def create_menu_bar_app(orchestrator=None, settings=None):
    """Create and return the menu bar app. Call app.run() to start."""
    try:
        import rumps
    except ImportError:
        print("Menu bar app requires 'rumps'. Install with: pip install rumps")
        return None

    class JarvisMenuBar(rumps.App):
        def __init__(self, orchestrator=None, settings=None):
            name = "Jarvis"
            if settings:
                name = settings.assistant_name

            super().__init__(
                name,
                icon=None,  # Uses text title if no icon
                quit_button="Quit Jarvis",
            )

            self.orchestrator = orchestrator
            self.settings = settings
            self.voice_active = False
            self._voice_engine = None

            # Build menu
            self.menu = [
                rumps.MenuItem("Voice Mode: OFF", callback=self.toggle_voice),
                None,  # Separator
                rumps.MenuItem("Quick Command...", callback=self.quick_command),
                None,
                rumps.MenuItem("Reset Conversation", callback=self.reset_conversation),
                rumps.MenuItem("List Tools", callback=self.list_tools),
                None,
                rumps.MenuItem(f"Model: {settings.model if settings else 'claude-sonnet-4-5-20250929'}"),
            ]

        @rumps.clicked("Voice Mode: OFF")
        def toggle_voice(self, sender):
            self.voice_active = not self.voice_active
            if self.voice_active:
                sender.title = "Voice Mode: ON"
                self.title = "Jarvis (Listening)"
                self._start_voice()
            else:
                sender.title = "Voice Mode: OFF"
                self.title = "Jarvis"
                self._stop_voice()

        def _start_voice(self):
            if self.orchestrator is None:
                rumps.notification("Jarvis", "Error", "Orchestrator not initialized.")
                return

            def voice_thread():
                try:
                    from jarvis.voice.voice_engine import VoiceEngine
                    self._voice_engine = VoiceEngine(settings=self.settings)
                    self._voice_engine.run(self.orchestrator)
                except Exception as e:
                    rumps.notification("Jarvis", "Voice Error", str(e))

            threading.Thread(target=voice_thread, daemon=True).start()

        def _stop_voice(self):
            self._voice_engine = None

        @rumps.clicked("Quick Command...")
        def quick_command(self, _):
            window = rumps.Window(
                message="Enter a command for Jarvis:",
                title="Jarvis - Quick Command",
                default_text="",
                ok="Send",
                cancel="Cancel",
                dimensions=(320, 60),
            )
            response = window.run()
            if response.clicked and response.text.strip():
                if self.orchestrator:
                    try:
                        result = self.orchestrator.process(response.text.strip())
                        rumps.notification("Jarvis", "Response", result[:200])
                    except Exception as e:
                        rumps.notification("Jarvis", "Error", str(e))

        @rumps.clicked("Reset Conversation")
        def reset_conversation(self, _):
            if self.orchestrator:
                self.orchestrator.reset_conversation()
                rumps.notification("Jarvis", "", "Conversation cleared.")

        @rumps.clicked("List Tools")
        def list_tools(self, _):
            if self.orchestrator:
                tools = ", ".join(self.orchestrator.registry.tool_names)
                rumps.notification("Jarvis - Tools", "", tools[:200])

    return JarvisMenuBar(orchestrator=orchestrator, settings=settings)


def run_menu_bar(orchestrator=None, settings=None):
    """Convenience function to create and run the menu bar app."""
    app = create_menu_bar_app(orchestrator, settings)
    if app:
        app.run()
