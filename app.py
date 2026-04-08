"""
ChatRAG - Streamlit Web Interface
Modern AI-powered document Q&A system
"""

import os
import streamlit as st
from chatbot import build_rag_chain, ask_question
from ingestion_pipeline import (
    load_documents, 
    DOCUMENTS_FOLDER, 
    FAISS_DB_PATH, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load API key
try:
    key = st.secrets.get("OPENAI_API_KEY", "")
    if key:
        os.environ["OPENAI_API_KEY"] = key
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

# Auto-process documents on startup
if os.path.exists(DOCUMENTS_FOLDER) and not os.path.exists(FAISS_DB_PATH):
    try:
        documents = load_documents()
        if documents:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
            chunks = splitter.split_documents(documents)
            api_key = os.getenv("OPENAI_API_KEY", "")
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            vector_store = FAISS.from_documents(chunks, embeddings)
            vector_store.save_local(FAISS_DB_PATH)
    except Exception as e:
        pass

# Page configuration
st.set_page_config(
    page_title="ChatRAG - AI Document Assistant", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Dark Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0a0a !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #2a2a2a !important;
}

/* Buttons */
.stButton > button {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2a2a2a !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: #1a1a1a !important;
    border: 1px dashed #2a2a2a !important;
    border-radius: 8px !important;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 20px 0 !important;
}

[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 50% !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 50% !important;
}

/* Chat Input */
[data-testid="stChatInput"] textarea {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: #e8e8e8 !important;
}

/* Success/Error */
.stSuccess {
    background: #0a1a14 !important;
    border: 1px solid #1a3a28 !important;
    color: #00ff88 !important;
}
.stError {
    background: #1a0a0a !important;
    border: 1px solid #3a1a1a !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ✨ ChatRAG")
    st.markdown("AI-powered document assistant")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()
    
    st.divider()
    
    # Document Upload Section
    st.markdown("#### 📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, TXT, CSV, or Excel files",
        type=['pdf', 'txt', 'csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload documents to chat with"
    )
    
    if uploaded_files:
        if st.button("🔄 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                try:
                    # Save uploaded files
                    os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(DOCUMENTS_FOLDER, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    # Process documents
                    documents = load_documents()
                    if documents:
                        splitter = RecursiveCharacterTextSplitter(
                            chunk_size=CHUNK_SIZE,
                            chunk_overlap=CHUNK_OVERLAP
                        )
                        chunks = splitter.split_documents(documents)
                        
                        api_key = os.getenv("OPENAI_API_KEY", "")
                        embeddings = OpenAIEmbeddings(
                            model="text-embedding-3-small",
                            base_url="https://openrouter.ai/api/v1",
                            api_key=api_key,
                        )
                        
                        vector_store = FAISS.from_documents(chunks, embeddings)
                        vector_store.save_local(FAISS_DB_PATH)
                        
                        st.session_state.chain = None
                        st.success(f"✅ Processed {len(chunks)} chunks from {len(documents)} documents!")
                        st.rerun()
                    else:
                        st.error("No documents found")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.divider()
    
    # Documents List
    st.markdown("#### 📚 Documents")
    if os.path.exists(DOCUMENTS_FOLDER):
        docs = [f for f in os.listdir(DOCUMENTS_FOLDER) 
                if os.path.isfile(os.path.join(DOCUMENTS_FOLDER, f))]
        if docs:
            for doc in docs[:10]:
                icon = "📄" if doc.endswith('.pdf') else "📊" if doc.endswith('.csv') else "📝"
                st.text(f"{icon} {doc}")
        else:
            st.info("No documents yet")
    
    st.divider()
    
    # Info
    st.markdown("#### ℹ️ About")
    st.markdown("""
    ChatRAG uses AI to answer questions about your documents.
    
    **How to use:**
    1. Upload documents
    2. Click "Process Documents"
    3. Ask questions!
    """)

# ═══════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════

# Check prerequisites
api_key = os.getenv("OPENAI_API_KEY", "")
db_ready = os.path.exists(FAISS_DB_PATH)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:100px 20px;'>
        <div style='font-size:64px;margin-bottom:20px;'>✨</div>
        <div style='font-size:32px;font-weight:600;margin-bottom:12px;color:#e8e8e8;'>
            How can I help you?
        </div>
        <div style='font-size:16px;color:#888;max-width:500px;margin:0 auto;'>
            Ask anything about your uploaded documents.<br>
            I'll find the answer for you.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Check API key
if not api_key:
    st.warning("⚠️ Please set your OPENAI_API_KEY in .env file")
    st.code("OPENAI_API_KEY=sk-or-v1-your-key-here", language="bash")
    st.stop()

# Check database
if not db_ready:
    st.info("📤 Upload documents using the sidebar to get started")
    st.stop()

# Initialize RAG chain
if "chain" not in st.session_state or st.session_state.chain is None:
    with st.spinner("Loading AI model..."):
        try:
            st.session_state.chain = build_rag_chain()
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            st.stop()

# Display chat history
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        
        # Show sources for assistant messages
        if msg["role"] == "assistant":
            sources = msg.get("sources", [])
            if sources:
                with st.expander(f"📎 {len(sources)} source(s)"):
                    for src in sources:
                        fname = os.path.basename(src["file"])
                        pg = f" · Page {src['page']}" if src.get("page") else ""
                        st.markdown(f"📄 **{fname}**{pg}")

# Chat input
if user_question := st.chat_input("Message ChatRAG..."):
    # Add user message
    with st.chat_message("user", avatar="🧑"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                response = ask_question(st.session_state.chain, user_question)
                answer = response["answer"]
                sources = response["sources"]
                
                st.write(answer)
                
                if sources:
                    with st.expander(f"📎 {len(sources)} source(s)"):
                        for src in sources:
                            fname = os.path.basename(src["file"])
                            pg = f" · Page {src['page']}" if src.get("page") else ""
                            st.markdown(f"📄 **{fname}**{pg}")
                            
            except Exception as e:
                answer = f"Error: {str(e)}"
                sources = []
                st.error(answer)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer, 
        "sources": sources
    })