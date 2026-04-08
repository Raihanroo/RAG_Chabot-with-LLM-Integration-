# 🚀 GitHub Push & Streamlit Cloud Deployment Guide

## 📦 Step 1: GitHub এ Push করো

### Option 1: deploy.bat ব্যবহার করো (Easiest)
```bash
deploy.bat
```

### Option 2: Manual Commands
```bash
# Git initialize (যদি না করা থাকে)
git init

# All files add করো
git add .

# Commit করো
git commit -m "Deploy ChatRAG - Multilingual AI Document Assistant"

# Remote add করো (যদি না করা থাকে)
git remote add origin https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-.git

# Push করো
git branch -M main
git push -u origin main
```

---

## ☁️ Step 2: Streamlit Cloud এ Deploy করো

### 1. Streamlit Cloud এ যাও
```
https://share.streamlit.io/
```

### 2. Sign In করো
- GitHub account দিয়ে login করো

### 3. New App Create করো
- **"New app"** button এ click করো
- অথবা: **"Create app"** → **"From existing repo"**

### 4. Repository Settings
```
Repository: Raihanroo/RAG_Chabot-with-LLM-Integration-
Branch: main
Main file path: app.py
```

### 5. Advanced Settings (Optional)
- Python version: 3.11
- Click **"Advanced settings"** if needed

### 6. Secrets Add করো (IMPORTANT!)
**"Advanced settings"** → **"Secrets"** section এ যাও

Add this:
```toml
OPENAI_API_KEY = "sk-or-v1-your-actual-api-key-here"
```

⚠️ **Important:** তোমার actual API key দিয়ে replace করো!

### 7. Deploy!
- **"Deploy!"** button এ click করো
- Wait করো 2-3 minutes
- Done! 🎉

---

## 🌐 Your App URL

Deploy হওয়ার পর তোমার app এই URL এ available হবে:
```
https://share.streamlit.io/raihanroo/rag_chabot-with-llm-integration-/main/app.py
```

অথবা custom subdomain:
```
https://raihanroo-rag-chabot.streamlit.app
```

---

## 📝 Pre-Deployment Checklist

✅ `.env` file `.gitignore` এ আছে (committed হবে না)
✅ `requirements.txt` updated আছে
✅ `app.py` properly configured
✅ Documents folder এ sample files আছে
✅ README.md updated
✅ All code tested locally

---

## 🔧 Troubleshooting

### Issue 1: "Module not found"
**Solution:** 
- Check `requirements.txt` এ সব dependencies আছে কিনা
- Streamlit Cloud logs check করো

### Issue 2: "OPENAI_API_KEY not set"
**Solution:**
- Streamlit Cloud Secrets properly add করেছো কিনা check করো
- Format ঠিক আছে কিনা check করো (TOML format)

### Issue 3: App crashes on startup
**Solution:**
- Local এ test করো: `streamlit run app.py`
- Logs check করো Streamlit Cloud dashboard এ
- Python version check করো (3.11 recommended)

### Issue 4: Documents not loading
**Solution:**
- `documents/` folder এ sample files আছে কিনা check করো
- First time এ user কে documents upload করতে বলো

---

## 🔄 Update Deployment

যখন code change করবে:

```bash
# Changes commit করো
git add .
git commit -m "Update: Your changes"

# Push করো
git push origin main

# Streamlit Cloud automatically redeploy করবে! ✨
```

---

## 📊 Monitor Your App

### Streamlit Cloud Dashboard:
1. Go to: https://share.streamlit.io/
2. Click on your app
3. View:
   - ✅ App status
   - 📊 Analytics
   - 📝 Logs
   - ⚙️ Settings

---

## 🎯 Post-Deployment

### Share Your App:
```
Direct Link: https://your-app-url.streamlit.app
GitHub: https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-
```

### Add to README:
```markdown
🌐 **Live Demo**: [ChatRAG on Streamlit Cloud](https://your-app-url.streamlit.app)
```

---

## 🔐 Security Notes

1. ❌ **Never commit `.env` file**
2. ✅ Always use Streamlit Secrets for API keys
3. ✅ Keep `.gitignore` updated
4. ✅ Regularly rotate API keys
5. ✅ Monitor usage on OpenRouter dashboard

---

## 💡 Tips

- **First deployment** takes 2-3 minutes
- **Redeployments** are faster (1-2 minutes)
- **Free tier** has resource limits
- **Custom domain** available on paid plans
- **Analytics** available in dashboard

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Create an issue in your repo

---

**Ready to deploy? Let's go! 🚀**
