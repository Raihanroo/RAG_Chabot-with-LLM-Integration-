# ChatRAG - AI Document Assistant ✨

A modern, AI-powered chatbot that lets you chat with your documents using RAG (Retrieval-Augmented Generation).

🌐 **Live Demo**: [Coming Soon on Streamlit Cloud](https://share.streamlit.io/)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)

---

## 🌟 Features

- 📤 **Easy Document Upload** - PDF, TXT, CSV, Excel support
- 💬 **Smart AI Chat** - Powered by GPT-4o-mini
- 🌍 **Multilingual** - English & Bangla support
- 🔍 **Semantic Search** - Understands synonyms & context
- 🎨 **Modern Dark UI** - Sleek, responsive interface
- 📎 **Source Citations** - See which documents were used
- ⚡ **Fast & Accurate** - FAISS vector search
- 🌐 **Cloud Ready** - Deploy to Streamlit Cloud

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
Create `.env` file:
```env
OPENAI_API_KEY=sk-or-v1-your-key-here
```

Get your API key from [OpenRouter](https://openrouter.ai/)

### 3. Add Documents
Put your PDF, TXT, or CSV files in the `documents/` folder

### 4. Process Documents
```bash
python ingestion_pipeline.py
```

### 5. Run the App
```bash
streamlit run app.py
```

Or use the shortcut:
```bash
run.bat  # Windows
```

Browser will open at `http://localhost:8501`

---

## 📁 Project Structure

```
ChatRAG/
├── app.py                    # Streamlit web interface
├── chatbot.py                # RAG logic
├── ingestion_pipeline.py     # Document processing
├── api.py                    # FastAPI backend (optional)
│
├── documents/                # Your documents here
├── faiss_db/                 # Vector database (auto-generated)
│
├── .env                      # API key (don't commit!)
├── requirements.txt          # Python dependencies
│
├── README.md                 # This file
├── PROJECT_SUMMARY.md        # Detailed documentation
└── DEPLOYMENT.md             # Deployment guide
```

---

## 💡 How to Use

### Upload Documents via UI:
1. Open the app: `streamlit run app.py`
2. Click "Choose files" in sidebar
3. Select your documents
4. Click "Process Documents"
5. Wait for processing to complete
6. Start chatting!

### Upload Documents via Terminal:
1. Copy files to `documents/` folder
2. Run: `python ingestion_pipeline.py`
3. Start the app: `streamlit run app.py`

### Ask Questions:
```
You: "When was Google founded?"
AI:  "Google was founded on September 4, 1998..."
     📎 Sources: google_history_deep.txt
```

---

## 🔧 Configuration

### Environment Variables (.env):
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### Customize Settings (chatbot.py):
```python
FAISS_DB_PATH = "./faiss_db"           # Database location
TOP_K_CHUNKS = 4                        # Chunks to retrieve
OPENROUTER_MODEL = "openai/gpt-4o-mini" # AI model
```

### Customize Processing (ingestion_pipeline.py):
```python
DOCUMENTS_FOLDER = "./documents"  # Documents location
CHUNK_SIZE = 500                  # Chunk size
CHUNK_OVERLAP = 50                # Overlap between chunks
```

---

## 🌐 Deployment

### Quick Deploy to Streamlit Cloud:

**Option 1: Use deploy script**
```bash
deploy.bat  # Windows
```

**Option 2: Manual**
```bash
# Push to GitHub
git add .
git commit -m "Deploy ChatRAG"
git push origin main

# Then deploy on Streamlit Cloud
# See DEPLOY_INSTRUCTIONS.md for details
```

### Streamlit Cloud Setup:
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Select repository: `Raihanroo/RAG_Chabot-with-LLM-Integration-`
4. Main file: `app.py`
5. Add secret: `OPENAI_API_KEY = "your-key"`
6. Deploy!

📖 **Detailed Guide**: [DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md)

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not set"
Create `.env` file with your API key:
```env
OPENAI_API_KEY=sk-or-v1-your-key-here
```

### "FAISS database not found"
Run document ingestion:
```bash
python ingestion_pipeline.py
```

### "I don't have that information"
- Make sure documents are uploaded
- Check if documents are processed
- Try more specific questions

### PDF not loading
Install PyPDF2:
```bash
pip install PyPDF2
```

---

## 📚 Documentation

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Detailed project documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [API_GUIDE.md](API_GUIDE.md) - API documentation (FastAPI)

---

## 🛠️ Tech Stack

- **Python 3.11** - Programming language
- **Streamlit** - Web framework
- **LangChain** - RAG framework
- **FAISS** - Vector database
- **OpenRouter** - AI API access
- **GPT-4o-mini** - Language model

---

## 📝 License

MIT License - feel free to use for your projects!

---

## 🙏 Acknowledgments

- OpenRouter for AI API access
- LangChain for RAG framework
- Streamlit for web framework
- FAISS for vector search

---

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-/issues)
- **Documentation**: See PROJECT_SUMMARY.md
- **Streamlit Docs**: https://docs.streamlit.io/

---

**Made with ❤️ by Raihan**

**Star ⭐ this repo if you find it helpful!**
