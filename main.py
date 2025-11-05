from fastapi import FastAPI, Request
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import random

load_dotenv()

app = FastAPI(
    title="Airtable Server API",
    description="Complete CRUD API for Airtable integration",
    version="1.0.0",
    servers=[
        {"url": "https://drop2.fullpotential.ai", "description": "Production server"},
        {"url": "http://drop2.fullpotential.ai", "description": "Production server (HTTP)"},
        {"url": "http://164.92.86.253:8000", "description": "Direct IP access"}
    ]
)

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
    return {
        "message": "Airtable Server Running",
        "domain": "drop2.fullpotential.ai",
        "endpoints": {
            "sprints": "/sprints",
            "cells": "/cells",
            "proof": "/proof",
            "heartbeats": "/heartbeats",
            "webhooks": ["/webhook", "/proof-webhook", "/heartbeat-webhook"]
        },
        "access": [
            "https://drop2.fullpotential.ai",
            "http://drop2.fullpotential.ai"
        ]
    }

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

@app.post("/proof-webhook")
async def proof_webhook(request: Request):
    """Handle proof webhooks"""
    payload = await request.json()
    print(f"🎯 Proof webhook: {json.dumps(payload, indent=2)}")
    return {"status": "proof received", "data": payload}

@app.post("/heartbeat-webhook")
async def heartbeat_webhook(request: Request):
    """Handle heartbeat webhooks"""
    payload = await request.json()
    print(f"💓 Heartbeat webhook: {json.dumps(payload, indent=2)}")
    return {"status": "heartbeat received", "data": payload}

# Individual table endpoints
@app.get("/sprints")
def get_sprints():
    """Get all sprints"""
    try:
        response = requests.get(f"{BASE_URL}/Sprints", headers=headers)
        print(f"📖 Read Sprints: {len(response.json().get('records', []))} records")
        return response.json()
    except Exception as e:
        print(f"❌ Read Sprints error: {str(e)}")
        return {"error": str(e)}

@app.post("/sprints")
async def create_sprint(request: Request):
    """Create new sprint"""
    try:
        data = await request.json()
        payload = {"records": [{"fields": data}]}
        response = requests.post(f"{BASE_URL}/Sprints", headers=headers, json=payload)
        print(f"✅ Created Sprint: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Create Sprint error: {str(e)}")
        return {"error": str(e)}

@app.get("/cells")
def get_cells():
    """Get all cells"""
    try:
        response = requests.get(f"{BASE_URL}/Cells", headers=headers)
        print(f"📖 Read Cells: {len(response.json().get('records', []))} records")
        return response.json()
    except Exception as e:
        print(f"❌ Read Cells error: {str(e)}")
        return {"error": str(e)}

@app.post("/cells")
async def create_cell(request: Request):
    """Create new cell"""
    try:
        data = await request.json()
        payload = {"records": [{"fields": data}]}
        response = requests.post(f"{BASE_URL}/Cells", headers=headers, json=payload)
        print(f"✅ Created Cell: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Create Cell error: {str(e)}")
        return {"error": str(e)}

@app.get("/proof")
def get_proof():
    """Get all proof records"""
    try:
        response = requests.get(f"{BASE_URL}/Proof", headers=headers)
        print(f"📖 Read Proof: {len(response.json().get('records', []))} records")
        return response.json()
    except Exception as e:
        print(f"❌ Read Proof error: {str(e)}")
        return {"error": str(e)}

@app.post("/proof")
async def create_proof_record(request: Request):
    """Create new proof record"""
    try:
        data = await request.json()
        payload = {"records": [{"fields": data}]}
        response = requests.post(f"{BASE_URL}/Proof", headers=headers, json=payload)
        print(f"✅ Created Proof: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Create Proof error: {str(e)}")
        return {"error": str(e)}

@app.get("/heartbeats")
def get_heartbeats():
    """Get all heartbeats"""
    try:
        response = requests.get(f"{BASE_URL}/Heartbeats", headers=headers)
        print(f"📖 Read Heartbeats: {len(response.json().get('records', []))} records")
        return response.json()
    except Exception as e:
        print(f"❌ Read Heartbeats error: {str(e)}")
        return {"error": str(e)}

@app.post("/heartbeats")
async def create_heartbeat(request: Request):
    """Create new heartbeat"""
    try:
        data = await request.json()
        payload = {"records": [{"fields": data}]}
        response = requests.post(f"{BASE_URL}/Heartbeats", headers=headers, json=payload)
        print(f"✅ Created Heartbeat: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Create Heartbeat error: {str(e)}")
        return {"error": str(e)}

