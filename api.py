import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- Database Setup ---
DATABASE_URL = "sqlite:///./aegis.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TransactionLog(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    amount = Column(Float)
    distance_km = Column(Float)
    hour = Column(Integer)      # New Field
    frequency = Column(Integer) # New Field
    prediction = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- API Setup ---
app = FastAPI(title="Aegis Advanced Fraud Detection")
model = joblib.load("model")

class TransactionIn(BaseModel):
    transaction_id: str
    amount: float
    distance_km: float
    hour: int          # New Input
    frequency: int     # New Input

class TransactionOut(BaseModel):
    transaction_id: str
    is_fraud: bool
    message: str

@app.post("/predict", response_model=TransactionOut)
def predict_transaction(txn: TransactionIn):
    # 1. Prepare features (Order must match model training!)
    features = pd.DataFrame(
        [[txn.amount, txn.distance_km, txn.hour, txn.frequency]], 
        columns=['amount', 'distance_km', 'hour', 'frequency']
    )
    
    # 2. Predict
    prediction = model.predict(features)[0]
    is_fraud = True if prediction == -1 else False
    
    # 3. Log to DB
    db = SessionLocal()
    db_record = TransactionLog(
        transaction_id=txn.transaction_id,
        amount=txn.amount,
        distance_km=txn.distance_km,
        hour=txn.hour,
        frequency=txn.frequency,
        prediction=int(prediction)
    )
    db.add(db_record)
    db.commit()
    db.close()
    
    # 4. Response
    msg = "Approved"
    if is_fraud:
        # Determine reason for blocking for the message
        if txn.hour < 5:
            msg = "Blocked: Suspicious Time (Late Night)"
        elif txn.frequency > 10:
            msg = "Blocked: High Frequency Burst"
        elif txn.amount > 5000:
            msg = "Blocked: Large Amount"
        else:
            msg = "Blocked: Anomalous Pattern"

    return {
        "transaction_id": txn.transaction_id,
        "is_fraud": is_fraud,
        "message": msg
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)