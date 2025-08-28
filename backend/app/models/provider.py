"""
Healthcare provider data models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from bson import ObjectId

class ProviderType(str, Enum):
    """Healthcare provider types"""
    PRIMARY_CARE = "primary_care"
    SPECIALIST = "specialist"
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    URGENT_CARE = "urgent_care"
    MENTAL_HEALTH = "mental_health"
    PHARMACY = "pharmacy"
    LABORATORY = "laboratory"
    IMAGING_CENTER = "imaging_center"
    REHABILITATION = "rehabilitation"
    HOME_HEALTH = "home_health"
    HOSPICE = "hospice"

class ProviderStatus(str, Enum):
    """Provider status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class ProviderBase(BaseModel):
    """Base provider model"""
    name: str = Field(..., min_length=1, max_length=200)
    provider_type: ProviderType
    npi_number: Optional[str] = Field(None, regex=r'^\d{10}$')
    
    specialties: List[str] = Field(default_factory=list)
    subspecialties: List[str] = Field(default_factory=list)
    
    address_line1: str = Field(..., min_length=1, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=50)
    zip_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="US", min_length=2, max_length=2)
    
    phone: str = Field(..., regex=r'^\+?1?\d{9,15}$')
    fax: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=255)
    
    languages_spoken: List[str] = Field(default_factory=list)
    accepts_new_patients: bool = Field(default=True)
    
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class ProviderCreate(ProviderBase):
    """Provider creation model"""
    license_numbers: List[Dict[str, str]] = Field(default_factory=list)
    board_certifications: List[Dict[str, Any]] = Field(default_factory=list)

class Provider(ProviderBase):
    """Complete provider model"""
    id: str = Field(alias="_id")
    provider_id: str = Field(..., description="Unique provider identifier")
    
    status: ProviderStatus = Field(default=ProviderStatus.PENDING_VERIFICATION)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_verified: Optional[datetime] = None
    
    license_numbers: List[Dict[str, str]] = Field(default_factory=list)
    board_certifications: List[Dict[str, Any]] = Field(default_factory=list)
    
    insurance_networks: List[Dict[str, Any]] = Field(default_factory=list)
    accepted_insurance: List[str] = Field(default_factory=list)
    
    ratings: Dict[str, float] = Field(default_factory=dict)
    reviews_count: int = Field(default=0)
    average_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    
    patient_outcomes: Dict[str, Any] = Field(default_factory=dict)
    quality_metrics: Dict[str, float] = Field(default_factory=dict)
    
    availability_schedule: Dict[str, Any] = Field(default_factory=dict)
    appointment_types: List[str] = Field(default_factory=list)
    
    telemedicine_available: bool = Field(default=False)
    emergency_services: bool = Field(default=False)
    
    hospital_affiliations: List[str] = Field(default_factory=list)
    medical_groups: List[str] = Field(default_factory=list)
    
    conditions_treated: List[str] = Field(default_factory=list)
    procedures_performed: List[str] = Field(default_factory=list)
    
    match_history: List[Dict[str, Any]] = Field(default_factory=list)
    referral_patterns: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class ProviderMatchScore(BaseModel):
    """Provider matching score breakdown"""
    overall_score: float = Field(..., ge=0.0, le=1.0)
    
    clinical_expertise_score: float = Field(..., ge=0.0, le=1.0)
    patient_outcomes_score: float = Field(..., ge=0.0, le=1.0)
    insurance_coverage_score: float = Field(..., ge=0.0, le=1.0)
    geographic_proximity_score: float = Field(..., ge=0.0, le=1.0)
    patient_preferences_score: float = Field(..., ge=0.0, le=1.0)
    
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    matching_factors: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)

class ProviderMatch(BaseModel):
    """Provider matching result"""
    id: str = Field(alias="_id")
    match_id: str = Field(..., description="Unique match identifier")
    
    patient_id: str = Field(..., min_length=1)
    provider_id: str = Field(..., min_length=1)
    
    provider: Provider
    match_score: ProviderMatchScore
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    
    status: str = Field(default="active", regex="^(active|contacted|scheduled|expired|declined)$")
    
    ai_explanation: str = Field(..., min_length=1)
    confidence_level: str = Field(..., regex="^(high|medium|low)$")
    
    estimated_wait_time: Optional[str] = None
    estimated_cost: Optional[Dict[str, float]] = None
    
    contact_information: Dict[str, str] = Field(default_factory=dict)
    scheduling_instructions: Optional[str] = None
    
    patient_feedback: Optional[Dict[str, Any]] = None
    outcome_tracked: bool = Field(default=False)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
