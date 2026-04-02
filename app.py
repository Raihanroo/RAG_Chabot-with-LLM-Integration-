import os
import streamlit as st
from chatbot import build_rag_chain, ask_question
from ingestion_pipeline import main as run_ingestion

# Load secrets
try:
    key = st.secrets.get("OPENAI_API_KEY", "")
    if key:
        os.environ["OPENAI_API_KEY"] = key
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

st.set_page_config(page_title="RAG Chatbot", page_icon="�", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    margin: 8px 0 !important;
    backdrop-filter: blur(8px);
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 24px !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
}

/* Success/Error boxes */
.stSuccess {
    background: rgba(0,200,100,0.15) !important;
    border: 1px solid rgba(0,200,100,0.3) !important;
    border-radius: 10px !important;
}
.stError {
    background: rgba(255,80,80,0.15) !important;
    border: 1px solid rgba(255,80,80,0.3) !important;
    border-radius: 10px !important;
}

/* Source box */
.source-box {
    background: rgba(102,126,234,0.15);
    border-left: 3px solid #667eea;
    padding: 8px 14px;
    border-radius: 8px;
    margin: 4px 0;
    font-size: 0.82rem;
    color: #c0c8ff;
}

/* Title */
.main-title {
    text-align: center;
    padding: 20px 0 10px 0;
}
.main-title h1 {
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0;
}
.main-title p {
    color: rgba(255,255,255,0.5);
    font-size: 0.95rem;
    margin-top: 6px;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Text color */
p, span, label, .stMarkdown {
    color: #d0d0d0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 RAG Chatbot")
    st.markdown("*Powered by OpenRouter + FAISS*")
    st.divider()

    # API Key
    st.markdown("### � API Key")
    existing_key = os.getenv("OPENAI_API_KEY", "")
    if existing_key:
        st.success("OpenRouter key loaded ✅")
    else:
        typed_key = st.text_input("Enter OpenRouter API key:", type="password", placeholder="sk-or-v1-...")
        if typed_key:
            os.environ["OPENAI_API_KEY"] = typed_key
            st.success("Key set ✅")

    st.divider()

    # Document Status
    st.markdown("### � Documents")
    if os.path.exists("./faiss_db"):
        st.success("Indexed & ready ✅")
    elif os.getenv("OPENAI_API_KEY", ""):
        with st.spinner("Indexing documents..."):
            try:
                run_ingestion()
                st.success("Indexed ✅")
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")
    else:
        st.error("Not ready — add API key first")

    st.divider()

    show_sources = st.toggle("Show sources", value=True)

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()

    st.divider()
    st.markdown("<small style='color:rgba(255,255,255,0.3)'>© 2025 RAG Chatbot</small>", unsafe_allow_html=True)

# ── Main Area ─────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h1>💬 Chat with your Documents</h1>
    <p>Ask anything from your uploaded files — powered by AI</p>
</div>
""", unsafe_allow_html=True)

st.divider()

api_key = os.getenv("OPENAI_API_KEY", "")
db_ready = os.path.exists("./faiss_db")

if not api_key:
    st.info("👈 Add your OpenRouter API key in the sidebar to get started.")
    st.stop()

if not db_ready:
    st.warning("📂 No indexed documents found. Add your API key and the app will index automatically.")
    st.stop()

# Init session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    with st.spinner("Loading AI model..."):
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
                with st.expander(f"📚 {len(sources)} source(s) used"):
                    for src in sources:
                        filename = os.path.basename(src["file"])
                        page_str = f" · page {src['page']}" if src.get("page") is not None else ""
                        st.markdown(f'<div class="source-box">📄 <b>{filename}</b>{page_str}</div>', unsafe_allow_html=True)

# Chat input
if user_question := st.chat_input("Ask something about your documents..."):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask_question(st.session_state.chain, user_question)
                answer = response["answer"]
                sources = response["sources"]
                st.write(answer)
                if show_sources and sources:
                    with st.expander(f"📚 {len(sources)} source(s) used"):
                        for src in sources:
                            filename = os.path.basename(src["file"])
                            page_str = f" · page {src['page']}" if src.get("page") is not None else ""
                            st.markdown(f'<div class="source-box">📄 <b>{filename}</b>{page_str}</div>', unsafe_allow_html=True)
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                sources = []
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
