import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_and_preprocess_data(path):

    # -----------------------
    # Load dataset
    # -----------------------
    df = pd.read_excel(path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # -----------------------
    # Clean labels
    # -----------------------
    df["Class_Label"] = df["Class_Label"].astype(str).str.strip()

    df["Class_Label"] = df["Class_Label"].replace({
        "Type1": 1,
        "Type 1": 1,
        "1": 1,

        "Type2": 0,
        "Type 2": 0,

        "Non-Type1": 0,
        "Non Type1": 0,

        "Normal": 0,
        "normal": 0,

        "0": 0
    })

    # Drop rows that still have invalid labels
    df = df.dropna(subset=["Class_Label"])

    # Convert to integer
    df["Class_Label"] = df["Class_Label"].astype(int)

    # -----------------------
    # Features and target
    # -----------------------
    X = df.drop("Class_Label", axis=1)
    y = df["Class_Label"]

    # -----------------------
    # Feature scaling
    # -----------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # -----------------------
    # Train / Test split
    # -----------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train.values, y_test.values, scaler