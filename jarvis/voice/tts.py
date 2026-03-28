"""
Text-to-Speech engine - ElevenLabs API with pyttsx3 offline fallback.
"""

import io
import os
import threading
from typing import Optional


class TTSEngine:
    """Text-to-speech with ElevenLabs (natural) and pyttsx3 (offline) backends."""

    def __init__(self, engine: str = "elevenlabs", voice_id: str = "21m00Tcm4TlvDq8ikWAM",
                 pyttsx3_rate: int = 175, pyttsx3_volume: float = 0.9):
        self.engine = engine
        self.voice_id = voice_id
        self.pyttsx3_rate = pyttsx3_rate
        self.pyttsx3_volume = pyttsx3_volume
        self._pyttsx3_engine = None
        self.is_speaking = False

    def speak(self, text: str) -> None:
        """Speak text aloud using the configured engine.

        Args:
            text: The text to speak.
        """
        if not text:
            return

        self.is_speaking = True
        try:
            if self.engine == "elevenlabs":
                self._elevenlabs_speak(text)
            else:
                self._pyttsx3_speak(text)
        finally:
            self.is_speaking = False

    def speak_async(self, text: str) -> threading.Thread:
        """Speak text in a background thread."""
        t = threading.Thread(target=self.speak, args=(text,), daemon=True)
        t.start()
        return t

    def stop(self) -> None:
        """Stop current speech output."""
        self.is_speaking = False
        if self._pyttsx3_engine:
            try:
                self._pyttsx3_engine.stop()
            except Exception:
                pass

    def _elevenlabs_speak(self, text: str) -> None:
        """Speak using ElevenLabs API with streaming playback."""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("Warning: ELEVENLABS_API_KEY not set, falling back to pyttsx3.")
            self._pyttsx3_speak(text)
            return

        try:
            import requests
            import sounddevice as sd
            import numpy as np

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key,
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            }

            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()

            # Decode MP3 to play via sounddevice
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_mp3(io.BytesIO(response.content))
                samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
                samples = samples / (2**15)  # Normalize int16 to float32

                if audio.channels == 2:
                    samples = samples.reshape(-1, 2)

                sd.play(samples, samplerate=audio.frame_rate)
                sd.wait()
            except ImportError:
                # If pydub not available, save and play via system command
                import tempfile
                import subprocess
                tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                tmp.write(response.content)
                tmp.close()
                subprocess.run(["afplay", tmp.name], timeout=60)
                os.unlink(tmp.name)

        except Exception as e:
            print(f"ElevenLabs error: {e}, falling back to pyttsx3.")
            self._pyttsx3_speak(text)

    def _pyttsx3_speak(self, text: str) -> None:
        """Speak using pyttsx3 (offline, no API needed)."""
        try:
            import pyttsx3

            if self._pyttsx3_engine is None:
                self._pyttsx3_engine = pyttsx3.init()
                self._pyttsx3_engine.setProperty("rate", self.pyttsx3_rate)
                self._pyttsx3_engine.setProperty("volume", self.pyttsx3_volume)

            self._pyttsx3_engine.say(text)
            self._pyttsx3_engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 error: {e}")
