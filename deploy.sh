#!/bin/bash

# ChatRAG - GitHub Deployment Script for Git Bash/Linux/Mac

clear
echo "========================================"
echo "  ChatRAG - GitHub Deployment"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "[1/5] Initializing Git repository..."
    git init
    echo ""
else
    echo "[1/5] Git repository already initialized"
    echo ""
fi

echo "[2/5] Adding files to Git..."
git add .
echo ""

echo "[3/5] Enter commit message:"
read -p "Commit message (press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy ChatRAG - Multilingual AI Document Assistant"
fi
echo ""

echo "[4/5] Committing changes..."
git commit -m "$commit_msg"
echo ""

echo "[5/5] Checking remote repository..."
if ! git remote | grep -q "origin"; then
    echo "Adding remote repository..."
    git remote add origin https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-.git
    echo ""
fi

echo "Pushing to GitHub..."
git branch -M main
git push -u origin main
echo ""

echo "========================================"
echo "  ✅ Successfully Pushed to GitHub!"
echo "========================================"
echo ""
echo "🌐 Next Steps - Deploy to Streamlit Cloud:"
echo ""
echo "1. Go to: https://share.streamlit.io/"
echo "2. Click 'New app'"
echo "3. Select your repository:"
echo "   Repository: Raihanroo/RAG_Chabot-with-LLM-Integration-"
echo "   Branch: main"
echo "   Main file: app.py"
echo ""
echo "4. Add Secret (IMPORTANT!):"
echo "   Go to Advanced settings > Secrets"
echo "   Add: OPENAI_API_KEY = \"sk-or-v1-your-key\""
echo ""
echo "5. Click 'Deploy!'"
echo ""
echo "📖 See DEPLOY_INSTRUCTIONS.md for detailed guide"
echo "========================================"
echo ""
read -p "Press Enter to exit..."
