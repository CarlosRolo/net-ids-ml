import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Tuple

MODEL_PATH = "models/ids_model.pkl"
SCALER_PATH = "models/scaler.pkl"


def train_model(X_train: np.ndarray, contamination: float = 0.1) -> Tuple:
    """
    Entrena Isolation Forest con tráfico normal del NSL-KDD.
    contamination = fracción esperada de anomalías (10% por defecto).
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled)
    return model, scaler


def save_model(model, scaler) -> None:
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"[✓] Modelo guardado en {MODEL_PATH}")


def load_model() -> Tuple:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modelo no encontrado. Ejecuta train.py primero.")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def predict(model, scaler, feature_vector: np.ndarray) -> dict:
    """
    Retorna predicción para un vector de features.
    Isolation Forest: -1 = anomalía, 1 = normal
    """
    X_scaled = scaler.transform(feature_vector)
    prediction = model.predict(X_scaled)[0]
    score = model.score_samples(X_scaled)[0]

    return {
        "is_anomaly": prediction == -1,
        "score": float(score),
        "label": "ANOMALY" if prediction == -1 else "normal"
    }
