RAG Chatbot Project Summary
AI-Powered Document Q&A System Using Google Gemini
==================
Project Overview
==================
This project is a Retrieval-Augmented Generation (RAG) Chatbot that allows users to ask questions about their documents and receive intelligent, context-aware answers. The system combines document retrieval with Google's Gemini AI model to provide accurate responses based on the content of uploaded documents. The application features a user-friendly web interface built with Streamlit and supports multiple document formats including PDF, text files, CSV, and web pages.

System Architecture:

┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│                  (Streamlit Web App)                        │
│  • Chat interface with conversation history                 │
│  • Sidebar for API configuration                            │
│  • Source display with expandable sections                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CHATBOT ENGINE                            │
│              (LangChain + Gemini LLM)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Question Processing                              │   │
│  │  2. Document Retrieval (ChromaDB)                    │   │
│  │  3. Context Building with History                    │   │
│  │  4. Response Generation via Gemini 1.5 Flash         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  VECTOR DATABASE                            │
│                    (ChromaDB)                               │
│  • Stores document embeddings (1024 dimensions)             │
│  • Enables semantic similarity search                       │
│  • Persistent storage for reusability                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 DATA INGESTION                              │
│              (Ingestion Pipeline)                           │
│  • PDF files (page-level processing)                        │
│  • Text files (.txt, .md)                                   │
│  • CSV files (tabular data)                                 │
│  • Web pages (URL ingestion)                                │
│  • Chunking: 500 chars with 50 overlap                      │

└─────────────────────────────────────────────────────────────┘

Technology Stack:

Component	Technology	Version/Purpose
LLM Model	Google Gemini 1.5 Flash	Fast, efficient responses
Embeddings	Google Generative AI Embeddings	model: embedding-001
Vector Database	ChromaDB	Persistent vector storage
Framework	LangChain	Orchestration & chains
Frontend	Streamlit	Web interface
Document Loaders	PyPDF2, TextLoader, CSVLoader, WebBaseLoader	Multi-format support
Programming Language	Python	3.8+

📁 Project Structure

rag-chatbot-project/
│
├── app.py                      # Streamlit web application (main UI)
├── chatbot.py                  # Core RAG logic and conversation handling
├── ingestion_pipeline.py       # Document loading and vector indexing
├── .env                        # Environment variables (API keys)
├── requirements.txt            # Python dependencies
│
├── documents/                  # Source documents folder
│   ├── *.pdf                   # PDF documents
│   ├── *.txt                   # Text files
│   ├── *.csv                   # CSV data files
│   └── *.url                   # Web page URLs (optional)
│
├── chroma_db/                  # Vector database storage
│   ├── chroma.sqlite3          # SQLite database
│   └── *.parquet               # Embedding storage
│
└── README.md                   # Project documentation

Core Features:

1. Multi-format Document Support
✅ PDF files: With page-level metadata tracking

✅ Text files: Plain text documents (.txt, .md)

✅ CSV files: Tabular data with row-by-row processing

✅ Web pages: URL-based content extraction

2. Intelligent Document Processing:

Smart Chunking: Documents split into 500-character chunks with 50-character overlap for context preservation

Semantic Retrieval: Returns top 4 most relevant chunks per query using cosine similarity

Source Tracking: Maintains complete metadata (filename, page number, chunk ID) for each retrieved chunk

Batch Processing: Handles documents in batches of 100 to manage API rate limits

3. Conversational Interface:

Chat History: Maintains conversation context (last 4 exchanges)

Source Citation: Displays exact documents and pages used for each answer

Session Management: Clear conversation option with one click

Real-time Generation: Streaming-like experience with loading indicators

4. User Experience:
   
Sidebar Configuration: API key input with status indicators

Document Status: Visual feedback on indexed documents

Source Visibility: Toggle to show/hide source citations

Bilingual UI: Bangla (Bengali) language support in interface elements

Responsive Design: Works on desktop and tablet devices

