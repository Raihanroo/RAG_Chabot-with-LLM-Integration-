import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage

# Load API key
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            os.environ["OPENAI_API_KEY"] = key
    else:
        from dotenv import load_dotenv
        load_dotenv()
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()

FAISS_DB_PATH = "./faiss_db"
TOP_K_CHUNKS = 4
OPENROUTER_MODEL = "openai/gpt-4o-mini"


def get_embeddings():
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set!")
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=api_key,
    )


def load_vector_store():
    if not os.path.exists(FAISS_DB_PATH):
        raise FileNotFoundError("Run ingestion_pipeline.py first!")
    return FAISS.load_local(FAISS_DB_PATH, get_embeddings(), allow_dangerous_deserialization=True)


def build_rag_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_CHUNKS})

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set!")

    llm = ChatOpenAI(
        model=OPENROUTER_MODEL,
        temperature=0,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=api_key,
    )

    return {"retriever": retriever, "llm": llm, "history": []}


def ask_question(chain, question: str):
    retriever = chain["retriever"]
    llm = chain["llm"]
    history = chain["history"]

    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    messages = []
    for h in history[-4:]:
        messages.append(HumanMessage(content=h["q"]))
        messages.append(AIMessage(content=h["a"]))

    prompt = f"""You are a helpful assistant. Answer using ONLY this context:

{context}

If the answer is not in the context, say: I don't have that information in the provided documents.

Question: {question}"""

    messages.append(HumanMessage(content=prompt))
    response = llm.invoke(messages)
    answer = response.content

    history.append({"q": question, "a": answer})

    sources = []
    seen = set()
    for doc in docs:
        meta = doc.metadata
        key = f"{meta.get('source', 'unknown')}_p{meta.get('page', '')}"
        if key not in seen:
            seen.add(key)
            sources.append({"file": meta.get("source", "unknown"), "page": meta.get("page", None)})

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    print("=" * 50)
    print("  RAG Chatbot - Terminal Mode")
    print("=" * 50)
    chain = build_rag_chain()
    print("Ask a question. Type 'quit' to exit.\n")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        response = ask_question(chain, question)
        print(f"\nBot: {response['answer']}")
        if response["sources"]:
            print("\nSources:")
            for src in response["sources"]:
                print(f"  - {src['file']}")
