import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("🧪 Testing Airtable Server\n")
    
    # Test health check
    print("1️⃣ Health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # Test write endpoint
    print("2️⃣ Writing sample data...")
    response = requests.post(f"{BASE_URL}/write")
    print(f"Status: {response.status_code}\n")
    
    # Test read endpoint
    print("3️⃣ Reading records...")
    response = requests.get(f"{BASE_URL}/read")
    print(f"Status: {response.status_code}\n")
    
    # Test webhook endpoint
    print("4️⃣ Testing webhook...")
    test_payload = {"test": "webhook data", "timestamp": "2025-01-03T10:00:00"}
    response = requests.post(f"{BASE_URL}/webhook", json=test_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_endpoints()