<div align="center">

# 🎙️ Voice-Controlled Local AI Agent

### Speak. It Understands. It Acts.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> A fully voice-driven AI agent that **transcribes speech**, **classifies intent**, **executes local tools**, and displays everything in a clean UI — all powered by Groq's blazing-fast AI.

<br/>

![App Demo](https://img.shields.io/badge/Demo-Watch%20on%20YouTube-red?style=for-the-badge&logo=youtube)

</div>

---
    
## ✨ What It Does

You speak → It listens → It understands → It acts.

| You Say | Agent Does |
|---------|-----------|
| *"Write a Python retry function"* | Generates code → saves to `output/retry.py` |
| *"Create a file called notes.txt"* | Creates file → saves to `output/notes.txt` |
| *"Summarize this: ..."* | Summarizes text → shows result |
| *"What is machine learning?"* | Responds conversationally |

---

## 🖥️ UI Preview

```
┌─────────────────────────────────────────────────────────┐
│  🎙️  Voice AI Agent — Speak. It Understands.            │
├──────────────────────────────────┬──────────────────────┤
│                                  │   Session Log        │
│  01 · Choose Input Method        │                      │
│  ┌──────────┐  ┌──────────────┐  │  #1 · write_code    │
│  │  🎤 Mic  │  │  📁 Upload   │  │  #2 · summarize     │
│  └──────────┘  └──────────────┘  │  #3 · chat          │
│                                  │                      │
│  02 · Record Your Voice          │                      │
│  [🎙️ Click to Record ────────]   │                      │
│                                  │                      │
│  [⚡ Process Audio ───────────]  │                      │
│                                  │                      │
│  03 · Pipeline Results           │                      │
│  📝 Transcribed Text             │                      │
│  🧠 Detected Intent [write_code] │                      │
│  ⚙️  Action Taken                │                      │
│                                  │                      │
│  04 · Final Output (code)        │                      │
└──────────────────────────────────┴──────────────────────┘
```

---

## 🏗️ Architecture

```
🎤 Audio Input (Mic / File Upload)
         │
         ▼
🔤 Speech-to-Text  ──────────────────── Groq Whisper large-v3
         │
         ▼
🧠 Intent Classification ─────────────  Groq LLaMA 3.3 70B
         │
    ┌────┴──────────────────────┐
    ▼         ▼         ▼       ▼
📄 create   💻 write  📋 sum  💬 chat
   file       code    marize
    │         │         │       │
    └────┬────┴─────────┘       │
         ▼                      ▼
    output/ folder         Chat reply
         │
         ▼
    🖥️ Streamlit UI
```

---

## 🌟 Features

- 🎤 **Dual Input** — Live microphone recording or audio file upload (`.wav`, `.mp3`, `.m4a`)
- ⚡ **Blazing Fast STT** — Groq Whisper large-v3 transcribes in under 2 seconds
- 🧠 **Smart Intent Detection** — LLaMA 3.3 70B classifies intent with high accuracy
- 💻 **Code Generation** — Generates clean, commented code and saves to file
- 📄 **File Operations** — Creates files safely inside `output/` sandbox
- 📋 **Text Summarization** — Summarizes any text content
- 💬 **General Chat** — Conversational responses for any query
- 🔗 **Compound Commands** — "Write a retry function and save it to utils.py" — works!
- ✋ **Human-in-the-Loop** — Confirmation prompt before any file operation
- 📜 **Session Memory** — Last 4 turns passed as context to the LLM
- 🛡️ **Safe Sandbox** — All file writes restricted to `output/` folder

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A free [Groq API Key](https://console.groq.com) (takes 2 minutes)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/voice-ai-agent.git
cd voice-ai-agent

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Add your Groq API key inside .env

# 5. Run!
streamlit run app.py
```

Open **http://localhost:8501** in your browser. 🎉

---

## ⚙️ Configuration

Edit your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free key at → [console.groq.com](https://console.groq.com)

---

## 📁 Project Structure

```
voice-ai-agent/
│
├── app.py                  # Streamlit UI (main entry point)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment config template
├── .gitignore
├── README.md
│
├── utils/
│   ├── __init__.py
│   ├── stt.py              # Speech-to-Text (Groq Whisper)
│   ├── intent.py           # Intent Classification (Groq LLaMA)
│   └── tools.py            # Tool Execution (file ops, code gen, chat)
│
└── output/                 # All generated files saved here (sandboxed)
```

---

## 🛡️ Safety & Security

- ✅ All file writes are **sandboxed to `output/`** — no system files touched
- ✅ Path traversal attacks blocked by filename sanitization
- ✅ **Human-in-the-loop** confirmation before any file operation
- ✅ API key stored in `.env` — never hardcoded
- ✅ `.env` is in `.gitignore` — never pushed to GitHub

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `groq` | Whisper STT + LLaMA LLM |
| `python-dotenv` | Environment variable management |

---

## 🧠 Models Used

| Task | Model | Why |
|------|-------|-----|
| Speech-to-Text | `groq/whisper-large-v3` | Fast, accurate, free tier available |
| Intent + Code + Chat | `groq/llama-3.3-70b-versatile` | Powerful, free, runs on Groq cloud |

---

## 💡 Example Voice Commands

```
"Write a bubble sort function in Python"
"Create a file called todo.txt"
"Summarize this: Artificial intelligence is the simulation..."
"What is the difference between RAM and ROM?"
"Write a login system in Python and save it to auth.py"
"Generate a REST API in Python using Flask"
```

---

## 🎯 Bonus Features Implemented

- [x] Compound commands support
- [x] Human-in-the-loop confirmation
- [x] Graceful error handling & fallback
- [x] Session memory (last 4 turns)
- [x] Safe file sandbox

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">



</div>
