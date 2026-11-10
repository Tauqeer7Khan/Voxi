# tests/test_stt.py
"""Test Whisper STT pipeline end-to-end."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.stt.whisper_stt import WhisperSTT


def test_stt():
    print("=" * 40)
    print("  🎙️✨ voxi — STT Test")
    print("=" * 40)

    stt = WhisperSTT()

    print("\nSay something into your microphone...")
    print("(Speak for 2-3 seconds, then pause)")

    text = stt.listen_and_transcribe()

    if text:
        print(f"\n✅ STT Test PASSED!")
        print(f"   Transcribed: \"{text}\"")
    else:
        print(f"\n❌ STT Test FAILED — no text captured")
        print("   Try speaking louder or closer to the mic")


if __name__ == "__main__":
    test_stt()

