#!/usr/bin/env python3
"""
Startup script for BOA API application.

This script starts the FastAPI application using Uvicorn with proper configuration.
"""

import uvicorn
from app.main import app
from app.utils.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"Starting {settings.app_name}")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")
    print(f"Server: http://{settings.host}:{settings.port}")
    print(f"Documentation: http://{settings.host}:{settings.port}/docs")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
        access_log=True
    )
