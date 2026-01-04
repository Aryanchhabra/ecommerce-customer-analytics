@echo off
echo Starting E-Commerce Analytics Platform...

REM Check if models exist
if not exist "models\churn_model.pkl" (
    echo Training ML models...
    python train_models.py
)

REM Start Streamlit Dashboard
echo Starting Streamlit Dashboard...
start "Dashboard" cmd /k streamlit run app.py --server.port=8501

REM Start FastAPI Backend
timeout /t 3 /nobreak >nul
echo Starting FastAPI Backend...
start "API" cmd /k uvicorn api:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Services started!
echo Dashboard: http://localhost:8501
echo API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
pause

