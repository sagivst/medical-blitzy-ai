"""
Document management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional, Dict, Any
from datetime import datetime
import hashlib
import uuid

from app.core.security import verify_token, require_patient_access, audit_logger
from app.core.database import get_mongodb
from app.models.document import DocumentType, DocumentStatus

router = APIRouter()
security = HTTPBearer()

@router.post("/upload", response_model=Dict[str, Any])
async def upload_document(
    patient_id: str = Form(...),
    document_type: DocumentType = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Upload medical document"""
    try:
        token_data = await verify_token(credentials)
        require_patient_access(patient_id, token_data)
        
        if file.size > 50 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 50MB limit"
            )
        
        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "image/tiff",
            "text/plain"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not supported"
            )
        
        file_content = await file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        existing_doc = await db.medical_documents.find_one({
            "patient_id": patient_id,
            "file_hash": file_hash
        })
        
        if existing_doc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document already exists"
            )
        
        document_id = f"DOC_{uuid.uuid4().hex.upper()}"
        file_path = f"documents/{patient_id}/{document_id}_{file.filename}"
        
        document_dict = {
            "document_id": document_id,
            "patient_id": patient_id,
            "filename": file.filename,
            "document_type": document_type,
            "file_size": file.size,
            "mime_type": file.content_type,
            "uploaded_by": token_data.get("sub"),
            "description": description,
            "file_path": file_path,
            "file_hash": file_hash,
            "status": DocumentStatus.UPLOADED,
            "upload_date": datetime.utcnow(),
            "last_modified": datetime.utcnow(),
            "is_sensitive": True,
            "encryption_status": "encrypted",
            "processing_history": [{
                "timestamp": datetime.utcnow(),
                "action": "uploaded",
                "user_id": token_data.get("sub"),
                "details": {"filename": file.filename, "size": file.size}
            }]
        }
        
        result = await db.medical_documents.insert_one(document_dict)
        
        await db.patients.update_one(
            {"patient_id": patient_id},
            {"$inc": {"document_count": 1}}
        )
        
        audit_logger.log_access(
            token_data.get("sub"),
            "document",
            document_id,
            "create"
        )
        
        return {
            "message": "Document uploaded successfully",
            "document_id": document_id,
            "status": DocumentStatus.UPLOADED,
            "processing_queued": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )

@router.get("/", response_model=List[Dict[str, Any]])
async def get_documents(
    patient_id: Optional[str] = Query(None),
    document_type: Optional[DocumentType] = Query(None),
    status: Optional[DocumentStatus] = Query(None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get documents with filtering"""
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
        
        if document_type:
            query_filter["document_type"] = document_type
        if status:
            query_filter["status"] = status
        
        cursor = db.medical_documents.find(query_filter).skip(offset).limit(limit).sort("upload_date", -1)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            audit_logger.log_access(
                token_data.get("sub"),
                "document",
                doc["document_id"],
                "read"
            )
        
        return documents
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve documents: {str(e)}"
        )

@router.get("/{document_id}", response_model=Dict[str, Any])
async def get_document(
    document_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_mongodb)
):
    """Get document by ID"""
    try:
        token_data = await verify_token(credentials)
        
        document = await db.medical_documents.find_one({"document_id": document_id})
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        require_patient_access(document["patient_id"], token_data)
        
        audit_logger.log_access(
            token_data.get("sub"),
            "document",
            document_id,
            "read"
        )
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}"
        )
