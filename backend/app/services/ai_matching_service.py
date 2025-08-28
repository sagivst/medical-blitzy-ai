"""
AI-powered provider matching service
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import math

from app.core.config import get_settings
from app.models.provider import ProviderMatchScore
from app.models.patient import PatientSummary

logger = logging.getLogger(__name__)
settings = get_settings()

class AIMatchingService:
    """AI-powered provider matching service"""
    
    def __init__(self):
        self.matching_timeout = settings.PROVIDER_MATCHING_TIMEOUT
        
        self.weights = {
            "clinical_expertise": 0.40,
            "patient_outcomes": 0.25,
            "insurance_coverage": 0.20,
            "geographic_proximity": 0.10,
            "patient_preferences": 0.05
        }
    
    async def calculate_provider_match_score(
        self, 
        provider: Dict[str, Any], 
        patient_summary: PatientSummary,
        condition: str,
        insurance_provider: Optional[str] = None,
        max_distance_miles: float = 25.0,
        patient_location: Optional[Dict[str, float]] = None,
        language_preference: str = "en",
        gender_preference: Optional[str] = None
    ) -> ProviderMatchScore:
        """Calculate AI-powered provider matching score"""
        try:
            clinical_expertise_score = await self._calculate_clinical_expertise_score(
                provider, condition, patient_summary.primary_conditions
            )
            
            patient_outcomes_score = await self._calculate_patient_outcomes_score(provider)
            
            insurance_coverage_score = await self._calculate_insurance_coverage_score(
                provider, insurance_provider
            )
            
            geographic_proximity_score = await self._calculate_geographic_proximity_score(
                provider, patient_location, max_distance_miles
            )
            
            patient_preferences_score = await self._calculate_patient_preferences_score(
                provider, language_preference, gender_preference
            )
            
            overall_score = (
                clinical_expertise_score * self.weights["clinical_expertise"] +
                patient_outcomes_score * self.weights["patient_outcomes"] +
                insurance_coverage_score * self.weights["insurance_coverage"] +
                geographic_proximity_score * self.weights["geographic_proximity"] +
                patient_preferences_score * self.weights["patient_preferences"]
            )
            
            matching_factors = await self._generate_matching_factors(
                provider, condition, clinical_expertise_score, patient_outcomes_score,
                insurance_coverage_score, geographic_proximity_score
            )
            
            concerns = await self._generate_concerns(
                provider, insurance_coverage_score, geographic_proximity_score
            )
            
            return ProviderMatchScore(
                overall_score=min(max(overall_score, 0.0), 1.0),
                clinical_expertise_score=clinical_expertise_score,
                patient_outcomes_score=patient_outcomes_score,
                insurance_coverage_score=insurance_coverage_score,
                geographic_proximity_score=geographic_proximity_score,
                patient_preferences_score=patient_preferences_score,
                score_breakdown={
                    "clinical_expertise": clinical_expertise_score,
                    "patient_outcomes": patient_outcomes_score,
                    "insurance_coverage": insurance_coverage_score,
                    "geographic_proximity": geographic_proximity_score,
                    "patient_preferences": patient_preferences_score
                },
                matching_factors=matching_factors,
                concerns=concerns
            )
            
        except Exception as e:
            logger.error(f"Provider matching calculation failed: {str(e)}")
            return ProviderMatchScore(
                overall_score=0.0,
                clinical_expertise_score=0.0,
                patient_outcomes_score=0.0,
                insurance_coverage_score=0.0,
                geographic_proximity_score=0.0,
                patient_preferences_score=0.0,
                score_breakdown={},
                matching_factors=[],
                concerns=["Matching calculation failed"]
            )
    
    async def _calculate_clinical_expertise_score(
        self, provider: Dict[str, Any], condition: str, patient_conditions: List[str]
    ) -> float:
        """Calculate clinical expertise score"""
        score = 0.0
        
        conditions_treated = provider.get("conditions_treated", [])
        if any(condition.lower() in treated.lower() for treated in conditions_treated):
            score += 0.4
        
        specialties = provider.get("specialties", [])
        subspecialties = provider.get("subspecialties", [])
        
        condition_specialty_mapping = {
            "diabetes": ["endocrinology", "internal medicine"],
            "heart": ["cardiology", "internal medicine"],
            "cancer": ["oncology", "hematology"],
            "mental health": ["psychiatry", "psychology"],
            "orthopedic": ["orthopedics", "sports medicine"],
            "skin": ["dermatology"],
            "eye": ["ophthalmology"],
            "kidney": ["nephrology", "internal medicine"]
        }
        
        for keyword, relevant_specialties in condition_specialty_mapping.items():
            if keyword in condition.lower():
                if any(spec.lower() in [s.lower() for s in specialties + subspecialties] 
                       for spec in relevant_specialties):
                    score += 0.3
                break
        
        provider_type = provider.get("provider_type", "")
        if provider_type == "specialist":
            score += 0.2
        elif provider_type == "primary_care":
            score += 0.1
        
        board_certifications = provider.get("board_certifications", [])
        if board_certifications:
            score += 0.1
        
        return min(score, 1.0)
    
    async def _calculate_patient_outcomes_score(self, provider: Dict[str, Any]) -> float:
        """Calculate patient outcomes score"""
        average_rating = provider.get("average_rating", 0.0)
        rating_score = average_rating / 5.0
        
        quality_metrics = provider.get("quality_metrics", {})
        quality_score = quality_metrics.get("overall_quality", 0.5)
        
        patient_outcomes = provider.get("patient_outcomes", {})
        outcomes_score = patient_outcomes.get("success_rate", 0.5)
        
        return (rating_score * 0.5 + quality_score * 0.3 + outcomes_score * 0.2)
    
    async def _calculate_insurance_coverage_score(
        self, provider: Dict[str, Any], insurance_provider: Optional[str]
    ) -> float:
        """Calculate insurance coverage score"""
        if not insurance_provider:
            return 0.5  # Neutral score if no insurance info
        
        accepted_insurance = provider.get("accepted_insurance", [])
        
        if insurance_provider in accepted_insurance:
            return 1.0
        
        insurance_groups = {
            "blue cross": ["blue cross blue shield", "anthem", "bcbs"],
            "aetna": ["aetna", "cvs health"],
            "united": ["united healthcare", "optum", "unitedhealthcare"],
            "cigna": ["cigna", "express scripts"],
            "humana": ["humana", "centerwell"]
        }
        
        insurance_lower = insurance_provider.lower()
        for group_key, group_insurances in insurance_groups.items():
            if any(group_key in ins.lower() for ins in [insurance_provider]):
                if any(any(group_ins in accepted.lower() for group_ins in group_insurances) 
                       for accepted in accepted_insurance):
                    return 0.8
        
        return 0.2
    
    async def _calculate_geographic_proximity_score(
        self, provider: Dict[str, Any], patient_location: Optional[Dict[str, float]], max_distance_miles: float
    ) -> float:
        """Calculate geographic proximity score"""
        if not patient_location or not provider.get("latitude") or not provider.get("longitude"):
            return 0.5  # Neutral score if location data unavailable
        
        try:
            distance = self._calculate_distance(
                patient_location.get("lat", 0),
                patient_location.get("lng", 0),
                provider["latitude"],
                provider["longitude"]
            )
            
            if distance <= max_distance_miles:
                return max(0.0, 1.0 - (distance / max_distance_miles))
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Distance calculation failed: {str(e)}")
            return 0.5
    
    async def _calculate_patient_preferences_score(
        self, provider: Dict[str, Any], language_preference: str, gender_preference: Optional[str]
    ) -> float:
        """Calculate patient preferences score"""
        score = 0.5  # Base score
        
        languages_spoken = provider.get("languages_spoken", ["en"])
        if language_preference in languages_spoken:
            score += 0.3
        
        if gender_preference and provider.get("gender") == gender_preference:
            score += 0.2
        
        if provider.get("telemedicine_available", False):
            score += 0.1
        
        if provider.get("accepts_new_patients", True):
            score += 0.1
        else:
            score -= 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in miles using Haversine formula"""
        R = 3959  # Earth's radius in miles
        
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    async def _generate_matching_factors(
        self, provider: Dict[str, Any], condition: str, clinical_score: float,
        outcomes_score: float, insurance_score: float, proximity_score: float
    ) -> List[str]:
        """Generate human-readable matching factors"""
        factors = []
        
        if clinical_score >= 0.8:
            factors.append(f"Excellent clinical expertise in {condition}")
        elif clinical_score >= 0.6:
            factors.append(f"Good clinical background for {condition}")
        
        if outcomes_score >= 0.8:
            rating = provider.get("average_rating", 0)
            factors.append(f"High patient satisfaction ({rating:.1f}/5.0)")
        elif outcomes_score >= 0.6:
            factors.append("Good patient outcomes")
        
        if insurance_score >= 0.8:
            factors.append("Accepts your insurance")
        elif insurance_score >= 0.5:
            factors.append("Limited insurance coverage")
        
        if proximity_score >= 0.8:
            factors.append("Conveniently located")
        elif proximity_score >= 0.5:
            factors.append("Reasonable distance")
        
        if provider.get("telemedicine_available"):
            factors.append("Offers telemedicine")
        
        if provider.get("accepts_new_patients"):
            factors.append("Accepting new patients")
        
        return factors
    
    async def _generate_concerns(
        self, provider: Dict[str, Any], insurance_score: float, proximity_score: float
    ) -> List[str]:
        """Generate potential concerns"""
        concerns = []
        
        if insurance_score < 0.3:
            concerns.append("May not accept your insurance")
        
        if proximity_score < 0.3:
            concerns.append("Located far from your area")
        
        if not provider.get("accepts_new_patients"):
            concerns.append("Not currently accepting new patients")
        
        rating = provider.get("average_rating", 0)
        if rating < 3.0 and rating > 0:
            concerns.append("Below average patient ratings")
        
        reviews_count = provider.get("reviews_count", 0)
        if reviews_count < 5:
            concerns.append("Limited patient reviews available")
        
        return concerns

ai_matching_service = AIMatchingService()
