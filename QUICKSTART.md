# 🚀 Quick Start Guide - DiagnoSync

## For Windows Users

### Option 1: One-Click Setup (Easiest)
1. Double-click `run.bat`
2. Wait for dependencies to install
3. Server will start automatically
4. Open `frontend/index.html` in your browser

### Option 2: Manual Setup
```bash
# Open Command Prompt in the project folder

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py

# In another terminal, open the frontend
cd frontend
python -m http.server 8080
# Visit: http://127.0.0.1:8080
```

## For Mac/Linux Users

### Quick Setup
```bash
# Make script executable
chmod +x run.sh

# Run it
./run.sh

# In another terminal
cd frontend
python -m http.server 8080
# Visit: http://127.0.0.1:8080
```

## First Time?

1. **Backend Server**
   - Starts at: `http://127.0.0.1:8000`
   - API Docs: `http://127.0.0.1:8000/api/docs`
   - Health Check: `http://127.0.0.1:8000/api/health`

2. **Frontend Interface**
   - Open `frontend/index.html` directly in browser
   - OR serve on separate port: `python -m http.server 8080`
   - Then visit: `http://127.0.0.1:8080`

## Folder Structure

```
├── main.py          → Start the server with this
├── requirements.txt → Dependencies
├── run.bat/run.sh   → Startup script
├── .env             → Configuration
│
├── backend/
│   └── api.py       → API endpoints
│
├── frontend/
│   ├── index.html   → Web interface
│   ├── app.js       → JavaScript logic
│   └── styles.css   → Styling
│
└── README.md        → Full documentation
```

## Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH"

### "Port 8000 already in use"
- Change port in `.env` file
- Or close the code taking port 8000

### "Cannot find module"
- Run: `pip install -r requirements.txt`

### "CORS errors"
- Make sure backend is running at: `http://127.0.0.1:8000`
- Check `.env` file ALLOWED_ORIGINS setting

## API Usage Example

```javascript
// Get risk assessment
const response = await fetch('http://127.0.0.1:8000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    Age: 35,
    BMI: 24.5,
    Fasting_Glucose: 95,
    Random_Glucose: 140,
    HbA1c: 5.7,
    Ketone: 0,
    Polyuria: 0,
    Polydipsia: 0,
    Weight_Loss: 0,
    Fatigue: 0,
    Blurred_Vision: 0
  })
});

const result = await response.json();
console.log(`Risk: ${result.risk_probability * 100}%`);
console.log(`Level: ${result.risk_level}`);
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Visit API docs at `/api/docs` for interactive testing
- Review FAQ section on the website

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `backend/api.py` | FastAPI backend |
| `frontend/index.html` | Web interface |
| `frontend/app.js` | Frontend logic |
| `requirements.txt` | Python dependencies |
| `.env` | Configuration settings |

## Support

Something not working? Check:
1. Python version: `python --version` (3.8+ required)
2. Dependencies: `pip list`
3. Server health: Open `http://127.0.0.1:8000/api/health` in browser
4. Logs in terminal for error messages

---

**Need more help?** See README.md or check the API documentation at `/api/docs`
