"""
Speech-to-Text engine - Whisper API, local Whisper, or Google fallback.
"""

import io
import os
import wave
import tempfile
from typing import Optional


class STTEngine:
    """Speech-to-text with multiple backend support."""

    def __init__(self, engine: str = "whisper_api", language: str = "en"):
        self.engine = engine
        self.language = language

    def transcribe(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[str]:
        """Transcribe audio bytes to text.

        Args:
            audio_data: Raw PCM audio bytes (int16, mono).
            sample_rate: Sample rate of the audio.

        Returns:
            Transcribed text, or None on failure.
        """
        if self.engine == "whisper_api":
            return self._whisper_api(audio_data, sample_rate)
        elif self.engine == "whisper_local":
            return self._whisper_local(audio_data, sample_rate)
        elif self.engine == "google":
            return self._google_stt(audio_data, sample_rate)
        else:
            print(f"Unknown STT engine: {self.engine}")
            return None

    def _audio_to_wav_file(self, audio_data: bytes, sample_rate: int) -> str:
        """Write raw PCM audio to a temporary WAV file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data)
        return tmp.name

    def _whisper_api(self, audio_data: bytes, sample_rate: int) -> Optional[str]:
        """Transcribe using OpenAI Whisper API."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set, falling back to Google STT.")
            return self._google_stt(audio_data, sample_rate)

        wav_path = self._audio_to_wav_file(audio_data, sample_rate)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            with open(wav_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=self.language[:2],  # "en" from "en-US"
                )
            return transcript.text if transcript.text else None
        except Exception as e:
            print(f"Whisper API error: {e}")
            return None
        finally:
            os.unlink(wav_path)

    def _whisper_local(self, audio_data: bytes, sample_rate: int) -> Optional[str]:
        """Transcribe using local Whisper model."""
        try:
            import whisper
            import numpy as np
        except ImportError:
            print("Local whisper not installed. Run: pip install openai-whisper")
            return None

        wav_path = self._audio_to_wav_file(audio_data, sample_rate)
        try:
            model = whisper.load_model("base")
            result = model.transcribe(wav_path, language=self.language[:2])
            return result.get("text")
        except Exception as e:
            print(f"Local Whisper error: {e}")
            return None
        finally:
            os.unlink(wav_path)

    def _google_stt(self, audio_data: bytes, sample_rate: int) -> Optional[str]:
        """Transcribe using Google Speech Recognition (free, no API key)."""
        try:
            import speech_recognition as sr

            audio = sr.AudioData(audio_data, sample_rate, 2)
            recognizer = sr.Recognizer()
            text = recognizer.recognize_google(audio, language=self.language)
            return text
        except Exception as e:
            print(f"Google STT error: {e}")
            return None
