@echo off
echo ========================================
echo   ChatRAG - Starting Application
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with:
    echo OPENAI_API_KEY=sk-or-v1-your-key-here
    echo.
    pause
    exit /b 1
)

REM Check if faiss_db exists
if not exist faiss_db (
    echo WARNING: Documents not processed yet!
    echo.
    echo Running document ingestion...
    python ingestion_pipeline.py
    echo.
)

echo Starting ChatRAG...
echo.
echo Browser will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

streamlit run app.py
