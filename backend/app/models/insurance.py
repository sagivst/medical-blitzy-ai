"""
Insurance and claims data models
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from bson import ObjectId

class InsuranceType(str, Enum):
    """Insurance plan types"""
    HMO = "hmo"
    PPO = "ppo"
    EPO = "epo"
    POS = "pos"
    HDHP = "hdhp"
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    TRICARE = "tricare"
    COBRA = "cobra"
    OTHER = "other"

class ClaimStatus(str, Enum):
    """Insurance claim status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    PARTIALLY_APPROVED = "partially_approved"
    DENIED = "denied"
    APPEALED = "appealed"
    PAID = "paid"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class ClaimType(str, Enum):
    """Claim types"""
    MEDICAL = "medical"
    PHARMACY = "pharmacy"
    DENTAL = "dental"
    VISION = "vision"
    MENTAL_HEALTH = "mental_health"
    PREVENTIVE = "preventive"
    EMERGENCY = "emergency"
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"

class ClaimLineItem(BaseModel):
    """Individual claim line item"""
    line_number: int = Field(..., ge=1)
    
    service_date: date
    procedure_code: str = Field(..., min_length=1, max_length=20)
    procedure_description: str = Field(..., min_length=1, max_length=500)
    
    diagnosis_codes: List[str] = Field(default_factory=list)
    modifier_codes: List[str] = Field(default_factory=list)
    
    units: int = Field(default=1, ge=1)
    unit_price: float = Field(..., gt=0)
    total_charge: float = Field(..., gt=0)
    
    provider_id: str = Field(..., min_length=1)
    place_of_service: str = Field(..., min_length=1, max_length=10)
    
    prior_authorization_number: Optional[str] = None
    
    approved_amount: Optional[float] = Field(None, ge=0)
    patient_responsibility: Optional[float] = Field(None, ge=0)
    insurance_payment: Optional[float] = Field(None, ge=0)
    
    denial_reason: Optional[str] = None
    denial_code: Optional[str] = None

class ClaimBase(BaseModel):
    """Base claim model"""
    patient_id: str = Field(..., min_length=1)
    insurance_id: str = Field(..., min_length=1)
    
    claim_type: ClaimType
    service_date_from: date
    service_date_to: date
    
    provider_id: str = Field(..., min_length=1)
    facility_id: Optional[str] = None
    
    line_items: List[ClaimLineItem] = Field(..., min_items=1)
    
    total_charge_amount: float = Field(..., gt=0)
    
    patient_signature_on_file: bool = Field(default=True)
    assignment_of_benefits: bool = Field(default=True)
    
    attachments: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=1000)

class ClaimCreate(ClaimBase):
    """Claim creation model"""
    pass

class ClaimUpdate(BaseModel):
    """Claim update model"""
    status: Optional[ClaimStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    attachments: Optional[List[str]] = None

class InsuranceClaim(ClaimBase):
    """Complete insurance claim model"""
    id: str = Field(alias="_id")
    claim_id: str = Field(..., description="Unique claim identifier")
    
    status: ClaimStatus = Field(default=ClaimStatus.DRAFT)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    submitted_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    claim_number: Optional[str] = None
    
    approved_amount: Optional[float] = Field(None, ge=0)
    patient_responsibility: Optional[float] = Field(None, ge=0)
    insurance_payment: Optional[float] = Field(None, ge=0)
    
    denial_reasons: List[str] = Field(default_factory=list)
    denial_codes: List[str] = Field(default_factory=list)
    
    appeal_deadline: Optional[date] = None
    appeal_submitted: bool = Field(default=False)
    appeal_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    processing_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    remittance_advice: Optional[Dict[str, Any]] = None
    explanation_of_benefits: Optional[Dict[str, Any]] = None
    
    auto_generated: bool = Field(default=False)
    ai_confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
