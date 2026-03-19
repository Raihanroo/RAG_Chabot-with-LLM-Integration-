import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"
TOP_K_CHUNKS = 4
GEMINI_MODEL = "gemini-2.0-flash-lite"


def load_vector_store():
    if not os.path.exists(CHROMA_DB_PATH):
        raise FileNotFoundError("Run python ingestion_pipeline.py first!")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)


# chatbot.py এর build_rag_chain ফাংশনে LLM এর সাথে max_retries যোগ করুন
def build_rag_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_CHUNKS})

    # এই অংশটি ফাংশনের ভেতরে থাকবে
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0,
        max_retries=6,
        version="v1",  # এরর এড়াতে এটি যোগ করা হয়েছে
    )

    # সবশেষে ডিকশনারিটি রিটার্ন করতে হবে
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
    print("প্রশ্ন করো। বের হতে 'quit' লেখো.\n")
    while True:
        question = input("\nতুমি: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        response = ask_question(chain, question)
        print(f"\nBot: {response['answer']}")
