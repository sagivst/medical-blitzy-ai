"""
FHIR resource management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.core.security import verify_token, require_patient_access, audit_logger
from app.core.database import get_mongodb
from app.models.fhir_models import FHIRResourceType

router = APIRouter()
security = HTTPBearer()

@router.get("/resources", response_model=List[Dict[str, Any]])
async def get_fhir_resources(
    patient_id: Optional[str] = Query(None),
    resource_type: Optional[FHIRResourceType] = Query(None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get FHIR resources with filtering"""
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
        
        if resource_type:
            query_filter["resource_type"] = resource_type
        
        cursor = db.fhir_resources.find(query_filter).skip(offset).limit(limit).sort("created_at", -1)
        resources = await cursor.to_list(length=limit)
        
        for resource in resources:
            audit_logger.log_access(
                token_data.get("sub"),
                "fhir_resource",
                resource["fhir_id"],
                "read"
            )
        
        return resources
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve FHIR resources: {str(e)}"
        )

@router.get("/resources/{fhir_id}", response_model=Dict[str, Any])
async def get_fhir_resource(
    fhir_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get FHIR resource by ID"""
    try:
        token_data = await verify_token(credentials)
        
        resource = await db.fhir_resources.find_one({"fhir_id": fhir_id})
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FHIR resource not found"
            )
        
        require_patient_access(resource["patient_id"], token_data)
        
        audit_logger.log_access(
            token_data.get("sub"),
            "fhir_resource",
            fhir_id,
            "read"
        )
        
        return resource
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve FHIR resource: {str(e)}"
        )
