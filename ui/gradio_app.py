# ui/gradio_app.py
"""
voxi — Web Dashboard (Gradio UI)
"your voice, your device, your data."
Interactive voice and text interface running 100% locally on Apple Silicon.
"""

import asyncio
import os
import sys
import tempfile
from typing import Optional
import edge_tts
import gradio as gr
import pyttsx3

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config.settings import (
    ASSISTANT_NAME,
    EDGE_TTS_VOICE,
    OLLAMA_MODEL,
    WHISPER_MODEL,
)
from src.llm.ollama_provider import OllamaProvider
from src.memory.conversation_memory import ConversationMemory
from src.stt.whisper_stt import WhisperSTT

# Global singletons for web server
print(f"🚀 Initializing {ASSISTANT_NAME} Web Engine...")
stt: WhisperSTT = WhisperSTT()
llm: OllamaProvider = OllamaProvider()
memory: ConversationMemory = ConversationMemory()
print(f"✨ {ASSISTANT_NAME} Web Engine ready!")


def synthesize_speech(text: str, engine_choice: str) -> Optional[str]:
    """
    Synthesize text to a playable audio file for Gradio audio component.

    Args:
        text: Response text to convert to speech.
        engine_choice: Selected engine ("edge-tts" or "pyttsx3").

    Returns:
        Optional[str]: Filepath to audio file, or None if failed.
    """
    if not text.strip():
        return None

    if "edge-tts" in engine_choice.lower():
        try:
            async def _gen_edge() -> str:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    tmp = f.name
                comm = edge_tts.Communicate(text, EDGE_TTS_VOICE)
                await comm.save(tmp)
                return tmp

            return asyncio.run(_gen_edge())
        except Exception as e:
            print(f"⚠️ edge-tts error: {e}, falling back to pyttsx3")

    # Default to pyttsx3 (100% offline macOS NSSpeechSynthesizer)
    try:
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f:
            tmp_path = f.name
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 0.9)
        for v in engine.getProperty("voices"):
            if "Samantha" in v.name or "Samantha" in v.id:
                engine.setProperty("voice", v.id)
                break
        engine.save_to_file(text, tmp_path)
        engine.runAndWait()
        return tmp_path
    except Exception as e:
        print(f"❌ TTS synthesis failed: {e}")
        return None


def handle_text_chat(
    user_message: str, history: Optional[list[dict[str, str]]], model_choice: str, tts_choice: str
) -> tuple[list[dict[str, str]], Optional[str], str]:
    """
    Process typed text input from user.

    Args:
        user_message: Input text from textbox.
        history: Current conversation history.
        model_choice: Chosen Ollama model.
        tts_choice: Chosen TTS engine.

    Returns:
        tuple: (Updated history, Audio filepath, Reset textbox string)
    """
    if not user_message or not user_message.strip():
        return history or [], None, ""

    llm.model = model_choice
    chat_history: list[dict[str, str]] = history or []

    chat_history.append({"role": "user", "content": user_message})
    memory.add_user_message(user_message)

    assistant_response = llm.generate(user_message, history=memory.get_history())
    memory.add_assistant_message(assistant_response)

    chat_history.append({"role": "assistant", "content": assistant_response})
    audio_path = synthesize_speech(assistant_response, tts_choice)

    return chat_history, audio_path, ""


def handle_audio_chat(
    audio_filepath: Optional[str], history: Optional[list[dict[str, str]]], model_choice: str, tts_choice: str
) -> tuple[list[dict[str, str]], Optional[str], None]:
    """
    Transcribe audio from microphone and process conversation.

    Args:
        audio_filepath: Temporary path to recorded audio.
        history: Current conversation history.
        model_choice: Chosen Ollama model.
        tts_choice: Chosen TTS engine.

    Returns:
        tuple: (Updated history, Audio filepath, Reset audio input)
    """
    if not audio_filepath or not os.path.exists(audio_filepath):
        return history or [], None, None

    llm.model = model_choice
    chat_history: list[dict[str, str]] = history or []

    try:
        segments, _ = stt.model.transcribe(
            audio_filepath,
            beam_size=5,
            language="en",
            vad_filter=True
        )
        transcribed_text = " ".join([seg.text for seg in segments]).strip()
    except Exception as e:
        transcribed_text = f"Error transcribing audio: {e}"

    if not transcribed_text:
        return chat_history, None, None

    chat_history.append({"role": "user", "content": f"🎤 {transcribed_text}"})
    memory.add_user_message(transcribed_text)

    assistant_response = llm.generate(transcribed_text, history=memory.get_history())
    memory.add_assistant_message(assistant_response)

    chat_history.append({"role": "assistant", "content": assistant_response})
    audio_path = synthesize_speech(assistant_response, tts_choice)

    return chat_history, audio_path, None


