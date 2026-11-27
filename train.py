from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from src.features import extract_url_features


def main():
    data_path = Path("data/urls.csv")
    df = pd.read_csv(data_path)

    # Extract numeric features for every URL in the dataset
    feature_rows = df["url"].apply(extract_url_features).tolist()
    X = pd.DataFrame(feature_rows)
    y = df["label"].astype(int)

    # Split into training and test sets (stratified so both classes are represented)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    # Save the trained model and feature column order for Day 4 (predict.py)
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(
        {"model": model, "feature_columns": list(X.columns)},
        models_dir / "phishing_model.joblib",
    )
    print("Saved trained model to models/phishing_model.joblib")


if __name__ == "__main__":
    main()