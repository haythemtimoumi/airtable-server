import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def test_sprints_without_status():
    print("🧪 Testing Sprints without Status field...\n")
    
    # Test without Status field
    sprint_data = {
        "records": [{
            "fields": {
                "Sprint_ID": "SP-2025-001",
                "Name": "Airtable Integration Sprint",
                "Dev_Name": "John Doe",
                "Time_Spent_hr": 4,
                "Notes": "FastAPI server with full CRUD operations"
            }
        }]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/Sprints", headers=headers, json=sprint_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_sprints_without_status()