# BOA API - RDW Rijbewijzenregister

Secure REST API for BOA (Buitengewoon Opsporingsambtenaar) organizations to query the RDW driver's license register.

## Overview

This API implements the Digikoppeling REST-API 2.0.2 standards with JWE encryption for secure photo retrieval. It provides BSN validation, date validation, and EC P-256 public key validation as specified in the BOA interface description.

## Features

- **BSN Validation**: 11-proef algorithm validation for Dutch BSN numbers
- **Date Validation**: ISO 8601 format support (YYYY-MM-DD, YYYY-00-00)
- **Public Key Validation**: EC P-256 key validation in JWK format
- **JWE Encryption**: ECDH-ES + AES256GCM encryption for photo data
- **Photo Watermarking**: Visible and invisible watermarks with transaction IDs
- **Comprehensive Error Handling**: Detailed error responses and logging
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Technology Stack

- **Python 3.9+**: Programming language
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation and settings management
- **python-jose**: JWT/JWE implementation
- **Pillow**: Image processing and watermarking
- **Cryptography**: Cryptographic operations

## Project Structure

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
│   └── __init__.py
├── requirements.txt           # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── PLANNING.md             # Project planning document
├── TASK.md                 # Task tracking
├── Changelog.md            # Change log
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BOA
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Usage Examples

### Basic Photo Request

```bash
curl -X POST "http://localhost:8000/api/boa/rijbewijs/pasfoto" \
     -H "Content-Type: application/json" \
     -d '{
       "BSN": "123456782",
       "geboortedatum": "2000-08-16",
       "pseudo-id-boa": "Boa-123",
       "ontvanger-publieke-sleutel": {
         "kty": "EC",
         "crv": "P-256",
         "x": "c6rIBg1HEE4qN7y-ppyfISXBf9z2N208QD5XOKX3Oc8",
         "y": "oqeScDnAeZZT5sG3BRwwiQD_c01faYWU8AOqI4bdbag"
       }
     }'
```

### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## Validation Rules

### BSN Validation
- Must be exactly 9 digits
- Must pass 11-proef algorithm validation
- Example valid BSN: `123456782`

### Date Validation
- Full date format: `YYYY-MM-DD` (e.g., `2000-08-16`)
- Year-only format: `YYYY-00-00` (e.g., `1995-00-00`)
- Must be a valid date (not in the future for birth dates)

### Public Key Validation
- Must be EC (Elliptic Curve) type
- Must use P-256 curve
- Must contain valid x and y coordinates in base64url format

## Error Handling

The API returns standardized error responses:

- **422 Unprocessable Entity**: Validation errors
- **404 Not Found**: Photo not found for given criteria
- **500 Internal Server Error**: Server-side processing errors

Example error response:
```json
{
  "error": "Validation Error",
  "message": "Invalid BSN: failed 11-proef validation",
  "type": "validation_error",
  "details": {
    "field": "BSN",
    "value": "123456789"
  }
}
```

## Security Features

- **TLS Encryption**: All communications encrypted in transit
- **JWE Token Security**: Photo data encrypted with client's public key
- **Input Validation**: Comprehensive validation of all inputs
- **Transaction Logging**: All requests logged with unique transaction IDs
- **Watermarking**: Photos watermarked for traceability

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run basic validation tests
python test_basic.py

# Run pytest (when tests are implemented)
pytest tests/
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Configuration

Environment variables can be set in `.env` file:

```env
# Application settings
APP_NAME="BOA API"
ENVIRONMENT="development"
DEBUG=true

# Server settings
HOST="0.0.0.0"
PORT=8000

# Security settings
SECRET_KEY="your-secret-key-here"

# Watermark settings
WATERMARK_TEXT="BOA APP RDW.NL"
WATERMARK_POSITION="bottom-right"
```

## Mock Data

For development and testing, the API includes mock photo data for the following BSNs:
- `123456782` (birth dates: `2000-08-16`, `1995-00-00`)
- `987654329` (birth date: `1985-12-25`)
- `147258369` (birth date: `1990-05-10`)

## License

This project is proprietary software. All rights reserved.

## Contact

For questions and support, please contact the BOA API development team.

---

**Note**: This is a development version. In production, ensure proper security measures are in place, including certificate-based authentication and secure key management.
