"""
Configuration management for BOA API.

This module handles application settings, environment variables,
and configuration validation using Pydantic.
"""

from typing import List
from pydantic import BaseSettings, Field
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings configuration.
    
    Uses Pydantic BaseSettings to automatically load from environment
    variables and provide validation.
    """
    
    # Application settings
    app_name: str = Field(default="BOA API", description="Application name")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # CORS settings
    allowed_origins: List[str] = Field(
        default=["*"], 
        description="Allowed CORS origins"
    )
    
    # Security settings
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for encryption"
    )
    
    # Photo settings
    photo_storage_path: str = Field(
        default="photos/",
        description="Path to photo storage directory"
    )
    
    # Watermark settings
    watermark_text: str = Field(
        default="BOA APP RDW.NL",
        description="Text for photo watermark"
    )
    
    watermark_position: str = Field(
        default="bottom-right",
        description="Position of watermark on photo"
    )
    
    # Logging settings
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    Uses LRU cache to ensure settings are loaded only once.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()
