# 🎙️✨ voxi — Master Project Status File

> **"your voice, your device, your data."**  
> **Last Updated:** 2026-11-11  
> **Status:** 🟡 IN PROGRESS — Phase 1 Complete (100%), Phase 2 Starting  
> **Plan:** 2-Day Build in Public Challenge 🔥

---

## 🧠 WHAT IS VOXI?

voxi is a fully local, privacy-first AI Voice Assistant that runs entirely on a MacBook M5 Air (24GB). It listens to your voice, understands what you said using a local LLM, and speaks back — all without sending a single byte of data to the cloud.

- **One-liner:** AI voice assistant that runs on your device. Nothing leaves.
- **Tagline:** "your voice, your device, your data."
- **Logo:** 🎙️✨

**Dual Purpose:**
1. **Academic/Portfolio:** 4th Year Engineering College Project + 2-Day Build in Public Challenge for GitHub & LinkedIn
2. **Future Business:** Scale into "AI Voice Agent as a Service" — sell to dental clinics, restaurants, real estate agents, small businesses

---

## ❗ THE CORE PROBLEM (Why voxi Was Built)

Most AI voice assistants (Siri, Alexa, Google) send your voice data to cloud servers. This raises massive privacy concerns. Existing open-source alternatives are fragmented — you need to stitch together STT, LLM, and TTS yourself, and most tutorials are outdated or use dead tools (like Piper TTS, archived Oct 2025).

**The journey:**
1. Wanted a voice assistant that respects privacy — no data leaving the device
2. Researched existing solutions:
   - **Siri / Alexa / Google:** Cloud-dependent, privacy nightmare
   - **Open Interpreter:** Great but cloud LLM by default
   - **Home Assistant + Wyoming:** Too complex for a quick build
   - **Most GitHub projects:** Use dead tools (Piper TTS), outdated models, or require cloud APIs
3. Realized: With Apple Silicon (M5 Air, 24GB), running a full AI pipeline locally is **NOW** possible
4. Decision: Build a modular, clean, privacy-first voice assistant from scratch — and document the entire journey publicly

> **The builder is a 4th Year Engineering Student** — this project serves as both a college project AND a portfolio piece for recruiters, AND the foundation for a future SaaS business.

---

## 👤 PROJECT OWNER

- **Builder:** Tauqeer Khan
- **GitHub:** https://github.com/Tauqeer7Khan
- **LinkedIn:** https://www.linkedin.com/in/tauqeer7khan/
- **Repo Name:** voxi
- **GitHub Repo:** https://github.com/Tauqeer7Khan/voxi
- **License:** MIT

---

## 🛠️ TECH STACK

### Current Stack (FREE / LOCAL — 2-Day Challenge)

| Component | Tool | Details | Cost |
|---|---|---|---|
| Speech-to-Text | OpenAI Whisper (faster-whisper) | Local, "small" model (~244MB), ~0.3-0.5s transcription | FREE |
| LLM Brain | Ollama + Qwen3.5:4b | 4B params, ~50+ tok/s on M5, Q4_K_M quantization | FREE |
| Text-to-Speech | Kokoro TTS (primary) / pyttsx3 (fallback) | Kokoro = natural offline voices; pyttsx3 = macOS NSSpeechSynthesizer | FREE |
| Orchestration | Python 3.11+ | Custom pipeline with streaming | FREE |
| UI | Gradio | Web-based chat + mic interface | FREE |
| Package Manager | Homebrew | All system dependencies | FREE |

### Future Paid Stack (Business Version)

| Component | Tool | Cost |
|---|---|---|
| STT | Deepgram | $0.0043/min |
| LLM | GPT-4o-mini / Gemini Flash | ~$0.002/call |
| TTS | ElevenLabs | from $5/month |
| Telephony | Twilio | $0.01/min + $1.15/mo |
| Orchestration | Pipecat (Open Source) | FREE |

**Business Economics:**
- **My cost:** ~$0.035/min
- **Charge clients:** $0.15–0.25/min
- **Profit margin:** 75–85%

---

## 💻 SYSTEM REQUIREMENTS

- macOS 14+ (Sonoma or later)
- Apple Silicon Mac — M1 / M2 / M3 / M4 / M5 (M5 Air used for development)
- Minimum 16GB RAM (24GB recommended — M5 Air 24GB is the dev machine)
- ~10 GB free disk space (models + dependencies)
- Internet — only for initial setup (brew, pip, model pulls); after that fully offline
- Microphone — built-in MacBook mic works fine

### Performance Benchmarks (MacBook M5 Air 24GB)

