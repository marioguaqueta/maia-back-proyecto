# Streamlit Cloud Deployment Guide

This guide explains how to deploy the Wildlife Detection System to Streamlit Cloud.

## 🎯 Architecture Overview

The system has two components:

1. **Flask Backend (API)** - Runs the ML models and handles image processing
2. **Streamlit Frontend (UI)** - Provides the web interface

For cloud deployment, you need to deploy these **separately**:
- **Backend**: Deploy to Heroku, Railway, Render, or any Python hosting
- **Frontend**: Deploy to Streamlit Cloud (free!)

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Backend deployed somewhere accessible (see Backend Deployment section)

---

## Part 1: Deploy Flask Backend

You need to deploy the Flask backend FIRST so the Streamlit app has an API to connect to.

### Option A: Deploy to Railway (Recommended - Free Tier)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push
   ```

2. **Deploy to Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the Flask app

3. **Configure Railway**
   - Add environment variables:
     ```
     PORT=8000
     ```
   - Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Use `requirements-backend.txt`: Rename it to `requirements.txt` for Railway

4. **Get your backend URL**
   - Railway will give you a URL like: `https://your-app-name.railway.app`
   - Save this URL - you'll need it for Streamlit!

### Option B: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   # or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-wildlife-api
   ```

3. **Create Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

4. **Use backend requirements**
   ```bash
   cp requirements-backend.txt requirements.txt
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Get your URL**: `https://your-wildlife-api.herokuapp.com`

### Option C: Deploy to Render

1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements-backend.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Deploy and get your URL

---

## Part 2: Deploy Streamlit Frontend to Streamlit Cloud

### Step 1: Prepare Repository

1. **Ensure these files exist in your repo:**
   ```
   ✓ streamlit_app.py
   ✓ requirements-streamlit.txt
   ✓ packages.txt
   ✓ .streamlit/config.toml
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud"
   git push origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository
   - Select branch (usually `main`)
   - Set main file path: `streamlit_app.py`
   - Click "Advanced settings"

3. **Configure Advanced Settings**

   **Python version**: `3.11`

   **Requirements file**: `requirements-streamlit.txt`

   **Secrets** (IMPORTANT!):
   ```toml
   API_BASE_URL = "https://your-backend-url.railway.app"
   ```
   Replace with your actual backend URL from Part 1!

4. **Deploy**
   - Click "Deploy!"
   - Wait 5-10 minutes for first deployment
   - Your app will be available at: `https://your-app-name.streamlit.app`

---

## 🔧 Configuration

### Configure API Endpoint

The Streamlit app needs to know where your Flask backend is. You can configure this in three ways:

#### Method 1: Streamlit Secrets (Recommended for Cloud)

In Streamlit Cloud dashboard → App Settings → Secrets:
```toml
API_BASE_URL = "https://your-backend.railway.app"
```

#### Method 2: Environment Variable (For Local)

```bash
export API_BASE_URL="http://localhost:8000"
streamlit run streamlit_app.py
```

#### Method 3: Local Secrets File

Create `.streamlit/secrets.toml`:
```toml
API_BASE_URL = "http://localhost:8000"
```

---

## 📝 Complete Deployment Checklist

### Backend Deployment

- [ ] Choose hosting platform (Railway/Heroku/Render)
- [ ] Use `requirements-backend.txt` for dependencies
- [ ] Configure Google Drive model downloading
- [ ] Set PORT environment variable
- [ ] Deploy and test `/health` endpoint
- [ ] Note down the backend URL

### Frontend Deployment

- [ ] Push code to GitHub
- [ ] Create Streamlit Cloud account
- [ ] Deploy app with `streamlit_app.py`
- [ ] Use `requirements-streamlit.txt`
- [ ] Configure API_BASE_URL in secrets
- [ ] Test the deployed app

---

## 🧪 Testing Your Deployment

### Test Backend

```bash
# Replace with your backend URL
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "models": {
    "herdnet": {"loaded": true},
    "yolov11": {"loaded": true}
  }
}
```

### Test Frontend

1. Open your Streamlit app URL
2. Go to "New Analysis" page
3. Upload a test ZIP file
4. Verify it connects to backend and processes images

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Models not loading
- **Solution**: Check if Google Drive folder is accessible
- Verify `gdown` is in requirements
- Check logs for download errors

**Problem**: Out of memory
- **Solution**: Use CPU-only PyTorch (included in requirements-backend.txt)
- Consider upgrading hosting plan
- Process fewer images at a time

**Problem**: Timeout errors
- **Solution**: Increase timeout limits in hosting platform settings
- Process smaller batches

### Frontend Issues

**Problem**: "Cannot connect to API"
- **Solution**: Verify `API_BASE_URL` is set correctly in Streamlit secrets
- Check backend is running: visit `your-backend-url/health`
- Check CORS settings in Flask app

**Problem**: Dependency conflicts
- **Solution**: Use `requirements-streamlit.txt` (minimal dependencies)
- Clear Streamlit Cloud cache and redeploy

**Problem**: Import errors
- **Solution**: Verify all imports in `streamlit_app.py` are in `requirements-streamlit.txt`

---

## 💰 Cost Estimates

### Free Tier Options

- **Streamlit Cloud**: Free (1 private app, 3 public apps)
- **Railway**: $5/month credit (usually enough for hobby projects)
- **Render**: Free tier with 750 hours/month
- **Heroku**: No longer has free tier (starts at $7/month)

### Recommended Setup for Free

1. Deploy frontend to **Streamlit Cloud** (free)
2. Deploy backend to **Railway** ($0 with free credit) or **Render** (free)

---

## 🚀 Production Checklist

Before going to production:

- [ ] Enable HTTPS on backend
- [ ] Set up proper error logging
- [ ] Add rate limiting to API
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Add authentication if needed
- [ ] Configure CORS properly
- [ ] Set up database backups
- [ ] Add health check monitoring
- [ ] Document API endpoints
- [ ] Set up CI/CD pipeline

---

## 📚 Additional Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🎉 Quick Reference

### Local Development
```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
streamlit run streamlit_app.py
```

### Cloud URLs (Example)
- **Backend API**: https://wildlife-api.railway.app
- **Frontend UI**: https://wildlife-detection.streamlit.app
- **Health Check**: https://wildlife-api.railway.app/health

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review deployment logs in your hosting platform
3. Test backend separately before frontend
4. Verify secrets/environment variables are set correctly

Good luck with your deployment! 🚀

