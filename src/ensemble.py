import sys
import os
import numpy as np

# Add src directory to path for imports
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mbgd_model import MBGDLogisticRegression
from ann_model import ANN

class EnsembleModel:
    """
    Ensemble model combining MBGD Logistic Regression and ANN
    Uses averaging strategy for combining predictions
    """
    
    def __init__(self, mbgd_weight=0.5, ann_weight=0.5):
        """
        Initialize Ensemble Model
        
        Args:
            mbgd_weight: Weight for MBGD predictions (default 0.5)
            ann_weight: Weight for ANN predictions (default 0.5)
        """
        self.mbgd_model = MBGDLogisticRegression()
        self.ann_model = ANN()
        
        # Normalize weights
        total_weight = mbgd_weight + ann_weight
        self.mbgd_weight = mbgd_weight / total_weight
        self.ann_weight = ann_weight / total_weight
    
    def fit(self, X, y):
        """
        Train both MBGD and ANN models
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training labels (n_samples,)
        """
        print("Training MBGD Logistic Regression...")
        self.mbgd_model.fit(X, y)
        
        print("Training Artificial Neural Network...")
        self.ann_model.fit(X, y)
        
        print("Ensemble training complete!")
    
    def predict_proba(self, X):
        """
        Predict probability using ensemble average
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Ensemble probabilities (n_samples,)
        """
        # Get predictions from both models
        mbgd_proba = self.mbgd_model.predict_proba(X)
        ann_proba = self.ann_model.predict_proba(X)
        
        # Weighted average
        ensemble_proba = (self.mbgd_weight * mbgd_proba + 
                         self.ann_weight * ann_proba)
        
        return ensemble_proba
    
    def predict(self, X):
        """
        Predict class labels using ensemble
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Binary predictions (n_samples,)
        """
        probs = self.predict_proba(X)
        return (probs >= 0.5).astype(int)
    
    def save_models(self, mbgd_path, ann_path):
        """
        Save both models
        
        Args:
            mbgd_path: Path to save MBGD model
            ann_path: Path to save ANN model
        """
        self.mbgd_model.save_model(mbgd_path)
        self.ann_model.save_model(ann_path)
        print(f"MBGD model saved to: {mbgd_path}")
        print(f"ANN model saved to: {ann_path}")
    
    def load_models(self, mbgd_path, ann_path):
        """
        Load both models
        
        Args:
            mbgd_path: Path to load MBGD model
            ann_path: Path to load ANN model
        """
        self.mbgd_model.load_model(mbgd_path)
        self.ann_model.load_model(ann_path)
        print(f"MBGD model loaded from: {mbgd_path}")
        print(f"ANN model loaded from: {ann_path}")
    
    def get_individual_predictions(self, X):
        """
        Get individual predictions from both models for analysis
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Dictionary with predictions from both models
        """
        mbgd_proba = self.mbgd_model.predict_proba(X)
        ann_proba = self.ann_model.predict_proba(X)
        ensemble_proba = self.predict_proba(X)
        
        return {
            "mbgd_probability": mbgd_proba,
            "ann_probability": ann_proba,
            "ensemble_probability": ensemble_proba,
            "ensemble_prediction": self.predict(X)
        }