| Metric | Value |
|---|---|
| LLM Speed (qwen3.5:4b) | ~50+ tokens/second |
| LLM Speed (llama3.2:3b) | ~45 tokens/second |
| LLM Speed (gemma3:12b) | ~17 tokens/second |
| Whisper Transcription | ~0.3–0.5 seconds |
| End-to-End Latency | ~1.2–1.5 seconds (with streaming) |
| RAM Usage (qwen3.5:4b) | ~3.3GB |
| Thermal Throttle | After 30+ min continuous (fanless M5 Air) |

---

## 📁 COMPLETE FILE STRUCTURE

```text
voxi/
│
├── Status.md                 ← THIS FILE — Master project status
├── README.md                 ← Public-facing documentation
├── LICENSE                   ← MIT License
├── requirements.txt          ← Python dependencies
├── setup.py                  ← Package setup
├── .env.example              ← Environment variables template
├── .gitignore                ← Ignores venv/, models/, audio files
│
├── docs/
│   ├── architecture.md       ← Technical architecture doc
│   ├── CONTRIBUTING.md       ← How to contribute
│   └── images/
│       └── architecture-diagram.png
│
├── src/
│   ├── __init__.py
│   ├── main.py               ← Entry point (voice mode + text mode)
│   │
│   ├── stt/
│   │   ├── __init__.py
│   │   └── whisper_stt.py    ← Speech-to-Text module (faster-whisper)
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── ollama_provider.py   ← Local LLM (FREE)
│   │   └── openai_provider.py   ← Paid LLM (future business)
│   │
│   ├── tts/
│   │   ├── __init__.py
│   │   ├── kokoro_tts.py        ← Recommended TTS (natural, offline)
│   │   ├── pyttsx3_tts.py       ← Basic offline TTS (macOS built-in)
│   │   └── elevenlabs_tts.py    ← Paid TTS (future business)
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── conversation_memory.py  ← Multi-turn context management
│   │
│   ├── telephony/             ← Future business version
│   │   ├── __init__.py
│   │   └── twilio_handler.py
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py        ← All configuration in one place
│
├── ui/
│   └── gradio_app.py          ← Web UI (Gradio)
│
├── tests/
│   ├── test_stt.py
│   ├── test_llm.py
│   └── test_tts.py
│
├── examples/
│   ├── basic_assistant.py     ← Simple demo script
│   └── phone_agent.py         ← Future telephony demo
│
└── venv/                      ← Python virtual environment (gitignored)
```

---

## 🏗️ SYSTEM ARCHITECTURE

### Free/Local Version (Current)

```text
🎤 MICROPHONE
  ↓
📝 WHISPER STT (faster-whisper, local, "small" model)
  Transcribes speech → text (~0.3-0.5s)
  ↓
🧠 OLLAMA LLM (Qwen3.5:4b, local, ~50+ tok/s)
  Processes text → generates response
  STREAMING: tokens sent as they arrive
  ↓
💬 RESPONSE (streamed token by token)
  Sentence boundaries detected → sent to TTS immediately
  ↓
🔊 TTS ENGINE (Kokoro TTS / pyttsx3, local)
  Converts text → speech audio
  ↓
🎧 SPEAKER OUTPUT
  User hears the response (~1.2-1.5s total latency)
```

### Future Paid/Business Version

```text
📞 TWILIO (inbound phone call)
  ↓
🔊 DEEPGRAM STT ($0.0043/min)
  ↓
🧠 GPT-4o-mini / GEMINI FLASH
  ↓
🤔 DECISION: Important call?
    YES → Transfer to human
    NO  → AI handles fully
  ↓
🔈 ELEVENLABS TTS (natural voice)
  ↓
📞 TWILIO (speak back to caller)
```

**Orchestration:** Pipecat (Open Source, FREE)

---

## 🗺️ FULL ROADMAP — ALL PHASES

### PHASE 1 — Day 1: Full Voice Pipeline (STT + LLM + TTS)
- **Goal:** Mic → Whisper STT → Ollama LLM → TTS → Speaker — complete loop working
- **Estimated Time:** 8–10 hours
- **Status:** ✅ COMPLETE

