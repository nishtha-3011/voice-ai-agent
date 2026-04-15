# Intent Classification utility — uses Groq LLM (free, fast).
# No OpenAI key needed.


import os
import json
import logging
import re
from groq import Groq

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"  # free model on Groq

SYSTEM_PROMPT = """You are an intent classifier for a voice-controlled local AI agent.

Given the user's transcribed speech, output ONLY a valid JSON object with these fields:

{
  "intent": "<one of: create_file | write_code | summarize | chat>",
  "details": "<brief human-readable description of what to do>",
  "filename": "<target filename if applicable, else null>",
  "language": "<programming language if write_code, else null>",
  "content_hint": "<key info extracted from the speech to guide tool execution>"
}

Rules:
- "create a file", "make a new file" → intent = create_file
- "write code", "generate a function", "create a script", "write a program" → intent = write_code
- "summarize", "give me a summary", "tldr" → intent = summarize
- Otherwise → intent = chat
- Compound commands like "write a retry function and save it to utils.py" → intent = write_code, filename = utils.py
- Respond with JSON only. No preamble, no markdown fences.
"""


def classify_intent(transcript: str, history: list) -> dict:
    messages = _build_messages(transcript, history)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0,
            max_tokens=300,
        )
        raw = response.choices[0].message.content
        return _parse_response(raw, f"groq:{GROQ_MODEL}")
    except Exception as e:
        logger.error(f"Groq LLM failed: {e}")
        return _keyword_fallback(transcript)


def _build_messages(transcript: str, history: list) -> list:
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history[-4:]:
        msgs.append({"role": "user", "content": item["transcript"]})
        msgs.append({"role": "assistant", "content": json.dumps({
            "intent": item["intent"],
            "details": item.get("details", ""),
        })})
    msgs.append({"role": "user", "content": transcript})
    return msgs


def _parse_response(raw: str, llm_label: str) -> dict:
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", clean, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except Exception:
                data = {"intent": "chat", "details": raw, "content_hint": raw}
        else:
            data = {"intent": "chat", "details": raw, "content_hint": raw}

    data["llm"] = llm_label
    for key in ("intent", "details", "filename", "language", "content_hint"):
        data.setdefault(key, None)
    return data


def _keyword_fallback(transcript: str) -> dict:
    t = transcript.lower()
    if any(w in t for w in ["create file", "make file", "new file"]):
        intent = "create_file"
    elif any(w in t for w in ["write code", "generate", "function", "script", "program"]):
        intent = "write_code"
    elif any(w in t for w in ["summarize", "summary", "tldr"]):
        intent = "summarize"
    else:
        intent = "chat"

    return {
        "intent": intent,
        "details": transcript,
        "filename": None,
        "language": "python" if "python" in t else None,
        "content_hint": transcript,
        "llm": "keyword_fallback",
    }
