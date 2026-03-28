"""
Wake Word Detection - Detects "Hey Jarvis" (or custom wake word) using Picovoice Porcupine.
Falls back to simple keyword spotting if Porcupine is not available.
"""

import threading
import time
from typing import Callable, Optional


class WakeWordDetector:
    """Listens for a wake word and triggers a callback when detected."""

    def __init__(self, wake_word: str = "hey jarvis", callback: Optional[Callable] = None):
        self.wake_word = wake_word.lower()
        self.callback = callback
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start listening for the wake word in a background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the wake word listener."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def _listen_loop(self) -> None:
        """Main listening loop - tries Porcupine first, falls back to continuous STT."""
        if self._try_porcupine():
            return

        # Fallback: periodic short STT checks for the wake word
        self._fallback_listen()

    def _try_porcupine(self) -> bool:
        """Try using Picovoice Porcupine for wake word detection."""
        try:
            import pvporcupine
            import sounddevice as sd
            import numpy as np

            access_key = None
            try:
                import os
                access_key = os.getenv("PICOVOICE_ACCESS_KEY")
            except Exception:
                pass

            if not access_key:
                return False

            porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=["jarvis"],  # Built-in keyword
            )

            frame_length = porcupine.frame_length
            sample_rate = porcupine.sample_rate

            print(f"Wake word detection active (Porcupine): '{self.wake_word}'")

            while self._running:
                audio = sd.rec(
                    frame_length,
                    samplerate=sample_rate,
                    channels=1,
                    dtype=np.int16,
                )
                sd.wait()

                pcm = audio.flatten()
                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print(f"Wake word detected!")
                    if self.callback:
                        self.callback()

            porcupine.delete()
            return True

        except ImportError:
            return False
        except Exception as e:
            print(f"Porcupine error: {e}")
            return False

    def _fallback_listen(self) -> None:
        """Fallback: use short STT bursts to detect the wake word."""
        try:
            import sounddevice as sd
            import numpy as np
            import speech_recognition as sr
        except ImportError:
            print("Wake word detection requires sounddevice and speech_recognition.")
            return

        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 3000
        sample_rate = 16000

        print(f"Wake word detection active (fallback STT): '{self.wake_word}'")

        while self._running:
            try:
                # Record 2 seconds of audio
                audio_data = sd.rec(
                    int(2 * sample_rate),
                    samplerate=sample_rate,
                    channels=1,
                    dtype=np.int16,
                )
                sd.wait()

                audio_bytes = audio_data.tobytes()
                audio = sr.AudioData(audio_bytes, sample_rate, 2)

                try:
                    text = recognizer.recognize_google(audio, language="en-US")
                    if self.wake_word in text.lower():
                        print(f"Wake word detected!")
                        if self.callback:
                            self.callback()
                except sr.UnknownValueError:
                    pass  # No speech detected, continue
                except sr.RequestError:
                    time.sleep(1)  # API error, brief pause

            except Exception:
                time.sleep(0.5)

    @property
    def is_running(self) -> bool:
        return self._running
