"""
BOA API Response Models

Defines Pydantic models for API responses following the BOA Interface Description.
All models include comprehensive validation and documentation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class BOAPhotoResponse(BaseModel):
    """
    Model for successful photo retrieval response.
    
    Contains encrypted photo data in JWE format along with transaction metadata.
    """
    
    transactie_id: str = Field(
        ..., 
        description="Unique transaction identifier (UUID4 format)",
        alias="transactie-id"
    )
    
    pasfoto_id: int = Field(
        ..., 
        description="Photo identifier from the request",
        alias="pasfoto-id"
    )
    
    pasfoto_jwe: str = Field(
        ..., 
        description="Encrypted photo data as JWE token",
        alias="pasfoto-jwe"
    )
    
    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "transactie-id": "7bdba0d1-bc9b-4e2a-b69e-4308a8373d32",
                "pasfoto-id": 1,
                "pasfoto-jwe": "eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkdDTSIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtMjU2IiwieCI6InRyV0pzVGZKSWdMdXU3UWJnSzUxRGJqM0c5SE1oZmlVdjdReFlkQXRmT1EiLCJ5IjoiWGJGTWl4dzVMeU5GaklPV0lYQkptZDFGaWduMzZJeWNqQktScXd4S1RfUSJ9fQ..K_5O9BUGxdq2rJAo.encrypted_payload_here.tag_here"
            }
        }


class PhotoPayload(BaseModel):
    """
    Model for photo payload data (used internally for JWE encryption).
    
    Contains the actual photo data before encryption.
    """
    
    pasfoto: str = Field(
        ..., 
        description="Base64 encoded photo data"
    )
    
    format: str = Field(
        ..., 
        description="Photo format (e.g., 'jpg', 'png')"
    )
    
    encoding: str = Field(
        default="base64", 
        description="Encoding type for photo data"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "pasfoto": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
                "format": "jpg",
                "encoding": "base64"
            }
        }


class ErrorResponse(BaseModel):
    """
    Model for error responses.
    
    Standardized error response format for all API errors.
    """
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    type: str = Field(..., description="Error category")
    details: Optional[dict] = Field(None, description="Additional error details")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "message": "Invalid BSN: failed 11-proef validation",
                "type": "validation_error",
                "details": {
                    "field": "BSN",
                    "value": "123456788"
                }
            }
        }


class HealthResponse(BaseModel):
    """
    Model for health check response.
    
    Returns current service status and basic information.
    """
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Runtime environment")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "BOA API",
                "version": "0.1.0",
                "environment": "development"
            }
        }
