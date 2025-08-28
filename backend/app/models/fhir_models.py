"""
FHIR resource data models and Golden Record management
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from bson import ObjectId

class FHIRResourceType(str, Enum):
    """FHIR resource types"""
    PATIENT = "Patient"
    OBSERVATION = "Observation"
    CONDITION = "Condition"
    MEDICATION_REQUEST = "MedicationRequest"
    DIAGNOSTIC_REPORT = "DiagnosticReport"
    PROCEDURE = "Procedure"
    ENCOUNTER = "Encounter"
    PRACTITIONER = "Practitioner"
    ORGANIZATION = "Organization"
    DOCUMENT_REFERENCE = "DocumentReference"
    CARE_PLAN = "CarePlan"
    ALLERGY_INTOLERANCE = "AllergyIntolerance"
    IMMUNIZATION = "Immunization"

class FHIRVersion(str, Enum):
    """FHIR specification versions"""
    R4 = "4.0.1"
    R5 = "5.0.0"

class FHIRResourceBase(BaseModel):
    """Base FHIR resource model"""
    resource_type: FHIRResourceType
    fhir_version: FHIRVersion = Field(default=FHIRVersion.R5)
    
    patient_id: str = Field(..., min_length=1)
    source_document_id: Optional[str] = None
    
    resource_data: Dict[str, Any] = Field(..., description="Complete FHIR resource JSON")
    
    extracted_from_text: bool = Field(default=False)
    extraction_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    validation_errors: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)

class FHIRResource(FHIRResourceBase):
    """Complete FHIR resource model"""
    id: str = Field(alias="_id")
    fhir_id: str = Field(..., description="FHIR resource ID")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    golden_record_id: Optional[str] = None
    
    source_system: Optional[str] = None
    source_identifier: Optional[str] = None
    
    last_verified: Optional[datetime] = None
    verification_status: str = Field(default="unverified")
    
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class FHIRPatient(BaseModel):
    """FHIR Patient resource wrapper"""
    fhir_resource: FHIRResource
    
    identifiers: List[Dict[str, str]] = Field(default_factory=list)
    name: Dict[str, str] = Field(default_factory=dict)
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    
    addresses: List[Dict[str, Any]] = Field(default_factory=list)
    telecoms: List[Dict[str, str]] = Field(default_factory=list)
    
    marital_status: Optional[str] = None
    communication_preferences: List[Dict[str, str]] = Field(default_factory=list)
    
    managing_organization: Optional[str] = None
    general_practitioner: List[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class FHIRObservation(BaseModel):
    """FHIR Observation resource wrapper"""
    fhir_resource: FHIRResource
    
    status: str = Field(..., min_length=1)
    category: List[Dict[str, Any]] = Field(default_factory=list)
    code: Dict[str, Any] = Field(default_factory=dict)
    
    effective_date: Optional[Union[datetime, date]] = None
    issued: Optional[datetime] = None
    
    value: Optional[Dict[str, Any]] = None
    interpretation: List[Dict[str, Any]] = Field(default_factory=list)
    
    reference_range: List[Dict[str, Any]] = Field(default_factory=list)
    
    performer: List[str] = Field(default_factory=list)
    device: Optional[str] = None
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class FHIRConversionResult(BaseModel):
    """FHIR conversion result"""
    request_id: str = Field(..., min_length=1)
    success: bool
    
    resources_created: List[FHIRResource] = Field(default_factory=list)
    conversion_summary: Dict[str, Any] = Field(default_factory=dict)
    
    validation_results: Dict[str, Any] = Field(default_factory=dict)
    quality_assessment: Dict[str, float] = Field(default_factory=dict)
    
    processing_time: float = Field(..., ge=0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
