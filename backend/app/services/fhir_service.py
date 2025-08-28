"""
FHIR conversion and Golden Record management service
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import uuid

from app.core.config import get_settings
from app.models.fhir_models import (
    FHIRResource, FHIRResourceType, FHIRVersion, 
    FHIRConversionResult, FHIRPatient, FHIRObservation
)

logger = logging.getLogger(__name__)
settings = get_settings()

class FHIRService:
    """FHIR conversion and management service"""
    
    def __init__(self):
        self.fhir_version = FHIRVersion.R5
        self.fhir_server_url = settings.FHIR_SERVER_URL
    
    async def convert_document_to_fhir(self, document_text: str, patient_id: str, document_type: str) -> FHIRConversionResult:
        """Convert extracted document text to FHIR resources"""
        try:
            start_time = datetime.utcnow()
            
            resources_created = []
            conversion_summary = {}
            
            if document_type == "lab_report":
                observations = await self._extract_lab_observations(document_text, patient_id)
                resources_created.extend(observations)
            elif document_type == "prescription":
                medication_requests = await self._extract_medication_requests(document_text, patient_id)
                resources_created.extend(medication_requests)
            elif document_type == "discharge_summary":
                conditions = await self._extract_conditions(document_text, patient_id)
                procedures = await self._extract_procedures(document_text, patient_id)
                resources_created.extend(conditions + procedures)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            conversion_result = FHIRConversionResult(
                request_id=str(uuid.uuid4()),
                success=len(resources_created) > 0,
                resources_created=resources_created,
                conversion_summary={
                    "total_resources": len(resources_created),
                    "resource_types": list(set([r.resource_type for r in resources_created]))
                },
                validation_results={"valid": True, "errors": []},
                quality_assessment={"completeness": 0.8, "accuracy": 0.9},
                processing_time=processing_time,
                confidence_score=0.85
            )
            
            logger.info(f"FHIR conversion completed: {len(resources_created)} resources created")
            return conversion_result
            
        except Exception as e:
            logger.error(f"FHIR conversion failed: {str(e)}")
            return FHIRConversionResult(
                request_id=str(uuid.uuid4()),
                success=False,
                errors=[str(e)],
                processing_time=0.0,
                confidence_score=0.0
            )
    
    async def _extract_lab_observations(self, text: str, patient_id: str) -> List[FHIRResource]:
        """Extract lab observations from text"""
        observations = []
        
        lab_patterns = [
            ("glucose", "mg/dL", "33747-0"),
            ("cholesterol", "mg/dL", "2093-3"),
            ("blood pressure", "mmHg", "85354-9"),
            ("heart rate", "bpm", "8867-4"),
            ("temperature", "°F", "8310-5")
        ]
        
        text_lower = text.lower()
        for lab_name, unit, loinc_code in lab_patterns:
            if lab_name in text_lower:
                fhir_id = f"obs-{uuid.uuid4().hex}"
                
                observation_data = {
                    "resourceType": "Observation",
                    "id": fhir_id,
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "laboratory"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": loinc_code,
                            "display": lab_name.title()
                        }]
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "effectiveDateTime": datetime.utcnow().isoformat(),
                    "valueQuantity": {
                        "unit": unit,
                        "system": "http://unitsofmeasure.org"
                    }
                }
                
                fhir_resource = FHIRResource(
                    fhir_id=fhir_id,
                    resource_type=FHIRResourceType.OBSERVATION,
                    patient_id=patient_id,
                    resource_data=observation_data,
                    extracted_from_text=True,
                    extraction_confidence=0.8
                )
                
                observations.append(fhir_resource)
        
        return observations
    
    async def _extract_medication_requests(self, text: str, patient_id: str) -> List[FHIRResource]:
        """Extract medication requests from text"""
        medications = []
        
        medication_keywords = [
            "aspirin", "ibuprofen", "acetaminophen", "metformin", "lisinopril",
            "atorvastatin", "amlodipine", "metoprolol", "omeprazole", "levothyroxine"
        ]
        
        text_lower = text.lower()
        for medication in medication_keywords:
            if medication in text_lower:
                fhir_id = f"med-{uuid.uuid4().hex}"
                
                medication_data = {
                    "resourceType": "MedicationRequest",
                    "id": fhir_id,
                    "status": "active",
                    "intent": "order",
                    "medicationCodeableConcept": {
                        "coding": [{
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "display": medication.title()
                        }]
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "authoredOn": datetime.utcnow().isoformat()
                }
                
                fhir_resource = FHIRResource(
                    fhir_id=fhir_id,
                    resource_type=FHIRResourceType.MEDICATION_REQUEST,
                    patient_id=patient_id,
                    resource_data=medication_data,
                    extracted_from_text=True,
                    extraction_confidence=0.7
                )
                
                medications.append(fhir_resource)
        
        return medications
    
    async def _extract_conditions(self, text: str, patient_id: str) -> List[FHIRResource]:
        """Extract conditions from text"""
        conditions = []
        
        condition_keywords = [
            ("diabetes", "E11.9"),
            ("hypertension", "I10"),
            ("asthma", "J45.9"),
            ("depression", "F32.9"),
            ("arthritis", "M19.9")
        ]
        
        text_lower = text.lower()
        for condition_name, icd_code in condition_keywords:
            if condition_name in text_lower:
                fhir_id = f"cond-{uuid.uuid4().hex}"
                
                condition_data = {
                    "resourceType": "Condition",
                    "id": fhir_id,
                    "clinicalStatus": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active"
                        }]
                    },
                    "code": {
                        "coding": [{
                            "system": "http://hl7.org/fhir/sid/icd-10-cm",
                            "code": icd_code,
                            "display": condition_name.title()
                        }]
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "recordedDate": datetime.utcnow().isoformat()
                }
                
                fhir_resource = FHIRResource(
                    fhir_id=fhir_id,
                    resource_type=FHIRResourceType.CONDITION,
                    patient_id=patient_id,
                    resource_data=condition_data,
                    extracted_from_text=True,
                    extraction_confidence=0.75
                )
                
                conditions.append(fhir_resource)
        
        return conditions
    
    async def _extract_procedures(self, text: str, patient_id: str) -> List[FHIRResource]:
        """Extract procedures from text"""
        procedures = []
        
        procedure_keywords = [
            ("surgery", "0DT70ZZ"),
            ("biopsy", "0HB0XZX"),
            ("x-ray", "BW00ZZZ"),
            ("mri", "BF00ZZZ"),
            ("ct scan", "BW00ZZZ")
        ]
        
        text_lower = text.lower()
        for procedure_name, cpt_code in procedure_keywords:
            if procedure_name in text_lower:
                fhir_id = f"proc-{uuid.uuid4().hex}"
                
                procedure_data = {
                    "resourceType": "Procedure",
                    "id": fhir_id,
                    "status": "completed",
                    "code": {
                        "coding": [{
                            "system": "http://www.cms.gov/Medicare/Coding/ICD10",
                            "code": cpt_code,
                            "display": procedure_name.title()
                        }]
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "performedDateTime": datetime.utcnow().isoformat()
                }
                
                fhir_resource = FHIRResource(
                    fhir_id=fhir_id,
                    resource_type=FHIRResourceType.PROCEDURE,
                    patient_id=patient_id,
                    resource_data=procedure_data,
                    extracted_from_text=True,
                    extraction_confidence=0.7
                )
                
                procedures.append(fhir_resource)
        
        return procedures

fhir_service = FHIRService()
