# Deployment Guide - DiagnoSync

## Local Development

### Windows

1. **Open Command Prompt** in the project directory
2. **Run the startup script**:
   ```bash
   run.bat
   ```
   This will:
   - Check Python installation
   - Install dependencies from requirements.txt
   - Start the backend server at http://127.0.0.1:8000

3. **Open the frontend**:
   - Open `frontend/index.html` in your web browser
   - Or serve with Python:
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     Then visit: http://127.0.0.1:8080

### Linux / Mac

1. **Open Terminal** in the project directory
2. **Make the script executable**:
   ```bash
   chmod +x run.sh
   ```
3. **Run the startup script**:
   ```bash
   ./run.sh
   ```

## Production Deployment

### Option 1: Simple Python Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 backend.api:app
```

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t diagnosync .
docker run -p 8000:8000 diagnosync
```

### Option 3: Cloud Deployment (Heroku)

1. **Create Procfile**:
   ```
   web: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy to Heroku**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Nginx Reverse Proxy Setup (Production)

```nginx
upstream diagnosync {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://diagnosync;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /frontend/ {
        alias /path/to/frontend/;
    }
}
```

## Environment Variables for Production

Update `.env` for production:

```env
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Security Considerations

- ✅ Always use HTTPS in production (SSL/TLS)
- ✅ Set ALLOWED_ORIGINS to specific domains
- ✅ Use a reverse proxy (Nginx, Apache)
- ✅ Enable logging and monitoring
- ✅ Keep dependencies updated
- ✅ Run behind a Web Application Firewall (WAF)
- ✅ Set up rate limiting

## Monitoring & Logging

### Application Logs

Logs are output to console by default. For production, redirect to file:

```bash
python main.py > app.log 2>&1 &
```

### Health Monitoring

Monitor the health endpoint:

```bash
curl http://your-domain.com:8000/api/health
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### Dependencies Issues
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache and reinstall
pip install --no-cache-dir -r requirements.txt
```

### Backend Not Responding
1. Check if server is running: `http://127.0.0.1:8000/api/health`
2. Check logs for errors
3. Verify firewall settings
4. Check network connectivity

## Performance Optimization

### API
- Increase workers: `API_WORKERS=4` (or more)
- Enable caching for predictions
- Use connection pooling for databases

### Frontend
- Minimize CSS/JS files
- Enable gzip compression
- Use CDN for static files
- Implement client-side caching

## Backup & Recovery

Important files to backup:
- `models/saved_model.npz` - Trained model
- `data/diabetes_synthetic_dataset.xlsx` - Training data
- `.env` - Configuration

## Updates & Maintenance

Check for updates:
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

## Support

For issues:
1. Check this guide
2. Review logs
3. Check API health endpoint
4. Review API documentation at `/api/docs`
