# E-Commerce Customer Analytics Platform 🚀

A **full-stack data science application** featuring interactive dashboards, machine learning models, and RESTful APIs for customer segmentation, churn prediction, and business intelligence.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This is a **production-ready data science platform** that transforms raw e-commerce transaction data into actionable business insights. The system includes:

- 📊 **Interactive Web Dashboard** (Streamlit)
- 🤖 **ML Models** for churn prediction and CLV forecasting
- 🔌 **RESTful API** (FastAPI) for programmatic access
- 💾 **Database Integration** for storing predictions
- 🐳 **Docker Support** for easy deployment

## ✨ Key Features

### 1. **Interactive Dashboard** (`app.py`)
- Real-time customer segmentation visualization
- Sales trend analysis with interactive charts
- Cohort retention heatmaps
- Geographic performance insights
- ML prediction interface

### 2. **Machine Learning Models**
- **Churn Prediction**: Random Forest classifier predicting customer churn probability
- **CLV Prediction**: Random Forest regressor forecasting customer lifetime value
- Automated model training pipeline

### 3. **RESTful API** (`api.py`)
- `/predict/churn` - Predict churn for individual customers
- `/predict/clv` - Predict customer lifetime value
- `/predict/batch` - Batch predictions for multiple customers
- `/stats/summary` - Get business summary statistics
- Interactive API documentation at `/docs`

### 4. **Data Analytics**
- RFM (Recency, Frequency, Monetary) customer segmentation
- Cohort analysis for retention tracking
- Sales pattern analysis (temporal, geographic, product-level)
- Business intelligence dashboards

## 📁 Project Structure

```
├── app.py                 # Streamlit dashboard application
├── api.py                 # FastAPI backend server
├── train_models.py        # ML model training pipeline
├── database.py            # Database operations module
├── ecommerce_analysis.ipynb  # Original analysis notebook
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Multi-container setup
├── run.sh / run.bat      # Startup scripts
├── models/               # Trained ML models (gitignored)
├── Online_Retail.xlsx    # Dataset
└── README.md            # This file
```

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Build and run all services
docker-compose up --build

# Access dashboard at http://localhost:8501
# Access API at http://localhost:8000
```

### Option 2: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aryanchhabra/ecommerce-customer-analytics.git
   cd ecommerce-customer-analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download dataset**
   - Get `Online_Retail.xlsx` from [UCI ML Repository](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx)
   - Place it in the project root directory

4. **Train ML models**
   ```bash
   python train_models.py
   ```

5. **Start the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Start the API** (in a separate terminal)
   ```bash
   uvicorn api:app --reload
   ```

### Option 3: Using Startup Scripts

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

## 📊 Dataset Information

**Source**: UCI Machine Learning Repository - Online Retail Dataset  
**Period**: December 2010 - December 2011  
**Records**: ~540K transactions  
**Features**: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

## 🎯 Usage Examples

### Using the Dashboard

1. Navigate to `http://localhost:8501`
2. Use the sidebar to explore different sections:
   - **Overview**: Business metrics and trends
   - **Customer Segmentation**: RFM analysis and segments
   - **Sales Analysis**: Temporal and geographic patterns
   - **Retention Analysis**: Cohort retention heatmaps
   - **ML Predictions**: Churn and CLV predictions
   - **Geographic Insights**: Country-level performance

### Using the API

**Predict churn for a customer:**
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

**Predict CLV:**
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

**Get summary statistics:**
```bash
curl http://localhost:8000/stats/summary
```

**Interactive API Documentation:**
- Visit `http://localhost:8000/docs` for Swagger UI
- Visit `http://localhost:8000/redoc` for ReDoc

## 🤖 Machine Learning Models

### Churn Prediction Model
- **Algorithm**: Random Forest Classifier
- **Features**: Recency, Frequency, Monetary (RFM)
- **Output**: Churn probability (0-1)
- **Threshold**: >0.5 indicates high churn risk

### CLV Prediction Model
- **Algorithm**: Random Forest Regressor
- **Features**: Recency, Frequency, Monetary (RFM)
- **Output**: Predicted customer lifetime value (£)

### Model Training

Models are automatically trained when you run `train_models.py`. The script:
1. Loads and preprocesses the data
2. Creates churn labels (customers with >90 days recency)
3. Trains both models with train/test split
4. Saves models to `models/` directory

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **SQLite**: Lightweight database for storing predictions
- **scikit-learn**: Machine learning models

### Frontend
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📈 Key Insights from Analysis

- **Champions**: 21% of customers drive 70% of revenue
- **Churn Rate**: ~19% month-1 retention, drops to 13% by month 6
- **Geographic**: UK accounts for 82% of revenue
- **Peak Performance**: Thursday at 12 PM shows highest sales
- **Product Concentration**: Top 10 products generate 15% of revenue

## 🔮 Future Enhancements

- [ ] Real-time data streaming integration
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] A/B testing framework
- [ ] Email/SMS alert system for high-risk customers
- [ ] Integration with CRM systems
- [ ] Automated report generation
- [ ] User authentication and multi-tenancy
- [ ] Advanced feature engineering pipeline

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict/churn` | POST | Predict churn probability |
| `/predict/clv` | POST | Predict customer lifetime value |
| `/predict/batch` | POST | Batch predictions |
| `/stats/summary` | GET | Business summary statistics |
| `/docs` | GET | Interactive API documentation |

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up --build
```

### Run Individual Services
```bash
# Dashboard only
docker run -p 8501:8501 -v $(pwd):/app ecommerce-analytics streamlit run app.py

# API only
docker run -p 8000:8000 -v $(pwd):/app ecommerce-analytics uvicorn api:app --host 0.0.0.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Aryan Chhabra**
- GitHub: [@Aryanchhabra](https://github.com/Aryanchhabra)
- Project: [ecommerce-customer-analytics](https://github.com/Aryanchhabra/ecommerce-customer-analytics)

## 🙏 Acknowledgments

- Dataset: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- Streamlit team for the amazing dashboard framework
- FastAPI team for the high-performance API framework

---

⭐ **Star this repo if you find it helpful!**
