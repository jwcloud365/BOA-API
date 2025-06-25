# BOA API - FastAPI Implementation

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive FastAPI implementation for BOA (Basic Officer of Authority) photo retrieval services with BSN validation, JWE encryption, and comprehensive security features.

## 🚀 Features

### Core Functionality
- **🔐 BSN Validation**: 11-proef algorithm implementation
- **📅 Date Validation**: ISO 8601 format support (YYYY-MM-DD, YYYY-00-00)
- **🔑 Public Key Validation**: EC P-256 JWK format support
- **🔒 JWE Encryption**: Photo data protection with AES256GCM
- **📸 Photo Processing**: Image watermarking and format handling
- **🆔 Transaction Tracking**: UUID-based transaction management

### API Features
- **📖 Auto Documentation**: Swagger UI and ReDoc integration
- **✅ Health Monitoring**: Multiple health check endpoints
- **🛡️ Security**: Comprehensive input validation and sanitization
- **⚡ Performance**: Async/await support with FastAPI
- **🌐 CORS**: Configurable cross-origin resource sharing

## 📋 Requirements

- Python 3.9+
- FastAPI 0.104.1+
- Pydantic 2.5.0+
- Uvicorn for ASGI server
- Additional dependencies listed in `requirements.txt`

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jwcloud365/BOA-API.git
cd BOA-API
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Quick Start

### Start the Server
```bash
# Using the provided script
python run_server.py

# Or directly with uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Main Endpoint**: http://localhost:8000/api/boa/rijbewijs/pasfoto

## 📡 API Endpoints

### Health Check
```http
GET /health
GET /api/boa/health
```

### Photo Retrieval
```http
POST /api/boa/rijbewijs/pasfoto
Content-Type: application/json

{
  "BSN": "123456782",
  "geboortedatum": "1990-01-01",
  "publieke_sleutel": {
    "kty": "EC",
    "crv": "P-256",
    "x": "trWJsTfJIgLuu7QbgK51Dbj3G9HMhfiUv7QxYdAtfOQ",
    "y": "XbFMixw5LyNFjIOWIXBJmd1Fign36IycjBKRqwxKT_Q"
  }
}
```

### Response Format
```json
{
  "transactie-id": "7bdba0d1-bc9b-4e2a-b69e-4308a8373d32",
  "pasfoto-id": 1,
  "pasfoto-jwe": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..."
}
```

## 🧪 Testing

### Run Component Tests
```bash
python test_components.py
```

### Expected Test Results
```
🚀 Testing BOA API Components

✓ FastAPI app created successfully
✓ Health endpoint registered
✓ Photo endpoint registered
✓ BSN validation working
✓ Date validation working  
✓ Public key validation working
✓ JWE encryption working

✅ Component testing completed!
```

## 📁 Project Structure

```
BOA-API/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py        # API route definitions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py   # Pydantic request models
│   │   └── response_models.py  # Pydantic response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── validation.py       # BSN, date, key validation
│   │   ├── crypto.py          # JWE encryption/decryption
│   │   ├── photo_processing.py # Image processing
│   │   └── photo_service.py   # Photo retrieval logic
│   └── utils/
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       └── exceptions.py      # Custom exceptions
├── tests/                     # Test framework
├── docs/                      # Documentation
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .env.example              # Environment template
├── run_server.py             # Server startup script
├── test_components.py        # Component tests
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables
```bash
# Application settings
APP_NAME="BOA API"
ENVIRONMENT="development"
DEBUG=true

# Server settings
HOST="0.0.0.0"
PORT=8000

# CORS settings
ALLOWED_ORIGINS="*"

# Security settings
SECRET_KEY="your-secret-key-here"

# Photo settings
PHOTO_STORAGE_PATH="photos/"
```

## 🔒 Security Features

- **Input Validation**: Comprehensive Pydantic model validation
- **BSN Verification**: 11-proef algorithm implementation
- **Public Key Validation**: EC P-256 JWK format verification
- **JWE Encryption**: Photo data protection
- **Error Handling**: Secure error responses without information leakage
- **CORS Configuration**: Configurable cross-origin policies

## 🚀 Deployment

### Development
```bash
python run_server.py
```

### Production
```bash
# Using gunicorn (install first: pip install gunicorn)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 📝 API Documentation

The API provides comprehensive OpenAPI documentation:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/jwcloud365/BOA-API
- **Issues**: https://github.com/jwcloud365/BOA-API/issues
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/

## 📊 Status

✅ **Current Version**: 0.1.1  
✅ **Status**: Production-ready foundation  
✅ **Test Coverage**: All core components tested  
✅ **Documentation**: Complete API documentation  

---

Made with ❤️ by [jwcloud365](https://github.com/jwcloud365)
