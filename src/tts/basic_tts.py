# src/tts/basic_tts.py
"""
voxi — Text-to-Speech Module
Supports pyttsx3 (100% offline macOS speech) and edge-tts (natural neural voice).
"""

import asyncio
import os
import subprocess
import tempfile
from typing import Generator, Optional
import edge_tts
import pyttsx3

from src.config.settings import TTS_ENGINE, EDGE_TTS_VOICE


class BasicTTS:
    """Text-to-Speech class supporting pyttsx3 (offline) and edge-tts (natural)."""

    def __init__(self) -> None:
        """Initialize the TTS engine configured in settings."""
        self.engine_type: str = TTS_ENGINE.lower()
        self.edge_voice: str = EDGE_TTS_VOICE
        self.pyttsx3_engine: Optional[pyttsx3.Engine] = None

        print(f"🔊 Loading TTS Engine: '{self.engine_type}'...")

        if self.engine_type == "pyttsx3":
            self._init_pyttsx3()
        elif self.engine_type == "edge-tts":
            self._init_pyttsx3()  # Available as offline fallback
            print(f"   Using Edge TTS voice: '{self.edge_voice}'")
        else:
            print(f"   ⚠️ Unknown TTS engine '{self.engine_type}', defaulting to pyttsx3")
            self.engine_type = "pyttsx3"
            self._init_pyttsx3()

        print(f"✅ TTS loaded successfully! (Engine: {self.engine_type})")

    def _init_pyttsx3(self) -> None:
        """Initialize pyttsx3 engine with rate, volume, and macOS voice."""
        if self.pyttsx3_engine is None:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_engine.setProperty("rate", 175)
            self.pyttsx3_engine.setProperty("volume", 0.9)

            # Look for natural macOS voices (Samantha or Rishi)
            voices = self.pyttsx3_engine.getProperty("voices")
            selected_voice: Optional[str] = None
            for v in voices:
                if "Samantha" in v.name or "Samantha" in v.id:
                    selected_voice = v.id
                    break

            if not selected_voice:
                for v in voices:
                    if "Rishi" in v.name or "Karen" in v.name:
                        selected_voice = v.id
                        break

            if not selected_voice and voices:
                selected_voice = voices[0].id

            if selected_voice:
                self.pyttsx3_engine.setProperty("voice", selected_voice)

    def speak(self, text: str) -> None:
        """
        Synthesize speech synchronously using the selected engine.

        Args:
            text: Text string to speak aloud. Empty strings are skipped.
        """
        text = text.strip()
        if not text:
            return

        print(f"\n🔊 Speaking: \"{text}\"")
        if self.engine_type == "edge-tts":
            self._speak_edge_tts(text)
        else:
            self._speak_pyttsx3(text)

    def speak_streaming(self, text_generator: Generator[str, None, None]) -> str:
        """
        Accumulate streaming tokens and speak at sentence boundaries.

        Args:
            text_generator: Generator yielding token chunks.

        Returns:
            str: Full assembled text spoken.
        """
        buffer: str = ""
        full_text: str = ""
        sentence_boundaries: set[str] = {".", "!", "?", ":", ";", "\n"}

        for token in text_generator:
            print(token, end="", flush=True)
            buffer += token
            full_text += token

            # Check if current buffer contains a punctuation boundary
            if any(punct in token for punct in sentence_boundaries) and len(buffer.strip()) > 15:
                chunk = buffer.strip()
                if chunk:
                    self.speak(chunk)
                buffer = ""

        # Speak any remaining tokens in buffer
        if buffer.strip():
            self.speak(buffer.strip())

        print()
        return full_text

    def _speak_pyttsx3(self, text: str) -> None:
        """
        Internal pyttsx3 speak using macOS NSSpeechSynthesizer.

        Args:
            text: Text to speak.
        """
        if not self.pyttsx3_engine:
            self._init_pyttsx3()
        if self.pyttsx3_engine:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()

    def _speak_edge_tts(self, text: str) -> None:
        """
        Internal async edge-tts speak (saves temp .mp3, plays via afplay).

        Args:
            text: Text to speak.
        """
        async def _synthesize() -> str:
            communicate = edge_tts.Communicate(text, self.edge_voice)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = tmp.name
            await communicate.save(tmp_path)
            return tmp_path

        tmp_file: Optional[str] = None
        try:
            tmp_file = asyncio.run(_synthesize())
            subprocess.run(["afplay", tmp_file], check=True)
        except Exception as e:
            print(f"   ⚠️ edge-tts audio playback failed: {e}. Falling back to pyttsx3.")
            self._speak_pyttsx3(text)
        finally:
            if tmp_file and os.path.exists(tmp_file):
                try:
                    os.unlink(tmp_file)
                except OSError:
                    pass
