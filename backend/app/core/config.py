"""
Configuration settings for Medical Blitzy AI IHN
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    APP_NAME: str = "Medical Blitzy AI IHN"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "medical_blitzy_ai")
    
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/fhir_db")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    FHIR_SERVER_URL: str = os.getenv("FHIR_SERVER_URL", "http://localhost:8080/fhir")
    FHIR_VERSION: str = "R5"
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    AZURE_TRANSLATOR_KEY: Optional[str] = os.getenv("AZURE_TRANSLATOR_KEY")
    AZURE_TRANSLATOR_REGION: str = os.getenv("AZURE_TRANSLATOR_REGION", "eastus")
    
    TESSERACT_PATH: str = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
    
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "medical-blitzy-documents")
    
    CHANGE_HEALTHCARE_API_KEY: Optional[str] = os.getenv("CHANGE_HEALTHCARE_API_KEY")
    AVAILITY_API_KEY: Optional[str] = os.getenv("AVAILITY_API_KEY")
    
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    OCR_TIMEOUT: int = 30  # seconds
    PROVIDER_MATCHING_TIMEOUT: int = 5  # seconds
    TRANSLATION_TIMEOUT: int = 2  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
