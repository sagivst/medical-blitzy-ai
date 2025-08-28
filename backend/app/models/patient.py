"""
Patient data models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from enum import Enum

class PatientTier(str, Enum):
    """Patient service tier"""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PatientStatus(str, Enum):
    """Patient status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class PatientBase(BaseModel):
    """Base patient model"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    date_of_birth: datetime
    gender: Optional[str] = Field(None, regex=r'^(male|female|other|unknown)$')
    preferred_language: str = Field(default="en", min_length=2, max_length=5)
    
    address_line1: Optional[str] = Field(None, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)
    zip_code: Optional[str] = Field(None, regex=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="US", min_length=2, max_length=2)
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50)

class PatientCreate(PatientBase):
    """Patient creation model"""
    password: str = Field(..., min_length=8, max_length=128)
    terms_accepted: bool = Field(..., description="Must accept terms and conditions")
    hipaa_authorization: bool = Field(..., description="Must authorize HIPAA disclosure")

class PatientUpdate(BaseModel):
    """Patient update model"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    preferred_language: Optional[str] = Field(None, min_length=2, max_length=5)
    
    address_line1: Optional[str] = Field(None, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)
    zip_code: Optional[str] = Field(None, regex=r'^\d{5}(-\d{4})?$')
    country: Optional[str] = Field(None, min_length=2, max_length=2)
    
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    emergency_contact_relationship: Optional[str] = Field(None, max_length=50)

class Patient(PatientBase):
    """Complete patient model"""
    id: str = Field(alias="_id")
    patient_id: str = Field(..., description="Unique patient identifier")
    
    tier: PatientTier = Field(default=PatientTier.FREE)
    status: PatientStatus = Field(default=PatientStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    medical_record_number: Optional[str] = None
    primary_care_physician: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    
    golden_record_id: Optional[str] = None
    fhir_patient_id: Optional[str] = None
    document_count: int = Field(default=0)
    provider_matches_count: int = Field(default=0)
    insurance_claims_count: int = Field(default=0)
    
    family_members: List[Dict[str, Any]] = Field(default_factory=list)
    caregivers: List[Dict[str, Any]] = Field(default_factory=list)
    
    communication_preferences: Dict[str, Any] = Field(default_factory=dict)
    privacy_settings: Dict[str, Any] = Field(default_factory=dict)
    
    hipaa_authorization_date: Optional[datetime] = None
    terms_acceptance_date: Optional[datetime] = None
    consent_version: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class PatientSummary(BaseModel):
    """Patient summary for provider matching"""
    patient_id: str
    age: int
    gender: Optional[str]
    primary_conditions: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    insurance_provider: Optional[str]
    preferred_language: str
    geographic_location: Dict[str, str] = Field(default_factory=dict)
    
    social_determinants: Dict[str, Any] = Field(default_factory=dict)
    
    recent_lab_results: List[Dict[str, Any]] = Field(default_factory=list)
    recent_imaging: List[Dict[str, Any]] = Field(default_factory=list)
    recent_procedures: List[Dict[str, Any]] = Field(default_factory=list)
    
    risk_factors: List[str] = Field(default_factory=list)
    comorbidities: List[str] = Field(default_factory=list)

class FamilyMember(BaseModel):
    """Family member model"""
    name: str = Field(..., min_length=1, max_length=200)
    relationship: str = Field(..., max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    preferred_language: str = Field(default="en", min_length=2, max_length=5)
    notification_preferences: Dict[str, bool] = Field(default_factory=dict)
    is_emergency_contact: bool = Field(default=False)
    is_healthcare_proxy: bool = Field(default=False)
    added_date: datetime = Field(default_factory=datetime.utcnow)

class Caregiver(BaseModel):
    """Caregiver model"""
    name: str = Field(..., min_length=1, max_length=200)
    title: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    specialization: Optional[str] = Field(None, max_length=100)
    license_number: Optional[str] = Field(None, max_length=50)
    relationship_type: str = Field(..., max_length=50)  # professional, family, friend
    access_level: str = Field(default="basic")  # basic, full, emergency
    added_date: datetime = Field(default_factory=datetime.utcnow)
