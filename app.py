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
@import url('https://fonts.googleapis.com/css2?family=Söhne:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #212121;
    color: #ececec;
}

.stApp { background: #212121; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #171717 !important;
    border-right: 1px solid #2f2f2f !important;
    width: 260px !important;
}
[data-testid="stSidebar"] * { color: #ececec !important; }

/* New chat button */
.stButton > button {
    background: transparent !important;
    border: 1px solid #3f3f3f !important;
    color: #ececec !important;
    border-radius: 8px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    transition: background 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #2f2f2f !important;
    border-color: #555 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 20px 0 !important;
    max-width: 720px;
    margin: 0 auto !important;
}

/* User message bubble */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: #2f2f2f !important;
    border-radius: 18px !important;
    padding: 14px 18px !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: #2f2f2f !important;
    border: 1px solid #3f3f3f !important;
    border-radius: 16px !important;
    color: #ececec !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
    resize: none !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #555 !important;
    box-shadow: none !important;
}
[data-testid="stChatInputContainer"] {
    background: #212121 !important;
    border-top: 1px solid #2f2f2f !important;
    padding: 12px 0 !important;
}

/* Success/error */
.stSuccess { background: rgba(16,163,127,0.1) !important; border: 1px solid rgba(16,163,127,0.25) !important; border-radius: 8px !important; }
.stError   { background: rgba(239,68,68,0.1)  !important; border: 1px solid rgba(239,68,68,0.25)  !important; border-radius: 8px !important; }
.stInfo    { background: rgba(99,102,241,0.1)  !important; border: 1px solid rgba(99,102,241,0.25)  !important; border-radius: 8px !important; }

/* Source box */
.source-box {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #aaa;
}

/* Expander */
[data-testid="stExpander"] {
    background: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: #2f2f2f !important; }

/* Toggle */
[data-testid="stToggle"] label { color: #aaa !important; font-size: 0.85rem !important; }

/* Spinner */
.stSpinner > div { border-top-color: #10a37f !important; }

/* Input label */
label { color: #aaa !important; font-size: 0.8rem !important; }

/* Text input */
input[type="password"], input[type="text"] {
    background: #2f2f2f !important;
    border: 1px solid #3f3f3f !important;
    border-radius: 8px !important;
    color: #ececec !important;
}

.main-content {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ ChatRAG")
    st.divider()

    if st.button("✏️  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()

    st.divider()
    st.markdown("<span style='font-size:0.75rem;color:#666'>SETTINGS</span>", unsafe_allow_html=True)
    st.markdown("")

    existing_key = os.getenv("OPENAI_API_KEY", "")
    if existing_key:
        st.success("API key loaded ✅")
    else:
        typed_key = st.text_input("OpenRouter API key", type="password", placeholder="sk-or-v1-...")
        if typed_key:
            os.environ["OPENAI_API_KEY"] = typed_key
            st.rerun()

    st.markdown("")
    show_sources = st.toggle("Show sources", value=True)

    st.divider()
    st.markdown("<span style='font-size:0.75rem;color:#666'>DOCUMENTS</span>", unsafe_allow_html=True)
    st.markdown("")

    if os.path.exists("./faiss_db"):
        st.success("Knowledge base ready ✅")
    elif os.getenv("OPENAI_API_KEY", ""):
        with st.spinner("Building knowledge base..."):
            try:
                run_ingestion()
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")
    else:
        st.caption("Add API key to index documents.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.72rem;color:#444'>ChatRAG · Built with LangChain</span>", unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────
api_key = os.getenv("OPENAI_API_KEY", "")
db_ready = os.path.exists("./faiss_db")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:12px;'>
        <div style='font-size:2.8rem;'>✦</div>
        <div style='font-size:1.6rem;font-weight:600;color:#ececec;'>How can I help you?</div>
        <div style='font-size:0.9rem;color:#666;'>Ask anything from your uploaded documents.</div>
    </div>
    """, unsafe_allow_html=True)

if not api_key:
    st.stop()

if not db_ready:
    st.stop()

if "chain" not in st.session_state:
    with st.spinner("Loading model..."):
        try:
            st.session_state.chain = build_rag_chain()
        except Exception as e:
            st.error(f"Failed to load: {e}")
            st.stop()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and show_sources:
            sources = msg.get("sources", [])
            if sources:
                with st.expander(f"📎 {len(sources)} source(s)"):
                    for src in sources:
                        filename = os.path.basename(src["file"])
                        page_str = f" · p.{src['page']}" if src.get("page") is not None else ""
                        st.markdown(f'<div class="source-box">📄 {filename}{page_str}</div>', unsafe_allow_html=True)

# Input
if user_question := st.chat_input("Message ChatRAG..."):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                response = ask_question(st.session_state.chain, user_question)
                answer = response["answer"]
                sources = response["sources"]
                st.write(answer)
                if show_sources and sources:
                    with st.expander(f"📎 {len(sources)} source(s)"):
                        for src in sources:
                            filename = os.path.basename(src["file"])
                            page_str = f" · p.{src['page']}" if src.get("page") is not None else ""
                            st.markdown(f'<div class="source-box">📄 {filename}{page_str}</div>', unsafe_allow_html=True)
            except Exception as e:
                answer = f"Something went wrong: {str(e)}"
                sources = []
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
