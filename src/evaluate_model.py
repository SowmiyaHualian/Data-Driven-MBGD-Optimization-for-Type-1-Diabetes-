import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import roc_curve, roc_auc_score

from data_preprocessing import load_and_preprocess_data
from mbgd_model import MBGDLogisticRegression


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, "data", "diabetes_synthetic_dataset.xlsx")
model_path = os.path.join(BASE_DIR, "models", "saved_model.npz")

X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(data_path)

model = MBGDLogisticRegression()
model.load_model(model_path)

preds = model.predict(X_test)
probs = model.predict_proba(X_test)

# -------------------
# Confusion Matrix
# -------------------

cm = confusion_matrix(y_test, preds)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()

plt.title("Confusion Matrix")
plt.show()

# -------------------
# ROC Curve
# -------------------

fpr, tpr, thresholds = roc_curve(y_test, probs)

auc_score = roc_auc_score(y_test, probs)

plt.figure()

plt.plot(fpr, tpr, label=f"AUC = {auc_score:.2f}")

plt.plot([0,1],[0,1],'--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")

plt.legend()

plt.show()