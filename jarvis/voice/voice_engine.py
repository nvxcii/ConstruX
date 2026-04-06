"""
Voice Engine - Unified voice pipeline connecting STT, TTS, wake word, and orchestrator.
"""

import threading
import time
from typing import Optional

import numpy as np
import sounddevice as sd

from jarvis.voice.stt import STTEngine
from jarvis.voice.tts import TTSEngine
from jarvis.voice.wake_word import WakeWordDetector


class VoiceEngine:
    """Unified voice pipeline that ties together:
    - Wake word detection ("Hey Jarvis")
    - Speech-to-text (Whisper / Google)
    - Orchestrator processing (Claude tool_use brain)
    - Text-to-speech (ElevenLabs / pyttsx3)
    """

    def __init__(self, settings=None):
        self.settings = settings
        self.sample_rate = 16000
        self.is_listening = False
        self.is_processing = False

        # Configure engines from settings
        stt_engine = "whisper_api"
        tts_engine = "elevenlabs"
        voice_id = "21m00Tcm4TlvDq8ikWAM"
        wake_word = "hey jarvis"
        wake_word_enabled = False

        if settings:
            stt_engine = settings.get("voice", "stt_engine", "whisper_api")
            tts_engine = settings.get("voice", "tts_engine", "elevenlabs")
            voice_id = settings.get("voice", "elevenlabs_voice_id", voice_id)
            wake_word = settings.get("assistant", "wake_word", "hey jarvis")
            wake_word_enabled = settings.get("voice", "wake_word_enabled", False)

        self.stt = STTEngine(engine=stt_engine)
        self.tts = TTSEngine(
            engine=tts_engine,
            voice_id=voice_id,
            pyttsx3_rate=settings.get("voice", "pyttsx3_rate", 175) if settings else 175,
            pyttsx3_volume=settings.get("voice", "pyttsx3_volume", 0.9) if settings else 0.9,
        )
        self.wake_detector = WakeWordDetector(
            wake_word=wake_word,
            callback=self._on_wake_word,
        ) if wake_word_enabled else None

        self._orchestrator = None
        self._wake_triggered = threading.Event()

    def run(self, orchestrator) -> None:
        """Main voice loop - connects voice I/O to the orchestrator."""
        self._orchestrator = orchestrator
        name = "Jarvis"
        if self.settings:
            name = self.settings.assistant_name

        self.tts.speak_async(f"{name} voice mode activated. I'm listening.")

        # Start wake word detection if enabled
        if self.wake_detector:
            self.wake_detector.start()
            print(f"Say '{self.wake_detector.wake_word}' to activate, or press Enter to type.")
        else:
            print("Voice mode active. Press Enter to speak, or type a command.")

        try:
            while True:
                # Wait for wake word or Enter key
                if self.wake_detector:
                    # Check for wake word trigger or keyboard input
                    self._wake_triggered.clear()
                    self._wake_triggered.wait(timeout=0.5)

                    if not self._wake_triggered.is_set():
                        continue
                else:
                    try:
                        cmd = input("\n[Press Enter to speak, or type]: ").strip()
                        if cmd.lower() in ("quit", "exit"):
                            break
                        if cmd:
                            # Text input mode
                            response = self._orchestrator.process(cmd)
                            print(f"\n{name}: {response}")
                            self.tts.speak_async(response)
                            continue
                    except (EOFError, KeyboardInterrupt):
                        break

                # Record and process voice
                self._process_voice_input(name)

        except KeyboardInterrupt:
            pass
        finally:
            if self.wake_detector:
                self.wake_detector.stop()
            print(f"\n{name} voice mode deactivated.")

    def _on_wake_word(self) -> None:
        """Called when the wake word is detected."""
        self._wake_triggered.set()

    def _process_voice_input(self, name: str) -> None:
        """Record audio, transcribe, process, and speak response."""
        # Record
        print("\nListening...")
        self.is_listening = True
        try:
            audio_data = sd.rec(
                int(5 * self.sample_rate),  # 5 second max
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
            )
            sd.wait()
            audio_bytes = audio_data.tobytes()
        except Exception as e:
            print(f"Recording error: {e}")
            return
        finally:
            self.is_listening = False

        # Transcribe
        print("Processing speech...")
        self.is_processing = True
        text = self.stt.transcribe(audio_bytes, self.sample_rate)

        if not text:
            print("Could not understand audio.")
            self.is_processing = False
            return

        print(f"You: {text}")

        # Process through orchestrator
        try:
            response = self._orchestrator.process(text)
            print(f"\n{name}: {response}")
            self.tts.speak_async(response)
        except Exception as e:
            error_msg = f"I encountered an error: {e}"
            print(f"\n{name}: {error_msg}")
            self.tts.speak_async("Sorry, I encountered an error processing that request.")
        finally:
            self.is_processing = False

    def listen_once(self, duration: float = 5.0) -> Optional[str]:
        """Record and transcribe a single utterance. Returns text or None."""
        try:
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
            )
            sd.wait()
            return self.stt.transcribe(audio_data.tobytes(), self.sample_rate)
        except Exception as e:
            print(f"Listen error: {e}")
            return None
