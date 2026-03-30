import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY")
)

CHROMA_DB_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Delete old collection if exists
try:
    chroma_client.delete_collection("my_knowledge_base")
except:
    pass

collection = chroma_client.create_collection(name="my_knowledge_base")

# OpenRouter models
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "openai/gpt-4o-mini"


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


def add_to_knowledge_base(text, text_id, metadata=None):
    try:
        print(f"📝 Adding: {text[:50]}...")
        result = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
        vector = result.data[0].embedding
        collection.add(
            ids=[text_id],
            embeddings=[vector],
            documents=[text],
            metadatas=[metadata or {}],
        )
        print(f"✅ Saved: {text_id}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def main():
    print("=" * 50)
    print("  RAG Chatbot - Document Ingestion")
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
                    "metadata": {
                        "source": doc["source"],
                        "chunk": i,
                        "total_chunks": len(chunks),
                    },
                }
            )
        print(f"  • {doc['source']}: {len(chunks)} chunks")

    print(f"\n  Total chunks: {len(all_chunks)}")

    print("\n[Step 3] Saving to vector database...")
    success_count = 0
    for chunk in all_chunks:
        if add_to_knowledge_base(chunk["text"], chunk["id"], chunk["metadata"]):
            success_count += 1

    print(f"\n✅ Successfully saved {success_count}/{len(all_chunks)} chunks")

    print("\n[Step 4] Testing...")
    test_query = "What is Python?"
    try:
        query_result = client.embeddings.create(model=EMBEDDING_MODEL, input=test_query)
        query_vector = query_result.data[0].embedding
        results = collection.query(query_embeddings=[query_vector], n_results=2)

        if results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            prompt = f"""Based on this context, answer: {test_query}

Context: {context}

Answer briefly:"""

            response = client.chat.completions.create(
                model=LLM_MODEL, messages=[{"role": "user", "content": prompt}]
            )
            print(f"\nQuestion: {test_query}")
            print(f"Answer: {response.choices[0].message.content}")
        else:
            print("No results found")
    except Exception as e:
        print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("✅ Ingestion Complete!")
    print("👉 Now run: streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