**Tasks:**
- [x] Install Ollama via Homebrew (`brew install ollama`)
- [x] Pull initial model (`ollama pull llama3.2:3b` then `qwen3.5:4b`)
- [x] Create project directory structure
- [x] Setup Python virtual environment
- [x] Install dependencies (`faster-whisper`, `sounddevice`, `scipy`, `numpy`, `requests`, `python-dotenv`)
- [x] Create `src/config/settings.py` with all configuration
- [x] Build `src/stt/whisper_stt.py` — mic capture + silence detection + transcription
- [x] Build `src/llm/ollama_provider.py` — local LLM calls with streaming
- [x] Build `src/memory/conversation_memory.py` — multi-turn context
- [x] Install TTS dependencies (`pyttsx3`, `edge-tts`)
- [x] Build `src/tts/basic_tts.py` — pyttsx3 + edge-tts dual engine
- [x] Implement streaming TTS (speak as LLM tokens arrive)
- [x] Build `src/main.py` — VoiceAssistant class with voice + text modes
- [x] Test STT pipeline end-to-end (speak → transcribe → print)
- [x] Test LLM pipeline (text → response → print)
- [x] Test TTS pipeline (blocking + streaming speech)
- [x] Test full voice loop: speak → transcribe → think → speak back
- [ ] Create GitHub repo "voxi"
- [ ] First commit and push
- [ ] LinkedIn Day 1 post

---

### PHASE 2 — Day 2: UI + Polish + Ship
- **Goal:** Gradio UI + Demo Video + Final GitHub + LinkedIn Showcase
- **Estimated Time:** 6–8 hours
- **Status:** 🟡 IN PROGRESS

**Tasks:**
- [x] Install Gradio (`pip install gradio`)
- [x] Build `ui/gradio_app.py` — web interface with mic + text input
- [x] Add model selection dropdown
- [x] Add conversation history display
- [x] Add real-time transcription display
- [x] Polish codebase (comments, error handling, clean structure)
- [x] Update `requirements.txt`
- [x] Write comprehensive `README.md`
- [x] Create architecture diagram
- [ ] Record demo video (60–90 sec, show offline working)
- [ ] Final GitHub push + create Release v1.0.0
- [ ] LinkedIn Day 2 showcase post with demo video

---

### PHASE 3 — Week 2: Polish + Documentation
- **Goal:** Professional-grade repo ready for recruiters
- **Estimated Time:** 3–4 hours
- **Status:** ⬜ NOT STARTED

**Tasks:**
- [ ] Add `docs/architecture.md`
- [ ] Add `docs/CONTRIBUTING.md`
- [ ] Add `setup.py` for pip-installable package
- [ ] Add unit tests (`tests/test_stt.py`, `test_llm.py`, `test_tts.py`)
- [ ] Add `.env.example` with all config options
- [ ] Performance benchmarks in README

---

### PHASE 4 — Week 3: Phone Call Capability
- **Goal:** Handle real phone calls via Twilio
- **Estimated Time:** 4–6 hours
- **Status:** ⬜ NOT STARTED  
- **Cost:** ~$5/month

**Tasks:**
- [ ] Install Pipecat (`pip install pipecat-ai`)
- [ ] Install Twilio (`pip install twilio`)
- [ ] Get Twilio account + phone number
- [ ] Build `src/telephony/twilio_handler.py`
- [ ] Setup call forwarding: Phone → Twilio → AI Agent
- [ ] Implement human transfer for important calls
- [ ] Test end-to-end phone call

---

### PHASE 5 — Week 4: Premium APIs
- **Goal:** Upgrade to paid APIs for business-grade quality
- **Estimated Time:** 3–4 hours
- **Status:** ⬜ NOT STARTED  
- **Cost:** ~$15/month

**Tasks:**
- [ ] Integrate Deepgram STT (`src/stt/deepgram_stt.py`)
- [ ] Integrate ElevenLabs TTS (`src/tts/elevenlabs_tts.py`)
- [ ] Integrate GPT-4o-mini (`src/llm/openai_provider.py`)
- [ ] Config-based switching (free ↔ paid via `.env`)
- [ ] Test quality difference

---

### PHASE 6 — Month 2: First Client
- **Goal:** Pitch and onboard first business client
- **Estimated Time:** Ongoing
- **Status:** ⬜ NOT STARTED

**Tasks:**
- [ ] Cold outreach to 10 local businesses
- [ ] Offer 1-week free trial
- [ ] Get testimonial
- [ ] Setup billing (Stripe or manual)
- [ ] Monitor costs vs revenue

---

### PHASE 7 — Month 3–4: Scale
- **Goal:** 5 clients, $1,000–1,825/month revenue
- **Status:** ⬜ NOT STARTED

**Tasks:**
- [ ] Scale to 5 clients
- [ ] Implement analytics dashboard
- [ ] Add multi-language support (Hindi/Hinglish)
- [ ] Hire VA for client management (optional)

---

## 📊 OVERALL PROGRESS TRACKER

