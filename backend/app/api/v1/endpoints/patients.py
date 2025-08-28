"""
Patient management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.core.security import verify_token, require_patient_access, audit_logger
from app.core.database import get_mongodb
from app.models.patient import Patient, PatientUpdate, PatientSummary

router = APIRouter()
security = HTTPBearer()

@router.get("/{patient_id}", response_model=Dict[str, Any])
async def get_patient(
    patient_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get patient by ID"""
    try:
        token_data = await verify_token(credentials)
        require_patient_access(patient_id, token_data)
        
        patient = await db.patients.find_one(
            {"patient_id": patient_id},
            {"password_hash": 0}
        )
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "patient",
            patient_id,
            "read"
        )
        
        return patient
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve patient: {str(e)}"
        )

@router.put("/{patient_id}", response_model=Dict[str, Any])
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Update patient information"""
    try:
        token_data = await verify_token(credentials)
        require_patient_access(patient_id, token_data)
        
        existing_patient = await db.patients.find_one({"patient_id": patient_id})
        if not existing_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        update_data = patient_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.patients.update_one(
            {"patient_id": patient_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No changes made"
            )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "patient",
            patient_id,
            "update",
            details={"fields_updated": list(update_data.keys())}
        )
        
        updated_patient = await db.patients.find_one(
            {"patient_id": patient_id},
            {"password_hash": 0}
        )
        
        return updated_patient
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update patient: {str(e)}"
        )

@router.get("/{patient_id}/summary", response_model=PatientSummary)
async def get_patient_summary(
    patient_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get patient summary for provider matching"""
    try:
        token_data = await verify_token(credentials)
        require_patient_access(patient_id, token_data)
        
        patient = await db.patients.find_one({"patient_id": patient_id})
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        documents = await db.medical_documents.find(
            {"patient_id": patient_id, "status": "indexed"}
        ).to_list(length=None)
        
        conditions = []
        medications = []
        
        for doc in documents:
            conditions.extend(doc.get("extracted_conditions", []))
            medications.extend(doc.get("extracted_medications", []))
        
        birth_date = patient.get("date_of_birth")
        age = 0
        if birth_date:
            age = (datetime.utcnow() - birth_date).days // 365
        
        summary = PatientSummary(
            patient_id=patient_id,
            age=age,
            gender=patient.get("gender"),
            primary_conditions=list(set(conditions)),
            current_medications=list(set(medications)),
            insurance_provider=patient.get("insurance_provider"),
            preferred_language=patient.get("preferred_language", "en"),
            geographic_location={
                "city": patient.get("city", ""),
                "state": patient.get("state", ""),
                "zip_code": patient.get("zip_code", "")
            }
        )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "patient_summary",
            patient_id,
            "read"
        )
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get patient summary: {str(e)}"
        )
