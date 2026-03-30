import os
import streamlit as st
from dotenv import load_dotenv
from chatbot import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(page_title="My RAG Chatbot", page_icon="🧠", layout="centered")

st.markdown(
    """
<style>
.source-box {
    background-color: #f0f2f6;
    border-left: 4px solid #4f8ef7;
    padding: 8px 12px;
    border-radius: 4px;
    margin: 4px 0;
    font-size: 0.85rem;
}
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🧠 RAG Chatbot")
    st.caption("OpenRouter দিয়ে তৈরি!")
    st.divider()

    st.subheader("🔑 OpenRouter API Key")
    existing_key = os.getenv("OPENAI_API_KEY", "")
    if existing_key:
        st.success("OpenRouter API key লোড হয়েছে ✅")
    else:
        typed_key = st.text_input(
            "API key দাও:", type="password", placeholder="sk-or-v1-..."
        )
        if typed_key:
            os.environ["OPENAI_API_KEY"] = typed_key
            st.success("Key set! ✅")

    st.divider()

    st.subheader("📦 Document Status")
    if os.path.exists("./chroma_db"):
        st.success("Documents indexed ✅")
    else:
        st.error("Not ready ❌")
        st.warning("আগে এটা run করো:")
        st.code("python ingestion_pipeline.py")

    st.divider()
    show_sources = st.checkbox("Sources দেখাও", value=True)
    st.divider()

    if st.button("🗑️ Conversation মুছো", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()

st.title("💬 তোমার Documents এর সাথে কথা বলো")
st.caption("Powered by OpenRouter + ChromaDB")

api_key = os.getenv("OPENAI_API_KEY", "")
db_ready = os.path.exists("./chroma_db")

if not api_key:
    st.warning("👈 Sidebar এ OpenRouter API key দাও।")
    st.stop()

if not db_ready:
    st.error("📦 কোনো indexed document পাওয়া যায়নি।")
    st.info("documents/ ফোল্ডারে file রাখো তারপর run করো: python ingestion_pipeline.py")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    with st.spinner("🔧 AI model লোড হচ্ছে..."):
        try:
            st.session_state.chain = build_rag_chain()
        except Exception as e:
            st.error(f"লোড করতে ব্যর্থ: {e}")
            st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and show_sources:
            sources = msg.get("sources", [])
            if sources:
                with st.expander(f"📚 {len(sources)}টি source ব্যবহার হয়েছে"):
                    for src in sources:
                        filename = os.path.basename(src["file"])
                        page_str = (
                            f" · page {src['page']}"
                            if src.get("page") is not None
                            else ""
                        )
                        st.markdown(
                            f'<div class="source-box">📄 <strong>{filename}</strong>{page_str}</div>',
                            unsafe_allow_html=True,
                        )

if user_question := st.chat_input("তোমার document সম্পর্কে প্রশ্ন করো..."):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        with st.spinner("🔍 খুঁজছি এবং উত্তর তৈরি করছি..."):
            try:
                response = ask_question(st.session_state.chain, user_question)
                answer = response["answer"]
                sources = response["sources"]
                st.write(answer)
                if show_sources and sources:
                    with st.expander(f"📚 {len(sources)}টি source ব্যবহার হয়েছে"):
                        for src in sources:
                            filename = os.path.basename(src["file"])
                            page_str = (
                                f" · page {src['page']}"
                                if src.get("page") is not None
                                else ""
                            )
                            st.markdown(
                                f'<div class="source-box">📄 <strong>{filename}</strong>{page_str}</div>',
                                unsafe_allow_html=True,
                            )
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                sources = []
                st.error(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
