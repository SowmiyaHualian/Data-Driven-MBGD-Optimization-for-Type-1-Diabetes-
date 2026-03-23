@echo off
REM DiagnoSync - Type-1 Diabetes Risk Prediction API
REM Windows Startup Script

echo.
echo ============================================================
echo   DiagnoSync - Type-1 Diabetes Risk Prediction API
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Start the server
echo.
echo Starting backend server...
echo Server will be available at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
