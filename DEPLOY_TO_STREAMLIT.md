# 🚀 Deploy to Streamlit Cloud - Quick Start

## ⚡ 5-Minute Deployment Guide

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Backend deployed (see Step 1)

---

## Step 1: Deploy Backend (5 min)

Choose ONE option:

### Option A: Railway (Recommended - Easiest)

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **New Project** → "Deploy from GitHub repo"
4. **Select** your repository
5. **Environment Variables**: Add this:
   ```
   PORT=8000
   ```
6. **Wait** for deployment (~3 minutes)
7. **Copy** your Railway URL: `https://your-app.railway.app`

✅ **Done!** Backend is live.

### Option B: Render (Free Tier)

1. **Go to Render**: https://render.com
2. **New** → **Web Service**
3. **Connect** your GitHub repo
4. **Build Command**: `pip install -r requirements-backend.txt`
5. **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. **Deploy** and copy your URL

---

## Step 2: Deploy Frontend to Streamlit Cloud (5 min)

1. **Go to Streamlit Cloud**: https://streamlit.io/cloud

2. **Sign in** with GitHub

3. **New app**:
   - Repository: Your repo
   - Branch: `main`
   - Main file: `streamlit_app.py`

4. **Advanced settings** → Click it!

5. **Python version**: `3.11`

6. **Requirements file**: Type this exactly:
   ```
   requirements-streamlit.txt
   ```

7. **Secrets** → Add this (IMPORTANT!):
   ```toml
   API_BASE_URL = "https://your-backend.railway.app"
   ```
   ⚠️ **Replace with YOUR actual backend URL from Step 1!**

8. **Deploy!** (Wait ~5 minutes)

---

## ✅ Verify It Works

### Test 1: Backend Health Check
Open in browser: `https://your-backend.railway.app/health`

Should see:
```json
{
  "status": "healthy",
  "models": {...}
}
```

### Test 2: Streamlit App
1. Open your Streamlit app URL
2. Go to "New Analysis"
3. Upload a test ZIP file
4. Should process successfully!

---

## 🐛 Troubleshooting

### "Cannot connect to API"
- **Fix**: Check `API_BASE_URL` in Streamlit secrets
- Make sure it matches your backend URL exactly
- No trailing slash!

### Backend not responding
- **Fix**: Check Railway/Render logs
- Make sure models downloaded (first run takes 5-10 min)
- Visit `/health` endpoint to verify

### Dependency errors on Streamlit
- **Fix**: Verify you set requirements file to `requirements-streamlit.txt`
- Clear cache and redeploy

---

## 📋 Deployment Checklist

**Backend (Railway/Render):**
- [ ] Code pushed to GitHub
- [ ] Backend deployed
- [ ] Backend URL copied
- [ ] `/health` endpoint works

**Frontend (Streamlit Cloud):**
- [ ] App created
- [ ] Requirements file: `requirements-streamlit.txt`
- [ ] `API_BASE_URL` secret set
- [ ] App deployed successfully
- [ ] Can upload and analyze images

---

## 💡 Pro Tips

1. **First deployment** takes longer (models download)
2. **Free tier limits**: Railway gives $5/month free credit
3. **Monitor usage**: Check Railway/Streamlit dashboards
4. **Environment**: Backend runs 24/7, Streamlit sleeps when inactive

---

## 📞 Need Help?

- Full guide: [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)
- Fix summary: [STREAMLIT_FIX_SUMMARY.md](STREAMLIT_FIX_SUMMARY.md)
- Main docs: [README.md](README.md)

---

## 🎉 That's It!

Your Wildlife Detection System is now live on Streamlit Cloud! 🦁

Share your URL: `https://your-app.streamlit.app`

