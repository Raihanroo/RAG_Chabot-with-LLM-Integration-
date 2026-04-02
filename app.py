import os
import streamlit as st
from chatbot import build_rag_chain, ask_question
from ingestion_pipeline import main as run_ingestion

try:
    key = st.secrets.get("OPENAI_API_KEY", "")
    if key:
        os.environ["OPENAI_API_KEY"] = key
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

st.set_page_config(page_title="ChatRAG", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #000000;
    color: #ececec;
}

.stApp { background: #000000 !important; }

#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d0d0d !important;
    border-right: 1px solid #1e1e1e !important;
}
[data-testid="stSidebar"] * { color: #ececec !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #2a2a2a !important;
    color: #ececec !important;
    border-radius: 8px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    width: 100% !important;
    text-align: left !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #1a1a1a !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 24px 0 !important;
    max-width: 680px;
    margin: 0 auto !important;
}

/* ── User avatar: circle with person icon ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: transparent !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #19c37d !important;
    border-radius: 4px !important;
    width: 30px !important;
    height: 30px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #000 !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: #000 !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    width: 30px !important;
    height: 30px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: #0d0d0d !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: #ececec !important;
    font-size: 1rem !important;
    padding: 14px 52px 14px 18px !important;
    resize: none !important;
    box-shadow: 0 0 0 1px #2a2a2a !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #444 !important;
    box-shadow: 0 0 0 1px #444 !important;
}
[data-testid="stChatInputContainer"] {
    background: #000 !important;
    border-top: 1px solid #1e1e1e !important;
    padding: 12px 0 16px !important;
    max-width: 680px;
    margin: 0 auto !important;
}

/* ── Status boxes ── */
.stSuccess {
    background: #0a1a14 !important;
    border: 1px solid #1a3a28 !important;
    border-radius: 8px !important;
    color: #19c37d !important;
}
.stError {
    background: #1a0a0a !important;
    border: 1px solid #3a1a1a !important;
    border-radius: 8px !important;
}
.stInfo {
    background: #0a0a1a !important;
    border: 1px solid #1a1a3a !important;
    border-radius: 8px !important;
}

/* ── Source box ── */
.source-box {
    background: #111;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #888;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0d0d0d !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: #888 !important; font-size: 0.82rem !important; }

/* ── Toggle ── */
[data-testid="stToggle"] label { color: #888 !important; font-size: 0.82rem !important; }

/* ── Input ── */
input[type="password"] {
    background: #0d0d0d !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    color: #ececec !important;
}
label { color: #888 !important; font-size: 0.8rem !important; }

hr { border-color: #1e1e1e !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #19c37d !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:12px 0 4px;font-size:1rem;font-weight:600;color:#ececec'>✦ ChatRAG</div>", unsafe_allow_html=True)
    st.divider()

    if st.button("＋  New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.7rem;color:#444;text-transform:uppercase;letter-spacing:0.08em'>Settings</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    existing_key = os.getenv("OPENAI_API_KEY", "")
    if existing_key:
        st.markdown("<div style='font-size:0.82rem;color:#19c37d;padding:6px 0'>● API key connected</div>", unsafe_allow_html=True)
    else:
        typed_key = st.text_input("OpenRouter API key", type="password", placeholder="sk-or-v1-...")
        if typed_key:
            os.environ["OPENAI_API_KEY"] = typed_key
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    show_sources = st.toggle("Show sources", value=True)

    st.divider()
    st.markdown("<span style='font-size:0.7rem;color:#444;text-transform:uppercase;letter-spacing:0.08em'>Knowledge Base</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if os.path.exists("./faiss_db"):
        st.markdown("<div style='font-size:0.82rem;color:#19c37d;padding:6px 0'>● Documents indexed</div>", unsafe_allow_html=True)
    elif os.getenv("OPENAI_API_KEY", ""):
        with st.spinner("Indexing..."):
            try:
                run_ingestion()
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")
    else:
        st.markdown("<div style='font-size:0.82rem;color:#555;padding:6px 0'>Add API key to index</div>", unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.7rem;color:#333'>ChatRAG · LangChain + FAISS</span>", unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────
api_key = os.getenv("OPENAI_API_KEY", "")
db_ready = os.path.exists("./faiss_db")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state — ChatGPT style center prompt
if not st.session_state.messages:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;
                height:65vh;gap:16px;text-align:center;'>
        <div style='width:52px;height:52px;background:#000;border:1px solid #333;border-radius:12px;
                    display:flex;align-items:center;justify-content:center;font-size:1.6rem;'>✦</div>
        <div style='font-size:1.75rem;font-weight:600;color:#ececec;'>How can I help you?</div>
        <div style='font-size:0.9rem;color:#555;max-width:380px;line-height:1.6;'>
            Ask anything about your uploaded documents.<br>I'll find the answer for you.
        </div>
    </div>
    """, unsafe_allow_html=True)

if not api_key or not db_ready:
    st.stop()

if "chain" not in st.session_state:
    with st.spinner(""):
        try:
            st.session_state.chain = build_rag_chain()
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            st.stop()

# Chat history
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "✦"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg["role"] == "assistant" and show_sources:
            sources = msg.get("sources", [])
            if sources:
                with st.expander(f"📎 {len(sources)} source(s)"):
                    for src in sources:
                        fname = os.path.basename(src["file"])
                        pg = f" · p.{src['page']}" if src.get("page") is not None else ""
                        st.markdown(f'<div class="source-box">📄 {fname}{pg}</div>', unsafe_allow_html=True)

# Input
if user_question := st.chat_input("Message ChatRAG..."):
    with st.chat_message("user", avatar="🧑"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant", avatar="✦"):
        with st.spinner(""):
            try:
                response = ask_question(st.session_state.chain, user_question)
                answer   = response["answer"]
                sources  = response["sources"]
                st.write(answer)
                if show_sources and sources:
                    with st.expander(f"📎 {len(sources)} source(s)"):
                        for src in sources:
                            fname = os.path.basename(src["file"])
                            pg = f" · p.{src['page']}" if src.get("page") is not None else ""
                            st.markdown(f'<div class="source-box">📄 {fname}{pg}</div>', unsafe_allow_html=True)
            except Exception as e:
                answer  = f"Something went wrong: {str(e)}"
                sources = []
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
