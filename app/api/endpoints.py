"""
API endpoints for BOA API.

This module defines the main API endpoints for BOA photo requests
and other API operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import uuid4
import logging
from typing import Optional

from app.models.request_models import BOAPhotoRequest
from app.models.response_models import BOAPhotoResponse, PhotoPayload
from app.services.photo_service import get_photo_by_criteria
from app.services.crypto import encrypt_photo_as_jwe
from app.services.photo_processing import add_watermark_to_photo
from app.utils.exceptions import (
    BOAValidationError, 
    BOANotFoundError, 
    PhotoNotFoundError,
    EncryptionError,
    PhotoProcessingError
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/boa/rijbewijs/pasfoto",
    response_model=BOAPhotoResponse,
    status_code=200,
    summary="Retrieve driver's license photo",
    description="""
    Retrieve a driver's license photo from the RDW register.
    
    This endpoint accepts a BSN, birth date, and public key, validates the input,
    retrieves the corresponding photo, applies watermarking, encrypts it using
    JWE with the provided public key, and returns the encrypted result.
    
    **Security Features:**
    - BSN validation with 11-proef algorithm
    - ISO 8601 date format validation  
    - EC P-256 public key validation
    - JWE encryption using ECDH-ES + AES256GCM
    - Photo watermarking with transaction ID
    
    **Error Handling:**
    - 422: Validation errors (invalid BSN, date, or key format)
    - 404: No photo found for given criteria
    - 500: Internal server errors (encryption, processing failures)
    """,
    responses={
        200: {
            "description": "Photo successfully retrieved and encrypted",
            "content": {
                "application/json": {
                    "example": {
                        "transactie-id": "7bdba0d1-bc9b-4e2a-b69e-4308a8373d32",
                        "pasfoto-id": 1,
                        "pasfoto-jwe": "eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkdDTSIs..."
                    }
                }
            }
        },
        404: {
            "description": "No photo found for the given criteria",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Not Found",
                        "message": "Photo not found for criteria: BSN: 123456789, Birth date: 2000-08-16",
                        "type": "not_found_error"
                    }
                }
            }
        },
        422: {
            "description": "Validation error in request data",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Validation Error",
                        "message": "Invalid BSN: failed 11-proef validation",
                        "type": "validation_error"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred",
                        "type": "internal_error"
                    }
                }
            }
        }
    },
    tags=["BOA Photo Retrieval"]
)
async def get_driver_photo(request: BOAPhotoRequest):
    """
    Retrieve and encrypt a driver's license photo.
    
    Args:
        request (BOAPhotoRequest): Photo request with BSN, birth date, and public key
        
    Returns:
        BOAPhotoResponse: Response with transaction ID and encrypted photo
        
    Raises:
        HTTPException: For various error conditions (validation, not found, etc.)
    """
    # Generate unique transaction ID for audit trail
    transaction_id = str(uuid4())
    
    logger.info(
        f"Photo request received - Transaction ID: {transaction_id}, "
        f"Pseudo ID: {request.pseudo_id_boa}"
    )
    
    try:
        # Step 1: Retrieve photo based on BSN and birth date
        logger.info(f"Retrieving photo for BSN: {request.BSN[:3]}***{request.BSN[-2:]}")
        
        photo_data, photo_id = await get_photo_by_criteria(
            bsn=request.BSN,
            birth_date=request.geboortedatum
        )
        
        if not photo_data:
            logger.warning(f"No photo found - Transaction ID: {transaction_id}")
            raise PhotoNotFoundError(request.BSN, request.geboortedatum)
        
        logger.info(f"Photo found - Photo ID: {photo_id}, Transaction ID: {transaction_id}")
        
        # Step 2: Add watermark to photo
        logger.info(f"Adding watermark - Transaction ID: {transaction_id}")
        
        watermarked_photo = add_watermark_to_photo(
            photo_data=photo_data,
            transaction_id=transaction_id
        )
        
        # Step 3: Create photo payload for encryption
        photo_payload = PhotoPayload(
            pasfoto=watermarked_photo,
            format="jpg",
            encoding="base64"
        )
        
        # Step 4: Encrypt photo using JWE with client's public key
        logger.info(f"Encrypting photo - Transaction ID: {transaction_id}")
        
        jwe_token = encrypt_photo_as_jwe(
            photo_payload=photo_payload.dict(),
            public_key=request.ontvanger_publieke_sleutel.dict()
        )
        
        # Step 5: Create and return response
        response = BOAPhotoResponse(
            transactie_id=transaction_id,
            pasfoto_id=photo_id,
            pasfoto_jwe=jwe_token
        )
        
        logger.info(
            f"Photo request completed successfully - Transaction ID: {transaction_id}"
        )
        
        return response
        
    except PhotoNotFoundError:
        # Re-raise to be handled by the exception handler
        raise
        
    except (EncryptionError, PhotoProcessingError) as e:
        logger.error(f"Processing error - Transaction ID: {transaction_id}, Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Photo processing failed: {str(e)}"
        )
        
    except Exception as e:
        logger.error(
            f"Unexpected error - Transaction ID: {transaction_id}, Error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during photo processing"
        )


@router.get(
    "/boa/health",
    summary="Health check for BOA endpoints",
    description="Check the health status of BOA-specific endpoints",
    tags=["Health"]
)
async def boa_health_check():
    """
    BOA-specific health check endpoint.
    
    Returns:
        dict: Health status of BOA endpoints
    """
    return {
        "status": "healthy",
        "endpoint": "BOA API",
        "services": {
            "validation": "operational",
            "photo_retrieval": "operational", 
            "encryption": "operational",
            "watermarking": "operational"
        }
    }