| Phase | Name | Status | % Done |
|---|---|---|---|
| Planning | Full roadmap + tech stack + business plan | ✅ Complete | 100% |
| Phase 1 | Day 1: Full Voice Pipeline (STT + LLM + TTS) | ✅ Complete | 100% |
| Phase 2 | Day 2: UI + Polish + Ship | 🟡 In Progress | 0% |
| Phase 3 | Week 2: Documentation + Tests | ⬜ Not Started | 0% |
| Phase 4 | Week 3: Phone Calls (Twilio) | ⬜ Not Started | 0% |
| Phase 5 | Week 4: Premium APIs | ⬜ Not Started | 0% |
| Phase 6 | Month 2: First Client | ⬜ Not Started | 0% |
| Phase 7 | Month 3–4: Scale to 5 Clients | ⬜ Not Started | 0% |
| **TOTAL** | | 🟡 **In Progress** | **~50%** |

**Status Key:**
- ⬜ Not Started
- 🟡 In Progress
- ✅ Complete
- ❌ Blocked

---

## 🎯 CURRENT NEXT STEP

`→ PHASE 1 COMPLETE / STARTING PHASE 2: Day 2 — UI + Polish + Ship`

**Immediate next commands:**
1. `pip install gradio` → install web UI dependencies
2. Build `ui/gradio_app.py` → web interface with mic & text chat
3. Write `README.md` with architecture, quickstart & benchmarks
4. Record demo video showing offline operation
5. Final GitHub push + create Release v1.0.0
6. LinkedIn Day 2 showcase post

---

## 📅 2-DAY EXECUTION PLAN

> **Goal:** Build a working AI voice assistant, push to GitHub, post on LinkedIn — in 2 days.  
> **Estimated total time:** 12–16 hours of focused work.

| Day | Time Block | Phase | Tasks | Status |
|---|---|---|---|---|
| Pre | Night Before | Setup | GitHub repo + Pre-challenge LinkedIn post | ⬜ |
| Day 1 | Morning | Phase 1 | Environment + Whisper STT + Ollama LLM | ✅ |
| Day 1 | Afternoon | Phase 1 | TTS + Full voice pipeline | 🟡 |
| Day 1 | Evening | Phase 1 | GitHub commit + LinkedIn Day 1 | ⬜ |
| Day 2 | Morning | Phase 2 | Gradio UI | ⬜ |
| Day 2 | Afternoon | Phase 2 | README + Demo video | ⬜ |
| Day 2 | Evening | Phase 2 | Final push + Big LinkedIn post | ⬜ |

**End of Day 2 Goal:**
- ✅ voxi fully working locally on Mac
- ✅ Full pipeline: Mic → Whisper → Ollama → TTS → Speaker
- ✅ Gradio web UI running
- ✅ Repo live on GitHub (public, professional)
- ✅ Demo video recorded and posted
- ✅ 3 LinkedIn posts published (Pre-challenge, Day 1, Day 2)
- ✅ 4th year project ready for showcase

---

## 🚨 KNOWN RISKS & GOTCHAS

- **PIPER TTS IS DEAD:** Piper was archived October 2025. Many old tutorials still recommend it. DO NOT use Piper. Use Kokoro TTS or Coqui XTTS instead.
- **THERMAL THROTTLING:** MacBook Air M5 is fanless. Sessions under 10–15 min are fine. 30+ min continuous load may throttle. Solution for business: use cloud APIs.
- **LATENCY IS KING:** In voice AI, 2+ seconds delay feels broken. ALWAYS implement streaming — feed TTS as LLM tokens arrive. Target: under 1.5s end-to-end.
- **macOS MICROPHONE PERMISSIONS:** Terminal and any app using the mic needs Microphone permission in System Settings → Privacy & Security. First run will prompt — don't deny it.
- **WHISPER MODEL DOWNLOAD:** First time running faster-whisper, it downloads the model (~244MB for "small"). Needs internet for this one-time download.
- **OLLAMA MUST BE RUNNING:** The Ollama server (`ollama serve`) must be running in a separate terminal before the Python code can call it. Common mistake: forgetting to start it.
- **RAM MANAGEMENT:** `qwen3.5:4b` uses ~3.3GB RAM. `gemma3:12b` uses ~9.5GB. With 24GB total, both fit comfortably, but don't run both simultaneously with Whisper.
- **CONCURRENT CALLS (LOCAL):** Local Mac handles 1–3 concurrent calls max. For business with multiple calls → cloud APIs needed.
- **TELEPHONY ALWAYS COSTS:** No free way to handle real phone calls. Twilio minimum: $1.15/month + $0.01/min. Everything else CAN be free.
- **HINDI/HINGLISH SUPPORT:** Whisper handles Hindi decently but Deepgram/Google STT is better for heavy Hindi. For Indian business clients, paid STT may be needed.

