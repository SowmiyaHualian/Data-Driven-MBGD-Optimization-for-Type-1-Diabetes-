import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from ensemble import EnsembleModel

df = pd.read_excel("data/diabetes_synthetic_dataset.xlsx")

X = df.drop("Class_Label", axis=1)

scaler = StandardScaler()
scaler.fit(X)

sample = np.array([[

25,
23,
110,
140,
6.5,
0,
1,
1,
0,
1,
0

]])

sample_scaled = scaler.transform(sample)

# Load ensemble model
ensemble = EnsembleModel()
ensemble.load_models("models/mbgd_model.npz", "models/ann_model.npz")

# Get ensemble prediction
prob = ensemble.predict_proba(sample_scaled)[0]
prediction = ensemble.predict(sample_scaled)[0]

# Get individual predictions for comparison
individual = ensemble.get_individual_predictions(sample_scaled)

print("\n" + "="*60)
print("ENSEMBLE PREDICTION RESULTS")
print("="*60)

print(f"\nMBGD Probability: {individual['mbgd_probability'][0]:.4f}")
print(f"ANN Probability:  {individual['ann_probability'][0]:.4f}")
print(f"\nEnsemble Probability: {prob:.4f}")
print(f"Ensemble Prediction: {prediction}")

if prediction == 1:
    print("\n⚠️  HIGH RISK of Type 1 Diabetes")
else:
    print("\n✓ LOW RISK - Continue regular health monitoring")
    
print("="*60)