# DiagnoSync - Render Deployment Guide

## Step 1: Prepare Your GitHub Repository

1. Make sure all your code is committed to GitHub
2. Create a `.gitignore` file with:
   ```
   __pycache__/
   .env
   *.pyc
   .DS_Store
   data/diagnosync.db
   node_modules/
   venv/
   .venv/
   ```

## Step 2: Deploy to Render

### Option A: Using Render Dashboard (Manual)

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: diagnosync
   - **Environment**: Python 3
   - **Region**: Choose nearest to you
   - **Branch**: main (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Click "Advanced" and add Environment Variables:
   - `ENVIRONMENT`: `production`
   - `API_HOST`: `0.0.0.0`
   - `API_WORKERS`: `1`
   - `SECRET_KEY`: Generate a strong key (use the Render random value generator)
   - `ALLOWED_ORIGINS`: `https://yourdomain.render.com` (will be provided after deployment)

6. Click "Create Web Service"
7. Wait for deployment (3-5 minutes)

### Option B: Using render.yaml (One-Click)

1. Ensure `render.yaml` is in your repository root
2. Go to [render.com](https://render.com)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Click "Apply"
6. Add environment variables when prompted
7. Deploy!

## Step 3: Configure Environment Variables on Render

After deployment, update these in Render Dashboard → Environment:

1. **SECRET_KEY**: 
   - Click the random value generator (⚙️ icon)
   - Generate a 32+ character secure key
   
2. **ALLOWED_ORIGINS**: 
   - Set to: `https://diagnosync-xxxx.onrender.com` 
   - (Replace xxxx with your actual subdomain)

3. **ENVIRONMENT**: `production`

## Step 4: Access Your Deployed App

- **Main App**: https://diagnosync-xxxx.onrender.com/
- **API Docs**: https://diagnosync-xxxx.onrender.com/api/docs
- **API Playground**: https://diagnosync-xxxx.onrender.com/api/redoc

## Step 5: Data Persistence

Your SQLite database is stored in the `/data` disk. It persists across deploys.

To download your database:
1. Go to Render Dashboard → Your Service → Shell
2. Run: `tar -czf database.tar.gz data/`
3. Download the file

## Troubleshooting

### Check Logs
1. Render Dashboard → Your Service → Logs
2. Look for any errors

### Common Issues

**Issue**: Database not persisting
- **Solution**: Ensure disk is mounted at `/data` in render.yaml

**Issue**: CORS errors in browser
- **Solution**: Update `ALLOWED_ORIGINS` to include your domain

**Issue**: App crashes on startup
- **Solution**: Check logs for missing dependencies or syntax errors

### Testing Database Connection
Access the shell and run:
```bash
python -c "from backend.database import Database; db = Database(); print('Database OK')"
```

## Important Notes

1. **Free Tier Limits**: 
   - Instances spin down after 15 min of inactivity
   - Max 50 concurrent connections
   - 100GB data limit

2. **Security**:
   - Never commit `.env` to GitHub
   - Use strong SECRET_KEY
   - Enable HTTPS (automatic on Render)

3. **Monitoring**:
   - Check Render Dashboard regularly
   - Monitor resource usage
   - Set up alerts for downtime

## Need Help?

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- GitHub Issues: Create an issue in your repository
