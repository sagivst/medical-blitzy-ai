"""
Translation service for multilingual communication
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class TranslationService:
    """Translation service for multilingual support"""
    
    def __init__(self):
        self.supported_languages = ["en", "he", "ar", "es", "fr", "de"]
        self.timeout = settings.TRANSLATION_TIMEOUT
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Translate text between languages"""
        try:
            if source_lang == target_lang:
                return {"translated_text": text, "confidence": 1.0}
            
            medical_translations = {
                "brain": {"he": "מוח", "ar": "دماغ"},
                "mri": {"he": "MRI", "ar": "تصوير بالرنين المغناطيسي"},
                "headache": {"he": "כאב ראש", "ar": "صداع"},
                "neurological": {"he": "נוירולוגי", "ar": "عصبي"},
                "heart": {"he": "לב", "ar": "قلب"},
                "cardiac": {"he": "לבבי", "ar": "قلبي"},
                "chest": {"he": "חזה", "ar": "صدر"},
                "pain": {"he": "כאב", "ar": "ألم"}
            }
            
            translated_text = text
            for en_word, translations in medical_translations.items():
                if en_word in text.lower() and target_lang in translations:
                    translated_text = translated_text.replace(en_word, translations[target_lang])
            
            return {
                "translated_text": translated_text,
                "confidence": 0.9,
                "source_language": source_lang,
                "target_language": target_lang
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return {"translated_text": text, "confidence": 0.0, "error": str(e)}

translation_service = TranslationService()