def clear_chat() -> tuple[list[dict[str, str]], None]:
    """
    Reset conversation history and memory.

    Returns:
        tuple: (Empty history list, None audio path)
    """
    memory.clear()
    return [], None


CUSTOM_CSS = """
.voxi-header {
    text-align: center;
    padding: 1.5rem 0;
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.voxi-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
}
.voxi-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-top: 0.3rem;
    font-style: italic;
}
.voxi-badge {
    display: inline-block;
    background: #22c55e;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 0.5rem;
}
"""


def build_app() -> gr.Blocks:
    """
    Construct the Gradio Blocks user interface.

    Returns:
        gr.Blocks: Compiled Gradio app.
    """
    with gr.Blocks(title=f"{ASSISTANT_NAME} — your voice, your device, your data.", css=CUSTOM_CSS) as demo:
        gr.HTML(
            f"""
            <div class="voxi-header">
                <div class="voxi-title">🎙️✨ {ASSISTANT_NAME}</div>
                <div class="voxi-subtitle">"your voice, your device, your data."</div>
                <span class="voxi-badge">100% LOCAL • ZERO CLOUD • APPLE SILICON</span>
            </div>
            """
        )

        with gr.Row():
            # Left Column: Configuration Controls
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Engine Settings")

                model_dropdown = gr.Dropdown(
                    choices=["qwen3.5:4b", "qwen3.5:9b", "llama3.2:3b", "qwen2.5:7b"],
                    value=OLLAMA_MODEL,
                    label="🧠 Local LLM Brain",
                    interactive=True
                )

                tts_dropdown = gr.Dropdown(
                    choices=["pyttsx3 (100% Offline)", "edge-tts (Neural Indian English)"],
                    value="pyttsx3 (100% Offline)",
                    label="🔊 Speech Synthesis Engine",
                    interactive=True
                )

                clear_btn = gr.Button("🗑️ Clear Conversation", variant="secondary")

                gr.Markdown(
                    f"""
                    ---
                    **System Architecture:**
                    - **STT:** `faster-whisper` ({WHISPER_MODEL})
                    - **LLM Speed:** ~31 tokens/sec
                    - **Latency Target:** < 1.5 seconds
                    - **Privacy:** 100% on-device
                    """
                )

            # Right Column: Chat & Audio Interaction
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=450
                )

                spoken_audio = gr.Audio(
                    label=f"🔊 {ASSISTANT_NAME} Spoken Response",
                    type="filepath",
                    autoplay=True,
                    interactive=False
                )

                with gr.Tab("🎙️ Voice Mode"):
                    mic_input = gr.Audio(
                        sources=["microphone"],
                        type="filepath",
                        label="Click to record your voice, then click Stop to send"
                    )

                with gr.Tab("💬 Text Mode"):
                    with gr.Row():
                        text_input = gr.Textbox(
                            placeholder=f"Type a message to {ASSISTANT_NAME} and hit Enter...",
                            label="Message",
                            lines=1,
                            scale=4
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)

        # Wire text events
        text_input.submit(
            handle_text_chat,
            inputs=[text_input, chatbot, model_dropdown, tts_dropdown],
            outputs=[chatbot, spoken_audio, text_input]
        )
        send_btn.click(
            handle_text_chat,
            inputs=[text_input, chatbot, model_dropdown, tts_dropdown],
            outputs=[chatbot, spoken_audio, text_input]
        )

        # Wire mic events
        mic_input.change(
            handle_audio_chat,
            inputs=[mic_input, chatbot, model_dropdown, tts_dropdown],
            outputs=[chatbot, spoken_audio, mic_input]
        )

        # Wire clear button
        clear_btn.click(
            clear_chat,
            inputs=[],
            outputs=[chatbot, spoken_audio]
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch(server_name="127.0.0.1", server_port=7860, inbrowser=False)
