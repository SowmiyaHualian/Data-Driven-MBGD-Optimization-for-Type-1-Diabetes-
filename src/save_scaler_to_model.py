"""
Quick fix: Save the scaler to the existing model file
Run this once to update saved_model.npz with the scaler
"""
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from data_preprocessing import load_and_preprocess_data

# Get paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "diabetes_synthetic_dataset.xlsx")
model_path = os.path.join(BASE_DIR, "models", "saved_model.npz")

# Load scaler from data
print("Loading scaler from training data...")
_, _, _, _, scaler = load_and_preprocess_data(data_path)

# Load existing model
print("Loading existing model...")
model_data = np.load(model_path)
weights = model_data['weights']
bias = model_data['bias']

# Save model with scaler
print("Saving model with scaler...")
np.savez(
    model_path,
    weights=weights,
    bias=bias,
    scaler_mean=scaler.mean_,
    scaler_scale=scaler.scale_
)

print(f"✅ Model updated with scaler at {model_path}")

# Verify
data = np.load(model_path)
print(f"Keys in saved_model.npz: {list(data.keys())}")
