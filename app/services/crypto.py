"""
Cryptographic services for BOA API.

This module handles JWE encryption and decryption operations using
ECDH-ES key exchange and AES256GCM encryption as specified in the
BOA interface requirements.
"""

import json
import base64
from typing import Dict, Any
from jose import jwe, jwk, constants
from jose.backends import ECDHESBackend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.concat_kdf import ConcatKDFHash
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

from app.utils.exceptions import EncryptionError


def encrypt_photo_as_jwe(photo_payload: Dict[str, Any], public_key: Dict[str, str]) -> str:
    """
    Encrypt photo payload as JWE token using ECDH-ES + AES256GCM.
    
    This function implements the encryption specified in the BOA interface:
    - ECDH-ES key exchange with Concat KDF
    - AES256GCM encryption
    - JWE token format
    
    Args:
        photo_payload (Dict[str, Any]): Photo data payload to encrypt
        public_key (Dict[str, str]): Client's EC P-256 public key in JWK format
        
    Returns:
        str: JWE token string
        
    Raises:
        EncryptionError: If encryption fails
        
    Example:
        >>> payload = {"pasfoto": "base64data", "format": "jpg", "encoding": "base64"}
        >>> pub_key = {"kty": "EC", "crv": "P-256", "x": "...", "y": "..."}
        >>> jwe_token = encrypt_photo_as_jwe(payload, pub_key)
    """
    try:
        # Convert payload to JSON string
        payload_json = json.dumps(photo_payload)
        payload_bytes = payload_json.encode('utf-8')
        
        # Create JWK from public key dictionary
        client_public_jwk = jwk.construct(public_key)
        
        # Encrypt using ECDH-ES + A256GCM
        # The jose library handles the ECDH-ES key agreement and AES256GCM encryption
        jwe_token = jwe.encrypt(
            plaintext=payload_bytes,
            key=client_public_jwk,
            algorithm=constants.ALGORITHMS.ECDH_ES,  # ECDH-ES key agreement
            encryption=constants.ALGORITHMS.A256GCM  # AES256GCM encryption
        )
        
        return jwe_token.decode('utf-8') if isinstance(jwe_token, bytes) else jwe_token
        
    except Exception as e:
        raise EncryptionError(
            operation="JWE encryption",
            reason=f"Failed to encrypt photo payload: {str(e)}"
        )


def decrypt_photo_from_jwe(jwe_token: str, private_key: Dict[str, str]) -> Dict[str, Any]:
    """
    Decrypt photo payload from JWE token.
    
    This function decrypts a JWE token using the corresponding private key.
    Note: This is primarily for testing purposes as the API only encrypts data.
    
    Args:
        jwe_token (str): JWE token to decrypt
        private_key (Dict[str, str]): Private key in JWK format
        
    Returns:
        Dict[str, Any]: Decrypted photo payload
        
    Raises:
        EncryptionError: If decryption fails
    """
    try:
        # Create JWK from private key dictionary
        private_jwk = jwk.construct(private_key)
        
        # Decrypt JWE token
        decrypted_bytes = jwe.decrypt(jwe_token, private_jwk)
        
        # Parse JSON payload
        payload_json = decrypted_bytes.decode('utf-8')
        photo_payload = json.loads(payload_json)
        
        return photo_payload
        
    except Exception as e:
        raise EncryptionError(
            operation="JWE decryption",
            reason=f"Failed to decrypt JWE token: {str(e)}"
        )


