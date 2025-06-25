#!/usr/bin/env python3
"""
Test script for BOA API endpoints
"""

from app.main import app
import json

def test_health_endpoint():
    """Test the health endpoint directly."""
    # Test application creation
    print("✓ FastAPI app created successfully")
    
    # Check if routes are registered
    routes = [route.path for route in app.routes]
    print(f"✓ Registered routes: {routes}")
    
    # Check if health endpoint exists
    health_routes = [route for route in app.routes if hasattr(route, 'path') and route.path == '/health']
    if health_routes:
        print("✓ Health endpoint registered")
    else:
        print("✗ Health endpoint not found")
      # Check photo endpoint
    photo_routes = [route for route in app.routes if hasattr(route, 'path') and 'pasfoto' in route.path]
    if photo_routes:
        print(f"✓ Photo endpoint registered: {photo_routes[0].path}")
    else:
        print("✗ Photo endpoint not found")

def test_validation_service():
    """Test validation services."""
    try:
        from app.services.validation import validate_bsn, validate_birth_date, validate_public_key
          # Test BSN validation
        try:
            valid_bsn = validate_bsn("123456782")  # Valid test BSN
            print(f"✓ BSN validation works: valid BSN accepted")
        except Exception:
            print("✗ Valid BSN was rejected")
            
        try:
            invalid_bsn = validate_bsn("123456789")  # Invalid BSN
            print("✗ Invalid BSN was accepted")
        except Exception:
            print("✓ BSN validation works: invalid BSN rejected")
          # Test date validation  
        try:
            valid_date = validate_birth_date("2023-01-01")
            print(f"✓ Date validation works: valid date accepted")
        except Exception:
            print("✗ Valid date was rejected")
            
        try:
            invalid_date = validate_birth_date("2023-13-01")
            print("✗ Invalid date was accepted")
        except Exception:
            print("✓ Date validation works: invalid date rejected")
        
        # Test public key validation
        test_jwk = {
            "kty": "EC",
            "crv": "P-256",
            "x": "trWJsTfJIgLuu7QbgK51Dbj3G9HMhfiUv7QxYdAtfOQ",
            "y": "XbFMixw5LyNFjIOWIXBJmd1Fign36IycjBKRqwxKT_Q"
        }
        valid_key = validate_public_key(test_jwk)
        print(f"✓ Public key validation works: {valid_key}")
        
    except Exception as e:
        print(f"✗ Validation service error: {e}")

def test_crypto_service():
    """Test crypto services."""
    try:
        from app.services.crypto import encrypt_photo_as_jwe, validate_public_key_jwk
        
        test_payload = {
            "pasfoto": "base64data",
            "format": "jpg", 
            "encoding": "base64"
        }
        
        test_public_key = {
            "kty": "EC",
            "crv": "P-256",
            "x": "trWJsTfJIgLuu7QbgK51Dbj3G9HMhfiUv7QxYdAtfOQ",
            "y": "XbFMixw5LyNFjIOWIXBJmd1Fign36IycjBKRqwxKT_Q"
        }
        
        # Test key validation
        valid_key = validate_public_key_jwk(test_public_key)
        print(f"✓ Crypto key validation works: {valid_key}")
        
        # Test encryption (simplified version)
        jwe_token = encrypt_photo_as_jwe(test_payload, test_public_key)
        print(f"✓ Photo encryption works: token length = {len(jwe_token)}")
        
    except Exception as e:
        print(f"✗ Crypto service error: {e}")

if __name__ == "__main__":
    print("🚀 Testing BOA API Components\n")
    
    test_health_endpoint()
    print()
    
    test_validation_service()
    print()
    
    test_crypto_service()
    print()
    
    print("✅ Component testing completed!")
