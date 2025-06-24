# PLANNING.md - BOA API Implementation

## Current Status: Initial Setup Phase

Based on the `planning_document.md`, this document tracks the current state and next steps for the BOA API implementation.

## Architecture Overview

### System Components
1. **BOA API Module** - FastAPI-based REST API implementation
2. **Photo Processing Module** - Image watermarking system
3. **Security Module** - ECDH-ES key exchange and JWE encryption
4. **Documentation Module** - Auto-generated Swagger/OpenAPI docs

### Technology Stack
- **Core**: Python 3.9+, FastAPI, Uvicorn
- **Security**: python-jose, cryptography
- **Image Processing**: Pillow, opencv-python, numpy
- **Validation**: pydantic, python-dateutil
- **Testing**: pytest, httpx

## Project Structure (Planned)
```
BOA/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py   # Pydantic request models
│   │   └── response_models.py  # Pydantic response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── validation.py       # BSN, date, key validation
│   │   ├── crypto.py          # JWE encryption/decryption
│   │   ├── photo_processing.py # Image watermarking
│   │   └── photo_service.py   # Photo retrieval logic
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py       # API endpoint definitions
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py      # Custom exceptions
│       └── config.py          # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_crypto.py
│   ├── test_endpoints.py
│   └── fixtures/              # Test data
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
└── Dockerfile
```

## Current Phase: Environment Setup

### Immediate Next Steps
1. Set up Python virtual environment
2. Initialize Git repository
3. Create basic project structure
4. Install core dependencies
5. Create basic FastAPI application

### Success Criteria for Current Phase
- [ ] Virtual environment created and activated
- [ ] Git repository initialized
- [ ] Basic project structure created
- [ ] FastAPI application runs successfully
- [ ] Health check endpoint functional

## Implementation Strategy

### Phase 1: Foundation (Current)
- Environment setup
- Basic FastAPI app
- Project structure
- Core dependencies

### Phase 2: Core Validation
- BSN validation with 11-proef
- Date validation (ISO 8601)
- EC P-256 public key validation
- Pydantic models

### Phase 3: Security Implementation
- JWE token handling
- ECDH-ES key exchange
- AES256GCM encryption
- Secure key management

### Phase 4: Image Processing
- Photo loading and processing
- Visible watermarking
- Invisible watermarking
- Base64 encoding

### Phase 5: API Integration
- Complete endpoint implementation
- Error handling
- Response formatting
- Transaction ID generation

### Phase 6: Testing & Documentation
- Comprehensive test suite
- API documentation
- Examples and usage guides
- Performance testing

### Phase 7: Deployment Preparation
- Docker configuration
- Production settings
- Security hardening
- Monitoring setup

## Key Requirements Tracking

### Security Requirements ✓
- TLS + JWE photo encryption
- PKIO certificate authentication
- Transaction ID traceability
- OWASP compliance

### Functional Requirements ✓
- BSN 11-proef validation
- ISO 8601 date format support
- EC P-256 public key validation
- JWE response encryption

### Performance Requirements ✓
- Response time < 2 seconds
- Concurrent request support
- Efficient image processing
- Scalable architecture

## Notes
- Following KISS principle (Keep It Simple and Secure)
- Compliance with Digikoppeling REST-API 2.0.2
- Mock photo data for development phase
- Comprehensive error handling and logging
