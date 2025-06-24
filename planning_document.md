# Planning Document - BOA API Implementation

## High-Level Vision

This project implements a secure REST API for BOA (Buitengewoon Opsporingsambtenaar) organizations to query the RDW driver's license register. The application provides a FastAPI-based service that handles encrypted photo requests and responses according to the Dutch Digikoppeling REST-API 2.0.2 standards, with additional watermarking capabilities for security and traceability.

## Architecture Overview

### System Components

1. **BOA API Module**
   - FastAPI-based REST API implementation
   - JWT/JWE encryption/decryption handling
   - BSN validation with 11-proef algorithm
   - Date validation (ISO 8601)
   - Public key validation (EC P-256)

2. **Photo Processing Module**
   - Image watermarking system (visible and invisible)
   - Base64 encoding/decoding
   - Image format handling (JPG primary)

3. **Security Module**
   - ECDH-ES key exchange implementation
   - AES256GCM encryption
   - JWE token creation and validation
   - TLS certificate handling

4. **Documentation Module**
   - Auto-generated Swagger/OpenAPI documentation
   - Interactive API testing interface

## Technical Architecture

### API Flow
1. BOA client sends request with BSN, birth date, and ephemeral public key
2. API validates input data (BSN 11-proef, date format, key structure)
3. System generates transaction ID and retrieves/simulates photo data
4. Photo is watermarked with transaction ID and "BOA APP RDW.NL"
5. Photo is encrypted using JWE with client's public key
6. Encrypted response is returned to client

### Security Measures
- **Confidentiality**: TLS + JWE photo encryption
- **Integrity**: JWE guarantees data integrity
- **Authentication**: PKIO certificate validation (BOA employer responsibility)
- **Non-repudiation**: Traceable via PKIO and transaction IDs

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Programming language
- **Uvicorn**: ASGI server for FastAPI

### Security & Encryption
- **python-jose**: JWT/JWE implementation
- **cryptography**: Cryptographic operations
- **passlib**: Password hashing utilities

### Image Processing
- **Pillow (PIL)**: Image manipulation and watermarking
- **opencv-python**: Advanced image processing for invisible watermarks
- **numpy**: Numerical operations for image data

### Data Validation
- **pydantic**: Data validation and settings management
- **python-dateutil**: Date parsing and validation

### Testing & Documentation
- **pytest**: Testing framework
- **httpx**: HTTP client for testing
- **swagger-ui**: API documentation interface

### Development Tools
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Constraints & Requirements

### Functional Constraints
- Must comply with Digikoppeling REST-API 2.0.2 standards
- BSN must pass 11-proef validation
- Only EC P-256 public keys accepted
- ISO 8601 date format required
- JWE encryption using ECDH-ES + AES256GCM

### Security Constraints
- Follow OWASP guidelines
- Implement KISS principle (Keep It Simple and Secure)
- All sensitive data must be encrypted in transit
- Transaction logging for audit trail
- Secure key management

### Performance Constraints
- Response time < 2 seconds for photo queries
- Support concurrent requests
- Efficient memory usage for image processing
- Scalable architecture for future expansion

## Development Environment

### Local Development
- **OS**: Windows 11 compatible
- **Python**: 3.9+ with virtual environment
- **IDE**: VS Code or PyCharm recommended
- **Database**: SQLite for development/testing
- **Port**: 8000 (FastAPI default)

### Production Considerations
- **Deployment**: Docker containerization ready
- **Monitoring**: Structured logging with transaction IDs
- **Error Handling**: Comprehensive exception handling
- **Rate Limiting**: API throttling capabilities

## API Endpoints

### Primary Endpoint
- **POST /boa/rijbewijs/pasfoto**
  - Request: BSN, birth date, public key
  - Response: Transaction ID, photo ID, encrypted JWE photo
  - Authentication: PKIO certificate based

### Health & Monitoring
- **GET /health**: System health check
- **GET /docs**: Swagger documentation
- **GET /redoc**: Alternative documentation format

## Error Handling Strategy

### HTTP Status Codes
- **200**: Successful photo retrieval
- **404**: No photo found for given criteria
- **422**: Validation errors (BSN, date, key format)
- **500**: Internal server errors

### Validation Rules
- BSN: 9 digits with valid 11-proef
- Date: YYYY-MM-DD or YYYY-00-00 format
- Public Key: EC type with P-256 curve
- Required fields presence validation

## Watermarking Specifications

### Visible Watermark
- Text: "BOA APP RDW.NL"
- Transaction ID included
- Position: Bottom-right corner
- Semi-transparent overlay
- Readable font size

### Invisible Watermark
- Steganographic embedding
- Contains transaction ID
- Tamper-evident
- Does not affect image quality significantly

## Quality Assurance

### Testing Strategy
- Unit tests for all validation functions
- Integration tests for API endpoints
- Security testing for encryption/decryption
- Performance testing for image processing
- Mock data for development and testing

### Code Quality
- Type hints throughout codebase
- Comprehensive docstrings
- PEP 8 compliance
- Security code review
- Automated testing pipeline

## Documentation Strategy

### API Documentation
- Auto-generated OpenAPI 3.0 specification
- Interactive Swagger UI with examples
- Request/response schema documentation
- Error code explanations

### Code Documentation
- Inline comments for complex logic
- README with setup instructions
- Architecture decision records
- Security implementation notes

## Future Considerations

### Scalability
- Microservice architecture readiness
- Database abstraction for future migrations
- Caching strategy for frequent requests
- Load balancing capabilities

### Monitoring & Logging
- Transaction audit logging
- Performance metrics collection
- Error tracking and alerting
- Security event monitoring

### Compliance
- GDPR compliance for personal data
- Dutch government security standards
- Regular security updates and patches
- Penetration testing schedule