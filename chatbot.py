import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"
TOP_K_CHUNKS = 4
OPENROUTER_MODEL = "openai/gpt-4o-mini"


def load_vector_store():
    if not os.path.exists(CHROMA_DB_PATH):
        raise FileNotFoundError("Run python ingestion_pipeline.py first!")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)


def build_rag_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_CHUNKS})

    llm = ChatOpenAI(
        model=OPENROUTER_MODEL,
        temperature=0,
        max_retries=6,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    return {"retriever": retriever, "llm": llm, "history": []}


def ask_question(chain, question: str):
    retriever = chain["retriever"]
    llm = chain["llm"]
    history = chain["history"]

    # Find relevant documents
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    # Build messages with history
    messages = []
    for h in history[-4:]:
        messages.append(HumanMessage(content=h["q"]))
        messages.append(AIMessage(content=h["a"]))

    # Build prompt
    prompt = f"""You are a helpful assistant. Answer using ONLY this context:

{context}

If the answer is not in the context, say: I don't have that information in the provided documents.

Question: {question}"""

    messages.append(HumanMessage(content=prompt))

    # Get answer
    response = llm.invoke(messages)
    answer = response.content

    # Save to history
    history.append({"q": question, "a": answer})

    # Extract sources
    sources = []
    seen = set()
    for doc in docs:
        meta = doc.metadata
        key = f"{meta.get('source', 'unknown')}_p{meta.get('page', '')}"
        if key not in seen:
            seen.add(key)
            sources.append(
                {"file": meta.get("source", "unknown"), "page": meta.get("page", None)}
            )

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
