import os
import warnings
from sklearn.metrics import accuracy_score, classification_report

from data_preprocessing import load_and_preprocess_data
from mbgd_model import MBGDLogisticRegression


# Ignore harmless future warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
data_path = os.path.join(BASE_DIR, "data", "diabetes_synthetic_dataset.xlsx")

# Load dataset
X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(data_path)

# Initialize model
model = MBGDLogisticRegression(
    lr=0.01,
    epochs=1000,
    batch_size=32
)

# Train model
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Evaluation
print("\nModel Evaluation")
print("---------------------------")
print("Accuracy:", accuracy_score(y_test, preds))
print(classification_report(y_test, preds))

# Save model
model_path = os.path.join(BASE_DIR, "models", "saved_model.npz")
model.save_model(model_path)

print("\nModel saved successfully at:", model_path)