---

## 🔮 FUTURE ROADMAP / UPGRADES

### Post v1.0 Ideas
- [ ] Wake Word Detection: "Hey Aria" trigger using openwakeword library
- [ ] Kokoro TTS Integration: Replace pyttsx3 with Kokoro for natural-sounding offline voices
- [ ] Phone Call Handling: Twilio + Pipecat for real business phone calls
- [ ] Business Dashboard: Analytics, call logs, client management
- [ ] Multi-Language Support: Hindi, Hinglish, Tamil, Telugu for Indian market
- [ ] CRM Integration: HubSpot/Salesforce for lead qualification
- [ ] Custom Voice Cloning: ElevenLabs voice cloning for brand-specific voices
- [ ] Mobile App: React Native companion app for monitoring
- [ ] HIPAA Compliance: For medical/dental clients
- [ ] Call Recording + Transcription Logs: With consent management

### Free → Paid Code Transition (Key Design Principle)
Code is modular so switching is just a config change:

```python
# FREE (Academic):
STT = WhisperSTT(model="small")
LLM = OllamaProvider(model="qwen3.5:4b")
TTS = KokoroTTS()

# PAID (Business):
STT = DeepgramSTT(api_key=KEY)
LLM = OpenAIProvider(model="gpt-4o-mini", api_key=KEY)
TTS = ElevenLabsTTS(api_key=KEY, voice_id=ID)
```

No restructuring needed — just swap providers!

---

## 📝 NOTES FOR AI ASSISTANTS READING THIS FILE

If you are an AI reading this file to help with development:

1. The project is called voxi — always lowercase, not VoiceForge, not anything else.
2. The core pipeline is: Mic → Whisper STT → Ollama LLM → TTS → Speaker
3. The code MUST be modular — each component (STT, LLM, TTS) is a separate class that can be swapped independently. This is critical for both academic showcase AND future business scaling.
4. DO NOT recommend Piper TTS — it is archived/dead since October 2025. Use Kokoro TTS or Coqui XTTS.
5. Everything must run locally for the 2-day challenge — no cloud APIs, no external calls except initial model downloads.
6. The builder's machine: MacBook M5 Air, 24GB RAM, 1TB Storage, 10-Core CPU/GPU. Optimize for this hardware.
7. Primary communication language: Hinglish (Hindi + English mixed).
8. Check the Progress Tracker above to know what is done and what needs to be done next before suggesting or making changes.
9. When a phase is completed, update the status in the Progress Tracker and add the completion date.
10. The builder is a 4th year engineering student — explain things step by step, don't skip details.
11. Streaming responses are CRITICAL for latency. Always feed TTS as LLM tokens arrive, never wait for full response.
12. The business plan is real — code architecture must support easy transition from free to paid components.
13. This file should be updated every time work is done on voxi. Update the status emoji, % done, and check off completed tasks.

> **"your voice, your device, your data."** 🎙️✨

---

## 📋 CHANGE LOG

### 2026-11-11 — REBRAND TO VOXI
- 🔄 Project renamed: VoiceForge AI → voxi
- 🏷️ New tagline: "your voice, your device, your data."
- 🎨 Brand identity: 🎙️✨
- 🔗 GitHub repo URL updated: https://github.com/Tauqeer7Khan/voxi

### 2026-11-11 — DAY 1 COMPLETE & DAY 2 INITIATED
- 🔄 Changed from 3-day to 2-day build challenge
- ✅ Phase 1 (STT + LLM) complete
- ✅ Phase 1 (TTS) complete — full voice pipeline working
- 🟡 Phase 2 (Day 2: UI + Polish + Ship) started

### 2026-11-12 — DAY 2: TTS & FULL VOICE PIPELINE
- ✅ Installed TTS dependencies (pyttsx3, edge-tts)
- ✅ Built src/tts/basic_tts.py with dual engine support (offline pyttsx3 + neural edge-tts)
- ✅ Implemented low-latency streaming TTS with sentence boundary detection
- ✅ Built src/main.py (VoiceAssistant supporting both voice mode and text mode)
- ✅ Created tests/test_tts.py for verifying blocking & streaming speech synthesis
- 🟡 Phase 2 Day 2 in progress (ready for showcase & git push)

### 2026-11-11 — PROJECT INITIATED
- ✅ Full planning complete — roadmap, tech stack, business plan defined
- ✅ Status.md created — master project status file
- 🟡 Phase 1 starting — Day 1 Foundation (STT + LLM)
- 🎯 2-Day Build in Public Challenge begins