# UPDATE operations
@app.put("/sprints/{record_id}")
async def update_sprint(record_id: str, request: Request):
    """Update sprint record"""
    try:
        data = await request.json()
        payload = {"records": [{"id": record_id, "fields": data}]}
        response = requests.patch(f"{BASE_URL}/Sprints", headers=headers, json=payload)
        print(f"✅ Updated Sprint {record_id}: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Update Sprint error: {str(e)}")
        return {"error": str(e)}

@app.put("/cells/{record_id}")
async def update_cell(record_id: str, request: Request):
    """Update cell record"""
    try:
        data = await request.json()
        payload = {"records": [{"id": record_id, "fields": data}]}
        response = requests.patch(f"{BASE_URL}/Cells", headers=headers, json=payload)
        print(f"✅ Updated Cell {record_id}: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Update Cell error: {str(e)}")
        return {"error": str(e)}

@app.put("/proof/{record_id}")
async def update_proof(record_id: str, request: Request):
    """Update proof record"""
    try:
        data = await request.json()
        payload = {"records": [{"id": record_id, "fields": data}]}
        response = requests.patch(f"{BASE_URL}/Proof", headers=headers, json=payload)
        print(f"✅ Updated Proof {record_id}: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Update Proof error: {str(e)}")
        return {"error": str(e)}

