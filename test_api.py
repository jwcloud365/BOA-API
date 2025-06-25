#!/usr/bin/env python3
"""
Quick API test script to verify endpoints work
"""

import requests
import json
import time
import subprocess
import sys
from threading import Thread

def start_server():
    """Start the FastAPI server in background"""
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        pass

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API endpoints...")
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test health endpoint
        print("\n📊 Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test OpenAPI docs endpoint
        print("\n📚 Testing OpenAPI docs...")
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Docs available: {response.status_code == 200}")
        
        # Test photo endpoint with invalid data (should get validation error)
        print("\n📸 Testing photo endpoint (validation error expected)...")
        test_data = {
            "BSN": "invalid_bsn",
            "geboortedatum": "invalid_date",
            "publieke_sleutel": {}
        }
        response = requests.post(
            f"{base_url}/api/boa/rijbewijs/pasfoto",
            json=test_data,
            timeout=5
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        print("\n✅ All endpoint tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")

if __name__ == "__main__":
    print("🚀 Starting BOA API server test...")
    print("Note: This will try to connect to a running server on localhost:8000")
    print("If no server is running, please start it manually with:")
    print("  python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print()
    
    # Give user a moment to read the message
    time.sleep(3)
    
    test_api_endpoints()
