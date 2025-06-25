"""
Request models for BOA API.

This module defines Pydantic models for validating incoming API requests.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field, validator
from app.services.validation import validate_bsn, validate_birth_date, validate_public_key


class JWKPublicKey(BaseModel):
    """
    JSON Web Key (JWK) model for EC P-256 public key.
    
    Validates that the provided key is an EC key with P-256 curve.
    """
    
    kty: str = Field(..., description="Key type, must be 'EC'")
    crv: str = Field(..., description="Curve, must be 'P-256'")
    x: str = Field(..., description="X coordinate of the EC point")
    y: str = Field(..., description="Y coordinate of the EC point")
    
    @validator('kty')
    def validate_key_type(cls, v):
        """Validate that key type is EC."""
        if v != 'EC':
            raise ValueError("Key type must be 'EC'")
        return v
    
    @validator('crv')
    def validate_curve(cls, v):
        """Validate that curve is P-256."""
        if v != 'P-256':
            raise ValueError("Curve must be 'P-256'")
        return v
    
    @validator('x', 'y')
    def validate_coordinate(cls, v):
        """Validate that coordinates are valid base64url strings."""
        if not v or not isinstance(v, str):
            raise ValueError("Coordinate must be a non-empty string")
        return v
    
    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "kty": "EC",
                "crv": "P-256",
                "x": "NjB_LBvIlsEMbqkJYY1cC0ZFKZ3ISC6CtvADYhX53zQ",
                "y": "WPUY5Dq7qT_kJP3U4EYm70BzRRnyMTTXhQsXpHSdkKQ"
            }
        }


class BOAPhotoRequest(BaseModel):
    """
    Request model for BOA photo retrieval.
    
    Validates BSN, birth date, pseudo ID, and public key according to
    the BOA interface specification.
    """
    
    BSN: str = Field(
        ..., 
        description="9-digit BSN (Burgerservicenummer) with valid 11-proef",
        min_length=9,
        max_length=9,
        pattern=r"^\d{9}$"
    )
    
    geboortedatum: str = Field(
        ..., 
        description="Birth date in ISO 8601 format (YYYY-MM-DD or YYYY-00-00)",
        pattern=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$|^\d{4}-00-00$"
    )
    
    pseudo_id_boa: str = Field(
        ..., 
        description="Pseudo ID for the BOA making the request",
        alias="pseudo-id-boa",
        min_length=1,
        max_length=50
    )
    
    ontvanger_publieke_sleutel: JWKPublicKey = Field(
        ..., 
        description="EC P-256 public key for encrypting the response",
        alias="ontvanger-publieke-sleutel"
    )
    
    @validator('BSN')
    def validate_bsn_field(cls, v):
        """Validate BSN using 11-proef algorithm."""
        if not validate_bsn(v):
            raise ValueError("Invalid BSN: failed 11-proef validation")
        return v
    
    @validator('geboortedatum')
    def validate_birth_date_field(cls, v):
        """Validate birth date format."""
        if not validate_birth_date(v):
            raise ValueError("Invalid birth date format")
        return v
    
    @validator('ontvanger_publieke_sleutel')
    def validate_public_key_field(cls, v):
        """Validate public key structure and format."""
        if not validate_public_key(v.dict()):
            raise ValueError("Invalid public key format or parameters")
        return v
    
    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "BSN": "123456789",
                "geboortedatum": "2000-08-16",
                "pseudo-id-boa": "Boa-123",
                "ontvanger-publieke-sleutel": {
                    "kty": "EC",
                    "crv": "P-256",
                    "x": "c6rIBg1HEE4qN7y-ppyfISXBf9z2N208QD5XOKX3Oc8",
                    "y": "oqeScDnAeZZT5sG3BRwwiQD_c01faYWU8AOqI4bdbag"
                }
            }
        }
