import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from mbgd_model import MBGDLogisticRegression

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

model = MBGDLogisticRegression()
model.load_model("models/saved_model.npz")

prob = model.predict_proba(sample_scaled)[0]
prediction = model.predict(sample_scaled)[0]

print("Risk Probability:", prob)

if prediction == 1:
    print("High Risk of Type 1 Diabetes")
else:
    print("Low Risk")