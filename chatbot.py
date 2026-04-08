"""
ChatRAG - Advanced RAG Chain Logic
Handles multilingual document retrieval with semantic understanding
"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load API key
try:
    import streamlit as st
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            os.environ["OPENAI_API_KEY"] = key
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()

# Configuration
FAISS_DB_PATH = "./faiss_db"
TOP_K_CHUNKS = 6  # Increased for better coverage
OPENROUTER_MODEL = "openai/gpt-4o-mini"


def get_embeddings():
    """Get OpenAI embeddings instance with better configuration"""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set!")
    
    try:
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    except Exception as e:
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
        )


def load_vector_store():
    """Load FAISS vector store from disk"""
    if not os.path.exists(FAISS_DB_PATH):
        raise FileNotFoundError(
            "FAISS database not found! Run 'python ingestion_pipeline.py' first."
        )
    return FAISS.load_local(
        FAISS_DB_PATH, 
        get_embeddings(), 
        allow_dangerous_deserialization=True
    )


def build_rag_chain():
    """Build RAG chain with retriever and LLM"""
    vector_store = load_vector_store()
    
    # Use similarity search with score for better results
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_CHUNKS}
    )

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set!")

    try:
        llm = ChatOpenAI(
            model=OPENROUTER_MODEL,
            temperature=0.3,  # Slightly higher for better language flexibility
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    except Exception as e:
        llm = ChatOpenAI(
            model=OPENROUTER_MODEL,
            temperature=0.3,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
        )

    return {"retriever": retriever, "llm": llm, "history": []}


def ask_question(chain, question: str):
    """
    Ask a question using the RAG chain with advanced semantic understanding
    
    Supports:
    - Multilingual queries (English, Bangla)
    - Synonyms and antonyms
    - All document types (PDF, TXT, CSV, Excel)
    
    Args:
        chain: RAG chain dictionary
        question: User question in any language
        
    Returns:
        dict: {"answer": str, "sources": list}
    """
    retriever = chain["retriever"]
    llm = chain["llm"]
    history = chain["history"]

    # Retrieve relevant documents with similarity search
    try:
        docs = retriever.invoke(question)
    except Exception as e:
        print(f"Retrieval error: {e}")
        docs = []

    if not docs:
        return {
            "answer": "I couldn't find any relevant information in the documents. Please try rephrasing your question or upload more documents.",
            "sources": []
        }

    # Build comprehensive context from all retrieved chunks
    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[Document {i}]\n{doc.page_content}\n")
    
    context = "\n".join(context_parts)

    # Build conversation history
    messages = []
    
    # System message for multilingual and semantic understanding
    system_message = SystemMessage(content="""You are an intelligent AI assistant with advanced capabilities:

1. MULTILINGUAL SUPPORT:
   - Understand questions in English, Bengali/Bangla, and mixed languages
   - Respond in the SAME language as the question
   - If question is in Bangla, answer in Bangla
   - If question is in English, answer in English

2. SEMANTIC UNDERSTANDING:
   - Understand synonyms (e.g., "founder" = "creator" = "প্রতিষ্ঠাতা" = "স্থাপক")
   - Understand antonyms and related concepts
   - Understand context and implied meanings
   - Handle different phrasings of the same question

3. DOCUMENT ANALYSIS:
   - Analyze all types of documents (PDF, text, CSV, Excel)
   - Extract information from tables, lists, and structured data
   - Understand relationships between different pieces of information
   - Provide comprehensive answers using all relevant context

4. ANSWER GUIDELINES:
   - Use ONLY the provided context to answer
   - Be specific and accurate
   - If information is not in context, clearly state that
   - Cite specific details from the documents
   - Maintain the same language as the question""")
    
    messages.append(system_message)
    
    # Add recent conversation history
    for h in history[-3:]:  # Last 3 exchanges
        messages.append(HumanMessage(content=h["q"]))
        messages.append(AIMessage(content=h["a"]))

    # Create enhanced prompt
    user_prompt = f"""Based on the following context from the documents, please answer the question.

CONTEXT:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Answer in the SAME language as the question
- Use information from the context above
- Be specific and detailed
- If the exact answer is not in the context, try to provide related information
- If no relevant information exists, say so clearly
- For Bengali questions, respond in Bengali
- For English questions, respond in English"""

    messages.append(HumanMessage(content=user_prompt))
    
    # Get AI response
    try:
        response = llm.invoke(messages)
        answer = response.content
    except Exception as e:
        print(f"LLM error: {e}")
        answer = f"Error generating response: {str(e)}"

    # Save to history
    history.append({"q": question, "a": answer})

    # Extract sources with better metadata
    sources = []
    seen = set()
    for doc in docs:
        meta = doc.metadata
        source_file = meta.get('source', 'unknown')
        
        # Clean up source path
        if '\\' in source_file or '/' in source_file:
            source_file = os.path.basename(source_file)
        
        key = f"{source_file}_p{meta.get('page', '')}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": source_file, 
                "page": meta.get("page", None),
                "preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            })

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    """Terminal mode for testing"""
    print("=" * 60)
    print("  ChatRAG - Advanced Multilingual Terminal Mode")
    print("=" * 60)
    print("\n  Supports: English, Bangla, Synonyms, All Document Types")
    print("=" * 60)
    
    try:
        chain = build_rag_chain()
        print("\n✅ RAG chain loaded successfully!")
        print("\nAsk questions in English or Bangla. Type 'quit' to exit.\n")
        
        # Example questions
        print("Example questions:")
        print("  English: 'Who founded Google?'")
        print("  Bangla:  'গুগল কে প্রতিষ্ঠা করেছে?'")
        print("  Mixed:   'Google এর founder কে?'\n")
        
        while True:
            question = input("\n🧑 You: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                break
            if not question:
                continue
                
            try:
                response = ask_question(chain, question)
                print(f"\n🤖 Bot: {response['answer']}")
                
                if response["sources"]:
                    print("\n📎 Sources:")
                    for src in response["sources"]:
                        page_info = f" (Page {src['page']})" if src.get('page') else ""
                        print(f"  📄 {src['file']}{page_info}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except Exception as e:
        print(f"\n❌ Failed to load RAG chain: {e}")
        print("\nMake sure to run 'python ingestion_pipeline.py' first!")
