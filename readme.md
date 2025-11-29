# 🛡️ Aegis: AI-Powered Real-Time Fraud Detection System

> **Internship Project:** End-to-End Financial Anomaly Detection Pipeline  
> **Technique:** Unsupervised Machine Learning (Isolation Forest)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)
![Sklearn](https://img.shields.io/badge/Sklearn-IsolationForest-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)

---

## 📖 Project Overview

**Aegis** is a comprehensive fraud detection system designed to identify suspicious financial transactions in real-time. Unlike traditional rule-based systems, Aegis uses **Machine Learning (Isolation Forest)** to learn patterns and detect anomalies dynamically.

This project demonstrates a full-stack data science pipeline: from **Data Generation & Training** to **API Deployment** and **Live Monitoring**.

### 🎯 Internship Milestones
* **Week 1:** Data Analysis & Model Training (Synthetic Data Generation).
* **Week 2:** Model Deployment via REST API (FastAPI).
* **Week 3:** Database Integration & Logging (SQLite/SQLAlchemy).
* **Week 4:** Live Dashboard & Simulation (Streamlit).

---

## ✨ Key Features

Aegis analyzes transactions based on **4 Critical Risk Factors**:

1.  💸 **Amount Anomalies:** Detects unusually high transaction values.
2.  🌏 **Impossible Travel (Distance):** Flags transactions occurring at impossible distances from the user's location.
3.  🌙 **Time-Based Patterns (New):** Identifies suspicious activity during unusual hours (e.g., Late Night 1 AM - 4 AM).
4.  ⚡ **High-Frequency Bursts (New):** Detects "rapid-fire" transactions (e.g., 50+ transactions in seconds).

---

## 🛠️ Tech Stack

| Component | Technology Used | Description |
| :--- | :--- | :--- |
| **Model** | `Scikit-Learn` (Isolation Forest) | Unsupervised Anomaly Detection |
| **Data Processing** | `Pandas`, `Numpy` | Data manipulation & synthetic generation |
| **API Backend** | `FastAPI`, `Uvicorn` | Serving the model for real-time predictions |
| **Database** | `SQLite`, `SQLAlchemy` | Logging transaction history & predictions |
| **Dashboard** | `Streamlit`, `Altair` | Live visualization & KPI monitoring |
| **Simulation** | `Python Requests` | Simulates a live stream of user transactions |

---

## 📂 Project Structure

```bash
Aegis-Fraud-Detection/
├── Model/
│   ├── model.py          # 🧠 Trains and saves the Isolation Forest model
│   ├── api.py            # 🚀 FastAPI backend to serve predictions
│   ├── producer.py       # 📡 Simulates live transactions (Good/Fraud)
│   ├── Dashboard.py      # 📊 Streamlit Dashboard for monitoring
│   ├── aegis.db          # 🗄️ SQLite Database (Auto-generated)
│   └── model             # 📦 Serialized ML Model (Auto-generated)
└── README.md             # 📄 Documentation

#How to Run the Project
Follow these steps to launch the entire system on your local machine.

Step 1: Train the Model 🧠
Generate synthetic data (including new Time/Frequency patterns) and train the model.

Bash

Model/model.py
# Output: ✅ Advanced Model saved to model
Step 2: Start the API Server 🚀
Launch the FastAPI backend. This will also create the database aegis.db.

Bash

Model/api.py
# Output: Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000)
Step 3: Start Transaction Simulation 📡
Open a new terminal and run the producer to generate live traffic.

Bash

Model/producer.py
# Output: 🔴 Blocked: Suspicious Time | 🟢 Approved ...
Step 4: Launch the Dashboard 📊
Open a third terminal to visualize the data in real-time.

Bash

streamlit run Model/Dashboard.py
📊 Dashboard Preview
The dashboard provides real-time insights into the system's performance:

Live KPI Metrics: Total Transactions, Fraud Rate, Blocked Counts.

Interactive Scatter Plot: Visualizes normal vs. anomalous transactions based on Amount, Time, and Distance.

Live Logs: A scrolling table of the most recent API decisions.

🔮 Future Scope
Deep Learning: Implementing LSTM/Autoencoders for sequence-based fraud detection.

Geolocation API: Integration with Google Maps API for real coordinates.

Notification System: Email/SMS alerts for high-risk transactions.

👨‍💻 Author
Name: [Saurabh Mishra]

Role: Data Science & Machine Learning Intern

Project: Aegis Fraud Detection System