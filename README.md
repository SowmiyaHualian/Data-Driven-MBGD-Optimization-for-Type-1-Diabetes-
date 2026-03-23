# DiagnoSync - Type-1 Diabetes Risk Prediction Web Application

**DiagnoSync** is an advanced machine learning-powered web application that assesses your risk of developing Type-1 Diabetes using clinical markers and health indicators.

## 🌟 Features

- **AI-Powered Assessment**: Advanced MBGD Logistic Regression model trained on comprehensive diabetes research data
- **Instant Results**: Get risk assessment in seconds with visual insights
- **Secure & Private**: All data is processed locally in your browser - nothing is stored on our servers
- **Evidence-Based**: Built on validated clinical markers and medical research
- **Professional UI**: Modern, responsive interface with smooth animations
- **Full API Documentation**: Interactive OpenAPI (Swagger) documentation included

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd d:\T1D
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional)**
   - Edit `.env` file to customize API host, port, and other settings
   - Default: `http://127.0.0.1:8000`

4. **Start the backend server**
   ```bash
   python main.py
   ```
   
   The server will start at: `http://127.0.0.1:8000`

5. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it with a local web server:
     ```bash
     # Using Python's built-in server
     cd frontend
     python -m http.server 8080
     # Then visit: http://127.0.0.1:8080
     ```

## 📋 How It Works

### The Assessment Process

1. **Enter Health Data**: Provide your age, BMI, glucose levels, HbA1c, and symptom information
2. **ML Model Analysis**: Your data is sent to our trained MBGD Logistic Regression model
3. **Risk Calculation**: The model calculates your risk probability (0-100%)
4. **Personalized Results**: 
   - Risk level: Low, Moderate, or High
   - Risk probability percentage
   - Personalized recommendations based on your risk level

### Key Health Metrics

| Parameter | Description | Normal Range |
|-----------|-------------|--------------|
| **Age** | Your age in years | 0-150 |
| **BMI** | Body Mass Index | 10-60 kg/m² |
| **Fasting Glucose** | Blood glucose after 8+ hours fasting | 50-400 mg/dL |
| **Random Glucose** | Glucose at any time of day | 50-400 mg/dL |
| **HbA1c** | 3-month average blood glucose | 3-15% |
| **Ketone** | Presence of ketones (0=No, 1=Yes) | 0 or 1 |
| **Polyuria** | Excessive urination (0=No, 1=Yes) | 0 or 1 |
| **Polydipsia** | Excessive thirst (0=No, 1=Yes) | 0 or 1 |
| **Weight Loss** | Unexplained weight loss (0=No, 1=Yes) | 0 or 1 |
| **Fatigue** | Fatigue symptom (0=No, 1=Yes) | 0 or 1 |
| **Blurred Vision** | Blurred vision symptom (0=No, 1=Yes) | 0 or 1 |

## 🔌 API Endpoints

### Base URL
```
http://127.0.0.1:8000
```

### Available Endpoints

#### 1. Health Check
```
GET /api/health
```
Verify the API is operational.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

#### 2. Root Endpoint
```
GET /
```
Welcome message and version information.

#### 3. Prediction Endpoint
```
POST /api/predict
```
Submit patient data and receive risk assessment.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "risk_probability": 0.35,
  "prediction": 0,
  "message": "Low Risk - Continue regular health monitoring",
  "risk_level": "Low"
}
```

### Interactive API Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc

## 📂 Project Structure

```
d:\T1D/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── .env                             # Environment configuration
├── README.md                        # This file
│
├── backend/
│   ├── api.py                       # FastAPI application
│   └── __pycache__/                 # Cached Python files
│
├── frontend/
│   ├── index.html                   # Web interface
│   ├── app.js                       # Frontend logic
│   ├── styles.css                   # Styling
│   └── ...
│
├── src/
│   ├── mbgd_model.py                # ML model implementation
│   ├── data_preprocessing.py        # Data preparation
│   ├── train_model.py               # Model training script
│   ├── predict.py                   # Prediction utilities
│   └── ...
│
├── models/
│   └── saved_model.npz              # Trained model weights
│
└── data/
    └── diabetes_synthetic_dataset.xlsx  # Training dataset
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# API Settings
API_HOST=127.0.0.1          # Server host address
API_PORT=8000                # Server port
API_WORKERS=1               # Number of worker processes

# CORS Settings
ALLOWED_ORIGINS=*           # Allowed origin domains (comma-separated)

# Environment
ENVIRONMENT=development     # development or production
LOG_LEVEL=INFO             # Logging level (DEBUG, INFO, WARNING, ERROR)
```

## 🔒 Security & Privacy

- ✅ **No Data Storage**: Your health information is never stored on our servers
- ✅ **Local Processing**: Data is processed entirely in your browser
- ✅ **HTTPS Ready**: Can be deployed with SSL/TLS for production
- ✅ **CORS Configured**: Cross-origin requests are properly managed
- ⚠️ **Not Medical Diagnosis**: This tool provides risk assessment only, not medical diagnosis

## ⚠️ Important Disclaimer

**This application is for educational and informational purposes only.**

- **NOT a substitute for professional medical advice**
- **NOT for medical diagnosis or treatment**
- Always consult with a qualified healthcare provider for proper evaluation
- If you have symptoms of Type-1 Diabetes, seek immediate medical attention

## 🎓 About Type-1 Diabetes

Type-1 Diabetes is an autoimmune condition where:
- The pancreas doesn't produce enough insulin
- It typically appears in children and young adults
- It can develop at any age
- It requires medical management and treatment

**Common Symptoms:**
- Excessive thirst (polydipsia)
- Frequent urination (polyuria)
- Fatigue and weakness
- Unexplained weight loss
- Blurred vision
- Irritability or mood changes

If you suspect you may have Type-1 Diabetes, please consult a healthcare professional immediately.

## 📊 Model Information

- **Algorithm**: Minibatch Gradient Descent (MBGD) Logistic Regression
- **Training Data**: Synthetic diabetes dataset (diabetes_synthetic_dataset.xlsx)
- **Features**: 11 clinical markers and symptoms
- **Output**: Risk probability (0-1) and risk classification (Low/Moderate/High)

## 🛠️ Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Set environment
set ENVIRONMENT=development

# Start with auto-reload
python main.py
```

### Project Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning
- **pandas**: Data processing
- **python-dotenv**: Environment configuration

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues and bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

## 📞 Support

For issues, questions, or suggestions, please check the FAQ section on the website or review the API documentation at `/api/docs`.

---

**Last Updated**: March 2024  
**Version**: 1.0.0  
**Status**: ✅ Active & Maintained
