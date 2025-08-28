"""
Logging configuration for Medical Blitzy AI IHN
"""

import logging
import logging.config
import sys
from datetime import datetime
import structlog
from typing import Any, Dict

from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    """Setup structured logging configuration"""
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": settings.LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": sys.stdout,
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/medical_blitzy_ai.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "hipaa_audit": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/hipaa_audit.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 10,  # Keep more audit logs
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "hipaa": {
                "handlers": ["hipaa_audit"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
    
    import os
    os.makedirs("logs", exist_ok=True)
    
    logging.config.dictConfig(LOGGING_CONFIG)

class MedicalLogger:
    """Specialized logger for medical operations"""
    
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
    
    def log_document_processing(self, patient_id: str, document_id: str, 
                              operation: str, status: str, **kwargs):
        """Log document processing operations"""
        self.logger.info(
            "document_processing",
            patient_id=patient_id,
            document_id=document_id,
            operation=operation,
            status=status,
            **kwargs
        )
    
    def log_provider_matching(self, patient_id: str, match_score: float, 
                            provider_count: int, **kwargs):
        """Log provider matching operations"""
        self.logger.info(
            "provider_matching",
            patient_id=patient_id,
            match_score=match_score,
            provider_count=provider_count,
            **kwargs
        )
    
    def log_insurance_processing(self, patient_id: str, claim_id: str, 
                               operation: str, status: str, **kwargs):
        """Log insurance processing operations"""
        self.logger.info(
            "insurance_processing",
            patient_id=patient_id,
            claim_id=claim_id,
            operation=operation,
            status=status,
            **kwargs
        )
    
    def log_translation(self, source_lang: str, target_lang: str, 
                       text_length: int, accuracy_score: float, **kwargs):
        """Log translation operations"""
        self.logger.info(
            "translation",
            source_lang=source_lang,
            target_lang=target_lang,
            text_length=text_length,
            accuracy_score=accuracy_score,
            **kwargs
        )
    
    def log_hipaa_access(self, user_id: str, resource_type: str, 
                        resource_id: str, action: str, **kwargs):
        """Log HIPAA-compliant access to PHI"""
        hipaa_logger = logging.getLogger("hipaa")
        hipaa_logger.info(
            "hipaa_access",
            extra={
                "user_id": user_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "action": action,
                "timestamp": datetime.utcnow().isoformat(),
                **kwargs
            }
        )

def get_medical_logger(name: str) -> MedicalLogger:
    """Get a medical logger instance"""
    return MedicalLogger(name)
