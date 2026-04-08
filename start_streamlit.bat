@echo off
echo ========================================
echo   RAG Chatbot - Starting Streamlit
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file with your OPENAI_API_KEY
    pause
    exit /b 1
)

echo Starting Streamlit web app...
echo.
echo App will open automatically in your browser
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
