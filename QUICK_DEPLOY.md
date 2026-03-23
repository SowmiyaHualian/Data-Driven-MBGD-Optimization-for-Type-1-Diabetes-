# 🚀 Quick Start: Deploy DiagnoSync to Render

## What I've Done (Steps 2 & 3)

✅ **Step 2 - Prepared Application:**
- Updated `main.py` to work with Render's PORT environment variable
- Updated `.env` with production settings
- Created `.env.example` for safe sharing

✅ **Step 3 - Database Setup:**
- SQLite database ready (auto-creates on first run)
- Database location: `data/diagnosync.db`
- User table with profiles
- Predictions table with analysis history

✅ **Created Deployment Files:**
- `Procfile` - Tells Render how to start your app
- `render.yaml` - Infrastructure configuration
- `RENDER_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment checklist

## Your Turn (Step 1 - Render Setup)

### 1. Create Render Account
- Go to https://render.com
- Sign up with GitHub

### 2. Deploy
**Option A: One-Click (Easiest)**
- Click "New Blueprint" on Render
- Select your GitHub repo
- Click "Apply"

**Option B: Manual**
- Click "New Web Service"
- Connect GitHub repo
- Set Build: `pip install -r requirements.txt`
- Set Start: `python main.py`
- Add env variables (shown below)

### 3. Set Environment Variables on Render
These go in Render Dashboard → Environment Variables:

```
ENVIRONMENT=production
API_HOST=0.0.0.0
API_WORKERS=1
SECRET_KEY=[Click refresh icon to generate random key]
ALLOWED_ORIGINS=https://diagnosync-xxxx.onrender.com
```

### 4. Wait & Test
- Deployment takes 2-5 minutes
- You'll get a URL like: `https://diagnosync-1234.onrender.com`
- Visit and test: Register → Login → Analyze

## Files to Commit to Git

Before deploying, commit these to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push
```

## Need Help?

📖 Full guide: `RENDER_DEPLOYMENT.md`
✓ Checklist: `DEPLOYMENT_CHECKLIST.md`

---

**After Deployment:**
- Your app runs 24/7 on Render servers
- SQLite database persists across restarts
- Free tier: Includes 1 web service, 100GB storage

Ready? Follow the steps above and let me know the Render URL once it's deployed! 🎉
