@echo off
cls
echo ========================================
echo   ChatRAG - GitHub Deployment
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo [1/5] Initializing Git repository...
    git init
    echo.
) else (
    echo [1/5] Git repository already initialized
    echo.
)

echo [2/5] Adding files to Git...
git add .
echo.

echo [3/5] Enter commit message:
set /p commit_msg="Commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Deploy ChatRAG - Multilingual AI Document Assistant
echo.

echo [4/5] Committing changes...
git commit -m "%commit_msg%"
echo.

echo [5/5] Checking remote repository...
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo Adding remote repository...
    git remote add origin https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-.git
    echo.
)

echo Pushing to GitHub...
git branch -M main
git push -u origin main
echo.

echo ========================================
echo   ✅ Successfully Pushed to GitHub!
echo ========================================
echo.
echo 🌐 Next Steps - Deploy to Streamlit Cloud:
echo.
echo 1. Go to: https://share.streamlit.io/
echo 2. Click "New app"
echo 3. Select your repository:
echo    Repository: Raihanroo/RAG_Chabot-with-LLM-Integration-
echo    Branch: main
echo    Main file: app.py
echo.
echo 4. Add Secret (IMPORTANT!):
echo    Go to Advanced settings ^> Secrets
echo    Add: OPENAI_API_KEY = "sk-or-v1-your-key"
echo.
echo 5. Click "Deploy!"
echo.
echo 📖 See DEPLOY_INSTRUCTIONS.md for detailed guide
echo ========================================
echo.
pause
