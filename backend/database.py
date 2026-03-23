"""
Database models and user management for DiagnoSync
"""

import os
import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Use data/ directory for database (works locally and on Render)
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/diagnosync.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
TOKEN_EXPIRY_HOURS = 24


class Database:
    """SQLite database manager for user authentication"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with users table"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create predictions history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                age REAL,
                bmi REAL,
                fasting_glucose REAL,
                random_glucose REAL,
                hba1c REAL,
                ketone INTEGER,
                polyuria INTEGER,
                polydipsia INTEGER,
                weight_loss INTEGER,
                fatigue INTEGER,
                blurred_vision INTEGER,
                risk_probability REAL,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    
    def register_user(self, username: str, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User registered successfully"
            }
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return {"success": False, "error": "Username already exists"}
            elif "email" in str(e):
                return {"success": False, "error": "Email already exists"}
            return {"success": False, "error": "Registration failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and generate token"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, password_hash, full_name FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return {"success": False, "error": "Invalid username or password"}
            
            user_id, password_hash, full_name = user
            
            if not self.verify_password(password, password_hash):
                return {"success": False, "error": "Invalid username or password"}
            
            # Generate JWT token
            token = self.generate_token(user_id, username)
            
            return {
                "success": True,
                "token": token,
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "message": "Login successful"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_token(self, user_id: int, username: str) -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "username": username,
            "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user info by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username, email, full_name, created_at FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "full_name": user[3],
                    "created_at": user[4]
                }
            return None
        except Exception:
            return None
    
    def save_prediction(self, user_id: int, prediction_data: Dict[str, Any], risk_probability: float, risk_level: str) -> bool:
        """Save user prediction to history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions 
                (user_id, age, bmi, fasting_glucose, random_glucose, hba1c, 
                 ketone, polyuria, polydipsia, weight_loss, fatigue, blurred_vision,
                 risk_probability, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                prediction_data.get('Age'),
                prediction_data.get('BMI'),
                prediction_data.get('Fasting_Glucose'),
                prediction_data.get('Random_Glucose'),
                prediction_data.get('HbA1c'),
                prediction_data.get('Ketone'),
                prediction_data.get('Polyuria'),
                prediction_data.get('Polydipsia'),
                prediction_data.get('Weight_Loss'),
                prediction_data.get('Fatigue'),
                prediction_data.get('Blurred_Vision'),
                risk_probability,
                risk_level
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving prediction: {str(e)}")
            return False
    
    def get_user_predictions(self, user_id: int) -> list:
        """Get all predictions for a user"""
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC
            ''', (user_id,))
            
            predictions = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return predictions
        except Exception:
            return []


# Initialize database
db = Database()
