from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import numpy as np

NSL_KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

NUMERIC_FEATURES = [
    "duration", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
    "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell",
    "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login",
    "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
    "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]


@dataclass
class PacketFeatures:
    """Features extraídas de un paquete/flujo de red en tiempo real."""
    src_ip: str = ""
    dst_ip: str = ""
    protocol: str = "tcp"
    src_port: int = 0
    dst_port: int = 0
    src_bytes: int = 0
    dst_bytes: int = 0
    duration: float = 0.0
    flags: str = ""
    timestamp: float = 0.0

    def to_model_vector(self) -> np.ndarray:
        """Convierte las features del paquete al vector que espera el modelo."""
        protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
        proto_num = protocol_map.get(self.protocol.lower(), 0)
        vector = np.zeros(len(NUMERIC_FEATURES))
        vector[0] = self.duration
        vector[1] = self.src_bytes
        vector[2] = self.dst_bytes
        vector[19] = 1  # count mínimo
        return vector.reshape(1, -1)


def load_nslkdd(path: str) -> pd.DataFrame:
    """Carga el dataset NSL-KDD desde archivo .txt."""
    df = pd.read_csv(path, header=None, names=NSL_KDD_COLUMNS)
    df["label_binary"] = df["label"].apply(lambda x: 0 if x == "normal" else 1)
    return df


def prepare_training_data(df: pd.DataFrame) -> np.ndarray:
    """Retorna solo las filas normales para entrenar Isolation Forest."""
    normal = df[df["label_binary"] == 0][NUMERIC_FEATURES]
    return normal.values
