# RAG Chatbot API - Usage Guide

FastAPI-based REST API for the RAG Chatbot system.

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API key in `.env`
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### 3. Run the API server
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## API Endpoints

### 1. Health Check
**GET** `/`

Check if the API is running and database is ready.

**Response:**
```json
{
  "status": "ok",
  "message": "RAG Chatbot API is running",
  "details": {
    "db_ready": true,
    "chain_loaded": true
  }
}
```

---

### 2. Ask Question
**POST** `/ask`

Ask a question to the RAG chatbot.

**Request Body:**
```json
{
  "question": "When was Google founded?",
  "session_id": "user123"
}
```

**Response:**
```json
{
  "answer": "Google was formally incorporated on September 4, 1998.",
  "sources": [
    {
      "file": "documents/google_history_deep.txt",
      "page": null
    }
  ],
  "session_id": "user123"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "When was Google founded?"}'
```

---

### 3. Ingest Documents
**POST** `/ingest`

Process all documents in the `documents/` folder and create vector embeddings.

**Response:**
```json
{
  "status": "success",
  "message": "Documents ingested successfully",
  "details": {
    "total_documents": 5,
    "total_chunks": 30
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/ingest"
```

---

### 4. Upload Document
**POST** `/upload`

Upload a new document (PDF, TXT, or CSV).

**Request:**
- Form data with file field

**Response:**
```json
{
  "status": "success",
  "message": "File uploaded: example.pdf",
  "details": {
    "file_path": "documents/example.pdf"
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/document.pdf"
```

---

### 5. List Documents
**GET** `/documents`

Get a list of all documents in the system.

**Response:**
```json
{
  "status": "ok",
  "message": "Found 5 document(s)",
  "details": {
    "documents": [
      "google_history_deep.txt",
      "microsoft_evolution.txt",
      "tesla_gigafactories.txt"
    ]
  }
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/documents"
```

---

### 6. Reset Conversation
**DELETE** `/reset`

Clear conversation history (useful for starting fresh).

**Response:**
```json
{
  "status": "success",
  "message": "Chain history reset"
}
```

**cURL Example:**
```bash
curl -X DELETE "http://localhost:8000/reset"
```

---

## Complete Workflow Example

### Step 1: Check API status
```bash
curl http://localhost:8000/
```

### Step 2: Upload a document
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@documents/my_document.pdf"
```

### Step 3: Ingest documents
```bash
curl -X POST "http://localhost:8000/ingest"
```

### Step 4: Ask questions
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the document?"}'
```

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Check status
response = requests.get(f"{BASE_URL}/")
print(response.json())

# 2. Upload document
with open("my_document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(response.json())

# 3. Ingest documents
response = requests.post(f"{BASE_URL}/ingest")
print(response.json())

# 4. Ask question
data = {
    "question": "What is RAG?",
    "session_id": "user123"
}
response = requests.post(f"{BASE_URL}/ask", json=data)
result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

---

## JavaScript/Fetch Example

```javascript
const BASE_URL = "http://localhost:8000";

// Ask a question
async function askQuestion(question) {
  const response = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
      session_id: "user123"
    })
  });
  
  const data = await response.json();
  console.log("Answer:", data.answer);
  console.log("Sources:", data.sources);
  return data;
}

// Upload a file
async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });
  
  return await response.json();
}

// Usage
askQuestion("When was Google founded?");
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request (invalid input) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | Service unavailable (chain not initialized) |

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

---

## Configuration

Edit these values in `api.py` or the imported modules:

| Variable | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | API server host |
| `PORT` | `8000` | API server port |
| `DOCUMENTS_FOLDER` | `./documents` | Document storage location |
| `FAISS_DB_PATH` | `./faiss_db` | Vector database location |
| `TOP_K_CHUNKS` | `4` | Number of chunks to retrieve |

---

## Deployment

### Using Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t rag-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key rag-api
```

### Using Railway/Render

1. Push to GitHub
2. Connect repository
3. Set environment variable: `OPENAI_API_KEY`
4. Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

You can test all endpoints directly from the browser!

---

## Security Notes

- Add authentication middleware for production use
- Implement rate limiting
- Validate file uploads (size, type)
- Use HTTPS in production
- Store API keys securely (environment variables, secrets manager)

---

## Next Steps

- Add user authentication (JWT tokens)
- Implement conversation persistence (database)
- Add file deletion endpoint
- Support more document types
- Add streaming responses for real-time answers
- Implement caching for faster responses
