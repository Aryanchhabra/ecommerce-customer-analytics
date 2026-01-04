"""
Quick test script for the API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_churn_prediction():
    """Test churn prediction"""
    print("\nTesting /predict/churn endpoint...")
    try:
        data = {
            "customer_id": 12345,
            "recency": 45,
            "frequency": 5,
            "monetary": 1200.50
        }
        response = requests.post(f"{BASE_URL}/predict/churn", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_clv_prediction():
    """Test CLV prediction"""
    print("\nTesting /predict/clv endpoint...")
    try:
        data = {
            "customer_id": 12345,
            "recency": 45,
            "frequency": 5,
            "monetary": 1200.50
        }
        response = requests.post(f"{BASE_URL}/predict/clv", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_summary():
    """Test summary endpoint"""
    print("\nTesting /stats/summary endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats/summary")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("API Test Suite")
    print("=" * 50)
    print("\nMake sure the API is running: uvicorn api:app --reload")
    print("=" * 50)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Churn Prediction", test_churn_prediction()))
    results.append(("CLV Prediction", test_clv_prediction()))
    results.append(("Summary Stats", test_summary()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")

