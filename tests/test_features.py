import numpy as np
import pytest
from src.features import PacketFeatures, load_nslkdd, prepare_training_data

def test_packet_features_defaults():
    f = PacketFeatures()
    assert f.protocol == "tcp"
    assert f.src_bytes == 0

def test_to_model_vector_shape():
    f = PacketFeatures(src_bytes=500, dst_bytes=200, duration=1.5)
    vec = f.to_model_vector()
    assert vec.shape == (1, 38)

def test_to_model_vector_values():
    f = PacketFeatures(src_bytes=1000, dst_bytes=500, duration=2.0)
    vec = f.to_model_vector()
    assert vec[0][0] == 2.0   # duration
    assert vec[0][1] == 1000  # src_bytes
    assert vec[0][2] == 500   # dst_bytes

def test_load_nslkdd():
    df = load_nslkdd("data/nslkdd/KDDTrain+.txt")
    assert len(df) > 100000
    assert "label" in df.columns
    assert "label_binary" in df.columns
    assert set(df["label_binary"].unique()).issubset({0, 1})

def test_prepare_training_data_only_normal():
    df = load_nslkdd("data/nslkdd/KDDTrain+.txt")
    X = prepare_training_data(df)
    assert X.shape[1] == 38
    assert X.shape[0] == len(df[df["label_binary"] == 0])
