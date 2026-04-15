# Tool Execution utility — uses Groq LLM for code gen, summarize, chat.
# All file writes restricted to output/ folder.

import os
import re
import logging
from pathlib import Path
from datetime import datetime
from groq import Groq

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"


def execute_tool(intent_data: dict, transcript: str) -> dict:
    intent = (intent_data.get("intent") or "chat").lower()

    if intent == "create_file":
        return _create_file(intent_data)
    elif intent == "write_code":
        return _write_code(intent_data, transcript)
    elif intent == "summarize":
        return _summarize(intent_data, transcript)
    else:
        return _chat(transcript)


# ── Create File ───────────────────────────────────────────────────────────────
def _create_file(intent_data: dict) -> dict:
    filename = _safe_filename(intent_data.get("filename") or "new_file.txt")
    filepath = OUTPUT_DIR / filename
    content = intent_data.get("content_hint") or f"# Created by Voice AI Agent\n# {datetime.now()}\n"

    try:
        filepath.write_text(content, encoding="utf-8")
        return {
            "action": f"Created file: output/{filename}",
            "output": f"File `output/{filename}` created successfully.\n\nContent:\n{content}",
        }
    except Exception as e:
        return {"action": "File creation failed", "output": f"Error: {e}"}


# ── Write Code ────────────────────────────────────────────────────────────────
def _write_code(intent_data: dict, transcript: str) -> dict:
    language = (intent_data.get("language") or "python").lower()
    ext = _lang_to_ext(language)
    filename = _safe_filename(intent_data.get("filename") or f"generated_code{ext}")
    if not filename.endswith(ext):
        filename = filename.rsplit(".", 1)[0] + ext
    filepath = OUTPUT_DIR / filename

    code = _groq_call(
        f"Write clean, well-commented {language} code for:\n\n"
        f"{intent_data.get('content_hint') or transcript}\n\n"
        "Return ONLY the code. No explanations, no markdown fences."
    )
    
    code = re.sub(r"```(?:\w+)?\n?", "", code).strip().rstrip("`").strip()

    try:
        filepath.write_text(code, encoding="utf-8")
        return {
            "action": f"Generated and saved: output/{filename}",
            "output": code,
        }
    except Exception as e:
        return {"action": "Code write failed", "output": f"Error: {e}"}


# ── Summarize ─────────────────────────────────────────────────────────────────
def _summarize(intent_data: dict, transcript: str) -> dict:
    content = intent_data.get("content_hint") or transcript
    summary = _groq_call(f"Summarize the following text concisely:\n\n{content}")

    saved_msg = ""
    filename = intent_data.get("filename")
    if filename:
        safe = _safe_filename(filename)
        (OUTPUT_DIR / safe).write_text(summary, encoding="utf-8")
        saved_msg = f"\n\nSummary saved to `output/{safe}`"

    return {
        "action": f"Summarized text{(' → saved to output/' + filename) if filename else ''}",
        "output": summary + saved_msg,
    }


# ── Chat ──────────────────────────────────────────────────────────────────────
def _chat(transcript: str) -> dict:
    reply = _groq_call(transcript)
    return {"action": "Responded via chat", "output": reply}


# ── Groq API call ─────────────────────────────────────────────────────────────
def _groq_call(prompt: str) -> str:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq call failed: {e}")
        return f"Error: Could not get response from Groq. {e}"


# ── Helpers ───────────────────────────────────────────────────────────────────
def _safe_filename(name: str) -> str:
    name = os.path.basename(name)
    name = re.sub(r"[^\w.\-]", "_", name)
    return name or "output.txt"


def _lang_to_ext(language: str) -> str:
    mapping = {
        "python": ".py", "javascript": ".js", "typescript": ".ts",
        "java": ".java", "c": ".c", "cpp": ".cpp", "c++": ".cpp",
        "go": ".go", "rust": ".rs", "ruby": ".rb", "bash": ".sh",
        "shell": ".sh", "html": ".html", "css": ".css", "sql": ".sql",
    }
    return mapping.get(language.lower(), ".txt")
