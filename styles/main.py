def load_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 48px 24px 36px;
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    font-weight: 800;
    color: #111827;
    line-height: 1.15;
    margin-bottom: 14px;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(135deg, #6c63ff, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 16px;
    color: #6b7280;
    font-weight: 400;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Section title ── */
.section-title {
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #111827;
    margin-bottom: 14px;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #d1d5db;
}

/* ── Input Mode Cards ── */
.mode-card {
    border: 2px solid #e5e7eb;
    border-radius: 14px;
    padding: 22px 20px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
    background: #fafafa;
}
.mode-card:hover {
    border-color: #6c63ff;
    background: #f5f3ff;
}
.mode-card.active {
    border-color: #6c63ff;
    background: #f5f3ff;
}
.mode-icon { font-size: 32px; margin-bottom: 10px; }
.mode-label {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 4px;
}
.mode-desc {
    font-size: 13px;
    color: #9ca3af;
}

/* ── Pipeline Cards ── */
.pipe-card {
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    border: 1px solid;
}
.pipe-card.transcript {
    background: #eff6ff;
    border-color: #bfdbfe;
}
.pipe-card.intent {
    background: #fffbeb;
    border-color: #fde68a;
}
.pipe-card.action {
    background: #f0fdf4;
    border-color: #bbf7d0;
}
.pipe-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.pipe-label.blue  { color: #3b82f6; }
.pipe-label.amber { color: #d97706; }
.pipe-label.green { color: #059669; }
.pipe-value {
    font-size: 16px;
    color: #111827;
    line-height: 1.6;
    font-weight: 400;
}

/* ── Intent Badge ── */
.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    margin-right: 8px;
}
.badge-write_code  { background: #fef3c7; color: #92400e; }
.badge-create_file { background: #d1fae5; color: #065f46; }
.badge-summarize   { background: #dbeafe; color: #1e40af; }
.badge-chat        { background: #ede9fe; color: #4c1d95; }

/* ── History ── */
.hist-card {
    background: #f9fafb;
    border: 1px solid #f3f4f6;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.hist-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}
.hist-intent {
    font-size: 12px;
    font-weight: 700;
    color: #6c63ff;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.hist-time {
    font-size: 11px;
    color: #d1d5db;
}
.hist-text {
    font-size: 13px;
    color: #6b7280;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Meta ── */
.meta-bar {
    display: flex;
    gap: 16px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #f3f4f6;
    flex-wrap: wrap;
}
.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f3f4f6;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: #6b7280;
    font-weight: 500;
}

/* ── Streamlit overrides ── */
[data-testid="stRadio"] { display: none !important; }

div[data-testid="stFileUploader"] {
    background: #fafafa !important;
    border: 2px dashed #d1d5db !important;
    border-radius: 14px !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff !important;
}
div[data-testid="stFileUploader"] label {
    font-size: 15px !important;
    color: #374151 !important;
    font-weight: 500 !important;
}
div[data-testid="stFileUploader"] small {
    font-size: 13px !important;
    color: #9ca3af !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.35) !important;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 14px !important;
}
[data-testid="stCode"] {
    border-radius: 12px !important;
    font-size: 14px !important;
}
[data-testid="stExpander"] {
    border-radius: 12px !important;
    border: 1px solid #f3f4f6 !important;
}
[data-testid="stExpander"] summary {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

[data-testid="stAudioInput"] {
    background: #fafafa !important;
    border: 2px dashed #d1d5db !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f9fafb; }
::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 3px; }
</style>
"""
