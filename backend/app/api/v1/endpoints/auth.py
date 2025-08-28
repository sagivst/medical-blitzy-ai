"""
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from datetime import datetime, timedelta

from app.core.security import security_manager, audit_logger
from app.core.database import get_mongodb
from app.models.patient import Patient, PatientCreate

router = APIRouter()
security = HTTPBearer()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: Dict[str, Any]

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=Dict[str, Any])
async def register_patient(
    patient_data: PatientCreate,
    db = Depends(get_mongodb)
):
    """Register a new patient"""
    try:
        existing_patient = await db.patients.find_one({"email": patient_data.email})
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = security_manager.hash_password(patient_data.password)
        patient_id = security_manager.generate_patient_id()
        
        patient_dict = patient_data.dict(exclude={"password", "terms_accepted", "hipaa_authorization"})
        patient_dict.update({
            "patient_id": patient_id,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "hipaa_authorization_date": datetime.utcnow() if patient_data.hipaa_authorization else None,
            "terms_acceptance_date": datetime.utcnow() if patient_data.terms_accepted else None,
            "consent_version": "1.0"
        })
        
        result = await db.patients.insert_one(patient_dict)
        
        audit_logger.log_authentication(patient_id, True)
        
        return {
            "message": "Patient registered successfully",
            "patient_id": patient_id,
            "status": "active"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db = Depends(get_mongodb)
):
    """Authenticate patient and return tokens"""
    try:
        patient = await db.patients.find_one({"email": login_data.email})
        if not patient:
            audit_logger.log_authentication(login_data.email, False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not security_manager.verify_password(login_data.password, patient["password_hash"]):
            audit_logger.log_authentication(patient["patient_id"], False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        token_data = {
            "sub": patient["patient_id"],
            "email": patient["email"],
            "role": "patient"
        }
        
        access_token = security_manager.create_access_token(token_data)
        refresh_token = security_manager.create_refresh_token(token_data)
        
        await db.patients.update_one(
            {"patient_id": patient["patient_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        audit_logger.log_authentication(patient["patient_id"], True)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800,
            user_info={
                "patient_id": patient["patient_id"],
                "email": patient["email"],
                "first_name": patient["first_name"],
                "last_name": patient["last_name"],
                "tier": patient.get("tier", "free")
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(
    refresh_data: RefreshTokenRequest
):
    """Refresh access token using refresh token"""
    try:
        payload = security_manager.verify_token(refresh_data.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        token_data = {
            "sub": payload["sub"],
            "email": payload["email"],
            "role": payload["role"]
        }
        
        new_access_token = security_manager.create_access_token(token_data)
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 1800
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )

@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get current authenticated user information"""
    try:
        payload = security_manager.verify_token(credentials.credentials)
        patient_id = payload.get("sub")
        
        patient = await db.patients.find_one({"patient_id": patient_id})
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        patient_info = {
            "patient_id": patient["patient_id"],
            "email": patient["email"],
            "first_name": patient["first_name"],
            "last_name": patient["last_name"],
            "tier": patient.get("tier", "free"),
            "status": patient.get("status", "active"),
            "created_at": patient["created_at"],
            "last_login": patient.get("last_login")
        }
        
        return patient_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )
