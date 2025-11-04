import requests
import json
import time

BASE_URL = "http://localhost:8000"

def full_verification():
    print("🔍 COMPREHENSIVE AIRTABLE SERVER VERIFICATION")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Health Check
    print("\n1️⃣ HEALTH CHECK")
    print("-" * 30)
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        all_passed = False
    
    # Test 2: Write Operation
    print("\n2️⃣ WRITE OPERATION")
    print("-" * 30)
    try:
        response = requests.post(f"{BASE_URL}/write")
        if response.status_code == 200:
            print("✅ Write operation successful")
            results = response.json()
            for table, result in results.items():
                status = result.get('status', 'Unknown')
                if status in [200, 201]:
                    print(f"   ✅ {table}: {status}")
                else:
                    print(f"   ❌ {table}: {status}")
                    all_passed = False
        else:
            print(f"❌ Write operation failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Write operation error: {str(e)}")
        all_passed = False
    
    # Test 3: Read Operation
    print("\n3️⃣ READ OPERATION")
    print("-" * 30)
    try:
        response = requests.get(f"{BASE_URL}/read")
        if response.status_code == 200:
            print("✅ Read operation successful")
            results = response.json()
            for table, data in results.items():
                if 'records' in data:
                    record_count = len(data['records'])
                    print(f"   ✅ {table}: {record_count} records")
                else:
                    print(f"   ❌ {table}: No records found")
                    all_passed = False
        else:
            print(f"❌ Read operation failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Read operation error: {str(e)}")
        all_passed = False
    
    # Test 4: General Webhook
    print("\n4️⃣ GENERAL WEBHOOK")
    print("-" * 30)
    try:
        test_payload = {"test": "general webhook", "timestamp": "2025-01-04T10:00:00"}
        response = requests.post(f"{BASE_URL}/webhook", json=test_payload)
        if response.status_code == 200:
            print("✅ General webhook working")
            print(f"   Response: {response.json()['status']}")
        else:
            print(f"❌ General webhook failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ General webhook error: {str(e)}")
        all_passed = False
    
    # Test 5: Proof Webhook
    print("\n5️⃣ PROOF WEBHOOK")
    print("-" * 30)
    try:
        proof_payload = {"proof_id": "PR-TEST", "result": "verified", "token": "abc123"}
        response = requests.post(f"{BASE_URL}/proof", json=proof_payload)
        if response.status_code == 200:
            print("✅ Proof webhook working")
            print(f"   Response: {response.json()['status']}")
        else:
            print(f"❌ Proof webhook failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Proof webhook error: {str(e)}")
        all_passed = False
    
    # Test 6: Heartbeat Webhook
    print("\n6️⃣ HEARTBEAT WEBHOOK")
    print("-" * 30)
    try:
        heartbeat_payload = {"cell_id": "CL-TEST", "cpu": 45, "ram": 60, "status": "healthy"}
        response = requests.post(f"{BASE_URL}/heartbeat", json=heartbeat_payload)
        if response.status_code == 200:
            print("✅ Heartbeat webhook working")
            print(f"   Response: {response.json()['status']}")
        else:
            print(f"❌ Heartbeat webhook failed: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"❌ Heartbeat webhook error: {str(e)}")
        all_passed = False
    
    # Final Results
    print("\n" + "=" * 60)
    print("🎯 FINAL VERIFICATION RESULTS")
    print("=" * 60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your Airtable server is ready for client demo")
        print("\n📋 What works:")
        print("   • Health check endpoint")
        print("   • Write data to all 4 Airtable tables")
        print("   • Read data from all 4 Airtable tables")
        print("   • General webhook handler")
        print("   • Proof webhook handler")
        print("   • Heartbeat webhook handler")
        print("   • Console logging with emojis")
        print("\n🚀 Ready to show your client!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Check the errors above and fix them")
    
    return all_passed

if __name__ == "__main__":
    print("⏳ Starting comprehensive verification...")
    print("   Make sure your server is running: python main.py")
    time.sleep(1)
    
    result = full_verification()
    
    if result:
        print("\n🎊 CONGRATULATIONS! Your 5-hour sprint is complete!")
    else:
        print("\n🔧 Please fix the issues above before demo")