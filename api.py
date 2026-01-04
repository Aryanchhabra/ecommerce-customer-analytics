"""
FastAPI Backend for E-Commerce Analytics
REST API for ML predictions and data access
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
from typing import Optional, List

app = FastAPI(
    title="E-Commerce Analytics API",
    description="API for customer analytics and ML predictions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class CustomerPrediction(BaseModel):
    customer_id: int
    recency: float
    frequency: float
    monetary: float

class BatchPrediction(BaseModel):
    customers: List[CustomerPrediction]

# Load models and scalers
churn_model = None
clv_model = None
churn_scaler = None
clv_scaler = None

def load_models():
    """Load ML models and scalers"""
    global churn_model, clv_model, churn_scaler, clv_scaler
    if os.path.exists('models/churn_model.pkl'):
        with open('models/churn_model.pkl', 'rb') as f:
            churn_model = pickle.load(f)
    if os.path.exists('models/churn_scaler.pkl'):
        with open('models/churn_scaler.pkl', 'rb') as f:
            churn_scaler = pickle.load(f)
    if os.path.exists('models/clv_model.pkl'):
        with open('models/clv_model.pkl', 'rb') as f:
            clv_model = pickle.load(f)
    if os.path.exists('models/clv_scaler.pkl'):
        with open('models/clv_scaler.pkl', 'rb') as f:
            clv_scaler = pickle.load(f)

load_models()

@app.get("/")
def root():
    return {
        "message": "E-Commerce Analytics API",
        "endpoints": {
            "/predict/churn": "Predict customer churn probability",
            "/predict/clv": "Predict customer lifetime value",
            "/predict/batch": "Batch predictions for multiple customers",
            "/health": "Health check"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    models_loaded = churn_model is not None and clv_model is not None
    return {
        "status": "healthy",
        "models_loaded": models_loaded,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict/churn")
def predict_churn(customer: CustomerPrediction):
    """Predict churn probability for a single customer"""
    if churn_model is None or churn_scaler is None:
        raise HTTPException(status_code=503, detail="Churn model not loaded")
    
    features = np.array([[customer.recency, customer.frequency, customer.monetary]])
    features_scaled = churn_scaler.transform(features)
    probability = churn_model.predict_proba(features_scaled)[0][1]
    
    return {
        "customer_id": customer.customer_id,
        "churn_probability": float(probability),
        "churn_risk": "high" if probability > 0.5 else "low",
        "recommendation": "Retention campaign needed" if probability > 0.5 else "Customer is stable"
    }

@app.post("/predict/clv")
def predict_clv(customer: CustomerPrediction):
    """Predict customer lifetime value"""
    if clv_model is None or clv_scaler is None:
        raise HTTPException(status_code=503, detail="CLV model not loaded")
    
    features = np.array([[customer.recency, customer.frequency, customer.monetary]])
    features_scaled = clv_scaler.transform(features)
    clv = clv_model.predict(features_scaled)[0]
    
    return {
        "customer_id": customer.customer_id,
        "predicted_clv": float(clv),
        "current_value": float(customer.monetary),
        "potential_growth": float(clv - customer.monetary)
    }

@app.post("/predict/batch")
def batch_predict(customers: BatchPrediction):
    """Batch predictions for multiple customers"""
    if churn_model is None or clv_model is None or churn_scaler is None or clv_scaler is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    results = []
    for customer in customers.customers:
        features = np.array([[customer.recency, customer.frequency, customer.monetary]])
        
        # Scale features
        features_churn_scaled = churn_scaler.transform(features)
        features_clv_scaled = clv_scaler.transform(features)
        
        churn_prob = churn_model.predict_proba(features_churn_scaled)[0][1]
        clv_pred = clv_model.predict(features_clv_scaled)[0]
        
        results.append({
            "customer_id": customer.customer_id,
            "churn_probability": float(churn_prob),
            "predicted_clv": float(clv_pred),
            "churn_risk": "high" if churn_prob > 0.5 else "low"
        })
    
    return {
        "predictions": results,
        "total_customers": len(results),
        "high_risk_count": sum(1 for r in results if r["churn_risk"] == "high")
    }

@app.get("/stats/summary")
def get_summary_stats():
    """Get summary statistics from the dataset"""
    if not os.path.exists('Online_Retail.xlsx'):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    df = pd.read_excel('Online_Retail.xlsx')
    df_clean = df.dropna(subset=['CustomerID'])
    df_clean = df_clean[df_clean['Quantity'] > 0]
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    return {
        "total_customers": int(df_clean['CustomerID'].nunique()),
        "total_revenue": float(df_clean['TotalAmount'].sum()),
        "total_orders": int(df_clean['InvoiceNo'].nunique()),
        "avg_order_value": float(df_clean.groupby('InvoiceNo')['TotalAmount'].sum().mean()),
        "date_range": {
            "start": str(df_clean['InvoiceDate'].min()),
            "end": str(df_clean['InvoiceDate'].max())
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

