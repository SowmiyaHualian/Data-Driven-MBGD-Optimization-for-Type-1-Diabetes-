import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("data/diabetes_synthetic_dataset.xlsx")

print("First 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nDataset info:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nClass distribution:")
print(df["Class_Label"].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x="Class_Label", data=df)
plt.title("Class Distribution")
plt.show()

plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Feature Correlation")
plt.show()