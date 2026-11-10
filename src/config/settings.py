# src/config/settings.py
"""
voxi — Central Configuration
All settings in one place. Change here, affects everywhere.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# MODEL SETTINGS
# ============================================
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "small")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ============================================
# AUDIO SETTINGS
# ============================================
SAMPLE_RATE: int = 16000                # 16kHz — required by Whisper
CHANNELS: int = 1                       # Mono channel
SILENCE_THRESHOLD: float = 0.01         # RMS volume below this = silence
SILENCE_DURATION: float = 2.0           # Seconds of silence before stopping

# ============================================
# ASSISTANT SETTINGS
# ============================================
ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "voxi")
MAX_CONVERSATION_HISTORY: int = 10      # Maximum conversation turns retained

# ============================================
# TTS SETTINGS
# ============================================
TTS_ENGINE: str = os.getenv("TTS_ENGINE", "pyttsx3")
EDGE_TTS_VOICE: str = os.getenv("EDGE_TTS_VOICE", "en-IN-NeerjaNeural")

# ============================================
# SYSTEM PROMPT
# ============================================
SYSTEM_PROMPT: str = f"""You are {ASSISTANT_NAME}, a helpful, intelligent, and concise AI voice assistant.

RULES:
1. Keep responses SHORT — you are speaking, not writing
2. No bullet points, no markdown, no lists, no formatting
3. Speak naturally like a human in conversation
4. If asked something you don't know, say so honestly
5. Be warm, helpful, and slightly witty
6. Maximum 3-4 sentences per response unless user asks for detail
7. Never say "as an AI" or "as a language model"
"""
