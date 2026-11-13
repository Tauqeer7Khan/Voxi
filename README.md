# 🎙️✨ Voxi

> **"your voice, your device, your data."**

A fully local, privacy-first AI voice assistant running entirely on Apple Silicon.  
**Zero cloud. Zero cost. Zero data leakage.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Apple Silicon](https://img.shields.io/badge/platform-macOS%20Apple%20Silicon-lightgrey.svg)]()
[![Model: Qwen3.5 4B](https://img.shields.io/badge/LLM-qwen3.5%3A4b-orange.svg)]()
[![Offline First](https://img.shields.io/badge/privacy-100%25%20offline-green.svg)]()

---

## 💡 What is voxi?

**voxi** is an open-source, offline AI voice assistant built for Apple Silicon Macs. It listens to your voice, processes reasoning using a local LLM, and speaks back naturally — all without sending a single byte of voice or text data across the internet.

- **One-liner:** AI voice assistant that runs on your device. Nothing leaves.
- **Pitch:** voxi — your AI voice agent. Zero cloud, zero cost.
- **Logo:** 🎙️✨
- **Repository:** [https://github.com/Tauqeer7Khan/voxi](https://github.com/Tauqeer7Khan/voxi)

---

## ❗ Why voxi?

Mainstream voice assistants (Siri, Alexa, Google) stream your raw voice audio to remote cloud datacenters, creating persistent privacy liabilities and vendor lock-in. Existing open-source alternatives are often fragmented, complex to deploy, or rely on deprecated tools (e.g., Piper TTS, archived Oct 2025).

With modern unified memory architectures on Apple Silicon (M1–M5), running an entire production-grade voice pipeline locally is finally possible with conversational latency under **1.5 seconds**.

---

## 🏗️ Architecture

```text
🎤 MICROPHONE (Browser / macOS Mic)
  │
  ▼
📝 SPEECH-TO-TEXT [faster-whisper "small"]
  ~0.3–0.5s local transcription (CPU/MPS)
  │
  ▼
🧠 LOCAL LLM [Ollama + qwen3.5:4b]
  >31 tokens/sec on Apple Silicon M5
  Streaming token output
  │
  ▼
💬 STREAMING SENTENCE BUFFER
  Punctuation boundary detection (. ! ? : ;)
  │
  ▼
🔊 TEXT-TO-SPEECH [pyttsx3 (Offline) / edge-tts (Neural)]
  Speaks early chunks while LLM is still reasoning
  │
  ▼
🎧 SPEAKER OUTPUT (Sub-1.5s Voice Turnaround)
```

---

## ⚡ Performance Benchmarks (MacBook M5 Air, 24GB RAM)

| Metric | Measured Value | Notes |
|---|---|---|
| **STT Latency** | ~0.3 – 0.5s | `faster-whisper` (small model, ~244MB) |
| **LLM Inference** | **31.6 tokens/sec** | `qwen3.5:4b` with streaming |
| **Time to First Token (TTFT)** | **~0.9s** | Local inference via Ollama |
| **End-to-End Voice Latency** | **~1.2 – 1.5s** | Token-to-speech streaming |
| **RAM Footprint** | **~3.3 GB** | LLM + Whisper combined |
| **Cloud Data Sent** | **0 bytes** | 100% offline execution |

---

## 🛠️ Tech Stack

- **Speech-to-Text:** [OpenAI Whisper](https://github.com/SYSTRAN/faster-whisper) (`faster-whisper`, "small" model)
- **Local LLM:** [Ollama](https://ollama.com/) with `qwen3.5:4b`
- **Text-to-Speech:** 
  - `pyttsx3` (macOS NSSpeechSynthesizer — 100% offline, zero internet)
  - `edge-tts` (Optional neural Indian English voice fallback)
- **Audio Capture & Synthesis:** `sounddevice`, `scipy`, `numpy`
- **UI:** [Gradio](https://gradio.app/) web interface

---

## 🚀 Quick Start

### 1. Prerequisites
- macOS 14+ (Sonoma or later) on Apple Silicon (M1/M2/M3/M4/M5)
- [Homebrew](https://brew.sh/)
- [Ollama](https://ollama.com/)

### 2. Setup Ollama & Model
```bash
# Install and start Ollama
brew install ollama
ollama serve

# In a new terminal, pull the model
ollama pull qwen3.5:4b
```

### 3. Clone & Install
```bash
git clone https://github.com/Tauqeer7Khan/voxi.git
cd voxi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run voxi

#### 🎙️ Voice Mode (Hands-free Mic + Speaker):
```bash
python src/main.py
```
*Speak into your mic. voxi listens, transcribes, thinks, and responds aloud!*

#### 💬 Text Mode (Terminal Chat):
```bash
python src/main.py --text
```

#### 🌐 Web Dashboard (Gradio UI):
```bash
python ui/gradio_app.py
```
*Open http://localhost:7860 in your browser for a full graphical interface with microphone input, chat history, and model switching.*

---

## 📁 Repository Structure

```text
voxi/
├── Status.md                 ← Master project tracking & roadmap
├── README.md                 ← Documentation
├── requirements.txt          ← Python dependencies
├── .env.example              ← Environment template
├── .gitignore                ← Ignored files
│
├── src/
│   ├── main.py               ← Main orchestrator (Voice & Text CLI)
│   ├── config/
│   │   └── settings.py       ← Central configuration
│   ├── stt/
│   │   └── whisper_stt.py    ← Microphone capture & faster-whisper STT
│   ├── llm/
│   │   └── ollama_provider.py← Ollama streaming integration
│   ├── tts/
│   │   └── basic_tts.py      ← Dual-engine streaming speech synthesis
│   └── memory/
│       └── conversation_memory.py ← Multi-turn sliding context
│
├── ui/
│   └── gradio_app.py         ← Web application interface
│
├── tests/
│   ├── test_stt.py           ← Microphone transcription test
│   ├── test_llm.py           ← LLM streaming test suite
│   └── test_tts.py           ← Speech synthesis test
│
└── examples/
    └── basic_assistant.py    ← Simple pipeline demo
```

---

## 🔮 Roadmap

- [x] **Day 1: Full Voice Pipeline** (faster-whisper STT + Ollama LLM + streaming TTS)
- [x] **Day 2: Web Dashboard & Packaging** (Gradio Web UI, documentation, release v1.0.0)
- [ ] **Week 2:** OpenWakeWord trigger ("Hey voxi")
- [ ] **Week 3:** Telephony integration (Twilio + Pipecat for inbound business calls)
- [ ] **Week 4:** Multi-language support (Hindi / Hinglish / Regional Indian languages)
- [ ] **Month 2:** AI Voice Agent as a Service (B2B deployment for local clinics & SMBs)

---

## 👤 Author & License

**Tauqeer Khan**
- GitHub: [@Tauqeer7Khan](https://github.com/Tauqeer7Khan)
- LinkedIn: [linkedin.com/in/tauqeer7khan](https://www.linkedin.com/in/tauqeer7khan/)
- Project Link: [https://github.com/Tauqeer7Khan/voxi](https://github.com/Tauqeer7Khan/voxi)

Licensed under the [MIT License](LICENSE).
