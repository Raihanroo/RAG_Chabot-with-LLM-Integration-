import os
import chromadb
import time
from dotenv import load_dotenv
from google import genai
from pathlib import Path
from sentence_transformers import SentenceTransformer

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# HuggingFace embedding (to avoid Google embedding quota)
print("📥 Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model ready")

CHROMA_DB_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

try:
    chroma_client.delete_collection("my_knowledge_base")
except:
    pass

collection = chroma_client.create_collection(name="my_knowledge_base")

# Use a model with better free tier quota
LLM_MODEL = "models/gemini-2.0-flash-lite"  # More quota available


def get_embedding(text):
    """Get embedding using HuggingFace (no quota issues)"""
    return embedding_model.encode(text).tolist()


def generate_with_retry(prompt, max_retries=5):
    """Generate content with automatic retry on quota error"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model=LLM_MODEL, contents=prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = 20  # Wait 20 seconds
                print(
                    f"⚠️ Quota exceeded. Waiting {wait_time} seconds... (Attempt {attempt+1}/{max_retries})"
                )
                time.sleep(wait_time)
            else:
                print(f"Error: {e}")
                return f"Error: {e}"
    return "Quota exhausted. Please try again later."


def load_text_files(documents_folder="./documents"):
    documents = []
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        print(f"📁 '{documents_folder}' folder created.")
        return documents

    txt_files = list(Path(documents_folder).glob("*.txt"))
    if not txt_files:
        print("⚠️ No .txt files found.")
        return documents

    for txt_file in txt_files:
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                documents.append(
                    {
                        "content": content,
                        "source": txt_file.name,
                        "id": f"doc_{txt_file.stem}",
                    }
                )
                print(f"✅ Loaded: {txt_file.name}")
    return documents


def split_text_into_chunks(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks


def main():
    print("=" * 50)
    print("  RAG Chatbot - With Rate Limit Handling")
    print("=" * 50)

    print("\n[Step 1] Loading documents...")
    documents = load_text_files()

    if not documents:
        print("\n❌ No documents found!")
        return

    print("\n[Step 2] Splitting into chunks...")
    all_chunks = []
    for doc in documents:
        chunks = split_text_into_chunks(doc["content"])
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}_chunk_{i}"
            all_chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {"source": doc["source"], "chunk": i},
                }
            )
        print(f"  • {doc['source']}: {len(chunks)} chunks")

    print(f"\n  Total chunks: {len(all_chunks)}")

    print("\n[Step 3] Saving to vector database...")
    for i, chunk in enumerate(all_chunks):
        embedding = get_embedding(chunk["text"])
        collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[chunk["metadata"]],
        )
        if (i + 1) % 5 == 0 or (i + 1) == len(all_chunks):
            print(f"  ✅ {i + 1}/{len(all_chunks)} chunks saved")
        time.sleep(0.1)  # Small delay to avoid rate limits

    print(f"\n✅ Successfully saved {collection.count()} chunks")

    print("\n[Step 4] Testing...")
    test_query = "What is Python?"

    query_embedding = get_embedding(test_query)
    results = collection.query(query_embeddings=[query_embedding], n_results=2)

    if results["documents"][0]:
        context = "\n\n".join(results["documents"][0])
        prompt = f"""Based on this context, answer: {test_query}

Context: {context}

Answer briefly:"""

        print("\n🤖 Generating answer (may take a moment)...")
        answer = generate_with_retry(prompt)
        print(f"\nQuestion: {test_query}")
        print(f"Answer: {answer}")
    else:
        print("No results found")

    print("\n" + "=" * 50)
    print("✅ Ingestion Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
