# DiagnoSync - Pre-Deployment Checklist ✓

## Local Testing
- [ ] Run `python main.py` and verify server starts
- [ ] Test registration at http://127.0.0.1:8000/register.html
- [ ] Test login at http://127.0.0.1:8000/login.html
- [ ] Test analysis form at http://127.0.0.1:8000/analysis.html
- [ ] Verify CORS works (no browser console errors)
- [ ] Check API docs at http://127.0.0.1:8000/api/docs

## Code Quality
- [ ] All imports are correct
- [ ] No hardcoded passwords or secrets
- [ ] `requirements.txt` is up to date
- [ ] Python version compatible (3.8+)
- [ ] No console.log errors in browser

## Security
- [ ] Generated strong SECRET_KEY (32+ characters)
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` created with placeholder values
- [ ] No sensitive data in code comments
- [ ] CORS configured for production domain

## Files Created/Updated for Production
- [x] `main.py` - Updated for Render (PORT env variable)
- [x] `.env` - Production-ready template
- [x] `.env.example` - Safe to share
- [x] `Procfile` - Render knows how to start app
- [x] `render.yaml` - Infrastructure as code
- [x] `RENDER_DEPLOYMENT.md` - Deployment guide
- [x] `requirements.txt` - All dependencies listed

## Git & GitHub
- [ ] All files committed to git
- [ ] `.gitignore` configured correctly
- [ ] Repository is public (needed for Render free tier)
- [ ] No secrets in git history
- [ ] Branch name is main or your chosen deploy branch

## Render Setup
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Ready to create new Web Service

## Database
- [x] SQLite configured in `data/diagnosync.db`
- [x] Database will auto-create on first run
- [x] User table schema ready
- [x] Predictions table schema ready

## Ready to Deploy?
Once all boxes are ✓, proceed with deployment!

**Next Step**: Follow RENDER_DEPLOYMENT.md for step-by-step instructions
