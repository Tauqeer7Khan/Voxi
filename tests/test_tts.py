# tests/test_tts.py
"""Test BasicTTS pipeline (blocking + streaming)."""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.tts.basic_tts import BasicTTS


def test_tts():
    print("=" * 40)
    print("  🎙️✨ voxi — TTS Test")
    print("=" * 40)

    tts = BasicTTS()

    # Test 1: Single phrase speak
    print("\n📋 Test 1: Standard blocking speech")
    tts.speak("Hello! voxi speech synthesis is working.")

    # Test 2: Streaming generator speech
    print("\n📋 Test 2: Streaming speech with sentence boundaries")

    def fake_token_generator():
        tokens = [
            "This ", "is ", "sentence ", "one. ",
            "And ", "here ", "is ", "the ", "second ", "sentence! ",
            "Finally, ", "stream ", "done."
        ]
        for t in tokens:
            time.sleep(0.05)  # simulate LLM token delay
            yield t

    full_output = tts.speak_streaming(fake_token_generator())
    assert len(full_output) > 0, "Streaming output was empty!"

    print("\n✅ TTS Test Passed!")


if __name__ == "__main__":
    test_tts()

