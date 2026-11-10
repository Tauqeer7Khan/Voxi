# tests/test_llm.py
"""Test Ollama LLM integration."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.llm.ollama_provider import OllamaProvider
from src.memory.conversation_memory import ConversationMemory


def test_llm():
    print("=" * 40)
    print("  🎙️✨ voxi — LLM Test")
    print("=" * 40)

    llm = OllamaProvider()
    memory = ConversationMemory()

    # Test 1: Basic non-streaming response
    print("\n📋 Test 1: Non-streaming response")
    response = llm.generate("Say hello in one sentence.")
    print(f"   Response: {response}")
    assert len(response) > 0, "Empty response!"
    print("   ✅ Non-streaming OK")

    # Test 2: Streaming response
    print("\n📋 Test 2: Streaming response")
    print("   Response: ", end="", flush=True)
    full_response = ""
    for token in llm.generate_stream("What is 2 + 2? Answer in one word."):
        print(token, end="", flush=True)
        full_response += token
    print()
    assert len(full_response) > 0, "Empty streaming response!"
    print("   ✅ Streaming OK")

    # Test 3: Memory integration
    print("\n📋 Test 3: Conversation memory")
    memory.add_user_message("My name is Ronin")
    memory.add_assistant_message("Nice to meet you, Ronin!")
    memory.add_user_message("What is my name?")
    response = llm.generate(
        "What is my name?",
        history=memory.get_history()
    )
    print(f"   Response: {response}")
    print("   ✅ Memory OK")

    print("\n🎉 All LLM tests PASSED!")


if __name__ == "__main__":
    test_llm()

