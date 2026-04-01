import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

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

DOCUMENTS_FOLDER = "./documents"
FAISS_DB_PATH = "./faiss_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents():
    documents = []
    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)
        return documents

    for filename in os.listdir(DOCUMENTS_FOLDER):
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            elif filename.endswith(".txt"):
                loader = TextLoader(filepath, encoding="utf-8")
            elif filename.endswith(".csv"):
                loader = CSVLoader(filepath)
            else:
                continue
            docs = loader.load()
            documents.extend(docs)
            print(f"  Loaded: {filename} ({len(docs)} docs)")
        except Exception as e:
            print(f"  Failed to load {filename}: {e}")

    return documents


def main():
    print("=" * 50)
    print("  RAG Ingestion Pipeline (FAISS)")
    print("=" * 50)

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set!")
        return

    print("\n[Step 1] Loading documents...")
    documents = load_documents()
    if not documents:
        print("No documents found in ./documents/")
        return
    print(f"  Total: {len(documents)} documents")

    print("\n[Step 2] Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks)} chunks")

    print("\n[Step 3] Creating FAISS vector store...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=api_key,
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_DB_PATH)

    print(f"\nDone! Saved to {FAISS_DB_PATH}")
    print("Next: streamlit run app.py")


if __name__ == "__main__":
    main()