🔄 Data Flow:

Ingestion Pipeline (ingestion_pipeline.py)
Document Discovery: Scan documents/ folder for all supported file types

Document Loading:

PDFs: Loaded with PyPDFLoader, each page as separate document

Text files: Loaded with TextLoader (UTF-8 encoding)

CSV files: Loaded with CSVLoader, each row as document

URLs: Loaded with WebBaseLoader, entire page as document

Text Splitting: Split documents using RecursiveCharacterTextSplitter

Chunk size: 500 characters

Overlap: 50 characters

Separators: ["\n\n", "\n", " ", ""]

Embedding Generation: Create embeddings using Google's embedding-001 model

Vector Storage: Store in ChromaDB with metadata preservation

Persistence: Database saved to ./chroma_db for reuse

Query Processing (chatbot.py)
Question Submission: User submits question through UI

Semantic Search: Retriever finds top 4 relevant chunks (k=4)

Context Assembly: Retrieved chunks concatenated with separators

History Integration: Last 4 conversation exchanges added to context

Prompt Engineering: Structured prompt with instructions:

"Answer using ONLY this context"

"If not in context, say: I don't have that information"

LLM Invocation: Gemini 1.5 Flash generates answer (temperature=0)

Source Extraction: Metadata extracted from retrieved documents

Response Return: Answer with sources delivered to UI

Web Interface (app.py)
Initialization: Check API key and vector database availability

Session State: Maintain conversation history in Streamlit session

Message Display: Render chat history with role-based styling

User Input: Chat input field with question submission

Processing: Display loading spinner during LLM invocation

Source Display: Expandable sections showing document sources

Error Handling: Graceful error messages with troubleshooting tips

🎯 Technical Specifications:
Configuration Parameters

Parameter	Value	Description
Chunk Size	500 characters	Size of each document chunk
Chunk Overlap	50 characters	Overlap between consecutive chunks
Retrieved Chunks (k)	4	Number of chunks retrieved per query
Gemini Model	gemini-1.5-flash	LLM model for response generation
Embedding Model	models/embedding-001	Model for generating embeddings
Temperature	0	Deterministic responses (no randomness)
Max Retries	6	API retry attempts on failure
Batch Size	100	Documents per batch during ingestion
Batch Delay	2 seconds	Delay between batches for rate limiting
History Length	4 exchanges	Conversation history maintained

Performance :

Metric	Value
Response Time	2-5 seconds (depending on context size)
Embedding Dimension	1024
Max Document Size	Limited by API (typically 2MB per file)
Database Size	~1-5 MB per 1000 chunks
Concurrent Users	Single user (can be scaled)

Running the Application:
# Python 3.8 or higher required
python --version

# Install dependencies
pip install streamlit langchain langchain-google-genai langchain-chroma chromadb pypdf python-dotenv

# Set up environment
echo "GOOGLE_API_KEY=your_api_key_here" > .env

Step-by-Step Execution:
Add Documents:
# Place files in documents/ folder
cp your_document.pdf documents/
cp your_data.csv documents/

Ingest Data:
python ingestion_pipeline.py

Expected :
==================================================
  RAG Chatbot - Ingestion Pipeline (Gemini)
==================================================

[Step 1] Loading documents...
  [PDF Files]
  Loading PDF: document.pdf
    → Loaded 10 pages

[Step 2] Splitting into chunks...
  Created 247 chunks

[Step 3] Creating vector store...
  Saved 100 chunks...
  Saved 200 chunks...
  Saved 247 chunks...

==================================================
  Ingestion complete!
==================================================

Launch Application:
===================
streamlit run app.py

Opens browser at http://localhost:8501

Configure API Key

Enter API key in sidebar (if not in .env)

Or verify existing key is loaded

Start Chatting

Ask questions about your documents

View sources in expandable sections

Clear conversation as needed

Performance Features
Optimizations Implemented
Batch Processing: Documents processed in batches of 100 to:

