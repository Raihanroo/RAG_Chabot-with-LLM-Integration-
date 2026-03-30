import os
import shutil
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    WebBaseLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCUMENTS_FOLDER = "./documents"
CHROMA_DB_PATH = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def split_documents(documents):
    print(f"\n  Splitting {len(documents)} documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks)} chunks")
    return chunks


def load_pdfs():
    documents = []
    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)
        return documents
    pdf_files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith(".pdf")]
    if not pdf_files:
        print("  No PDF files found.")
        return documents
    for filename in pdf_files:
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        print(f"  Loading PDF: {filename}")
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        documents.extend(pages)
        print(f"    → Loaded {len(pages)} pages")
    return documents


def load_text_files():
    documents = []
    if not os.path.exists(DOCUMENTS_FOLDER):
        return documents
    txt_files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith(".txt")]
    for filename in txt_files:
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        print(f"  Loading text file: {filename}")
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()
        documents.extend(docs)
        print(f"    → Loaded {len(docs)} document(s)")
    return documents


def load_csv_files():
    documents = []
    if not os.path.exists(DOCUMENTS_FOLDER):
        return documents
    csv_files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith(".csv")]
    for filename in csv_files:
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        print(f"  Loading CSV: {filename}")
        loader = CSVLoader(filepath)
        docs = loader.load()
        documents.extend(docs)
        print(f"    → Loaded {len(docs)} rows")
    return documents


def load_web_pages(urls: list):
    documents = []
    if not urls:
        print("  No URLs provided.")
        return documents
    for url in urls:
        print(f"  Loading URL: {url}")
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            documents.extend(docs)
            print(f"    → Loaded content from {url}")
        except Exception as e:
            print(f"    Failed to load {url}: {e}")
    return documents


def create_vector_store(chunks):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY not set!")
        print("Please set your OpenRouter API key in Streamlit Cloud Secrets:")
        print("OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx")
        return None

    if not api_key.startswith("sk-or-v1-"):
        print("\n❌ ERROR: Invalid API key format!")
        print("OpenRouter API key should start with 'sk-or-v1-'")
        print(f"Your key starts with: {api_key[:10]}...")
        return None

    try:
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
        )

        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)

        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH, embedding_function=embeddings_model
        )

        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vector_store.add_documents(batch)
            print(f"  Saved {i + len(batch)} chunks...")
            time.sleep(2)

        return vector_store
    except Exception as e:
        print(f"\n❌ ERROR creating vector store: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. OpenRouter doesn't support embeddings endpoint")
        print("3. Network connection issue")
        return None


def main():
    print("=" * 50)
    print("  RAG Chatbot - Ingestion Pipeline (OpenRouter)")
    print("=" * 50)

    urls = []

    all_documents = []

    print("\n[Step 1] Loading documents...")
    print("\n  [PDF Files]")
    all_documents.extend(load_pdfs())

    print("\n  [Text Files]")
    all_documents.extend(load_text_files())

    print("\n  [CSV Files]")
    all_documents.extend(load_csv_files())

    print("\n  [Web Pages]")
    all_documents.extend(load_web_pages(urls))

    if not all_documents:
        print("\n  No documents loaded!")
        print("  Add PDF/TXT/CSV files to ./documents/ folder")
        return

    print(f"\n  Total documents loaded: {len(all_documents)}")

    print("\n[Step 2] Splitting into chunks...")
    chunks = split_documents(all_documents)

    print("\n[Step 3] Creating vector store...")
    vector_store = create_vector_store(chunks)

    if vector_store is None:
        print("\n❌ Failed to create vector store!")
        return

    print("\n" + "=" * 50)
    print("  Ingestion complete!")
    print("  Next: streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
