import numpy as np
import pytest
from src.detector import train_model, predict
from src.features import PacketFeatures

@pytest.fixture(scope="module")
def trained_model():
    X = np.random.rand(200, 38)
    model, scaler = train_model(X, contamination=0.1)
    return model, scaler

def test_train_model_returns_objects(trained_model):
    model, scaler = trained_model
    assert model is not None
    assert scaler is not None

def test_predict_returns_dict(trained_model):
    model, scaler = trained_model
    vec = np.zeros((1, 38))
    result = predict(model, scaler, vec)
    assert "is_anomaly" in result
    assert "score" in result
    assert "label" in result

def test_predict_label_values(trained_model):
    model, scaler = trained_model
    vec = np.zeros((1, 38))
    result = predict(model, scaler, vec)
    assert result["label"] in ("normal", "ANOMALY")

def test_predict_score_is_float(trained_model):
    model, scaler = trained_model
    vec = np.random.rand(1, 38) * 1000
    result = predict(model, scaler, vec)
    assert isinstance(result["score"], float)
