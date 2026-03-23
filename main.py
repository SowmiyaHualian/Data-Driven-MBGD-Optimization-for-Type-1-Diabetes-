#!/usr/bin/env python
"""
DiagnoSync - Type-1 Diabetes Risk Prediction Web Application
Main entry point for running the FastAPI backend server
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
HOST = os.getenv("API_HOST", "0.0.0.0")
# Render sets PORT, so check that first, then fall back to API_PORT
PORT = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
WORKERS = int(os.getenv("API_WORKERS", "1"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").lower()

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 DiagnoSync - Type-1 Diabetes Risk Prediction API")
    print("=" * 60)
    print(f"Environment: {ENVIRONMENT}")
    print(f"Server: http://{HOST}:{PORT}")
    print(f"API Docs: http://{HOST}:{PORT}/api/docs")
    print(f"Workers: {WORKERS}")
    print("=" * 60)
    print()

    try:
        uvicorn.run(
            "backend.api:app",
            host=HOST,
            port=PORT,
            workers=WORKERS,
            reload=(ENVIRONMENT == "development"),
            log_level=LOG_LEVEL
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {str(e)}")
        sys.exit(1)
