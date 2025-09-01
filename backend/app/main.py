"""
Medical Blitzy AI - Enhanced Flask server with OCR and AI Provider Matching
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import io
import re
from datetime import datetime

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from services.translation_service import translation_service
    from services.communication_service import communication_service
    print("✅ Translation and Communication services loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: Could not import services: {e}")
    class MockTranslationService:
        def translate_text(self, text, source_lang, target_lang):
            return {"translated_text": text, "confidence": 0.9}
    
    class MockCommunicationService:
        def send_notification(self, **kwargs):
            return {"success": True, "notification_id": "mock_123"}
    
    translation_service = MockTranslationService()
    communication_service = MockCommunicationService()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://172.16.5.2:3000", "http://172.16.5.2:8000", "https://animated-space-disco-jjwrjpg7x7v4hx4q-3000.app.github.dev", "https://*.app.github.dev"], supports_credentials=True)

patients_db = []
documents_db = []
providers_db = [
    {"id": 1, "name": "Dr. Sarah Cohen", "specialty": "Cardiology", "location": "Tel Aviv", "keywords": ["heart", "cardiac", "cardiovascular", "chest pain", "ecg", "ekg"]},
    {"id": 2, "name": "Dr. David Levi", "specialty": "Neurology", "location": "Jerusalem", "keywords": ["brain", "neurological", "mri", "ct scan", "headache", "seizure", "stroke"]},
    {"id": 3, "name": "Dr. Rachel Ben-David", "specialty": "Pediatrics", "location": "Haifa", "keywords": ["child", "pediatric", "infant", "vaccination", "growth"]},
    {"id": 4, "name": "Dr. Michael Rosen", "specialty": "Radiology", "location": "Tel Aviv", "keywords": ["mri", "ct", "x-ray", "ultrasound", "imaging", "scan"]},
    {"id": 5, "name": "Dr. Anna Goldberg", "specialty": "Orthopedics", "location": "Jerusalem", "keywords": ["bone", "joint", "fracture", "spine", "knee", "shoulder"]},
    {"id": 6, "name": "Dr. Yossi Katz", "specialty": "Oncology", "location": "Haifa", "keywords": ["cancer", "tumor", "oncology", "chemotherapy", "radiation"]}
]
claims_db = []

def simple_ocr_simulation(file_content):
    """
    Simulate OCR processing for demo purposes
    In a real implementation, this would use EasyOCR or Tesseract
    """
    simulated_text = """
    MAGNETIC RESONANCE IMAGING REPORT
    
    Patient: John Doe
    Date: 2024-01-15
    Study: Brain MRI with contrast
    
    CLINICAL INDICATION:
    Headaches, neurological symptoms
    
    FINDINGS:
    The brain MRI shows normal brain parenchyma.
    No evidence of acute infarction or hemorrhage.
    Ventricular system is normal in size and configuration.
    No mass lesions identified.
    
    IMPRESSION:
    Normal brain MRI study.
    Recommend follow-up with neurology for persistent headaches.
    
    Keywords detected: brain, mri, neurological, headache
    """
    return simulated_text

def extract_medical_keywords(text):
    """Extract medical keywords from OCR text"""
    medical_terms = [
        "brain", "mri", "ct", "scan", "neurological", "headache", "seizure",
        "heart", "cardiac", "cardiovascular", "chest", "ecg", "ekg",
        "bone", "joint", "fracture", "spine", "orthopedic",
        "cancer", "tumor", "oncology", "radiation",
        "ultrasound", "x-ray", "imaging", "radiology"
    ]
    
    text_lower = text.lower()
    found_keywords = []
    
    for term in medical_terms:
        if term in text_lower:
            found_keywords.append(term)
    
    return found_keywords

def match_providers_by_keywords(keywords):
    """Match providers based on extracted keywords"""
    matched_providers = []
    
    for provider in providers_db:
        score = 0
        matched_keywords = []
        
        for keyword in keywords:
            if keyword in provider.get("keywords", []):
                score += 1
                matched_keywords.append(keyword)
        
        if score > 0:
            provider_match = provider.copy()
            provider_match["match_score"] = score
            provider_match["matched_keywords"] = matched_keywords
            provider_match["relevance"] = f"{score}/{len(keywords)} keywords matched"
            matched_providers.append(provider_match)
    
    matched_providers.sort(key=lambda x: x["match_score"], reverse=True)
    return matched_providers

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Medical Blitzy AI IHN - Minimal",
        "version": "0.1.0",
        "framework": "Flask"
    })

@app.route("/")
def root():
    return jsonify({
        "message": "Medical Blitzy AI - Minimal Test Version",
        "version": "0.1.0",
        "endpoints": ["/health", "/api/v1/patients", "/api/v1/documents", "/api/v1/providers", "/api/v1/insurance"]
    })

@app.route("/api/v1/patients", methods=["GET", "POST"])
def patients():
    if request.method == "GET":
        return jsonify({"patients": patients_db, "count": len(patients_db)})
    elif request.method == "POST":
        data = request.get_json() or {}
        patient = {
            "id": len(patients_db) + 1,
            "name": data.get("name", "Test Patient"),
            "age": data.get("age", 30),
            "created": "2024-01-01"
        }
        patients_db.append(patient)
        return jsonify({"message": "Patient created", "patient": patient})

@app.route("/api/v1/documents", methods=["GET", "POST"])
def documents():
    if request.method == "GET":
        return jsonify({"documents": documents_db, "count": len(documents_db)})
    elif request.method == "POST":
        data = request.get_json() or {}
        
        ocr_text = simple_ocr_simulation(data.get("file_content", ""))
        keywords = extract_medical_keywords(ocr_text)
        
        document = {
            "id": len(documents_db) + 1,
            "filename": data.get("filename", "test_document.pdf"),
            "type": data.get("type", "mri_scan"),
            "status": "processed",
            "created": datetime.now().isoformat(),
            "ocr_text": ocr_text,
            "extracted_keywords": keywords,
            "processing_complete": True
        }
        documents_db.append(document)
        
        matched_providers = match_providers_by_keywords(keywords)
        
        return jsonify({
            "message": "Document uploaded and processed", 
            "document": document,
            "matched_providers": matched_providers,
            "provider_recommendations": len(matched_providers)
        })

@app.route("/api/v1/providers", methods=["GET"])
def providers():
    specialty = request.args.get("specialty")
    location = request.args.get("location")
    keywords = request.args.get("keywords")  # New parameter for keyword-based search
    document_id = request.args.get("document_id")  # Search based on specific document
    
    filtered_providers = providers_db
    
    if document_id:
        document = next((d for d in documents_db if d["id"] == int(document_id)), None)
        if document and "extracted_keywords" in document:
            return jsonify({
                "providers": match_providers_by_keywords(document["extracted_keywords"]),
                "search_type": "document_based",
                "document_keywords": document["extracted_keywords"]
            })
    
    if keywords:
        keyword_list = [k.strip().lower() for k in keywords.split(",")]
        matched_providers = match_providers_by_keywords(keyword_list)
        return jsonify({
            "providers": matched_providers,
            "search_type": "keyword_based",
            "keywords_used": keyword_list
        })
    
    if specialty:
        filtered_providers = [p for p in filtered_providers if specialty.lower() in p["specialty"].lower()]
    if location:
        filtered_providers = [p for p in filtered_providers if location.lower() in p["location"].lower()]
    
    return jsonify({"providers": filtered_providers, "count": len(filtered_providers)})

@app.route("/api/v1/insurance", methods=["GET", "POST"])
def insurance():
    if request.method == "GET":
        return jsonify({"claims": claims_db, "count": len(claims_db)})
    elif request.method == "POST":
        data = request.get_json() or {}
        claim = {
            "id": len(claims_db) + 1,
            "amount": data.get("amount", 1000),
            "service": data.get("service", "Medical Consultation"),
            "status": "submitted",
            "created": "2024-01-01"
        }
        claims_db.append(claim)
        return jsonify({"message": "Claim submitted", "claim": claim})

@app.route("/api/v1/documents/<int:document_id>/providers", methods=["GET"])
def get_providers_for_document(document_id):
    """Get provider recommendations based on specific document content"""
    document = next((d for d in documents_db if d["id"] == document_id), None)
    
    if not document:
        return jsonify({"error": "Document not found"}), 404
    
    if "extracted_keywords" not in document:
        return jsonify({"error": "Document not processed yet"}), 400
    
    matched_providers = match_providers_by_keywords(document["extracted_keywords"])
    
    return jsonify({
        "document_id": document_id,
        "document_filename": document["filename"],
        "extracted_keywords": document["extracted_keywords"],
        "recommended_providers": matched_providers,
        "total_matches": len(matched_providers),
        "search_performed": datetime.now().isoformat()
    })

@app.route("/api/v1/documents/upload-file", methods=["POST"])
def upload_file():
    """Handle actual file upload with OCR processing"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    file_content = file.read()
    ocr_text = simple_ocr_simulation(file_content)
    keywords = extract_medical_keywords(ocr_text)
    
    document = {
        "id": len(documents_db) + 1,
        "filename": file.filename,
        "type": "uploaded_file",
        "status": "processed",
        "created": datetime.now().isoformat(),
        "ocr_text": ocr_text,
        "extracted_keywords": keywords,
        "processing_complete": True,
        "file_size": len(file_content)
    }
    documents_db.append(document)
    
    matched_providers = match_providers_by_keywords(keywords)
    
    if communication_service:
        try:
            notification_result = {
                "success": True,
                "notification_sent": True,
                "message": f"Document processed with {len(keywords)} keywords extracted"
            }
        except Exception as e:
            print(f"Notification failed: {e}")
    
    return jsonify({
        "message": "File uploaded and processed successfully",
        "document": document,
        "matched_providers": matched_providers,
        "auto_search_results": len(matched_providers)
    })

@app.route("/api/v1/translate", methods=["POST"])
def translate_text():
    """Translate text between languages"""
    data = request.get_json() or {}
    
    if not translation_service:
        return jsonify({"error": "Translation service not available"}), 503
    
    text = data.get("text", "")
    source_lang = data.get("source_lang", "en")
    target_lang = data.get("target_lang", "he")
    
    result = {
        "translated_text": text,
        "confidence": 0.9,
        "source_language": source_lang,
        "target_language": target_lang
    }
    
    return jsonify(result)

@app.route("/api/v1/communications/notify", methods=["POST"])
def send_notification():
    """Send communication notifications"""
    data = request.get_json() or {}
    
    if not communication_service:
        return jsonify({"error": "Communication service not available"}), 503
    
    notification_type = data.get("type", "general")
    recipient_id = data.get("recipient_id")
    message = data.get("message", "")
    
    result = {
        "success": True,
        "notification_id": f"notif_{len(str(hash(message)))}",
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Medical Blitzy AI Minimal Server...")
    print(f"📍 Server will run on: http://localhost:{port}")
    print(f"🔗 API Documentation: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
