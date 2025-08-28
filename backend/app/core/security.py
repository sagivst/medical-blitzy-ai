"""
Security and authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

class SecurityManager:
    """Security and authentication manager"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)

security_manager = SecurityManager()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to verify JWT token"""
    return security_manager.verify_token(credentials.credentials)

async def get_current_user(token_data: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """Get current authenticated user"""
    user_id = token_data.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    return token_data

def require_permissions(required_permissions: list):
    """Decorator to require specific permissions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            user_permissions = current_user.get("permissions", [])
            if not all(perm in user_permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class HIPAACompliance:
    """HIPAA compliance utilities"""
    
    @staticmethod
    def log_access(user_id: str, resource_type: str, resource_id: str, action: str):
        """Log access to PHI for HIPAA compliance"""
        logger.info(
            f"HIPAA_ACCESS: user_id={user_id}, resource_type={resource_type}, "
            f"resource_id={resource_id}, action={action}, timestamp={datetime.utcnow()}"
        )
    
    @staticmethod
    def anonymize_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize sensitive data"""
        sensitive_fields = [
            "ssn", "social_security_number", "phone", "email", 
            "address", "date_of_birth", "full_name"
        ]
        
        anonymized = data.copy()
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = "***REDACTED***"
        
        return anonymized

hipaa = HIPAACompliance()

def get_current_user_id(token_data: Dict[str, Any]) -> str:
    """Extract user ID from token data"""
    user_id = token_data.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_id

def require_patient_access(patient_id: str, token_data: Dict[str, Any]) -> bool:
    """Check if user has access to patient data"""
    user_id = get_current_user_id(token_data)
    user_role = token_data.get("role", "patient")
    
    if user_role == "admin":
        return True
    elif user_role == "provider":
        return True
    elif user_role == "patient" and user_id == patient_id:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access patient data"
        )

class AuditLogger:
    """HIPAA-compliant audit logging"""
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    def log_authentication(self, user_id: str, success: bool, details: Optional[Dict[str, Any]] = None):
        """Log authentication attempts"""
        self.logger.info(
            f"AUTH: user_id={user_id}, success={success}, "
            f"timestamp={datetime.utcnow()}, details={details or {}}"
        )
    
    def log_access(self, user_id: str, resource_type: str, resource_id: str, 
                   action: str, details: Optional[Dict[str, Any]] = None):
        """Log access to protected resources"""
        self.logger.info(
            f"ACCESS: user_id={user_id}, resource_type={resource_type}, "
            f"resource_id={resource_id}, action={action}, "
            f"timestamp={datetime.utcnow()}, details={details or {}}"
        )

audit_logger = AuditLogger()

def generate_patient_id() -> str:
    """Generate unique patient ID"""
    import uuid
    return f"PAT_{uuid.uuid4().hex.upper()[:12]}"

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create refresh token"""
    to_encode = data.copy()
    to_encode.update({
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7)
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

SecurityManager.generate_patient_id = staticmethod(generate_patient_id)
SecurityManager.create_refresh_token = create_refresh_token
