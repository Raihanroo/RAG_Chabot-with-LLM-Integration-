# 🚀 Quick Start Guide - RAG Chatbot

তোমার RAG Chatbot local server এ চালানোর সম্পূর্ণ গাইড।

---

## 🎯 সবচেয়ে সহজ উপায় (Recommended)

### Windows:
```bash
start_chatrag.bat
```
**Double-click করলেই হবে!** এটা automatically:
1. ✅ API server চালু করবে
2. ✅ Browser এ UI খুলবে  
3. ✅ তুমি সরাসরি ব্যবহার শুরু করতে পারবে!

### Mac/Linux:
```bash
# Terminal 1: Start API
python api.py

# Browser: Open UI
open index.html
```

---

## 📖 কিভাবে ব্যবহার করবে

### Step 1: Documents Upload করো
1. UI তে "Choose Files" button এ click করো
2. তোমার PDF, TXT, বা CSV files select করো
3. Files automatically upload হবে

### Step 2: Process Documents
1. "Process Documents" button এ click করো
2. Wait করো processing complete হওয়া পর্যন্ত
3. Status "Ready" দেখাবে

### Step 3: Chat করো!
1. নিচের input box এ তোমার প্রশ্ন লেখো
2. Enter press করো বা "Send" button এ click করো
3. AI তোমার documents থেকে উত্তর দেবে!

---

## 📋 Prerequisites

1. Python 3.11 installed
2. Dependencies installed: `pip install -r requirements.txt`
3. API key set in `.env` file:
   ```
   OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
   ```

---

## 🎯 Option 1: FastAPI + HTML Frontend (Recommended)

### Step 1: Start Backend API

Terminal খুলে:
```bash
python api.py
```

Output দেখবে:
```
✅ RAG chain loaded successfully
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open Frontend

`frontend_example.html` file টা browser এ খোলো (double-click করো)

অথবা browser এ যাও:
- **Interactive API Docs**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/

### Step 3: Use the Chatbot

Frontend এ প্রশ্ন করো:
- "When was Google founded?"
- "Tell me about Microsoft"
- "What is RAG?"

---

## 🎨 Option 2: Streamlit Web App (All-in-One)

### Single Command:

```bash
streamlit run app.py
```

Browser automatically খুলবে: `http://localhost:8501`

এটা একটা complete ChatGPT-style interface।

---

## 🔧 Option 3: API Testing (For Developers)

### Test API with Python Script:

```bash
python test_api.py
```

### Test with cURL:

```bash
# Health check
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"When was Google founded?\"}"

# List documents
curl http://localhost:8000/documents

# Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@documents/my_file.pdf"

# Re-ingest documents
curl -X POST http://localhost:8000/ingest
```

---

## 📁 Adding New Documents

### Method 1: Manual (Recommended)

1. Copy your PDF/TXT/CSV files to `documents/` folder
2. Run ingestion:
   ```bash
   python ingestion_pipeline.py
   ```
3. Restart the server

### Method 2: Via API

```bash
# Upload file
curl -X POST http://localhost:8000/upload \
  -F "file=@path/to/your/document.pdf"

# Then ingest
curl -X POST http://localhost:8000/ingest
```

### Method 3: Via Streamlit

Streamlit app automatically ingests documents on startup.

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| FastAPI Server | http://localhost:8000 | Backend API |
| Swagger Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
| Streamlit App | http://localhost:8501 | Web UI (if running) |
| HTML Frontend | file:///path/to/frontend_example.html | Simple frontend |

---

## 🔄 Complete Workflow

### First Time Setup:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key in .env
echo "OPENAI_API_KEY=sk-or-v1-your-key" > .env

# 3. Add documents to documents/ folder
# (Already has some sample documents)

# 4. Ingest documents
python ingestion_pipeline.py

# 5. Start server
python api.py
```

### Daily Use:

```bash
# Start backend
python api.py

# Open frontend_example.html in browser
# OR
# Start Streamlit
streamlit run app.py
```

---

## 🛠️ Troubleshooting

### Port 8000 already in use:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Or change port in api.py:
# uvicorn.run(app, host="0.0.0.0", port=8001)
```

### FAISS database error:

```bash
# Delete old database
rm -rf faiss_db

# Re-ingest
python ingestion_pipeline.py
```

### API key not found:

Check `.env` file exists and has:
```
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### Documents not found:

Make sure files are in `documents/` folder and run:
```bash
python ingestion_pipeline.py
```

---

## 📊 Project Structure

```
Rag_for_beginner/
│
├── api.py                      # FastAPI backend (port 8000)
├── app.py                      # Streamlit web app (port 8501)
├── chatbot.py                  # RAG logic
├── ingestion_pipeline.py       # Document processing
│
├── frontend_example.html       # Simple HTML frontend
├── test_api.py                 # API testing script
│
├── documents/                  # Your documents here
├── faiss_db/                   # Vector database (auto-generated)
│
├── .env                        # API key
├── requirements.txt            # Dependencies
│
├── API_GUIDE.md               # Detailed API documentation
├── QUICK_START.md             # This file
└── README.md                  # Project overview
```

---

## 🎯 Common Use Cases

### Use Case 1: Personal Knowledge Base

```bash
# Add your notes/documents to documents/
# Run ingestion
python ingestion_pipeline.py

# Start Streamlit for easy access
streamlit run app.py
```

### Use Case 2: API for Mobile/Web App

```bash
# Start API backend
python api.py

# Your app connects to http://localhost:8000
# See API_GUIDE.md for endpoints
```

### Use Case 3: Development/Testing

```bash
# Start API
python api.py

# Test in another terminal
python test_api.py

# Or use Swagger UI
# http://localhost:8000/docs
```

---

## 🚀 Next Steps

1. **Add your own documents** to `documents/` folder
2. **Customize the frontend** - edit `frontend_example.html`
3. **Deploy to cloud** - See deployment guides in API_GUIDE.md
4. **Build mobile app** - Use the REST API
5. **Add authentication** - Implement JWT tokens
6. **Scale up** - Use cloud vector databases

---

## 📞 Quick Commands Cheat Sheet

```bash
# Start FastAPI backend
python api.py

# Start Streamlit web app
streamlit run app.py

# Ingest documents
python ingestion_pipeline.py

# Test API
python test_api.py

# Install dependencies
pip install -r requirements.txt

# Check API status
curl http://localhost:8000/

# Ask question via API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here"}'
```

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ `python api.py` shows: "✅ RAG chain loaded successfully"
2. ✅ http://localhost:8000/docs opens in browser
3. ✅ `frontend_example.html` shows "Connected & Ready"
4. ✅ You can ask questions and get answers with sources

---

## 🎉 You're Ready!

Your RAG Chatbot is now running locally. Start asking questions about your documents!

For detailed API documentation, see [API_GUIDE.md](API_GUIDE.md)
