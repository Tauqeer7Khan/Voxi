"""
voxi — Basic Interactive Demo (STT + LLM)
Listens to voice input, transcribes with Whisper, and streams response from Ollama.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.stt.whisper_stt import WhisperSTT
from src.llm.ollama_provider import OllamaProvider
from src.memory.conversation_memory import ConversationMemory


def main():
    print("=" * 50)
    print("  🎙️✨ voxi — STT + LLM Interactive Demo")
    print("  Say 'quit', 'exit', or press Ctrl+C to stop")
    print("=" * 50)

    # Initialize modules
    stt = WhisperSTT()
    llm = OllamaProvider()
    memory = ConversationMemory()

    print("\n✅ All systems ready! Start speaking...")

    while True:
        try:
            # 1. Listen and transcribe
            user_text = stt.listen_and_transcribe()

            if not user_text:
                continue

            # Check exit commands
            if user_text.lower() in ["exit", "quit", "exit.", "quit.", "goodbye", "goodbye."]:
                print("\n👋 Goodbye!")
                break

            # 2. Add to conversation memory
            memory.add_user_message(user_text)

            # 3. Stream response from local LLM
            print("\n🧠 Aria: ", end="", flush=True)
            full_response = ""

            for token in llm.generate_stream(user_text, history=memory.get_history()):
                print(token, end="", flush=True)
                full_response += token
            print("\n")

            # 4. Save response to memory
            memory.add_assistant_message(full_response.strip())

        except KeyboardInterrupt:
            print("\n\n⏹️  Session ended by user.")
            break


if __name__ == "__main__":
    main()

