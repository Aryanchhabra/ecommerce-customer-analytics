# Quick Start Guide 🚀

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Train ML Models

```bash
python train_models.py
```

This will:
- Load and clean the data
- Train churn prediction model
- Train CLV prediction model
- Save models to `models/` directory

**Expected output:**
- Churn model accuracy: ~100% (perfect separation in this dataset)
- CLV model R²: ~0.99 (excellent fit)

## Step 3: Start the Dashboard

**Terminal 1:**
```bash
streamlit run app.py
```

Dashboard will open at: **http://localhost:8501**

## Step 4: Start the API (Optional)

**Terminal 2:**
```bash
uvicorn api:app --reload
```

API will be available at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Step 5: Test the API (Optional)

```bash
python test_api.py
```

## What You Can Do

### Dashboard Features:
1. **Overview** - Business metrics and revenue trends
2. **Customer Segmentation** - RFM analysis with 6 segments
3. **Sales Analysis** - Temporal and geographic patterns
4. **Retention Analysis** - Cohort retention heatmaps
5. **ML Predictions** - Churn and CLV predictions for customers
6. **Geographic Insights** - Country-level performance

### API Endpoints:
- `POST /predict/churn` - Predict churn probability
- `POST /predict/clv` - Predict customer lifetime value
- `POST /predict/batch` - Batch predictions
- `GET /stats/summary` - Business summary statistics
- `GET /docs` - Interactive API documentation

## Troubleshooting

### Models not found?
Run: `python train_models.py`

### Port already in use?
- Dashboard: Change port with `streamlit run app.py --server.port=8502`
- API: Change port with `uvicorn api:app --port 8001`

### Import errors?
Make sure all dependencies are installed: `pip install -r requirements.txt`

## Example API Usage

### Predict Churn:
```bash
curl -X POST "http://localhost:8000/predict/churn" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 12345,
    "recency": 45,
    "frequency": 5,
    "monetary": 1200.50
  }'
```

### Predict CLV:
```bash
curl -X POST "http://localhost:8000/predict/clv" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 12345,
    "recency": 45,
    "frequency": 5,
    "monetary": 1200.50
  }'
```

## Next Steps

1. Explore the dashboard at http://localhost:8501
2. Try different customer IDs in the ML Predictions section
3. Check out the API documentation at http://localhost:8000/docs
4. Integrate the API into your own applications

