import os
import warnings
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

from data_preprocessing import load_and_preprocess_data
from mbgd_model import MBGDLogisticRegression
from ann_model import ANN
from ensemble import EnsembleModel


# Ignore harmless future warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
data_path = os.path.join(BASE_DIR, "data", "diabetes_synthetic_dataset.xlsx")

# Load dataset
X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(data_path)

print("\n" + "="*60)
print("ENSEMBLE MODEL TRAINING - Type-1 Diabetes Risk Prediction")
print("="*60)

# Initialize Ensemble Model
ensemble = EnsembleModel(mbgd_weight=0.5, ann_weight=0.5)

# Train ensemble (both MBGD and ANN)
print("\nTraining ensemble of models...")
ensemble.fit(X_train, y_train)

# Get ensemble predictions
ensemble_preds = ensemble.predict(X_test)

# Get individual model predictions for comparison
individual_preds = ensemble.get_individual_predictions(X_test)

# Evaluation
print("\n" + "="*60)
print("ENSEMBLE MODEL EVALUATION")
print("="*60)
print("\nEnsemble Accuracy:", accuracy_score(y_test, ensemble_preds))
print(classification_report(y_test, ensemble_preds, target_names=["Low Risk", "High Risk"]))

# Individual model evaluation
print("\n" + "="*60)
print("INDIVIDUAL MODEL COMPARISON")
print("="*60)

mbgd_preds = (individual_preds["mbgd_probability"] >= 0.5).astype(int)
print("\nMBGD Logistic Regression Accuracy:", accuracy_score(y_test, mbgd_preds))

ann_preds = (individual_preds["ann_probability"] >= 0.5).astype(int)
print("ANN Accuracy:", accuracy_score(y_test, ann_preds))

# Save models
print("\n" + "="*60)
print("SAVING MODELS")
print("="*60)

mbgd_path = os.path.join(BASE_DIR, "models", "mbgd_model.npz")
ann_path = os.path.join(BASE_DIR, "models", "ann_model.npz")

# Save MBGD model with scaler
ensemble.mbgd_model.weights = ensemble.mbgd_model.weights
ensemble.mbgd_model.bias = ensemble.mbgd_model.bias
np.savez(mbgd_path,
         weights=ensemble.mbgd_model.weights,
         bias=ensemble.mbgd_model.bias,
         scaler_mean=scaler.mean_,
         scaler_scale=scaler.scale_)

# Save ANN model
ensemble.ann_model.save_model(ann_path)

print("\n" + "="*60)
print("TRAINING COMPLETE!")
print("="*60)
print("\nModels saved:")
print(f"  - MBGD: {mbgd_path}")
print(f"  - ANN:  {ann_path}")
print("\nYou can now use the ensemble model for predictions.")