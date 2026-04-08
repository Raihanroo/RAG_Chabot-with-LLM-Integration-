# 🚀 Deployment Guide - ChatRAG

## 📦 GitHub এ Upload করার নিয়ম

### Step 1: Git Initialize (যদি না করা থাকে)
```bash
git init
git add .
git commit -m "Initial commit: ChatRAG with modern UI"
```

### Step 2: GitHub Repository এ Push করো
```bash
git remote add origin https://github.com/Raihanroo/RAG_Chabot-with-LLM-Integration-.git
git branch -M main
git push -u origin main
```

---

## ☁️ Streamlit Cloud এ Deploy করার নিয়ম

### Step 1: Streamlit Cloud এ যাও
1. https://share.streamlit.io/ এ যাও
2. তোমার GitHub account দিয়ে login করো

### Step 2: New App Deploy করো
1. **"New app"** button এ click করো
2. Repository select করো: `Raihanroo/RAG_Chabot-with-LLM-Integration-`
3. Branch: `main`
4. Main file path: `app.py`
5. **"Deploy!"** button এ click করো

### Step 3: Secrets Add করো
1. Deploy হওয়ার পর **"Settings"** এ যাও
2. **"Secrets"** section এ যাও
3. এই content add করো:
```toml
OPENAI_API_KEY = "sk-or-v1-your-actual-api-key-here"
```
4. **"Save"** button এ click করো

### Step 4: App Restart করো
App automatically restart হবে এবং তোমার ChatRAG live হয়ে যাবে!

---

## 🌐 Deployment URLs

### Local Development:
- **FastAPI**: http://localhost:8000
- **Streamlit**: http://localhost:8501
- **Modern UI**: index.html (file:// protocol)

### Production (Streamlit Cloud):
- **Your App**: https://share.streamlit.io/raihanroo/rag_chabot-with-llm-integration-/main/app.py

---

## ⚙️ Environment Variables

### Local (.env file):
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### Streamlit Cloud (Secrets):
```toml
OPENAI_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
```

---

## 📝 Pre-Deployment Checklist

✅ `.env` file আছে কিনা check করো (local এর জন্য)
✅ `requirements.txt` updated আছে কিনা
✅ `.gitignore` file আছে কিনা (sensitive files exclude করার জন্য)
✅ `documents/` folder এ sample documents আছে কিনা
✅ README.md updated আছে কিনা

---

## 🔧 Troubleshooting

### Issue 1: "Module not found" error
**Solution:** `requirements.txt` এ সব dependencies আছে কিনা check করো

### Issue 2: "OPENAI_API_KEY not set"
**Solution:** Streamlit Cloud Secrets এ API key properly add করেছো কিনা check করো

### Issue 3: Documents not loading
**Solution:** 
- `documents/` folder এ files আছে কিনা check করো
- `ingestion_pipeline.py` run করো locally test করার জন্য

### Issue 4: App crashes on startup
**Solution:**
- Streamlit Cloud logs check করো
- Local এ `streamlit run app.py` run করে test করো

---

## 🎯 Quick Deploy Commands

```bash
# 1. Commit changes
git add .
git commit -m "Update: Modern UI and fixes"

# 2. Push to GitHub
git push origin main

# 3. Streamlit Cloud automatically redeploys!
```

---

## 📊 Monitoring

### Streamlit Cloud Dashboard:
- App status check করো
- Logs দেখো
- Resource usage monitor করো
- Analytics দেখো

### Local Monitoring:
```bash
# API logs
python api.py

# Streamlit logs
streamlit run app.py
```

---

## 🔐 Security Best Practices

1. ❌ **Never commit `.env` file** to GitHub
2. ✅ Use Streamlit Secrets for API keys
3. ✅ Add `.env` to `.gitignore`
4. ✅ Use environment variables for sensitive data
5. ✅ Regularly rotate API keys

---

## 🚀 Continuous Deployment

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main

# Streamlit Cloud automatically detects and redeploys!
```

---

## 📞 Support

যদি কোনো সমস্যা হয়:
1. Streamlit Community Forum: https://discuss.streamlit.io/
2. GitHub Issues: Create an issue in your repository
3. Streamlit Docs: https://docs.streamlit.io/

---

## ✅ Success Indicators

Deploy successful হলে:
- ✅ App URL accessible হবে
- ✅ UI properly load হবে
- ✅ Documents upload করতে পারবে
- ✅ Chat functionality কাজ করবে
- ✅ No errors in logs

---

Happy Deploying! 🎉
