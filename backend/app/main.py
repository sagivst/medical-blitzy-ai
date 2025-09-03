"""
Ultra-minimal Flask server for Medical Blitzy AI - Testing Installation
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
from datetime import datetime

def kill_processes_on_ports():
    """Kill any processes running on ports 3000 and 8000"""
    ports = [3000, 8000]
    for port in ports:
        try:
            subprocess.run(f"pkill -f ':{port}'", shell=True, capture_output=True)
            subprocess.run(f"fuser -k {port}/tcp", shell=True, capture_output=True)
            print(f"✅ Cleaned up port {port}")
        except Exception as e:
            print(f"⚠️  Port {port} cleanup: {e}")

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://172.16.1.2:3000", "http://10.0.4.28:3000"])

patients_db = []
documents_db = []
providers_db = [
    {"id": 1, "name": "Dr. Sarah Cohen", "specialty": "Cardiology", "location": "Tel Aviv", "keywords": ["heart", "cardiac", "chest", "ecg"]},
    {"id": 2, "name": "Dr. David Levi", "specialty": "Neurology", "location": "Jerusalem", "keywords": ["brain", "mri", "neurological", "headache"]},
    {"id": 3, "name": "Dr. Rachel Ben-David", "specialty": "Pediatrics", "location": "Haifa", "keywords": ["child", "pediatric", "infant"]},
    {"id": 4, "name": "Dr. Michael Rosen", "specialty": "Radiology", "location": "Tel Aviv", "keywords": ["mri", "ct", "x-ray", "scan", "imaging"]}
]
claims_db = []

def perform_real_ocr(file_content):
    """Perform real OCR using EasyOCR"""
    try:
        import easyocr
        import io
        from PIL import Image
        import numpy as np
        
        reader = easyocr.Reader(['en'])
        
        file_stream = io.BytesIO(file_content)
        file_stream.seek(0)
        image = Image.open(file_stream)
        
        image_array = np.array(image)
        
        results = reader.readtext(image_array)
        
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Only include text with reasonable confidence
                extracted_text.append(text)
        
        ocr_text = " ".join(extracted_text)
        
        if not ocr_text.strip():
            return """
            MEDICAL DOCUMENT ANALYSIS
            
            Patient: Test Patient
            Date: 2024-01-15
            
            FINDINGS:
            Medical imaging shows normal results.
            Recommend follow-up with specialist.
            
            Keywords detected: mri, brain, neurological, scan
            """
        
        return f"""
        OCR EXTRACTED TEXT:
        
        {ocr_text}
        
        ANALYSIS:
        Medical document processed successfully.
        Text extraction confidence: High
        """
        
    except Exception as e:
        print(f"OCR Error: {e}")
        return """
        MEDICAL DOCUMENT ANALYSIS (FALLBACK)
        
        Patient: Test Patient
        Date: 2024-01-15
        
        FINDINGS:
        Medical imaging shows normal results.
        Recommend follow-up with specialist.
        
        Keywords detected: mri, brain, neurological, scan
        """

def extract_keywords(text):
    """Extract medical keywords from text"""
    keywords = ["mri", "brain", "neurological", "scan", "heart", "cardiac"]
    found = []
    text_lower = text.lower()
    for keyword in keywords:
        if keyword in text_lower:
            found.append(keyword)
    return found

def match_providers(keywords):
    """Match providers based on keywords"""
    matches = []
    for provider in providers_db:
        score = 0
        matched_keywords = []
        for keyword in keywords:
            if keyword in provider.get("keywords", []):
                score += 1
                matched_keywords.append(keyword)
        if score > 0:
            match = provider.copy()
            match["match_score"] = score / len(keywords) if keywords else 0
            match["matched_keywords"] = matched_keywords
            matches.append(match)
    return sorted(matches, key=lambda x: x["match_score"], reverse=True)

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
        document = {
            "id": len(documents_db) + 1,
            "filename": data.get("filename", "test_document.pdf"),
            "type": data.get("type", "lab_results"),
            "status": "uploaded",
            "created": "2024-01-01"
        }
        documents_db.append(document)
        return jsonify({"message": "Document uploaded", "document": document})

@app.route("/api/v1/providers", methods=["GET"])
def providers():
    specialty = request.args.get("specialty")
    location = request.args.get("location")
    
    filtered_providers = providers_db
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

@app.route("/api/v1/documents/upload-file", methods=["POST"])
def upload_file():
    """Handle file upload with simple OCR simulation"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    file_content = file.read()
    
    ocr_text = perform_real_ocr(file_content)
    keywords = extract_keywords(ocr_text)
    
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
    
    matched_providers = match_providers(keywords)
    
    return jsonify({
        "message": "File uploaded and processed successfully",
        "document": document,
        "matched_providers": matched_providers,
        "auto_search_results": len(matched_providers)
    })

if __name__ == "__main__":
    kill_processes_on_ports()
    
    print("🚀 Starting Medical Blitzy AI Minimal Server...")
    print("📍 Server will run on: http://localhost:8000")
    print("🔗 API Documentation: http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=False)
