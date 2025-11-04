from fastapi import FastAPI, Request
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import random

load_dotenv()

app = FastAPI()

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/")
def root():
    return {"message": "Airtable Server Running"}

@app.post("/write")
def write_sample_data():
    """Push sample data to all Airtable tables"""
    results = {}
    
    # Generate unique ID to avoid duplicates
    unique_id = random.randint(1000, 9999)
    
    # Sample Sprint
    sprint_data = {
        "records": [{
            "fields": {
                "Sprint_ID": f"SP-API-{unique_id}",
                "Name": "API Test Sprint",
                "Dev_Name": "API Bot",
                "Status": "Pending",
                "Time_Spent_hr": 2,
                "Notes": "API test successful"
            }
        }]
    }
    
    # Sample Cell
    cell_data = {
        "records": [{
            "fields": {
                "Cell_ID": f"CL-API-{unique_id}",
                "Role": "Builder",
                "IP_Address": f"192.168.1.{unique_id % 255}",
                "Health_Status": "OK",
                "Cost_per_hr": 0.007
            }
        }]
    }
    
    # Sample Proof
    proof_data = {
        "records": [{
            "fields": {
                "Proof_ID": f"PR-API-{unique_id}",
                "Sprint_ID": f"SP-API-{unique_id}",
                "Result": "All endpoints working",
                "Token": f"api_token_{unique_id}",
                "Timestamp": datetime.now().strftime("%Y-%m-%d")
            }
        }]
    }
    
    # Sample Heartbeat (no Timestamp - it's auto-computed)
    heartbeat_data = {
        "records": [{
            "fields": {
                "Cell_ID": f"CL-API-{unique_id}",
                "CPU_Usage": random.randint(20, 80),
                "RAM_Usage": random.randint(30, 90),
                "Status": "Healthy"
            }
        }]
    }
    
    tables = {
        "Sprints": sprint_data,
        "Cells": cell_data,
        "Proof": proof_data,
        "Heartbeats": heartbeat_data
    }
    
    for table_name, data in tables.items():
        try:
            response = requests.post(f"{BASE_URL}/{table_name}", headers=headers, json=data)
            results[table_name] = {"status": response.status_code, "response": response.json()}
            print(f"✅ {table_name}: {response.status_code}")
        except Exception as e:
            results[table_name] = {"error": str(e)}
            print(f"❌ {table_name}: {str(e)}")
    
    return results

@app.get("/read")
def read_records():
    """Fetch records from all Airtable tables"""
    results = {}
    tables = ["Sprints", "Cells", "Proof", "Heartbeats"]
    
    for table in tables:
        try:
            response = requests.get(f"{BASE_URL}/{table}", headers=headers)
            results[table] = response.json()
            print(f"📖 Read {table}: {len(response.json().get('records', []))} records")
        except Exception as e:
            results[table] = {"error": str(e)}
            print(f"❌ Read {table}: {str(e)}")
    
    return results

@app.post("/webhook")
async def webhook_handler(request: Request):
    """Receive POST requests and log payload"""
    try:
        payload = await request.json()
        timestamp = datetime.now().isoformat()
        
        print(f"🔔 Webhook received at {timestamp}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        return {
            "status": "received",
            "timestamp": timestamp,
            "payload": payload
        }
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        return {"error": str(e)}

@app.post("/proof")
async def proof_webhook(request: Request):
    """Handle proof webhooks"""
    payload = await request.json()
    print(f"🎯 Proof webhook: {json.dumps(payload, indent=2)}")
    return {"status": "proof received", "data": payload}

@app.post("/heartbeat")
async def heartbeat_webhook(request: Request):
    """Handle heartbeat webhooks"""
    payload = await request.json()
    print(f"💓 Heartbeat webhook: {json.dumps(payload, indent=2)}")
    return {"status": "heartbeat received", "data": payload}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)