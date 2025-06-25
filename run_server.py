#!/usr/bin/env python3
"""
Simple server start script for BOA API

This script starts the FastAPI server with uvicorn for testing.
"""

import os
import sys

def main():
    """Start the BOA API server"""
    print("🚀 Starting BOA API Server...")
    print("=" * 50)
    print("Server will be available at:")
    print("  • Main API: http://localhost:8000")
    print("  • Health Check: http://localhost:8000/health")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • ReDoc: http://localhost:8000/redoc")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Import and run uvicorn
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        os.system("python3 -m pip install uvicorn")
        print("✅ uvicorn installed. Please run the script again.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
