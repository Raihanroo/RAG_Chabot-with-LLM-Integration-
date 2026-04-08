"""
ChatRAG - Advanced Document Ingestion Pipeline
Supports PDF, TXT, CSV, Excel with better processing
"""

import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Load environment variables
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
DOCUMENTS_FOLDER = "./documents"
FAISS_DB_PATH = "./faiss_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents():
    """
    Load all documents from the documents folder
    Supports: PDF, TXT, CSV, Excel (XLSX, XLS)
    
    Returns:
        list: List of loaded documents
    """
    documents = []
    
    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)
        print(f"Created {DOCUMENTS_FOLDER} folder")
        return documents

    print(f"\nLoading documents from {DOCUMENTS_FOLDER}...")
    
    for filename in os.listdir(DOCUMENTS_FOLDER):
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        
        # Skip directories
        if not os.path.isfile(filepath):
            continue
            
        try:
            # PDF files
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✅ Loaded: {filename} ({len(docs)} pages)")
            
            # Text files
            elif filename.endswith(".txt"):
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✅ Loaded: {filename} ({len(docs)} sections)")
            
            # CSV files
            elif filename.endswith(".csv"):
                loader = CSVLoader(filepath)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✅ Loaded: {filename} ({len(docs)} rows)")
            
            # Excel files (XLSX, XLS)
            elif filename.endswith((".xlsx", ".xls")):
                try:
                    # Read Excel file
                    df = pd.read_excel(filepath)
                    
                    # Convert to text format
                    text_content = f"File: {filename}\n\n"
                    text_content += f"Columns: {', '.join(df.columns.tolist())}\n\n"
                    text_content += "Data:\n"
                    text_content += df.to_string(index=False)
                    
                    # Create document
                    doc = Document(
                        page_content=text_content,
                        metadata={"source": filepath, "type": "excel"}
                    )
                    documents.append(doc)
                    print(f"  ✅ Loaded: {filename} ({len(df)} rows, {len(df.columns)} columns)")
                except Exception as e:
                    print(f"  ❌ Failed to load Excel {filename}: {e}")
            
            else:
                print(f"  ⚠️  Skipped: {filename} (unsupported format)")
                continue
            
        except Exception as e:
            print(f"  ❌ Failed to load {filename}: {e}")

    return documents


def main():
    """Main ingestion pipeline"""
    print("=" * 60)
    print("  ChatRAG - Document Ingestion Pipeline")
    print("=" * 60)

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY not set!")
        print("\nPlease set your API key in .env file:")
        print("OPENAI_API_KEY=sk-or-v1-your-key-here")
        return

    # Step 1: Load documents
    print("\n[Step 1/3] Loading documents...")
    documents = load_documents()
    
    if not documents:
        print("\n⚠️  No documents found in ./documents/")
        print("\nPlease add PDF, TXT, or CSV files to the documents folder.")
        return
        
    print(f"\n  📚 Total documents loaded: {len(documents)}")

    # Step 2: Split into chunks
    print("\n[Step 2/3] Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"  ✂️  Created {len(chunks)} chunks")

    # Step 3: Create embeddings and save to FAISS
    print("\n[Step 3/3] Creating FAISS vector store...")
    print("  ⏳ This may take a few moments...")
    
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    except Exception as e:
        print(f"  ⚠️  Using fallback embeddings initialization")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
        )
    
    # Create and save vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_DB_PATH)

    # Success message
    print("\n" + "=" * 60)
    print("  ✅ SUCCESS!")
    print("=" * 60)
    print(f"\n  📊 Statistics:")
    print(f"     • Documents processed: {len(documents)}")
    print(f"     • Chunks created: {len(chunks)}")
    print(f"     • Database location: {FAISS_DB_PATH}")
    print(f"\n  🚀 Next step:")
    print(f"     streamlit run app.py")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
