"""
Main FastAPI application for BOA API.

This module initializes the FastAPI application with proper configuration,
middleware, and routing for the BOA driver's license register API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.endpoints import router
from app.utils.exceptions import BOAValidationError, BOANotFoundError
from app.utils.config import get_settings

settings = get_settings()

app = FastAPI(
    title="BOA API - RDW Rijbewijzenregister",
    description="""
    Secure REST API for BOA organizations to query the RDW driver's license register.
    
    This API implements the Digikoppeling REST-API 2.0.2 standards with JWE encryption
    for secure photo retrieval. BSN validation, date validation, and EC P-256 public
    key validation are included.
    
    ## Features
    
    * BSN validation with 11-proef algorithm
    * ISO 8601 date format validation (YYYY-MM-DD, YYYY-00-00)
    * EC P-256 public key validation
    * JWE encryption using ECDH-ES + AES256GCM
    * Photo watermarking with transaction ID
    * Comprehensive error handling
    
    ## Security
    
    * TLS encryption for all communications
    * JWE token encryption for photo data
    * Transaction ID tracking for audit trail
    * Input validation and sanitization
    """,
    version="0.1.0",
    contact={
        "name": "BOA API Team",
        "email": "support@boa-api.nl",
    },
    license_info={
        "name": "Private",
        "url": "https://www.example.com/license/",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.exception_handler(BOAValidationError)
async def validation_exception_handler(request, exc: BOAValidationError):
    """Handle custom validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": str(exc),
            "type": "validation_error"
        }
    )


@app.exception_handler(BOANotFoundError)
async def not_found_exception_handler(request, exc: BOANotFoundError):
    """Handle not found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": str(exc),
            "type": "not_found_error"
        }
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Request Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "type": "request_validation_error"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "type": "http_error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle all other exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "type": "internal_error"
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API service.
    
    Returns:
        dict: Service status information
    """
    return {
        "status": "healthy",
        "service": "BOA API",
        "version": "0.1.0",
        "environment": settings.environment
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    
    Returns basic API information and links to documentation.
    
    Returns:
        dict: API information and documentation links
    """
    return {
        "message": "BOA API - RDW Rijbewijzenregister",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )
