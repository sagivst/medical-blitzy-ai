"""
OCR processing service for medical documents
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import pytesseract
import easyocr
from PIL import Image
import cv2
import numpy as np
import io
import base64

from app.core.config import get_settings
from app.models.document import OCRResult, OCRConfidenceLevel

logger = logging.getLogger(__name__)
settings = get_settings()

class OCRService:
    """OCR processing service"""
    
    def __init__(self):
        self.tesseract_path = settings.TESSERACT_PATH
        self.easyocr_reader = None
        self.timeout = settings.OCR_TIMEOUT
    
    async def initialize_easyocr(self):
        """Initialize EasyOCR reader"""
        if self.easyocr_reader is None:
            self.easyocr_reader = easyocr.Reader(['en'])
    
    async def process_document(self, file_content: bytes, mime_type: str, document_id: str) -> OCRResult:
        """Process document with OCR"""
        try:
            start_time = datetime.utcnow()
            
            if mime_type == "application/pdf":
                extracted_text, confidence = await self._process_pdf(file_content)
            elif mime_type.startswith("image/"):
                extracted_text, confidence = await self._process_image(file_content)
            else:
                raise ValueError(f"Unsupported file type: {mime_type}")
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            confidence_level = self._determine_confidence_level(confidence)
            
            medical_entities = await self._extract_medical_entities(extracted_text)
            key_value_pairs = await self._extract_key_value_pairs(extracted_text)
            
            ocr_result = OCRResult(
                extracted_text=extracted_text,
                confidence_score=confidence,
                confidence_level=confidence_level,
                processing_time=processing_time,
                ocr_engine="tesseract+easyocr",
                medical_entities=medical_entities,
                key_value_pairs=key_value_pairs,
                language_detected="en"
            )
            
            logger.info(f"OCR processing completed for document {document_id}")
            return ocr_result
            
        except Exception as e:
            logger.error(f"OCR processing failed for document {document_id}: {str(e)}")
            return OCRResult(
                extracted_text="",
                confidence_score=0.0,
                confidence_level=OCRConfidenceLevel.FAILED,
                processing_time=0.0,
                ocr_engine="failed",
                language_detected="en"
            )
    
    async def _process_pdf(self, file_content: bytes) -> tuple[str, float]:
        """Process PDF document"""
        try:
            from pdf2image import convert_from_bytes
            
            images = convert_from_bytes(file_content)
            all_text = []
            confidences = []
            
            for i, image in enumerate(images):
                image_array = np.array(image)
                
                tesseract_text = pytesseract.image_to_string(image, config='--psm 6')
                tesseract_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                tesseract_confidence = np.mean([int(conf) for conf in tesseract_data['conf'] if int(conf) > 0])
                
                await self.initialize_easyocr()
                easyocr_results = self.easyocr_reader.readtext(image_array)
                easyocr_text = ' '.join([result[1] for result in easyocr_results])
                easyocr_confidence = np.mean([result[2] for result in easyocr_results]) * 100
                
                if tesseract_confidence > easyocr_confidence:
                    all_text.append(tesseract_text)
                    confidences.append(tesseract_confidence)
                else:
                    all_text.append(easyocr_text)
                    confidences.append(easyocr_confidence)
            
            combined_text = '\n'.join(all_text)
            average_confidence = np.mean(confidences) / 100.0
            
            return combined_text, average_confidence
            
        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}")
            return "", 0.0
    
    async def _process_image(self, file_content: bytes) -> tuple[str, float]:
        """Process image document"""
        try:
            image = Image.open(io.BytesIO(file_content))
            image_array = np.array(image)
            
            tesseract_text = pytesseract.image_to_string(image, config='--psm 6')
            tesseract_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            tesseract_confidence = np.mean([int(conf) for conf in tesseract_data['conf'] if int(conf) > 0])
            
            await self.initialize_easyocr()
            easyocr_results = self.easyocr_reader.readtext(image_array)
            easyocr_text = ' '.join([result[1] for result in easyocr_results])
            easyocr_confidence = np.mean([result[2] for result in easyocr_results]) * 100
            
            if tesseract_confidence > easyocr_confidence:
                return tesseract_text, tesseract_confidence / 100.0
            else:
                return easyocr_text, easyocr_confidence / 100.0
                
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            return "", 0.0
    
    def _determine_confidence_level(self, confidence: float) -> OCRConfidenceLevel:
        """Determine confidence level based on score"""
        if confidence >= 0.8:
            return OCRConfidenceLevel.HIGH
        elif confidence >= 0.6:
            return OCRConfidenceLevel.MEDIUM
        elif confidence >= 0.3:
            return OCRConfidenceLevel.LOW
        else:
            return OCRConfidenceLevel.FAILED
    
    async def _extract_medical_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract medical entities from text"""
        entities = []
        
        medical_keywords = [
            "diagnosis", "medication", "prescription", "dosage", "treatment",
            "symptoms", "condition", "procedure", "surgery", "therapy",
            "blood pressure", "heart rate", "temperature", "weight", "height",
            "allergies", "medical history", "family history", "lab results"
        ]
        
        text_lower = text.lower()
        for keyword in medical_keywords:
            if keyword in text_lower:
                entities.append({
                    "entity": keyword,
                    "type": "medical_term",
                    "confidence": 0.8
                })
        
        return entities
    
    async def _extract_key_value_pairs(self, text: str) -> Dict[str, str]:
        """Extract key-value pairs from text"""
        pairs = {}
        
        lines = text.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        pairs[key] = value
        
        return pairs

ocr_service = OCRService()