@app.put("/heartbeats/{record_id}")
async def update_heartbeat(record_id: str, request: Request):
    """Update heartbeat record"""
    try:
        data = await request.json()
        payload = {"records": [{"id": record_id, "fields": data}]}
        response = requests.patch(f"{BASE_URL}/Heartbeats", headers=headers, json=payload)
        print(f"✅ Updated Heartbeat {record_id}: {response.status_code}")
        return {"status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"❌ Update Heartbeat error: {str(e)}")
        return {"error": str(e)}

# DELETE operations
@app.delete("/sprints/{record_id}")
def delete_sprint(record_id: str):
    """Delete sprint record"""
    try:
        response = requests.delete(f"{BASE_URL}/Sprints/{record_id}", headers=headers)
        print(f"✅ Deleted Sprint {record_id}: {response.status_code}")
        return {"status": response.status_code, "message": "Sprint deleted"}
    except Exception as e:
        print(f"❌ Delete Sprint error: {str(e)}")
        return {"error": str(e)}

@app.delete("/cells/{record_id}")
def delete_cell(record_id: str):
    """Delete cell record"""
    try:
        response = requests.delete(f"{BASE_URL}/Cells/{record_id}", headers=headers)
        print(f"✅ Deleted Cell {record_id}: {response.status_code}")
        return {"status": response.status_code, "message": "Cell deleted"}
    except Exception as e:
        print(f"❌ Delete Cell error: {str(e)}")
        return {"error": str(e)}

@app.delete("/proof/{record_id}")
def delete_proof(record_id: str):
    """Delete proof record"""
    try:
        response = requests.delete(f"{BASE_URL}/Proof/{record_id}", headers=headers)
        print(f"✅ Deleted Proof {record_id}: {response.status_code}")
        return {"status": response.status_code, "message": "Proof deleted"}
    except Exception as e:
        print(f"❌ Delete Proof error: {str(e)}")
        return {"error": str(e)}

@app.delete("/heartbeats/{record_id}")
def delete_heartbeat(record_id: str):
    """Delete heartbeat record"""
    try:
        response = requests.delete(f"{BASE_URL}/Heartbeats/{record_id}", headers=headers)
        print(f"✅ Deleted Heartbeat {record_id}: {response.status_code}")
        return {"status": response.status_code, "message": "Heartbeat deleted"}
    except Exception as e:
        print(f"❌ Delete Heartbeat error: {str(e)}")
        return {"error": str(e)}

@app.post("/daily-digest")
def generate_daily_digest():
    """Generate daily digest summary"""
    try:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get data from all tables
        sprints_response = requests.get(f"{BASE_URL}/Sprints", headers=headers)
        cells_response = requests.get(f"{BASE_URL}/Cells", headers=headers)
        proof_response = requests.get(f"{BASE_URL}/Proof", headers=headers)
        heartbeats_response = requests.get(f"{BASE_URL}/Heartbeats", headers=headers)
        
        sprints = sprints_response.json().get('records', [])
        cells = cells_response.json().get('records', [])
        proofs = proof_response.json().get('records', [])
        heartbeats = heartbeats_response.json().get('records', [])
        
        # Calculate metrics
        total_droplets = len(cells)
        active_droplets = len([c for c in cells if c.get('fields', {}).get('Health_Status') == 'OK'])
        uptime_percentage = (active_droplets / total_droplets * 100) if total_droplets > 0 else 0
        offline_cells = total_droplets - active_droplets
        
        total_sprints = len(sprints)
        completed_sprints = len([s for s in sprints if s.get('fields', {}).get('Status') == 'Done'])
        in_progress_sprints = len([s for s in sprints if s.get('fields', {}).get('Status') in ['Active', 'Pending']])
        
        total_proofs = len(proofs)
        verified_proofs = len([p for p in proofs if 'passed' in str(p.get('fields', {}).get('Result', '')).lower()])
        failed_proofs = len([p for p in proofs if 'failed' in str(p.get('fields', {}).get('Result', '')).lower()])
        pending_proofs = total_proofs - verified_proofs - failed_proofs
        
        # Calculate heartbeat averages
        cpu_values = [h.get('fields', {}).get('CPU_Usage', 0) for h in heartbeats if h.get('fields', {}).get('CPU_Usage')]
        ram_values = [h.get('fields', {}).get('RAM_Usage', 0) for h in heartbeats if h.get('fields', {}).get('RAM_Usage')]
        
        average_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
        average_ram = sum(ram_values) / len(ram_values) if ram_values else 0
        
        # Get last ping time
        last_ping_time = ""
        if heartbeats:
            timestamps = [h.get('createdTime', '') for h in heartbeats]
            last_ping_time = max(timestamps) if timestamps else ""
        
        # Generate warnings
        offline_cell_ids = [c.get('fields', {}).get('Cell_ID', 'Unknown') for c in cells 
                           if c.get('fields', {}).get('Health_Status') != 'OK']
        warnings = f"Offline cells: {', '.join(offline_cell_ids)}" if offline_cell_ids else "All systems operational"
        
        # Create digest record
        digest_data = {
            "records": [{
                "fields": {
                    "Date": today,
                    "Total_Droplets": total_droplets,
                    "Active_Droplets": active_droplets,
                    "Uptime_Percentage": round(uptime_percentage, 2),
                    "Offline_Cells": offline_cells,
                    "Total_Sprints": total_sprints,
                    "Completed_Sprints": completed_sprints,
                    "In_Progress_Sprints": in_progress_sprints,
                    "Total_Proofs": total_proofs,
                    "Verified_Proofs": verified_proofs,
                    "Failed_Proofs": failed_proofs,
                    "Pending_Proofs": pending_proofs,
                    "Average_CPU": round(average_cpu, 2),
                    "Average_RAM": round(average_ram, 2),
                    "Last_Ping_Time": last_ping_time,
                    "Warnings": warnings,
                    "Timestamp": datetime.now().isoformat()
                }
            }]
        }
        
        # Save to Daily_Digest table
        response = requests.post(f"{BASE_URL}/Daily_Digest", headers=headers, json=digest_data)
        print(f"📊 Daily digest generated: {response.status_code}")
        
        return {
            "status": response.status_code,
            "message": "Daily digest generated successfully",
            "data": response.json(),
            "summary": {
                "total_droplets": total_droplets,
                "active_droplets": active_droplets,
                "uptime_percentage": f"{uptime_percentage:.2f}%",
                "total_sprints": total_sprints,
                "completed_sprints": completed_sprints,
                "total_proofs": total_proofs,
                "verified_proofs": verified_proofs
            }
        }
        
    except Exception as e:
        print(f"❌ Daily digest error: {str(e)}")
        return {"error": str(e)}

# Automatic daily digest scheduler
import threading
import time
from datetime import datetime, time as dt_time

def daily_digest_scheduler():
    """Run daily digest at 6 AM every day"""
    while True:
        now = datetime.now()
        # Run at 6:00 AM
        target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        
        # If it's past 6 AM today, schedule for tomorrow
        if now.time() > dt_time(6, 0):
            target_time = target_time.replace(day=target_time.day + 1)
        
        # Calculate seconds until target time
        sleep_seconds = (target_time - now).total_seconds()
        
        print(f"📅 Next daily digest scheduled for: {target_time}")
        time.sleep(sleep_seconds)
        
        # Generate daily digest
        try:
            print("🕕 Running scheduled daily digest...")
            generate_daily_digest()
        except Exception as e:
            print(f"❌ Scheduled digest error: {str(e)}")
        
        # Sleep for 1 hour to avoid running multiple times
        time.sleep(3600)

if __name__ == "__main__":
    import uvicorn
    
    # Start daily digest scheduler in background
    scheduler_thread = threading.Thread(target=daily_digest_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("🚀 Starting server with automatic daily digest scheduler...")
    uvicorn.run(app, host="0.0.0.0", port=8000)