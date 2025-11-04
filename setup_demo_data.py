import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import random

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def delete_all_records():
    print("🗑️ Emptying all tables...\n")
    
    tables = ["Sprints", "Cells", "Proof", "Heartbeats"]
    
    for table in tables:
        try:
            response = requests.get(f"{BASE_URL}/{table}", headers=headers)
            if response.status_code == 200:
                records = response.json().get('records', [])
                record_ids = [record['id'] for record in records]
                
                # Delete in batches of 10
                for i in range(0, len(record_ids), 10):
                    batch = record_ids[i:i+10]
                    delete_url = f"{BASE_URL}/{table}?" + "&".join([f"records[]={rid}" for rid in batch])
                    delete_response = requests.delete(delete_url, headers=headers)
                    
                print(f"🗑️ Deleted {len(record_ids)} records from {table}")
            
        except Exception as e:
            print(f"❌ Error deleting from {table}: {str(e)}")

def add_demo_data():
    print("\n📝 Adding 10 demo records to each table...\n")
    
    # Generate 10 Sprint records
    sprint_records = []
    dev_names = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Adams", 
                 "Frank Miller", "Grace Lee", "Henry Ford", "Ivy Chen", "Jack Wilson"]
    
    for i in range(10):
        sprint_records.append({
            "fields": {
                "Sprint_ID": f"SP-DEMO-{i+1:03d}",
                "Name": f"Sprint {i+1}: Infrastructure Enhancement",
                "Dev_Name": dev_names[i],
                "Status": "Pending",
                "Time_Spent_hr": random.randint(2, 8),
                "Notes": f"Demo sprint {i+1} - implementing core features and optimizations"
            }
        })
    
    # Generate 10 Cell records
    cell_records = []
    roles = ["Builder", "Verifier", "Connector"]
    health_statuses = ["OK", "Warning", "Offline"]
    
    for i in range(10):
        cell_records.append({
            "fields": {
                "Cell_ID": f"CL-DEMO-{i+1:03d}",
                "Role": random.choice(roles),
                "IP_Address": f"10.0.{random.randint(1,10)}.{random.randint(10,99)}",
                "Health_Status": random.choice(health_statuses),
                "Cost_per_hr": round(random.uniform(0.005, 0.025), 3)
            }
        })
    
    # Generate 10 Proof records
    proof_records = []
    results = ["All tests passed successfully", "Integration verified", "Performance benchmarks met", 
               "Security checks completed", "API endpoints validated", "Database sync confirmed",
               "Load testing successful", "Error handling verified", "Monitoring active", "Deployment ready"]
    
    for i in range(10):
        proof_records.append({
            "fields": {
                "Proof_ID": f"PR-DEMO-{i+1:03d}",
                "Sprint_ID": f"SP-DEMO-{i+1:03d}",
                "Result": results[i],
                "Token": f"demo_token_{random.randint(100000, 999999)}",
                "Timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            }
        })
    
    # Generate 10 Heartbeat records (no Timestamp - auto-computed)
    heartbeat_records = []
    statuses = ["Healthy", "Good", "Warning", "High Load", "Optimal", "Normal", "Stable", "Active", "Running", "Online"]
    
    for i in range(10):
        heartbeat_records.append({
            "fields": {
                "Cell_ID": f"CL-DEMO-{i+1:03d}",
                "CPU_Usage": random.randint(15, 95),
                "RAM_Usage": random.randint(25, 90),
                "Status": statuses[i]
            }
        })
    
    # Add records to tables (in batches of 10)
    tables_data = {
        "Sprints": {"records": sprint_records},
        "Cells": {"records": cell_records},
        "Proof": {"records": proof_records},
        "Heartbeats": {"records": heartbeat_records}
    }
    
    for table_name, data in tables_data.items():
        try:
            response = requests.post(f"{BASE_URL}/{table_name}", headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                print(f"✅ {table_name}: Added 10 demo records")
            else:
                print(f"❌ {table_name}: Error {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ {table_name}: Exception - {str(e)}")

if __name__ == "__main__":
    print("🎯 SETTING UP DEMO DATABASE")
    print("=" * 50)
    
    delete_all_records()
    add_demo_data()
    
    print("\n🎉 Demo database ready!")
    print("📊 Each table now has 10 professional demo records")
    print("✅ Perfect for client presentation!")
    print("\n🧪 Run 'python full_verification.py' to test everything")