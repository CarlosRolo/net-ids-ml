# NET-05: Homemade IDS with ML Anomaly Detection

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-orange?logo=scikitlearn)
![Scapy](https://img.shields.io/badge/Scapy-2.5-green)
![Tests](https://img.shields.io/badge/tests-9%20passed-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A homemade Intrusion Detection System (IDS) that captures live network traffic with Scapy, extracts relevant features, and applies an **Isolation Forest** anomaly detection model trained on the **NSL-KDD** dataset. Anomalies are reported in real time via Rich terminal output and optionally via Telegram.

---

## Architecture

```
Live Traffic
     │
     ▼
┌─────────────┐     ┌──────────────────┐
│ Scapy       │────▶│ Feature Extractor│
│ Sniffer     │     │ (38 features)    │
└─────────────┘     └────────┬─────────┘
                             │
                    ┌────────▼─────────┐     ┌──────────────┐
                    │ Isolation Forest │◀────│ NSL-KDD      │
                    │ Anomaly Detector │     │ Training Data│
                    └────────┬─────────┘     └──────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
    ┌──────────────────┐         ┌──────────────────┐
    │  Rich Terminal   │         │  Telegram Bot    │
    │  Alert           │         │  Notification    │
    └──────────────────┘         └──────────────────┘
```

---

## Features

- Real-time packet capture (TCP, UDP, ICMP) with Scapy
- 38-feature vector extraction per packet/flow
- Unsupervised anomaly detection with Isolation Forest
- Trained on NSL-KDD — the standard IDS research dataset
- Color-coded Rich terminal output (green = normal, red = anomaly)
- Optional Telegram bot alerts for remote monitoring
- 9 unit tests covering features and detector modules

---

## Project Structure

```
net-ids-ml/
├── src/
│   ├── capture.py       # Scapy real-time sniffer
│   ├── features.py      # Feature extraction + NSL-KDD loader
│   ├── detector.py      # Isolation Forest train/predict
│   └── alerter.py       # Rich console + Telegram alerts
├── data/
│   └── nslkdd/          # NSL-KDD dataset (not committed)
├── models/              # Trained model artifacts (.pkl)
├── tests/
│   ├── test_features.py
│   └── test_detector.py
├── train.py             # Training script
├── ids.py               # Main IDS entry point
├── Makefile
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/CarlosRolo/net-ids-ml.git
cd net-ids-ml
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Download the NSL-KDD dataset:

```bash
wget -P data/nslkdd https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt
wget -P data/nslkdd https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt
```

Train the model:

```bash
make train
```

Run the IDS:

```bash
sudo venv/bin/python ids.py
```

---

## Telegram Alerts (optional)

Create a bot via [@BotFather](https://t.me/BotFather) and get your Chat ID from [@userinfobot](https://t.me/userinfobot).

```bash
cp .env.example .env
# Edit .env with your credentials
```

```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## ML Model — Isolation Forest

| Parameter | Value |
|-----------|-------|
| Algorithm | Isolation Forest |
| Estimators | 100 trees |
| Contamination | 10% |
| Training set | 67,343 normal records (NSL-KDD) |
| Features | 38 numeric (bytes, duration, ports, flags…) |
| Output | normal / ANOMALY + anomaly score |

Isolation Forest works by randomly partitioning the feature space. Anomalous points are isolated in fewer splits — they get a higher anomaly score and are flagged as intrusions.

---

## Usage

```bash
make train        # Train the model on NSL-KDD
make run          # Start live IDS (requires sudo)
make test         # Run all 9 unit tests
make clean        # Remove __pycache__ and .pyc files
```

---

## Dataset

[NSL-KDD](https://github.com/defcom17/NSL_KDD) — the improved version of the KDD Cup 1999 dataset, widely used in IDS research. Contains 125,973 labeled network connection records across 41 features with attack categories: DoS, Probe, R2L, U2R.

---

## Stack

| Tool | Purpose |
|------|---------|
| Scapy 2.5 | Raw packet capture |
| scikit-learn 1.4 | Isolation Forest model |
| pandas / numpy | Feature engineering |
| joblib | Model persistence |
| Rich | Terminal alerts |
| python-dotenv | Environment config |
| pytest | Unit testing |

---

## Author

**Carlos David Rodriguez Lopez**  
Telematic Engineer — ESPOCH  
Riobamba, Chimborazo, Ecuador  
Manta, Manabí, Ecuador  
GitHub: [github.com/CarlosRolo](https://github.com/CarlosRolo)  
LinkedIn: [linkedin.com/in/carlosdrodriguezl](https://linkedin.com/in/carlosdrodriguezl)  

---

## License

MIT License — see [LICENSE](LICENSE)
