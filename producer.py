import time
import requests
import random
import uuid

API_URL = "http://localhost:8000/predict"

def generate_transaction():
    is_fraud = random.random() < 0.035 # 3.5% fraud chance

    # Default Normal Behavior
    amount = round(random.uniform(10, 500), 2)
    dist = round(random.uniform(1, 20), 2)
    hour = random.randint(9, 22) # Daytime
    freq = random.randint(1, 3)  # Normal frequency
    
    if is_fraud:
        fraud_type = random.choice(['amount', 'dist', 'time', 'freq'])
        
        if fraud_type == 'amount':
            amount = round(random.uniform(5000, 15000), 2)
        elif fraud_type == 'dist':
            dist = round(random.uniform(500, 2000), 2)
        elif fraud_type == 'time':
            hour = random.choice([1, 2, 3, 4]) # Late night!
        elif fraud_type == 'freq':
            freq = random.randint(15, 50) # Rapid fire transactions!

    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": amount,
        "distance_km": dist,
        "hour": hour,
        "frequency": freq
    }

print("🚀 Starting Advanced Simulation...")
print(f"📡 Connecting to {API_URL}...")

while True:
    try:
        txn = generate_transaction()
        resp = requests.post(API_URL, json=txn)
        data = resp.json()
        
        icon = "🔴" if data['is_fraud'] else "🟢"
        # Print details including the new features
        print(f"{icon} {data['message']} | Amt:${txn['amount']} | Time:{txn['hour']}h | Freq:{txn['frequency']}")
        
    except Exception as e:
        print("❌ Connection Failed. Ensure API is running.")
    
    time.sleep(1)