"""
Train ML Models for Customer Churn and CLV Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import pickle
import os
from datetime import datetime, timedelta

def load_and_prepare_data():
    """Load and prepare data for modeling"""
    print("Loading data...")
    df = pd.read_excel('Online_Retail.xlsx')
    
    # Clean data
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['CustomerID'])
    df_clean = df_clean[df_clean['Quantity'] > 0]
    df_clean = df_clean[df_clean['UnitPrice'] > 0]
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    
    # Calculate RFM
    snapshot_date = df_clean['InvoiceDate'].max() + timedelta(days=1)
    
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    return rfm

def create_churn_labels(rfm, threshold_days=90):
    """Create churn labels based on recency"""
    # If customer hasn't purchased in threshold_days, consider them churned
    rfm['Churned'] = (rfm['Recency'] > threshold_days).astype(int)
    return rfm

def train_churn_model(rfm):
    """Train churn prediction model"""
    print("\n=== Training Churn Prediction Model ===")
    
    # Features
    X = rfm[['Recency', 'Frequency', 'Monetary']].values
    y = rfm['Churned'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and scaler
    os.makedirs('models', exist_ok=True)
    with open('models/churn_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/churn_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Churn model saved to models/churn_model.pkl")
    return model, scaler

def train_clv_model(rfm):
    """Train Customer Lifetime Value prediction model"""
    print("\n=== Training CLV Prediction Model ===")
    
    # Features
    X = rfm[['Recency', 'Frequency', 'Monetary']].values
    y = rfm['Monetary'].values  # Using current monetary as target (can be enhanced)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"MSE: {mse:,.2f}")
    print(f"R² Score: {r2:.4f}")
    
    # Save model and scaler
    with open('models/clv_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/clv_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("CLV model saved to models/clv_model.pkl")
    return model, scaler

def main():
    print("=" * 50)
    print("ML Model Training Pipeline")
    print("=" * 50)
    
    # Load data
    rfm = load_and_prepare_data()
    print(f"Loaded {len(rfm)} customers")
    
    # Create churn labels
    rfm = create_churn_labels(rfm)
    print(f"Churn rate: {rfm['Churned'].mean()*100:.1f}%")
    
    # Train models
    churn_model, churn_scaler = train_churn_model(rfm)
    clv_model, clv_scaler = train_clv_model(rfm)
    
    print("\n" + "=" * 50)
    print("All models trained and saved successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()

