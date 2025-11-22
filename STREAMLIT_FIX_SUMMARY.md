# Streamlit Deployment Fix - Summary

## 🐛 The Problem

You were getting a **numpy version conflict error** when deploying to Streamlit Cloud:

```
ERROR: Cannot install ... numpy==2.3.5 ...
streamlit 1.28.0 depends on numpy<2 and >=1.19.3
```

**Root Cause**: Your `requirements.txt` had `numpy==2.3.5`, but Streamlit 1.28.0 requires `numpy<2.0`.

## ✅ The Solution

I've created **three separate requirements files** for different deployment scenarios:

### 1. `requirements.txt` (Local Development)
- For running both Flask backend AND Streamlit frontend locally
- Balanced versions compatible with Streamlit
- Key change: `numpy>=1.24.0,<2.0.0` (instead of 2.3.5)

### 2. `requirements-backend.txt` (Flask Backend Deployment)
- For deploying ONLY the Flask backend to Railway/Heroku/Render
- Includes PyTorch, YOLO, HerdNet, Flask, etc.
- Excludes Streamlit (not needed for backend)

### 3. `requirements-streamlit.txt` (Streamlit Cloud Deployment) ⭐
- **USE THIS ONE for Streamlit Cloud!**
- Minimal dependencies for frontend only
- Just: streamlit, requests, pandas, plotly, pillow
- No heavy ML libraries (PyTorch, YOLO, etc.)

## 🎯 How to Deploy to Streamlit Cloud

### Step 1: Deploy Backend FIRST

The Streamlit app is just a UI - it needs the Flask backend API to actually process images.

**Option A: Railway (Recommended)**
1. Push code to GitHub
2. Go to https://railway.app
3. Create new project from your repo
4. Rename `requirements-backend.txt` to `requirements.txt` (or configure Railway to use it)
5. Get your backend URL (e.g., `https://your-app.railway.app`)

**Option B: Heroku**
```bash
cp requirements-backend.txt requirements.txt
heroku create wildlife-api
git push heroku main
```

### Step 2: Deploy Frontend to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://streamlit.io/cloud
2. **New App** → Select your repository
3. **Advanced Settings**:
   - **Python version**: 3.11
   - **Requirements file**: `requirements-streamlit.txt`
   - **Secrets** (IMPORTANT!):
     ```toml
     API_BASE_URL = "https://your-backend.railway.app"
     ```
4. **Deploy!**

## 📁 New Files Created

```
✅ requirements.txt              - Local development (both services)
✅ requirements-backend.txt      - Flask backend only
✅ requirements-streamlit.txt    - Streamlit frontend only ⭐
✅ packages.txt                  - System dependencies for Streamlit
✅ .streamlit/config.toml        - Streamlit configuration
✅ .streamlit/secrets.toml.example - Secrets template
✅ STREAMLIT_DEPLOYMENT_GUIDE.md - Detailed deployment guide
```

## 🔧 Configuration Changes

### streamlit_app.py
Updated to read API endpoint from environment/secrets:
```python
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    st.secrets.get("API_BASE_URL", "http://localhost:8000")
)
```

This allows you to:
- Use `http://localhost:8000` for local development
- Override with backend URL for production

## 📋 Quick Reference

### For Local Development
```bash
pip install -r requirements.txt
./start.sh  # Starts both backend + frontend
```

### For Streamlit Cloud Deployment
1. Deploy backend first (Railway/Heroku/Render)
2. Use `requirements-streamlit.txt`
3. Set `API_BASE_URL` secret in Streamlit Cloud
4. Deploy!

## ⚠️ Important Notes

### Why Separate Deployment?

Streamlit Cloud is **frontend-only** hosting. It can't run heavy ML models efficiently. That's why we:

1. **Backend** (Flask + ML models) → Railway/Heroku (has more resources)
2. **Frontend** (Streamlit UI) → Streamlit Cloud (free, optimized for Streamlit)

### Cost
- **Streamlit Cloud**: Free! (1 private + 3 public apps)
- **Railway**: $5/month free credit (enough for most projects)
- **Render**: Free tier available

### Models
Models still auto-download from Google Drive on the **backend** deployment. No changes needed there!

## 🧪 Testing

### Test Backend
```bash
curl https://your-backend.railway.app/health
```

Expected:
```json
{
  "status": "healthy",
  "models": {...}
}
```

### Test Frontend
1. Open your Streamlit app URL
2. Try uploading a ZIP file
3. Should connect to backend and process images

## 📚 Documentation

- **Full deployment guide**: [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)
- **Main README**: [README.md](README.md)

## 🎉 Summary

**The fix**: Use `requirements-streamlit.txt` for Streamlit Cloud deployment, with numpy<2.0

**The architecture**: Deploy backend and frontend separately

**The result**: Your app will work on Streamlit Cloud! 🚀

---

**Next Steps:**
1. Deploy backend to Railway (5 minutes)
2. Get backend URL
3. Deploy frontend to Streamlit Cloud (5 minutes)
4. Add `API_BASE_URL` secret pointing to backend
5. Done! ✅

