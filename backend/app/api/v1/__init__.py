"""
API v1 package
"""

from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.patients import router as patients_router
from .endpoints.documents import router as documents_router
from .endpoints.providers import router as providers_router
from .endpoints.insurance import router as insurance_router
from .endpoints.fhir import router as fhir_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(patients_router, prefix="/patients", tags=["patients"])
api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
api_router.include_router(providers_router, prefix="/providers", tags=["providers"])
api_router.include_router(insurance_router, prefix="/insurance", tags=["insurance"])
api_router.include_router(fhir_router, prefix="/fhir", tags=["fhir"])
