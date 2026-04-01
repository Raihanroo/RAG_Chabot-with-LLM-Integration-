# RAG Chatbot — Beginner's Guide

A Retrieval-Augmented Generation (RAG) chatbot that lets you chat with your own documents using OpenRouter AI and ChromaDB.

---

## What is RAG?

RAG (Retrieval-Augmented Generation) is a technique where the AI first **retrieves** relevant chunks from your documents, then **generates** an answer based only on that context — so it doesn't hallucinate or make things up.

```
Your Question
     ↓
ChromaDB (Vector Search) → Finds relevant document chunks
     ↓
LLM (GPT-4o-mini via OpenRouter) → Generates answer from those chunks
     ↓
Answer + Sources
```

---

## Project Structure

```
Rag_for_beginner/
│
├── app.py                  # Streamlit web UI (main entry point)
├── chatbot.py              # RAG chain logic (retriever + LLM)
├── ingestion_pipeline.py   # Loads & indexes documents into ChromaDB
├── main.py                 # Alternate ingestion script (raw OpenAI client)
│
├── documents/              # Put your PDF, TXT, CSV files here
│   ├── google_history_deep.txt
│   ├── microsoft_evolution.txt
│   └── tesla_gigafactories.txt
│
├── chroma_db/              # Auto-generated vector database (don't edit)
├── .env                    # Your API key goes here
├── requirements.txt        # Python dependencies
└── .streamlit/
    └── secrets.toml.example
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or if using a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

### 2. Set your API key

Get a free API key from [openrouter.ai](https://openrouter.ai), then add it to `.env`:

```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### 3. Add your documents

Drop your `.txt`, `.pdf`, or `.csv` files into the `documents/` folder.

### 4. Index the documents

```bash
python ingestion_pipeline.py
```

This reads your documents, splits them into chunks, creates embeddings, and saves them to `chroma_db/`.

### 5. Run the chatbot

```bash
streamlit run app.py
```

Or if `streamlit` is not in PATH:

```bash
python -m streamlit run app.py
```

---

## How Each File Works

### `ingestion_pipeline.py`
- Loads PDF, TXT, and CSV files from `documents/`
- Splits them into 500-character chunks (with 50-char overlap)
- Creates vector embeddings using `text-embedding-3-small` via OpenRouter
- Saves everything to ChromaDB at `./chroma_db`

### `chatbot.py`
- Loads the ChromaDB vector store
- Builds a RAG chain: retriever + LLM
- `build_rag_chain()` — initializes the chain
- `ask_question(chain, question)` — retrieves top 4 relevant chunks, builds a prompt with conversation history, and returns answer + sources
- Can also be run standalone in terminal mode: `python chatbot.py`

### `app.py`
- Streamlit web UI
- Sidebar: API key input, document status, settings
- Chat interface with message history
- Shows source documents used for each answer

### `main.py`
- Alternative ingestion script using raw `chromadb` + `openai` clients (no LangChain)
- Useful for understanding the low-level flow

---

## Configuration

These values can be changed in `chatbot.py`:

| Variable | Default | Description |
|---|---|---|
| `CHROMA_DB_PATH` | `./chroma_db` | Where the vector DB is stored |
| `TOP_K_CHUNKS` | `4` | How many document chunks to retrieve per query |
| `OPENROUTER_MODEL` | `openai/gpt-4o-mini` | LLM model used for answers |

These values can be changed in `ingestion_pipeline.py`:

| Variable | Default | Description |
|---|---|---|
| `DOCUMENTS_FOLDER` | `./documents` | Where to look for documents |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |

---

## Supported Document Types

| Type | Extension | Loader Used |
|---|---|---|
| Text files | `.txt` | `TextLoader` |
| PDF files | `.pdf` | `PyPDFLoader` |
| CSV files | `.csv` | `CSVLoader` |
| Web pages | URL | `WebBaseLoader` |

---

## Deploying to Streamlit Cloud

1. Push your project to GitHub (without `.env`)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and connect your repo
3. In the app settings, add your secret:
   ```
   OPENAI_API_KEY = "sk-or-v1-xxxxxxxx"
   ```
4. Set main file to `app.py` and deploy

---

## Common Errors

**`streamlit` not recognized**
```bash
python -m streamlit run app.py
```

**`OPENAI_API_KEY not set`**
Make sure `.env` file exists and has the correct key starting with `sk-or-v1-`.

**`Run python ingestion_pipeline.py first`**
The `chroma_db/` folder doesn't exist yet. Run ingestion before starting the chatbot.

**`chromadb` version conflict**
```bash
pip install chromadb --upgrade
```
