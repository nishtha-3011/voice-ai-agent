from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import tempfile
from datetime import datetime
from utils.stt import transcribe_audio
from utils.intent import classify_intent
from utils.tools import execute_tool
from styles.main import load_css          
st.set_page_config(
    page_title="VoiceAgent AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(load_css(), unsafe_allow_html=True)   

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "confirm_pending" not in st.session_state:
    st.session_state.confirm_pending = None
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "mic"


def append_history(transcript, intent_data, result, stt_model):
    st.session_state.history.append({
        "transcript": transcript,
        "intent": intent_data.get("intent", "unknown"),
        "details": intent_data.get("details", ""),
        "action": result.get("action", ""),
        "output": result.get("output", ""),
        "llm": intent_data.get("llm", "unknown"),
        "stt_model": stt_model,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Voice AI Agent — <span>Speak, It Understands.</span></div>
    <div class="hero-sub">Record your voice or upload an audio file. The agent transcribes, understands your intent, and executes the right action.</div>
</div>
""", unsafe_allow_html=True)

col_main, col_hist = st.columns([2, 1], gap="large")

with col_main:

    # ── Input Mode ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">01 · Choose Input Method</div>', unsafe_allow_html=True)

    col_mic, col_upload = st.columns(2)
    with col_mic:
        mic_active = "active" if st.session_state.input_mode == "mic" else ""
        st.markdown(f"""
        <div class="mode-card {mic_active}">
            <div class="mode-icon">🎤</div>
            <div class="mode-label">Record via Microphone</div>
            <div class="mode-desc">Speak directly in your browser</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Use Microphone", use_container_width=True, key="btn_mic"):
            st.session_state.input_mode = "mic"
            st.rerun()

    with col_upload:
        upload_active = "active" if st.session_state.input_mode == "upload" else ""
        st.markdown(f"""
        <div class="mode-card {upload_active}">
            <div class="mode-icon">📁</div>
            <div class="mode-label">Upload Audio File</div>
            <div class="mode-desc">Upload .wav, .mp3, .m4a, .ogg</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upload File", use_container_width=True, key="btn_upload"):
            st.session_state.input_mode = "upload"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Audio Input ───────────────────────────────────────────────────────────
    audio_bytes = None
    uploaded = None

    if st.session_state.input_mode == "mic":
        st.markdown('<div class="section-title">02 · Record Your Voice</div>', unsafe_allow_html=True)
        audio_bytes = st.audio_input("Click the mic button below to start recording", label_visibility="visible")
    else:
        st.markdown('<div class="section-title">02 · Upload Audio File</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Drag and drop your audio file here, or click to browse",
            type=["wav", "mp3", "m4a", "ogg"],
        )
        if uploaded:
            audio_bytes = uploaded.read()
            st.audio(audio_bytes)

    st.markdown("<br>", unsafe_allow_html=True)

    if audio_bytes and st.button("  Process Audio", use_container_width=True):
        st.session_state.confirm_pending = None

        with st.spinner("Transcribing your audio…"):
            suffix = ".wav"
            if uploaded:
                suffix = "." + uploaded.name.rsplit(".", 1)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                data = audio_bytes if isinstance(audio_bytes, bytes) else audio_bytes.getvalue()
                tmp.write(data)
                tmp_path = tmp.name
            transcript, stt_model_used = transcribe_audio(tmp_path)
            os.unlink(tmp_path)

        if not transcript:
            st.error("⚠️ Could not transcribe audio. Please try again.")
            st.stop()

        with st.spinner("Understanding your intent…"):
            intent_data = classify_intent(transcript, st.session_state.history)

        file_intents = {"create_file", "write_code"}
        if intent_data["intent"] in file_intents:
            st.session_state.confirm_pending = {
                "transcript": transcript,
                "intent_data": intent_data,
                "stt_model": stt_model_used,
            }
            st.rerun()
        else:
            with st.spinner("Executing action…"):
                result = execute_tool(intent_data, transcript)
            append_history(transcript, intent_data, result, stt_model_used)
            st.rerun()

    # ── Confirm ───────────────────────────────────────────────────────────────
    if st.session_state.confirm_pending:
        pending = st.session_state.confirm_pending
        intent = pending["intent_data"]["intent"]
        details = pending["intent_data"].get("details", "")
        st.warning(f"⚠️ **Confirmation Required**\n\nThe agent wants to perform: **{intent}**\n\n_{details}_\n\nDo you want to proceed?")
        c1, c2 = st.columns(2)
        if c1.button("✅ Approve & Execute", type="primary", use_container_width=True):
            with st.spinner("Executing…"):
                result = execute_tool(pending["intent_data"], pending["transcript"])
            append_history(pending["transcript"], pending["intent_data"], result, pending["stt_model"])
            st.session_state.confirm_pending = None
            st.rerun()
        if c2.button("❌ Cancel", use_container_width=True):
            st.session_state.confirm_pending = None
            st.rerun()

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.history:
        latest = st.session_state.history[-1]
        intent = latest["intent"]
        badge_cls = f"badge-{intent}" if intent in ("write_code", "create_file", "summarize", "chat") else "badge-chat"

        st.markdown('<div class="section-title">03 · Pipeline Results</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="pipe-card transcript">
  <div class="pipe-label blue">📝 Transcribed Text</div>
  <div class="pipe-value">{latest['transcript']}</div>
</div>
<div class="pipe-card intent">
  <div class="pipe-label amber">🧠 Detected Intent</div>
  <div class="pipe-value">
    <span class="badge {badge_cls}">{intent}</span>
    {latest.get('details', '')}
  </div>
</div>
<div class="pipe-card action">
  <div class="pipe-label green">⚙️ Action Taken</div>
  <div class="pipe-value">{latest['action']}</div>
</div>
""", unsafe_allow_html=True)

        output = latest.get("output", "")
        if output:
            st.markdown('<div class="section-title">04 · Final Output</div>', unsafe_allow_html=True)
            if latest["intent"] in ("create_file", "write_code"):
                lang = "python" if ".py" in latest.get("action", "") else "text"
                st.code(output, language=lang)
            else:
                st.markdown(output)

        st.markdown(f"""
<div class="meta-bar">
  <span class="meta-chip">🎙️ {latest.get('stt_model', '–')}</span>
  <span class="meta-chip">🤖 {latest.get('llm', '–')}</span>
  <span class="meta-chip">🕐 {latest['timestamp']}</span>
</div>
""", unsafe_allow_html=True)


# ── History ────────────────────────────────────────────────────────────────────
with col_hist:
    st.markdown('<div class="section-title">Session Log</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
<div class="hist-card" style="text-align:center; padding: 32px 16px;">
  <div style="font-size:36px; margin-bottom:12px;">🎙️</div>
  <div style="font-size:15px; font-weight:600; color:#374151; margin-bottom:6px;">No actions yet</div>
  <div style="font-size:13px; color:#9ca3af;">Record or upload audio to get started</div>
</div>
""", unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            num = len(st.session_state.history) - i
            intent = item["intent"]
            preview = item["transcript"][:50] + "…" if len(item["transcript"]) > 50 else item["transcript"]
            time = item["timestamp"][-8:]
            st.markdown(f"""
<div class="hist-card">
  <div class="hist-top">
    <span class="hist-intent">#{num} · {intent}</span>
    <span class="hist-time">{time}</span>
  </div>
  <div class="hist-text">{preview}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()


