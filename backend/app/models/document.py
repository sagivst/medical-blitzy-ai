"""
Medical document data models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from bson import ObjectId

class DocumentType(str, Enum):
    """Medical document types"""
    LAB_REPORT = "lab_report"
    IMAGING = "imaging"
    PRESCRIPTION = "prescription"
    DISCHARGE_SUMMARY = "discharge_summary"
    CONSULTATION_NOTE = "consultation_note"
    INSURANCE_CARD = "insurance_card"
    REFERRAL = "referral"
    TREATMENT_PLAN = "treatment_plan"
    MEDICAL_HISTORY = "medical_history"
    CONSENT_FORM = "consent_form"
    OTHER = "other"

class DocumentStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    OCR_COMPLETE = "ocr_complete"
    FHIR_CONVERTED = "fhir_converted"
    INDEXED = "indexed"
    ERROR = "error"
    ARCHIVED = "archived"

class OCRConfidenceLevel(str, Enum):
    """OCR confidence levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    FAILED = "failed"

class DocumentBase(BaseModel):
    """Base document model"""
    filename: str = Field(..., min_length=1, max_length=255)
    document_type: DocumentType
    file_size: int = Field(..., gt=0)
    mime_type: str = Field(..., min_length=1, max_length=100)
    patient_id: str = Field(..., min_length=1)
    uploaded_by: str = Field(..., min_length=1)
    
    description: Optional[str] = Field(None, max_length=500)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DocumentCreate(DocumentBase):
    """Document creation model"""
    file_content: bytes = Field(..., description="Base64 encoded file content")

class DocumentUpdate(BaseModel):
    """Document update model"""
    document_type: Optional[DocumentType] = None
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class OCRResult(BaseModel):
    """OCR processing result"""
    extracted_text: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    confidence_level: OCRConfidenceLevel
    processing_time: float = Field(..., gt=0)
    ocr_engine: str = Field(..., min_length=1)
    
    structured_data: Dict[str, Any] = Field(default_factory=dict)
    medical_entities: List[Dict[str, Any]] = Field(default_factory=list)
    key_value_pairs: Dict[str, str] = Field(default_factory=dict)
    
    bounding_boxes: List[Dict[str, Any]] = Field(default_factory=list)
    page_count: int = Field(default=1, ge=1)
    language_detected: str = Field(default="en")

class FHIRConversionResult(BaseModel):
    """FHIR conversion result"""
    fhir_resources: List[Dict[str, Any]] = Field(default_factory=list)
    conversion_status: str
    conversion_confidence: float = Field(..., ge=0.0, le=1.0)
    mapped_fields: Dict[str, str] = Field(default_factory=dict)
    unmapped_content: List[str] = Field(default_factory=list)
    validation_errors: List[str] = Field(default_factory=list)

class MedicalDocument(DocumentBase):
    """Complete medical document model"""
    id: str = Field(alias="_id")
    document_id: str = Field(..., description="Unique document identifier")
    
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    last_modified: datetime = Field(default_factory=datetime.utcnow)
    
    file_path: str = Field(..., min_length=1)
    file_hash: str = Field(..., min_length=1)
    
    ocr_result: Optional[OCRResult] = None
    fhir_conversion: Optional[FHIRConversionResult] = None
    
    processing_history: List[Dict[str, Any]] = Field(default_factory=list)
    access_log: List[Dict[str, Any]] = Field(default_factory=list)
    
    retention_date: Optional[datetime] = None
    is_sensitive: bool = Field(default=True)
    encryption_status: str = Field(default="encrypted")
    
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    clinical_relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    extracted_conditions: List[str] = Field(default_factory=list)
    extracted_medications: List[str] = Field(default_factory=list)
    extracted_procedures: List[str] = Field(default_factory=list)
    extracted_dates: List[Dict[str, Any]] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