Manage API rate limits

Reduce memory usage

Provide progress feedback

Retry Logic: Built-in retry mechanism with:

Max 6 retries for transient failures

Exponential backoff (implicit in LangChain)

Efficient Storage:

Persistent vector database eliminates re-indexing

ChromaDB optimizes query performance with HNSW indexing

Session Persistence:

Conversation history maintained during session

Vector database persists across application restarts

Memory Management:

Only relevant chunks loaded per query

Chat history limited to last 4 exchanges


User Interface Highlights
Design Elements
Clean, Modern Design: Custom CSS for source box with left border accent

Responsive Layout: Centered content with fixed-width sidebar

Real-time Feedback: Loading spinners during processing

Visual Status Indicators:

✅ Green success messages

❌ Red error alerts

⚠️ Yellow warnings

ℹ️ Blue information

Interactive Components:

Component	Functionality:

Chat Input	Text box with placeholder in Bangla
Sidebar	Configuration and status panel
API Key Input	Password field with visual feedback
Sources Toggle	Show/hide document sources
Clear Button	Reset conversation history
Expandable Sources	Collapsible sections for sources

Source Display Format:
📄 filename.pdf · page 3
📄 data.csv
📄 manual.txt · page 12

Security Considerations:
Implemented Security Features
API Key Management

Stored in environment variables (not hardcoded)

Password field in UI (input type="password")

Not persisted in session state

Data Privacy

No user data transmitted externally (except Gemini API)

Local vector database storage

Conversation history cleared on session reset

Error Handling

Graceful failures without exposing system details

User-friendly error messages

No stack traces displayed to users

Potential Risks & Mitigations

Risk	Mitigation

API key exposure	Use .env files, never commit to version control
Large document DoS	Chunk size limits, rate limiting
Sensitive data	Local deployment only, no cloud storage
API rate limits	Batch processing with delays, retry logic

Potential Enhancements
Short-term Improvements
Document Management

Add ability to add/remove documents without re-indexing

Implement incremental updates

Enhanced Search

Hybrid search (semantic + keyword)

Metadata filtering

Export Capabilities

Export conversations as PDF/JSON

Share conversation links

Advanced UI

Dark mode support

Mobile-responsive improvements

Long-term Enhancements
Multi-user Support

User authentication

Separate vector spaces per user

Session persistence across logins

Advanced Analytics

Question-answer analytics

Document usage statistics

Response quality metrics

Integration Features

Slack/Discord bot integration

API endpoints for external services

Webhook support

Enhanced LLM Capabilities

Streaming responses

Multiple model support (GPT-4, Claude)

Fine-tuning on domain-specific data

Enterprise Features

Role-based access control

Audit logging

Compliance certifications:
Use Cases
Academic Research
Query research papers stored as PDFs

Extract specific methodologies from papers

Compare findings across multiple documents

Literature review assistance

Legal Document Review
Extract specific clauses from contracts

Find precedents in case law documents

Analyze compliance requirements

Quick reference to legal terms

Customer Support
Query knowledge base documents

Provide instant answers to common questions

Troubleshooting guides accessible via chat

Product documentation search

Data Analysis
Query CSV data in natural language

Extract insights from spreadsheets

Business intelligence queries

Report generation assistance

Technical Documentation:

Get answers from API documentation

Search through code documentation

Troubleshoot with error message lookup

Quick reference to technical specs

System Requirements
Component	Minimum Requirement
Python	3.8 or higher
RAM	4GB (8GB recommended)
Storage	1GB for vector database
Internet	Required for Gemini API
API Key	Valid Google AI Studio API key

🏁 Conclusion
This RAG Chatbot provides a robust, production-ready solution for document-based question answering. It successfully combines modern AI capabilities with practical usability, offering a scalable foundation for various document-intensive applications. The system is completely free to use (Gemini's free tier) and can be deployed locally or on any cloud platform.

Prepared for Supervisor Review | Project Status: Complete and Functional
