#!/bin/bash
# DiagnoSync - Type-1 Diabetes Risk Prediction API
# Linux/Mac Startup Script

echo ""
echo "============================================================"
echo "  DiagnoSync - Type-1 Diabetes Risk Prediction API"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Start the server
echo ""
echo "Starting backend server..."
echo "Server will be available at: http://127.0.0.1:8000"
echo "API Documentation: http://127.0.0.1:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
