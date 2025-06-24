"""
Validation services for BOA API.

This module provides validation functions for BSN, birth dates,
and public keys according to Dutch standards and BOA specifications.
"""

import re
from datetime import datetime
from typing import Dict, Any
from app.utils.exceptions import BSNValidationError, DateValidationError, PublicKeyValidationError


def validate_bsn(bsn: str) -> bool:
    """
    Validate BSN using the 11-proef algorithm.
    
    The BSN (Burgerservicenummer) is validated using the 11-proef (11-check)
    algorithm as specified by the Dutch government.
    
    Args:
        bsn (str): 9-digit BSN string
        
    Returns:
        bool: True if BSN is valid, False otherwise
        
    Raises:
        BSNValidationError: If BSN format is invalid
        
    Example:
        >>> validate_bsn("123456782")
        True
        >>> validate_bsn("123456789")
        False
    """
    # Check if BSN is a string of exactly 9 digits
    if not isinstance(bsn, str) or not re.match(r'^\d{9}$', bsn):
        raise BSNValidationError(bsn, "BSN must be exactly 9 digits")
    
    # Convert to list of integers
    digits = [int(digit) for digit in bsn]
    
    # Apply 11-proef algorithm
    # Multiply each digit by its position weight (9, 8, 7, 6, 5, 4, 3, 2, -1)
    weights = [9, 8, 7, 6, 5, 4, 3, 2, -1]
    total = sum(digit * weight for digit, weight in zip(digits, weights))
    
    # BSN is valid if the total is divisible by 11
    is_valid = total % 11 == 0
    
    if not is_valid:
        raise BSNValidationError(bsn, "Failed 11-proef validation")
    
    return True


def validate_birth_date(date_str: str) -> bool:
    """
    Validate birth date format according to ISO 8601.
    
    Accepts two formats:
    - YYYY-MM-DD: Full date
    - YYYY-00-00: Year only (when exact date is unknown)
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        bool: True if date format is valid, False otherwise
        
    Raises:
        DateValidationError: If date format is invalid
        
    Example:
        >>> validate_birth_date("2000-08-16")
        True
        >>> validate_birth_date("1985-00-00")
        True
        >>> validate_birth_date("2000-13-01")
        False
    """
    if not isinstance(date_str, str):
        raise DateValidationError(date_str, "Date must be a string")
    
    # Check for year-only format (YYYY-00-00)
    year_only_pattern = r'^\d{4}-00-00$'
    if re.match(year_only_pattern, date_str):
        year = int(date_str[:4])
        current_year = datetime.now().year
        
        # Validate year range (reasonable birth year range)
        if year < 1900 or year > current_year:
            raise DateValidationError(
                date_str, 
                f"Year must be between 1900 and {current_year}"
            )
        return True
    
    # Check for full date format (YYYY-MM-DD)
    full_date_pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if not re.match(full_date_pattern, date_str):
        raise DateValidationError(
            date_str, 
            "Date must be in format YYYY-MM-DD or YYYY-00-00"
        )
    
    # Validate that the date is actually valid (e.g., not February 30)
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as e:
        raise DateValidationError(date_str, f"Invalid date: {str(e)}")
    
    # Check if date is not in the future
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj > datetime.now():
            raise DateValidationError(date_str, "Birth date cannot be in the future")
    except ValueError:
        pass  # Already handled above
    
    return True


def validate_public_key(key_data: Dict[str, Any]) -> bool:
    """
    Validate EC P-256 public key in JWK format.
    
    Validates that the provided key is:
    - Type 'EC' (Elliptic Curve)
    - Curve 'P-256'
    - Contains valid x and y coordinates
    
    Args:
        key_data (Dict[str, Any]): JWK public key data
        
    Returns:
        bool: True if public key is valid, False otherwise
        
    Raises:
        PublicKeyValidationError: If public key is invalid
        
    Example:
        >>> key = {
        ...     "kty": "EC",
        ...     "crv": "P-256", 
        ...     "x": "NjB_LBvIlsEMbqkJYY1cC0ZFKZ3ISC6CtvADYhX53zQ",
        ...     "y": "WPUY5Dq7qT_kJP3U4EYm70BzRRnyMTTXhQsXpHSdkKQ"
        ... }
        >>> validate_public_key(key)
        True
    """
    if not isinstance(key_data, dict):
        raise PublicKeyValidationError("Public key must be a dictionary")
    
    # Check required fields
    required_fields = ['kty', 'crv', 'x', 'y']
    for field in required_fields:
        if field not in key_data:
            raise PublicKeyValidationError(f"Missing required field: {field}")
    
    # Validate key type
    if key_data['kty'] != 'EC':
        raise PublicKeyValidationError(
            f"Invalid key type: {key_data['kty']}. Must be 'EC'"
        )
    
    # Validate curve
    if key_data['crv'] != 'P-256':
        raise PublicKeyValidationError(
            f"Invalid curve: {key_data['crv']}. Must be 'P-256'"
        )
    
    # Validate coordinates are non-empty strings
    for coord in ['x', 'y']:
        if not isinstance(key_data[coord], str) or not key_data[coord]:
            raise PublicKeyValidationError(
                f"Coordinate '{coord}' must be a non-empty string"
            )
    
    # Basic validation of base64url format (simple check)
    import base64
    try:
        for coord in ['x', 'y']:
            # Add padding if needed for base64url
            coord_value = key_data[coord]
            padding = 4 - (len(coord_value) % 4)
            if padding != 4:
                coord_value += '=' * padding
            
            # Try to decode as base64
            base64.urlsafe_b64decode(coord_value)
    except Exception as e:
        raise PublicKeyValidationError(
            f"Invalid base64url encoding in coordinates: {str(e)}"
        )
    
    return True


def validate_pseudo_id(pseudo_id: str) -> bool:
    """
    Validate pseudo ID format.
    
    Basic validation for BOA pseudo ID format.
    
    Args:
        pseudo_id (str): Pseudo ID to validate
        
    Returns:
        bool: True if pseudo ID is valid, False otherwise
        
    Raises:
        ValueError: If pseudo ID format is invalid
    """
    if not isinstance(pseudo_id, str):
        raise ValueError("Pseudo ID must be a string")
    
    if not pseudo_id.strip():
        raise ValueError("Pseudo ID cannot be empty")
    
    if len(pseudo_id) > 50:
        raise ValueError("Pseudo ID cannot be longer than 50 characters")
    
    # Basic pattern validation (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', pseudo_id):
        raise ValueError(
            "Pseudo ID can only contain letters, numbers, hyphens, and underscores"
        )
    
    return True