def generate_key_pair() -> tuple[Dict[str, str], Dict[str, str]]:
    """
    Generate EC P-256 key pair for testing purposes.
    
    Returns:
        tuple: (public_key_jwk, private_key_jwk) in JWK format
        
    Raises:
        EncryptionError: If key generation fails
        
    Example:
        >>> public_key, private_key = generate_key_pair()
        >>> # Use public_key for encryption requests
        >>> # Keep private_key for decryption testing
    """
    try:
        # Generate EC P-256 private key
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        
        # Convert to JWK format using jose library
        private_jwk = jwk.construct(private_key, algorithm=constants.ALGORITHMS.ES256)
        public_jwk = jwk.construct(public_key, algorithm=constants.ALGORITHMS.ES256)
        
        # Extract JWK dictionaries
        public_key_dict = public_jwk.to_dict()
        private_key_dict = private_jwk.to_dict()
        
        # Ensure we only return the necessary fields for public key
        public_key_clean = {
            "kty": public_key_dict["kty"],
            "crv": public_key_dict["crv"],
            "x": public_key_dict["x"],
            "y": public_key_dict["y"]
        }
        
        return public_key_clean, private_key_dict
        
    except Exception as e:
        raise EncryptionError(
            operation="key generation",
            reason=f"Failed to generate key pair: {str(e)}"
        )


def validate_jwe_token(jwe_token: str) -> bool:
    """
    Validate JWE token format without decrypting.
    
    Performs basic validation of JWE token structure.
    
    Args:
        jwe_token (str): JWE token to validate
        
    Returns:
        bool: True if token format is valid
        
    Raises:
        EncryptionError: If validation fails
    """
    try:
        # JWE tokens have 5 parts separated by dots
        parts = jwe_token.split('.')
        if len(parts) != 5:
            raise EncryptionError(
                operation="JWE validation",
                reason=f"Invalid JWE format: expected 5 parts, got {len(parts)}"
            )
        
        # Validate that each part is valid base64url
        for i, part in enumerate(parts):
            try:
                # Add padding if needed
                padding = 4 - (len(part) % 4)
                if padding != 4:
                    part += '=' * padding
                base64.urlsafe_b64decode(part)
            except Exception:
                raise EncryptionError(
                    operation="JWE validation",
                    reason=f"Invalid base64url encoding in part {i+1}"
                )
        
        return True
        
    except EncryptionError:
        raise
    except Exception as e:
        raise EncryptionError(
            operation="JWE validation",
            reason=f"JWE validation failed: {str(e)}"
        )


def get_jwe_header(jwe_token: str) -> Dict[str, Any]:
    """
    Extract and decode JWE header without decrypting the payload.
    
    Args:
        jwe_token (str): JWE token
        
    Returns:
        Dict[str, Any]: Decoded JWE header
        
    Raises:
        EncryptionError: If header extraction fails
    """
    try:
        # Get the first part (header)
        header_part = jwe_token.split('.')[0]
        
        # Add padding if needed
        padding = 4 - (len(header_part) % 4)
        if padding != 4:
            header_part += '=' * padding
        
        # Decode base64url
        header_bytes = base64.urlsafe_b64decode(header_part)
        header_dict = json.loads(header_bytes.decode('utf-8'))
        
        return header_dict
        
    except Exception as e:
        raise EncryptionError(
            operation="JWE header extraction",
            reason=f"Failed to extract JWE header: {str(e)}"
        )


def create_test_jwe_token(payload: Dict[str, Any]) -> tuple[str, Dict[str, str]]:
    """
    Create a test JWE token with a generated key pair.
    
    This is a utility function for testing that creates a complete
    JWE encryption example.
    
    Args:
        payload (Dict[str, Any]): Payload to encrypt
        
    Returns:
        tuple: (jwe_token, private_key_for_decryption)
        
    Example:
        >>> payload = {"test": "data"}
        >>> jwe_token, private_key = create_test_jwe_token(payload)
        >>> # Use jwe_token as example, private_key for decryption testing
    """
    try:
        # Generate key pair
        public_key, private_key = generate_key_pair()
        
        # Encrypt payload
        jwe_token = encrypt_photo_as_jwe(payload, public_key)
        
        return jwe_token, private_key
        
    except Exception as e:
        raise EncryptionError(
            operation="test JWE creation",
            reason=f"Failed to create test JWE token: {str(e)}"
        )
