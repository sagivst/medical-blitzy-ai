"""
Healthcare provider endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import math

from app.core.security import verify_token, require_patient_access, audit_logger
from app.core.database import get_mongodb
from app.models.provider import ProviderType, ProviderMatch, ProviderMatchScore

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[Dict[str, Any]])
async def search_providers(
    specialty: Optional[str] = Query(None),
    provider_type: Optional[ProviderType] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    zip_code: Optional[str] = Query(None),
    radius_miles: float = Query(default=25.0, gt=0, le=500),
    insurance_accepted: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    accepts_new_patients: Optional[bool] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Search healthcare providers"""
    try:
        token_data = await verify_token(credentials)
        
        query_filter: Dict[str, Any] = {"status": "active"}
        
        if specialty:
            query_filter["$or"] = [
                {"specialties": {"$regex": specialty, "$options": "i"}},
                {"subspecialties": {"$regex": specialty, "$options": "i"}}
            ]
        
        if provider_type:
            query_filter["provider_type"] = provider_type
        
        if city:
            query_filter["city"] = {"$regex": city, "$options": "i"}
        
        if state:
            query_filter["state"] = state
        
        if zip_code:
            query_filter["zip_code"] = zip_code
        
        if insurance_accepted:
            query_filter["accepted_insurance"] = {"$in": [insurance_accepted]}
        
        if language:
            query_filter["languages_spoken"] = {"$in": [language]}
        
        if accepts_new_patients is not None:
            query_filter["accepts_new_patients"] = accepts_new_patients
        
        if min_rating:
            query_filter["average_rating"] = {"$gte": min_rating}
        
        cursor = db.providers.find(query_filter).skip(offset).limit(limit)
        providers = await cursor.to_list(length=limit)
        
        audit_logger.log_access(
            token_data.get("sub"),
            "provider_search",
            "multiple",
            "read",
            details={"query_params": query_filter, "results_count": len(providers)}
        )
        
        return providers
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Provider search failed: {str(e)}"
        )

@router.get("/{provider_id}", response_model=Dict[str, Any])
async def get_provider(
    provider_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get provider by ID"""
    try:
        token_data = await verify_token(credentials)
        
        provider = await db.providers.find_one({"provider_id": provider_id})
        if not provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider not found"
            )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "provider",
            provider_id,
            "read"
        )
        
        return provider
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve provider: {str(e)}"
        )
