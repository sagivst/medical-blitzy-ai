"""
Insurance and claims management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta

from app.core.security import verify_token, require_patient_access, audit_logger
from app.core.database import get_mongodb
from app.models.insurance import ClaimCreate, ClaimStatus, ClaimType

router = APIRouter()
security = HTTPBearer()

@router.post("/claims", response_model=Dict[str, Any])
async def create_claim(
    claim_data: ClaimCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Create new insurance claim"""
    try:
        token_data = await verify_token(credentials)
        require_patient_access(claim_data.patient_id, token_data)
        
        patient = await db.patients.find_one({"patient_id": claim_data.patient_id})
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        claim_id = f"CLM_{datetime.utcnow().strftime('%Y%m%d')}_{hash(f'{claim_data.patient_id}_{datetime.utcnow()}') % 100000:05d}"
        
        claim_dict = claim_data.dict()
        claim_dict.update({
            "claim_id": claim_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "processing_history": [{
                "timestamp": datetime.utcnow(),
                "action": "created",
                "user_id": token_data.get("sub"),
                "details": {"claim_type": claim_data.claim_type, "total_amount": claim_data.total_charge_amount}
            }]
        })
        
        result = await db.insurance_claims.insert_one(claim_dict)
        
        await db.patients.update_one(
            {"patient_id": claim_data.patient_id},
            {"$inc": {"insurance_claims_count": 1}}
        )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "insurance_claim",
            claim_id,
            "create"
        )
        
        return {
            "message": "Insurance claim created successfully",
            "claim_id": claim_id,
            "status": ClaimStatus.DRAFT
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create claim: {str(e)}"
        )

@router.get("/claims", response_model=List[Dict[str, Any]])
async def get_claims(
    patient_id: Optional[str] = Query(None),
    status: Optional[ClaimStatus] = Query(None),
    claim_type: Optional[ClaimType] = Query(None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get insurance claims with filtering"""
    try:
        token_data = await verify_token(credentials)
        
        query_filter = {}
        
        if patient_id:
            require_patient_access(patient_id, token_data)
            query_filter["patient_id"] = patient_id
        else:
            user_role = token_data.get("role", "patient")
            if user_role == "patient":
                query_filter["patient_id"] = token_data.get("sub")
            elif user_role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        
        if status:
            query_filter["status"] = status
        if claim_type:
            query_filter["claim_type"] = claim_type
        
        cursor = db.insurance_claims.find(query_filter).skip(offset).limit(limit).sort("created_at", -1)
        claims = await cursor.to_list(length=limit)
        
        for claim in claims:
            audit_logger.log_access(
                token_data.get("sub"),
                "insurance_claim",
                claim["claim_id"],
                "read"
            )
        
        return claims
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve claims: {str(e)}"
        )
