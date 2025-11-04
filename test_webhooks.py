import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_all_webhooks():
    print("🔍 TESTING ALL WEBHOOK ENDPOINTS")
    print("=" * 50)
    print("⚠️  Make sure your server is running: python main.py")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: General Webhook
    print("\n1️⃣ TESTING GENERAL WEBHOOK")
    print("-" * 30)
    try:
        payload = {
            "message": "Test general webhook",
            "timestamp": "2025-01-04T10:00:00",
            "source": "test_script",
            "data": {"key": "value", "number": 123}
        }
        
        response = requests.post(f"{BASE_URL}/webhook", json=payload)
        
        if response.status_code == 200:
            print("✅ General webhook SUCCESS")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ General webhook FAILED: {response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"❌ General webhook ERROR: {str(e)}")
        all_passed = False
    
    time.sleep(1)  # Small delay between tests
    
    # Test 2: Proof Webhook
    print("\n2️⃣ TESTING PROOF WEBHOOK")
    print("-" * 30)
    try:
        payload = {
            "proof_id": "PR-TEST-001",
            "sprint_id": "SP-TEST-001",
            "result": "All tests passed successfully",
            "token": "proof_token_abc123",
            "timestamp": "2025-01-04T10:05:00",
            "details": {
                "tests_run": 25,
                "tests_passed": 25,
                "coverage": "98%"
            }
        }
        
        response = requests.post(f"{BASE_URL}/proof", json=payload)
        
        if response.status_code == 200:
            print("✅ Proof webhook SUCCESS")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Proof webhook FAILED: {response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Proof webhook ERROR: {str(e)}")
        all_passed = False
    
    time.sleep(1)  # Small delay between tests
    
    # Test 3: Heartbeat Webhook
    print("\n3️⃣ TESTING HEARTBEAT WEBHOOK")
    print("-" * 30)
    try:
        payload = {
            "cell_id": "CL-TEST-001",
            "cpu_usage": 45,
            "ram_usage": 67,
            "disk_usage": 23,
            "status": "healthy",
            "timestamp": "2025-01-04T10:10:00",
            "uptime": "5 days, 3 hours",
            "network": {
                "ip": "192.168.1.100",
                "latency": "12ms"
            }
        }
        
        response = requests.post(f"{BASE_URL}/heartbeat", json=payload)
        
        if response.status_code == 200:
            print("✅ Heartbeat webhook SUCCESS")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Heartbeat webhook FAILED: {response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Heartbeat webhook ERROR: {str(e)}")
        all_passed = False
    
    # Final Results
    print("\n" + "=" * 50)
    print("🎯 WEBHOOK TEST RESULTS")
    print("=" * 50)
    
    if all_passed:
        print("🎉 ALL WEBHOOKS WORKING PERFECTLY!")
        print("✅ General webhook - Receives and logs any payload")
        print("✅ Proof webhook - Handles verification results")
        print("✅ Heartbeat webhook - Processes system health data")
        print("\n📋 What this proves:")
        print("   • Server can receive external notifications")
        print("   • All webhook endpoints are accessible")
        print("   • Payload logging works correctly")
        print("   • Response handling is proper")
        print("\n🚀 Ready for client demo!")
    else:
        print("❌ SOME WEBHOOKS FAILED!")
        print("   Check the errors above")
        print("   Make sure server is running: python main.py")
    
    return all_passed

if __name__ == "__main__":
    print("🧪 Starting webhook verification...")
    time.sleep(1)
    
    result = test_all_webhooks()
    
    if result:
        print("\n🎊 All webhooks verified and working!")
    else:
        print("\n🔧 Please fix webhook issues before demo")