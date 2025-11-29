import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import random
import os

def load_or_generate_data(n_samples=5000):
    """
    Generates synthetic data including Time and Frequency patterns.
    """
    print(f"⚠️ Generating {n_samples} synthetic records with advanced patterns...")
    
    data = []
    for _ in range(n_samples):
        # 3.5% chance of fraud
        is_fraud = random.random() < 0.035
        
        if is_fraud:
            # Fraud Patterns (One of these will be suspicious)
            fraud_type = random.choice(['amount', 'distance', 'time', 'frequency'])
            
            if fraud_type == 'amount':
                amount = random.uniform(5000, 20000) # Very high amount
                dist = random.uniform(0, 50)
                hour = int(random.uniform(8, 22))    # Normal time
                freq = random.randint(1, 3)
            elif fraud_type == 'distance':
                amount = random.uniform(10, 500)
                dist = random.uniform(500, 5000)     # Impossible travel
                hour = int(random.uniform(8, 22))
                freq = random.randint(1, 3)
            elif fraud_type == 'time':
                amount = random.uniform(10, 500)
                dist = random.uniform(0, 50)
                hour = random.choice([0, 1, 2, 3, 4]) # Late night (suspicious)
                freq = random.randint(1, 3)
            elif fraud_type == 'frequency':
                amount = random.uniform(10, 500)
                dist = random.uniform(0, 50)
                hour = int(random.uniform(8, 22))
                freq = random.randint(10, 50)         # High frequency (many txns)
            
            label = -1 # Anomaly
        else:
            # Normal Pattern
            amount = random.uniform(10, 1000)
            dist = random.uniform(0, 100)
            hour = int(random.uniform(6, 23))    # Daytime/Evening
            freq = random.randint(1, 5)          # Low frequency
            label = 1 # Normal
            
        data.append([amount, dist, hour, freq, label])
        
    return pd.DataFrame(data, columns=['amount', 'distance_km', 'hour', 'frequency', 'actual_label'])

def train():
    # Step 1: Generate Data
    df = load_or_generate_data()
    
    # Step 2: Select Features (Added 'hour' and 'frequency')
    features = ['amount', 'distance_km', 'hour', 'frequency']
    X = df[features]
    y = df['actual_label']
    
    # Step 3: Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("🧠 Training Isolation Forest with new features...")
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X_train)
    
    # Step 4: Evaluate
    y_pred = model.predict(X_test)
    print("\n📊 Model Performance:")
    print(classification_report(y_test, y_pred, target_names=['Fraud', 'Normal']))
    
    # Step 5: Save
    model_path = "model"
    joblib.dump(model, model_path)
    print(f"✅ Advanced Model saved to {model_path}")

if __name__ == "__main__":
    train()