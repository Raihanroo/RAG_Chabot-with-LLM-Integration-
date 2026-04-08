import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from chatbot import build_rag_chain, ask_question
from ingestion_pipeline import load_documents, DOCUMENTS_FOLDER, FAISS_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP

load_dotenv()

# Global chain storage
rag_chain = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global rag_chain
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not set!")
    elif os.path.exists(FAISS_DB_PATH):
        try:
            rag_chain = build_rag_chain()
            print("✅ RAG chain loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load RAG chain: {e}")
            import traceback
            traceback.print_exc()
    
    yield
    
    # Shutdown (cleanup if needed)
    print("Shutting down...")


app = FastAPI(
    title="RAG Chatbot API",
    description="AI-powered document Q&A system using RAG",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"


class AnswerResponse(BaseModel):
    answer: str
    sources: List[dict]
    session_id: str


class StatusResponse(BaseModel):
    status: str
    message: str
    details: Optional[dict] = None


@app.get("/", response_model=StatusResponse)
async def root():
    """Health check endpoint"""
    return StatusResponse(
        status="ok",
        message="RAG Chatbot API is running",
        details={
            "db_ready": os.path.exists(FAISS_DB_PATH),
            "chain_loaded": rag_chain is not None
        }
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """Ask a question to the RAG chatbot"""
    global rag_chain
    
    if not rag_chain:
        raise HTTPException(
            status_code=503,
            detail="RAG chain not initialized. Run /ingest first or check API key."
        )
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        response = ask_question(rag_chain, request.question)
        return AnswerResponse(
            answer=response["answer"],
            sources=response["sources"],
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.post("/ingest", response_model=StatusResponse)
async def ingest_documents():
    """Ingest documents from the documents folder"""
    global rag_chain
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=400, detail="OPENAI_API_KEY not set")
    
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS
        
        # Load documents
        documents = load_documents()
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found in ./documents/")
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
        )
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(FAISS_DB_PATH)
        
        # Reload chain
        rag_chain = build_rag_chain()
        
        return StatusResponse(
            status="success",
            message="Documents ingested successfully",
            details={
                "total_documents": len(documents),
                "total_chunks": len(chunks)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/upload", response_model=StatusResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to the documents folder"""
    allowed_extensions = [".txt", ".pdf", ".csv"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)
        file_path = os.path.join(DOCUMENTS_FOLDER, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return StatusResponse(
            status="success",
            message=f"File uploaded: {file.filename}",
            details={"file_path": file_path}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/documents", response_model=StatusResponse)
async def list_documents():
    """List all documents in the documents folder"""
    if not os.path.exists(DOCUMENTS_FOLDER):
        return StatusResponse(
            status="ok",
            message="No documents folder found",
            details={"documents": []}
        )
    
    files = [f for f in os.listdir(DOCUMENTS_FOLDER) if os.path.isfile(os.path.join(DOCUMENTS_FOLDER, f))]
    return StatusResponse(
        status="ok",
        message=f"Found {len(files)} document(s)",
        details={"documents": files}
    )


@app.delete("/reset", response_model=StatusResponse)
async def reset_chain():
    """Reset the RAG chain (clear conversation history)"""
    global rag_chain
    
    if rag_chain:
        rag_chain["history"] = []
        return StatusResponse(status="success", message="Chain history reset")
    
    return StatusResponse(status="ok", message="No chain to reset")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
