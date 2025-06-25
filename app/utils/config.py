"""
Configuration management for BOA API.

This module handles application settings, environment variables,
and configuration validation using Pydantic.
"""

from typing import List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings configuration.
    
    Uses Pydantic BaseSettings to automatically load from environment
    variables and provide validation.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application settings
    app_name: str = Field(default="BOA API", description="Application name")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")    # CORS settings
    allowed_origins: str = Field(
        default="*", 
        description="Allowed CORS origins (comma-separated)"
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from environment variable."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
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


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    Uses LRU cache to ensure settings are loaded only once.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()
