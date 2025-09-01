"""
Communication hub for family notifications and provider messaging
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class CommunicationService:
    """Communication hub service"""
    
    def __init__(self):
        self.notification_channels = ["email", "sms", "app_notification"]
    
    async def send_provider_match_notification(
        self, patient_id: str, matched_providers: List[Dict[str, Any]], 
        family_members: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send provider match notifications to patient and family"""
        try:
            notifications_sent = []
            
            provider_names = [p.get("name", "Unknown") for p in matched_providers[:3]]
            message = f"Found {len(matched_providers)} matching healthcare providers: {', '.join(provider_names)}"
            
            patient_notification = {
                "recipient_id": patient_id,
                "type": "provider_match",
                "message": message,
                "timestamp": datetime.utcnow(),
                "providers": matched_providers
            }
            notifications_sent.append(patient_notification)
            
            if family_members:
                for family_member in family_members:
                    family_notification = {
                        "recipient_id": family_member.get("id"),
                        "type": "family_provider_update",
                        "message": f"Provider recommendations available for {patient_id}",
                        "timestamp": datetime.utcnow(),
                        "patient_id": patient_id
                    }
                    notifications_sent.append(family_notification)
            
            return {
                "success": True,
                "notifications_sent": len(notifications_sent),
                "notifications": notifications_sent
            }
            
        except Exception as e:
            logger.error(f"Communication notification failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def send_document_processing_update(
        self, patient_id: str, document_id: str, status: str, ocr_results: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Send document processing status updates"""
        try:
            message = f"Document {document_id} processing {status}"
            if status == "completed" and ocr_results:
                keywords = ocr_results.get("extracted_keywords", [])
                message += f". Extracted keywords: {', '.join(keywords[:5])}"
            
            notification = {
                "recipient_id": patient_id,
                "type": "document_processing",
                "message": message,
                "timestamp": datetime.utcnow(),
                "document_id": document_id,
                "status": status
            }
            
            return {"success": True, "notification": notification}
            
        except Exception as e:
            logger.error(f"Document processing notification failed: {str(e)}")
            return {"success": False, "error": str(e)}

communication_service = CommunicationService()
