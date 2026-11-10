# src/stt/whisper_stt.py
"""
voxi — Speech-to-Text Module
Uses faster-whisper for local, offline transcription.
"""

import os
import tempfile
from typing import Optional
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
from faster_whisper import WhisperModel

from src.config.settings import (
    WHISPER_MODEL,
    SAMPLE_RATE,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
)


class WhisperSTT:
    """Handles microphone recording and speech-to-text transcription."""

    def __init__(self) -> None:
        """Initialize the faster-whisper STT model."""
        print(f"🎙️✨ Loading Whisper model: '{WHISPER_MODEL}'...")
        print("   (First run downloads model files once; subsequent runs are fully offline)")
        self.model = WhisperModel(
            WHISPER_MODEL,
            device="auto",
            compute_type="auto"
        )
        print("✅ Whisper STT loaded successfully!")

    def record_audio(self) -> Optional[np.ndarray]:
        """
        Record audio from microphone until silence is detected.

        Returns:
            np.ndarray: Recorded float32 audio samples, or None if no speech was detected.
        """
        print("\n🎙️✨ Listening... (speak now, pause to finish)")

        audio_chunks: list[np.ndarray] = []
        silence_counter: list[int] = [0]
        max_silence_chunks: int = int(SILENCE_DURATION * SAMPLE_RATE / 1024)
        has_speech: list[bool] = [False]

        def audio_callback(indata: np.ndarray, frames: int, time_info: dict, status: sd.CallbackFlags) -> None:
            if status:
                print(f"   ⚠️ Audio status: {status}")

            audio_chunks.append(indata.copy())

            # Calculate RMS volume
            volume = float(np.sqrt(np.mean(indata ** 2)))

            if volume < SILENCE_THRESHOLD:
                silence_counter[0] += 1
            else:
                silence_counter[0] = 0
                has_speech[0] = True

        try:
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                blocksize=1024,
                callback=audio_callback
            ):
                while True:
                    sd.sleep(100)
                    if has_speech[0] and silence_counter[0] >= max_silence_chunks:
                        break
                    # Safety timeout: 30 seconds max recording
                    if len(audio_chunks) > (30 * SAMPLE_RATE / 1024):
                        print("   ⏱️ Max recording time reached (30s)")
                        break

        except sd.PortAudioError as e:
            print(f"❌ Microphone error: {e}")
            print("   👉 Check macOS System Settings > Privacy & Security > Microphone")
            return None
        except KeyboardInterrupt:
            print("\n   ⏹️ Recording interrupted by user")

        print("⏹️ Done recording")

        if not audio_chunks or not has_speech[0]:
            print("   ⚠️ No speech detected")
            return None

        return np.concatenate(audio_chunks, axis=0)

    def transcribe(self, audio_data: Optional[np.ndarray]) -> str:
        """
        Transcribe audio numpy array to text using faster-whisper.

        Args:
            audio_data: Numpy float32 array of audio samples.

        Returns:
            str: Transcribed text string, or empty string on failure.
        """
        if audio_data is None:
            return ""

        # Write to temporary WAV file for faster-whisper input
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            audio_int16 = (audio_data * 32767).astype(np.int16)
            wav.write(tmp_path, SAMPLE_RATE, audio_int16)

        try:
            segments, _ = self.model.transcribe(
                tmp_path,
                beam_size=5,
                language="en",
                vad_filter=True
            )
            text = " ".join([seg.text for seg in segments]).strip()
        except Exception as e:
            print(f"   ⚠️ Transcription error: {e}")
            text = ""
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        if text:
            print(f"📝 You said: \"{text}\"")
        else:
            print("   ⚠️ Transcription empty")

        return text

    def listen_and_transcribe(self) -> str:
        """
        One-shot convenience method: Record from mic, then transcribe.

        Returns:
            str: Transcribed text string.
        """
        audio = self.record_audio()
        return self.transcribe(audio)
