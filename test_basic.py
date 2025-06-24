#!/usr/bin/env python3
"""
Test script to verify BOA API basic functionality.
"""

import sys
sys.path.append('.')

from app.services.validation import validate_bsn, validate_birth_date, validate_public_key


def test_bsn_validation():
    """Test BSN validation with 11-proef."""
    print("Testing BSN validation...")
    
    # Valid BSN (passes 11-proef)
    try:
        result = validate_bsn("123456782")
        print(f"✓ Valid BSN test passed: {result}")
    except Exception as e:
        print(f"✗ Valid BSN test failed: {e}")
    
    # Invalid BSN (fails 11-proef)
    try:
        result = validate_bsn("123456789")
        print(f"✗ Invalid BSN test should have failed but passed: {result}")
    except Exception as e:
        print(f"✓ Invalid BSN test correctly failed: {e}")


def test_date_validation():
    """Test birth date validation."""
    print("\nTesting date validation...")
    
    # Valid full date
    try:
        result = validate_birth_date("2000-08-16")
        print(f"✓ Valid date test passed: {result}")
    except Exception as e:
        print(f"✗ Valid date test failed: {e}")
    
    # Valid year-only date
    try:
        result = validate_birth_date("1995-00-00")
        print(f"✓ Valid year-only date test passed: {result}")
    except Exception as e:
        print(f"✗ Valid year-only date test failed: {e}")
    
    # Invalid date
    try:
        result = validate_birth_date("2000-13-45")
        print(f"✗ Invalid date test should have failed but passed: {result}")
    except Exception as e:
        print(f"✓ Invalid date test correctly failed: {e}")


def test_public_key_validation():
    """Test public key validation."""
    print("\nTesting public key validation...")
    
    # Valid public key
    valid_key = {
        "kty": "EC",
        "crv": "P-256",
        "x": "NjB_LBvIlsEMbqkJYY1cC0ZFKZ3ISC6CtvADYhX53zQ",
        "y": "WPUY5Dq7qT_kJP3U4EYm70BzRRnyMTTXhQsXpHSdkKQ"
    }
    
    try:
        result = validate_public_key(valid_key)
        print(f"✓ Valid public key test passed: {result}")
    except Exception as e:
        print(f"✗ Valid public key test failed: {e}")
    
    # Invalid public key (wrong type)
    invalid_key = {
        "kty": "RSA",
        "crv": "P-256",
        "x": "NjB_LBvIlsEMbqkJYY1cC0ZFKZ3ISC6CtvADYhX53zQ",
        "y": "WPUY5Dq7qT_kJP3U4EYm70BzRRnyMTTXhQsXpHSdkKQ"
    }
    
    try:
        result = validate_public_key(invalid_key)
        print(f"✗ Invalid public key test should have failed but passed: {result}")
    except Exception as e:
        print(f"✓ Invalid public key test correctly failed: {e}")


if __name__ == "__main__":
    print("BOA API Validation Tests")
    print("=" * 50)
    
    test_bsn_validation()
    test_date_validation()
    test_public_key_validation()
    
    print("\n" + "=" * 50)
    print("Test completed!")
