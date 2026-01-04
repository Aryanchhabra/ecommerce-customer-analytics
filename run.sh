#!/bin/bash

# Full-stack E-Commerce Analytics - Startup Script

echo "🚀 Starting E-Commerce Analytics Platform..."

# Check if models exist
if [ ! -f "models/churn_model.pkl" ] || [ ! -f "models/clv_model.pkl" ]; then
    echo "📊 Training ML models..."
    python train_models.py
fi

# Start services
echo "🌐 Starting Streamlit Dashboard..."
streamlit run app.py --server.port=8501 &

echo "🔌 Starting FastAPI Backend..."
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &

echo "✅ Services started!"
echo "📊 Dashboard: http://localhost:8501"
echo "🔌 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"

wait

