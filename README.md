# 🤖 ChatRAG - Multilingual AI Document Assistant

A powerful AI chatbot that reads your documents (PDF, TXT, CSV, Excel) and answers questions in both English and Bengali.

📦 **GitHub**: [Raihanroo/RAG_Chabot-with-LLM-Integration-](https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-)  
🌐 **Deploy**: Ready for [Streamlit Cloud](https://share.streamlit.io/)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🌍 **Multilingual** | Ask questions in English or Bengali, get answers in the same language |
| 📤 **Multiple Formats** | Supports PDF, TXT, CSV, Excel (XLSX/XLS) |
| 🔍 **Semantic Search** | Understands synonyms, antonyms, and context |
| 💬 **Smart Chat** | Powered by GPT-4o-mini AI |
| 📎 **Source Citations** | Shows which documents were used |
| 🎨 **Modern UI** | Dark theme, responsive design |
| ⚡ **Fast** | FAISS vector database for quick search |
| 🌐 **Cloud Ready** | Deploy to Streamlit Cloud in minutes |

---

## 🚀 Quick Start (3 Minutes)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Set API Key
Create `.env` file:
```env
OPENAI_API_KEY=sk-or-v1-your-key-here
```
Get API key from: [OpenRouter.ai](https://openrouter.ai/)

### 3️⃣ Add Documents
Put your files in `documents/` folder (PDF, TXT, CSV, Excel)

### 4️⃣ Process Documents
```bash
python ingestion_pipeline.py
```

### 5️⃣ Run App
```bash
streamlit run app.py
```
Or simply: `run.bat` (Windows)

Browser opens at: `http://localhost:8501`

---

## 💡 How to Use

### Upload Documents:

**Method 1: Via UI**
1. Sidebar → "Upload Documents" section
2. Select files
3. Click "Process Documents"

**Method 2: Via Folder**
1. Copy files to `documents/` folder
2. Run: `python ingestion_pipeline.py`

### Chat with Your Documents:

**English:**
```
"What is ACID in database?"
"Who founded Google?"
"Explain leadership principles"
```

**Bengali:**
```
"ডাটাবেসে ACID কি?"
"গুগল কে প্রতিষ্ঠা করেছে?"
"লিডারশিপ সম্পর্কে বলো"
```

**Synonyms/Mixed:**
```
"Who created Google?" (founder = creator)
"Google এর স্থাপক কে?" (প্রতিষ্ঠাতা = স্থাপক)
```

---

## 🏗️ Project Structure

```
ChatRAG/
│
├── 📱 Main Application
│   ├── app.py                    # Streamlit web interface
│   ├── chatbot.py                # RAG logic & AI brain
│   ├── ingestion_pipeline.py     # Document processing
│   └── api.py                    # FastAPI backend (optional)
│
├── 📁 Data & Storage
│   ├── documents/                # Your documents here
│   ├── faiss_db/                 # Vector database (auto-generated)
│   └── .env                      # API key (keep secret!)
│
├── 📚 Documentation
│   ├── README.md                 # This file
│   ├── COMPLETE_SUMMARY.md       # Complete guide (Bengali)
│   ├── PROJECT_SUMMARY.md        # Detailed documentation
│   ├── DEPLOY_INSTRUCTIONS.md    # Deployment guide
│   └── HOW_TO_USE.txt            # Quick reference
│
├── 🚀 Deployment Scripts
│   ├── run.bat                   # Quick start (Windows)
│   ├── deploy.bat                # GitHub push (Windows)
│   └── deploy.sh                 # Git Bash deploy (Linux/Mac)
│
└── ⚙️ Configuration
    ├── requirements.txt          # Python dependencies
    ├── .gitignore                # Git ignore rules
    └── .streamlit/config.toml    # Streamlit config
```

---

## 🔧 Technology Stack

### Backend:
- **Python 3.11** - Programming language
- **LangChain 0.2.16** - RAG framework
- **FAISS** - Vector database for fast search
- **OpenRouter API** - AI model access
- **GPT-4o-mini** - Language model
- **text-embedding-3-small** - Document embeddings

### Frontend:
- **Streamlit 1.56** - Web framework
- **Custom CSS** - Modern dark UI

### Document Processing:
- **PyPDF/PyPDF2** - PDF files
- **Pandas** - CSV & Excel files
- **OpenPyXL** - Excel XLSX files
- **XLRD** - Excel XLS files

---

## 🌐 Deployment

### 🚀 Deploy to Streamlit Cloud (Recommended)

#### Windows:
```bash
deploy.bat
```

#### Git Bash / Linux / Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Manual Deployment:

1. **Push to GitHub** (already done ✅)

2. **Go to Streamlit Cloud:**
   ```
   https://share.streamlit.io/
   ```

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure:**
   - Repository: `Raihanroo/RAG_Chabot-with-LLM-Integration-`
   - Branch: `main`
   - Main file: `app.py`

6. **Add Secrets (IMPORTANT!):**
   - Click "Advanced settings"
   - Go to "Secrets" section
   - Add:
   ```toml
   OPENAI_API_KEY = "sk-or-v1-your-actual-key"
   ```

7. **Click "Deploy!"**

Wait 2-3 minutes and your app will be live! 🎉

---

## 📊 How It Works

### Step-by-Step Process:

```
1. Document Upload
   ↓
2. Text Extraction (PDF/TXT/CSV/Excel)
   ↓
3. Chunking (500 chars with 50 overlap)
   ↓
4. Embeddings (Convert to numbers)
   ↓
5. FAISS Database (Store for fast search)
   ↓
6. User Question
   ↓
7. Semantic Search (Find relevant chunks)
   ↓
8. Context Building (Top 6 chunks)
   ↓
9. AI Processing (GPT-4o-mini)
   ↓
10. Answer + Sources
```

### Example Flow:

```
Question: "Who founded Google?"
         ↓
Embedding: [0.23, -0.45, 0.78, ...]
         ↓
FAISS Search: Find similar chunks
         ↓
Context: "Google was founded by Larry Page and Sergey Brin..."
         ↓
AI: "Google was founded by Larry Page and Sergey Brin in 1998."
         ↓
Sources: 📄 google_history_deep.txt
```

---

## 🎯 Key Features Explained

### 1. Multilingual Support
- **Understands**: English, Bengali, Mixed languages
- **Responds**: Same language as question
- **Smart**: Automatic language detection

### 2. Semantic Search
- **Synonyms**: founder = creator = প্রতিষ্ঠাতা
- **Context**: Understands meaning, not just words
- **Flexible**: Different phrasings work

### 3. Document Types
- **PDF**: Multi-page documents
- **TXT**: Plain text files
- **CSV**: Tabular data
- **Excel**: XLSX and XLS files

### 4. Source Citations
- Shows which document was used
- Page numbers (for PDFs)
- Preview of relevant text

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not set"
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-or-v1-your-key" > .env
```

### "FAISS database not found"
```bash
python ingestion_pipeline.py
```

### "I don't have that information"
- ✅ Check documents are uploaded
- ✅ Run ingestion pipeline
- ✅ Try more specific questions
- ✅ Check document content

### PDF not loading
```bash
pip install PyPDF2 pypdf
```

### Excel not loading
```bash
pip install pandas openpyxl xlrd
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [COMPLETE_SUMMARY.md](COMPLETE_SUMMARY.md) | Complete guide in Bengali - Everything in one place |
| [README.md](README.md) | This file - Quick overview in English |

---

## ⚙️ Configuration

### Environment Variables (.env):
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### Chatbot Settings (chatbot.py):
```python
FAISS_DB_PATH = "./faiss_db"           # Database location
TOP_K_CHUNKS = 6                        # Chunks to retrieve
OPENROUTER_MODEL = "openai/gpt-4o-mini" # AI model
```

### Processing Settings (ingestion_pipeline.py):
```python
DOCUMENTS_FOLDER = "./documents"  # Documents location
CHUNK_SIZE = 500                  # Chunk size (characters)
CHUNK_OVERLAP = 50                # Overlap between chunks
```

---

## 🔐 Security & Privacy

- ❌ Never commit `.env` file
- ✅ Use `.gitignore` properly
- ✅ Use Streamlit Secrets for cloud
- ✅ Rotate API keys regularly
- ✅ Keep documents private

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Document Load | < 1 second |
| Chunking | < 0.5 seconds |
| Embedding (per chunk) | ~0.1 seconds |
| Search | < 0.2 seconds |
| AI Response | 1-3 seconds |
| Supported Files | PDF, TXT, CSV, XLSX, XLS |
| Chunks Retrieved | 6 (configurable) |

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - Free to use for personal and commercial projects

---

## 🙏 Acknowledgments

- **OpenRouter** - AI API access
- **LangChain** - RAG framework
- **Streamlit** - Web framework
- **FAISS** - Vector search
- **OpenAI** - Embedding models

---

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-/issues)
📚 **Documentation**: [COMPLETE_SUMMARY.md](COMPLETE_SUMMARY.md) (Bengali) | [README.md](README.md) (English)
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io/)

---

## 🎓 Learn More

- **LangChain Docs**: [python.langchain.com](https://python.langchain.com/)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io/)

---

## ⭐ Star This Repo!

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ by Raihan**

**🚀 Ready to chat with your documents? Let's go!**
 
