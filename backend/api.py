import os
import logging
import numpy as np
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import pathlib

from src.mbgd_model import MBGDLogisticRegression
from backend.database import db
from sklearn.preprocessing import StandardScaler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with documentation
app = FastAPI(
    title="Type-1 Diabetes Risk Prediction API",
    description="Advanced machine learning model for Type-1 Diabetes risk assessment",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths - find project root by looking for models/ directory
def find_project_root():
    """Find the project root directory by searching for models/ folder"""
    current = os.path.dirname(os.path.abspath(__file__))
    # Walk up from backend/ directory
    for _ in range(5):
        if os.path.exists(os.path.join(current, "models")):
            return current
        parent = os.path.dirname(current)
        if parent == current:  # Reached filesystem root
            break
        current = parent
    # Fallback: go up 2 levels from backend/api.py
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = find_project_root()
model_path = os.path.join(BASE_DIR, "models", "saved_model.npz")

# Debug logging
logger.info(f"Backend file: {os.path.abspath(__file__)}")
logger.info(f"Project root: {BASE_DIR}")
logger.info(f"Looking for model at: {model_path}")
logger.info(f"Model exists: {os.path.exists(model_path)}")

# Load model components with error handling
try:
    logger.info("Loading trained model and scaler...")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    model = MBGDLogisticRegression()
    model.load_model(model_path)
    
    # Load scaler from model file
    model_data = np.load(model_path)
    scaler = StandardScaler()
    scaler.mean_ = model_data['scaler_mean']
    scaler.scale_ = model_data['scaler_scale']
    logger.info("Model and scaler loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise


# Input schema with validation
class Patient(BaseModel):
    """Patient data for diabetes risk prediction"""
    Age: float = Field(..., ge=0, le=150, description="Age in years")
    BMI: float = Field(..., ge=10, le=60, description="Body Mass Index (kg/m²)")
    Fasting_Glucose: float = Field(..., ge=50, le=400, description="Fasting glucose (mg/dL)")
    Random_Glucose: float = Field(..., ge=50, le=400, description="Random glucose (mg/dL)")
    HbA1c: float = Field(..., ge=3, le=15, description="HbA1c percentage")
    Ketone: float = Field(..., ge=0, le=1, description="Ketone presence (0 or 1)")
    Polyuria: float = Field(..., ge=0, le=1, description="Polyuria symptom (0 or 1)")
    Polydipsia: float = Field(..., ge=0, le=1, description="Polydipsia symptom (0 or 1)")
    Weight_Loss: float = Field(..., ge=0, le=1, description="Weight loss symptom (0 or 1)")
    Fatigue: float = Field(..., ge=0, le=1, description="Fatigue symptom (0 or 1)")
    Blurred_Vision: float = Field(..., ge=0, le=1, description="Blurred vision symptom (0 or 1)")

    class Config:
        json_schema_extra = {
            "example": {
                "Age": 35,
                "BMI": 24.5,
                "Fasting_Glucose": 95,
                "Random_Glucose": 140,
                "HbA1c": 5.7,
                "Ketone": 0,
                "Polyuria": 0,
                "Polydipsia": 0,
                "Weight_Loss": 0,
                "Fatigue": 0,
                "Blurred_Vision": 0
            }
        }


# Authentication schemas
class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    """User login request"""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class AuthResponse(BaseModel):
    """Authentication response"""
    success: bool
    token: Optional[str] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    message: str
    error: Optional[str] = None


# Health check endpoint
@app.get("/api/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Check if the API is operational"""
    return {"status": "healthy", "message": "API is operational"}


# Root endpoint
@app.get("/", tags=["Info"])
def home() -> Dict[str, str]:
    """Welcome endpoint"""
    return {"message": "T1D Risk Prediction API Running", "version": "1.0.0"}


# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/register", tags=["Auth"])
def register(request: RegisterRequest) -> Dict[str, Any]:
    """Register a new user"""
    logger.info(f"Registration request for username: {request.username}")
    
    result = db.register_user(
        username=request.username,
        email=request.email,
        password=request.password,
        full_name=request.full_name
    )
    
    if result["success"]:
        return {
            "success": True,
            "user_id": result["user_id"],
            "message": "Registration successful. Please log in."
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])


@app.post("/api/login", tags=["Auth"])
def login(request: LoginRequest) -> Dict[str, Any]:
    """Login user and get authentication token"""
    logger.info(f"Login request for username: {request.username}")
    
    result = db.login_user(username=request.username, password=request.password)
    
    if result["success"]:
        return {
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "username": result["username"],
            "full_name": result["full_name"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=401, detail=result["error"])


@app.get("/api/user/profile", tags=["User"])
def get_profile(authorization: str = Header(None)) -> Dict[str, Any]:
    """Get current user profile"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.replace("Bearer ", "")
    payload = db.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.get_user(payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@app.get("/api/user/predictions", tags=["User"])
def get_predictions(authorization: str = Header(None)) -> Dict[str, Any]:
    """Get all predictions for the current user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.replace("Bearer ", "")
    payload = db.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["user_id"]
    predictions = db.get_user_predictions(user_id)
    
    # Calculate statistics
    total = len(predictions)
    high_risk = sum(1 for p in predictions if p.get("risk_level") == "High")
    moderate_risk = sum(1 for p in predictions if p.get("risk_level") == "Moderate")
    low_risk = sum(1 for p in predictions if p.get("risk_level") == "Low")
    
    return {
        "predictions": predictions,
        "statistics": {
            "total": total,
            "high_risk": high_risk,
            "moderate_risk": moderate_risk,
            "low_risk": low_risk
        }
    }


# Rehabilitation Plan Generator
def generate_rehabilitation_plan(risk_level: str, age: float, bmi: float) -> list:
    """
    Generate personalized rehabilitation and management plan based on risk level
    """
    plans = {
        "Low": [
            "✓ Maintain Routine: Continue annual health screenings and diabetes testing.",
            "✓ Diet: Maintain a balanced diet rich in whole grains, vegetables, and lean proteins.",
            "✓ Exercise: Aim for 150 minutes of moderate activity per week.",
            "✓ Weight Management: Keep BMI within healthy range (18.5-24.9).",
            "✓ Stress Management: Practice yoga, meditation, or mindfulness regularly."
        ],
        "Moderate": [
            "⚠ Medical Consultation: Schedule appointment with endocrinologist within 2-3 weeks.",
            "⚠ Blood Testing: Get fasting glucose and HbA1c levels monitored every 3 months.",
            "⚠ Lifestyle Modification: Reduce refined sugars and processed foods significantly.",
            "⚠ Physical Activity: Increase exercise to 30 minutes daily, 5 days a week.",
            "⚠ Weight Loss: Target 5-10% weight reduction if overweight (BMI > 25).",
            "⚠ Family Monitoring: Inform family members to get screening done as well."
        ],
        "High": [
            "🚨 Urgent Consultation: Schedule immediate appointment with endocrinologist.",
            "🚨 Hospital Evaluation: Consider hospitalization for comprehensive metabolic evaluation.",
            "🚨 Continuous Monitoring: Daily blood glucose monitoring with home testing kit.",
            "🚨 Strict Diet Control: Follow diabetic diet plan prepared by nutritionist.",
            "🚨 Intensive Exercise: Start supervised exercise program (45 min, 5-6 days/week).",
            "🚨 Medication Review: Get prescription for preventive medication if recommended.",
            "🚨 Insulin Therapy: Be prepared for possible insulin therapy as prescribed by doctor."
        ]
    }
    
    return plans.get(risk_level, plans["Low"])


# Prediction endpoint
@app.post("/api/predict", tags=["Prediction"])
def predict(data: Patient, authorization: str = Header(None)) -> Dict[str, Any]:
    """
    Predict Type-1 Diabetes risk based on patient data
    Requires authentication token
    
    Returns:
        - risk_probability: Float between 0 and 1
        - prediction: 1 for high risk, 0 for low risk
        - message: Human-readable risk assessment
        - risk_level: 'Low', 'Moderate', or 'High'
        - rehabilitation_plan: List of rehabilitation recommendations
    """
    # Verify authentication
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.replace("Bearer ", "")
    payload = db.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload["user_id"]
    
    try:
        logger.info(f"Processing prediction request for user {user_id}, age {data.Age}")
        
        # Prepare input
        values = np.array([[
            data.Age,
            data.BMI,
            data.Fasting_Glucose,
            data.Random_Glucose,
            data.HbA1c,
            data.Ketone,
            data.Polyuria,
            data.Polydipsia,
            data.Weight_Loss,
            data.Fatigue,
            data.Blurred_Vision
        ]])

        # Scale input
        scaled = scaler.transform(values)

        # Get prediction
        probability = model.predict_proba(scaled)[0]
        prediction = model.predict(scaled)[0]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        # Generate rehabilitation plan
        rehab_plan = generate_rehabilitation_plan(risk_level, data.Age, data.BMI)

        # Save prediction to database
        db.save_prediction(user_id, data.dict(), float(probability), risk_level)

        logger.info(f"Prediction complete: {risk_level} risk (probability: {probability:.2f})")
        
        return {
            "success": True,
            "risk_probability": float(probability),
            "prediction": int(prediction),
            "message": "High Risk of Type-1 Diabetes - Consult a healthcare provider" if prediction == 1 else "Low Risk - Continue regular health monitoring",
            "risk_level": risk_level,
            "rehabilitation_plan": rehab_plan
        }
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing prediction")


# Mount static files (frontend)
frontend_path = os.path.join(BASE_DIR, "frontend")

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend(full_path: str):
    """Serve frontend files (catch-all route for HTML/CSS/JS files)"""
    # Don't serve files that start with /api (those are handled by API routes)
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Try to serve the requested file
    file_path = pathlib.Path(frontend_path) / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    
    # If it's not a file with an extension, try to serve index.html (for client-side routing)
    if "." not in full_path.split("/")[-1]:
        index_path = pathlib.Path(frontend_path) / "index.html"
        if index_path.is_file():
            return FileResponse(index_path)
    
    # If file doesn't exist, return 404
    raise HTTPException(status_code=404, detail="Not found")