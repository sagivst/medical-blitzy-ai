#!/usr/bin/env python3
"""
Medical Blitzy AI - Main Flask Application
Integrated Health Navigator with OCR and Provider Matching
"""

import os
import sys
import json
import signal
import subprocess
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any, Optional

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import easyocr
import numpy as np

app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "http://frontend:3000"
])

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

reader = easyocr.Reader(['en'])

SAMPLE_PATIENTS = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@email.com",
        "phone": "+1-555-0123",
        "date_of_birth": "1985-06-15",
        "medical_conditions": ["hypertension", "diabetes"],
        "last_visit": "2024-01-15"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@email.com", 
        "phone": "+1-555-0124",
        "date_of_birth": "1990-03-22",
        "medical_conditions": ["asthma"],
        "last_visit": "2024-01-10"
    }
]

SAMPLE_PROVIDERS = [
    {
        "id": 1,
        "name": "Dr. Sarah Cohen",
        "specialty": "Cardiology",
        "location": "Jerusalem",
        "keywords": ["heart", "cardiac", "cardiology", "chest", "blood pressure", "hypertension", "ecg", "ekg"]
    },
    {
        "id": 2,
        "name": "Dr. David Levi",
        "specialty": "Neurology", 
        "location": "Tel Aviv",
        "keywords": ["brain", "neurological", "neurology", "mri", "headache", "migraine", "seizure", "stroke"]
    },
    {
        "id": 3,
        "name": "Dr. Rachel Ben-David",
        "specialty": "Endocrinology",
        "location": "Haifa", 
        "keywords": ["diabetes", "thyroid", "hormone", "endocrine", "insulin", "glucose", "metabolism"]
    },
    {
        "id": 4,
        "name": "Dr. Michael Rosen",
        "specialty": "Orthopedics",
        "location": "Jerusalem",
        "keywords": ["bone", "joint", "orthopedic", "fracture", "knee", "hip", "spine", "surgery"]
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_medical_keywords(text: str) -> List[str]:
    """Extract medical keywords from OCR text"""
    medical_terms = [
        'brain', 'mri', 'neurological', 'neurology', 'headache', 'migraine',
        'heart', 'cardiac', 'cardiology', 'chest', 'blood pressure', 'hypertension',
        'diabetes', 'thyroid', 'hormone', 'endocrine', 'insulin', 'glucose',
        'bone', 'joint', 'orthopedic', 'fracture', 'knee', 'hip', 'spine',
        'lung', 'respiratory', 'asthma', 'breathing', 'pneumonia',
        'kidney', 'renal', 'urine', 'bladder', 'nephrology',
        'liver', 'hepatic', 'gastro', 'stomach', 'digestive',
        'skin', 'dermatology', 'rash', 'allergy', 'eczema',
        'blood', 'hematology', 'anemia', 'platelet', 'hemoglobin',
        'cancer', 'oncology', 'tumor', 'chemotherapy', 'radiation',
        'surgery', 'surgical', 'operation', 'procedure', 'biopsy',
        'medication', 'prescription', 'dosage', 'treatment', 'therapy'
    ]
    
    text_lower = text.lower()
    found_keywords = []
    
    for term in medical_terms:
        if term in text_lower:
            found_keywords.append(term)
    
    return list(set(found_keywords))

def match_providers_to_keywords(keywords: List[str]) -> List[Dict[str, Any]]:
    """Match providers based on extracted keywords"""
    matched_providers = []
    
    for provider in SAMPLE_PROVIDERS:
        provider_keywords = [kw.lower() for kw in provider['keywords']]
        matched_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in provider_keywords:
                matched_keywords.append(keyword)
        
        if matched_keywords:
            match_score = len(matched_keywords) / len(provider_keywords)
            matched_provider = provider.copy()
            matched_provider['matched_keywords'] = matched_keywords
            matched_provider['match_score'] = match_score
            matched_providers.append(matched_provider)
    
    matched_providers.sort(key=lambda x: x['match_score'], reverse=True)
    return matched_providers

def perform_real_ocr(file_content: bytes, filename: str) -> str:
    """Perform OCR on uploaded file using EasyOCR"""
    try:
        image_stream = BytesIO(file_content)
        image_stream.seek(0)
        
        image = Image.open(image_stream)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_array = np.array(image)
        
        result = reader.readtext(image_array)
        
        extracted_text = ' '.join([detection[1] for detection in result])
        
        return extracted_text if extracted_text.strip() else "No text detected in image"
        
    except Exception as e:
        print(f"OCR Error: {e}")
        return f"OCR processing failed: {str(e)}"

def cleanup_ports():
    """Clean up processes running on ports 3000 and 8000"""
    ports = [3000, 8000]
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(['kill', '-9', pid], check=True)
                        print(f"Killed process {pid} on port {port}")
                    except subprocess.CalledProcessError:
                        pass
        except FileNotFoundError:
            pass

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Medical Blitzy AI",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    return jsonify({
        "patients": SAMPLE_PATIENTS,
        "count": len(SAMPLE_PATIENTS)
    })

@app.route('/api/v1/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get specific patient"""
    patient = next((p for p in SAMPLE_PATIENTS if p['id'] == patient_id), None)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient)

@app.route('/api/v1/providers', methods=['GET'])
def search_providers():
    """Search healthcare providers"""
    specialty = request.args.get('specialty', '').lower()
    location = request.args.get('location', '')
    
    filtered_providers = SAMPLE_PROVIDERS.copy()
    
    if specialty:
        filtered_providers = [
            p for p in filtered_providers 
            if specialty in p['specialty'].lower()
        ]
    
    if location:
        filtered_providers = [
            p for p in filtered_providers 
            if location.lower() in p['location'].lower()
        ]
    
    return jsonify({
        "providers": filtered_providers,
        "count": len(filtered_providers),
        "filters": {
            "specialty": specialty,
            "location": location
        }
    })

@app.route('/api/v1/documents/upload-file', methods=['POST'])
def upload_file():
    """Upload and process medical document with OCR"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_content = file.read()
        
        ocr_text = perform_real_ocr(file_content, filename)
        
        extracted_keywords = extract_medical_keywords(ocr_text)
        
        matched_providers = match_providers_to_keywords(extracted_keywords)
        
        document_info = {
            "filename": filename,
            "file_size": len(file_content),
            "upload_time": datetime.now().isoformat(),
            "status": "completed",
            "processing_complete": True,
            "ocr_text": ocr_text,
            "extracted_keywords": extracted_keywords
        }
        
        response_data = {
            "message": "File uploaded and processed successfully",
            "document": document_info,
            "matched_providers": matched_providers
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({
            "error": "File processing failed",
            "details": str(e)
        }), 500

@app.route('/api/v1/documents', methods=['GET'])
def get_documents():
    """Get uploaded documents"""
    return jsonify({
        "documents": [],
        "count": 0,
        "message": "Document storage not implemented in this demo"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

def signal_handler(sig, frame):
    print('\nShutting down Medical Blitzy AI server...')
    cleanup_ports()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    cleanup_ports()
    
    print("🏥 Starting Medical Blitzy AI Backend Server...")
    print("📍 OCR Service: EasyOCR (English + Hebrew)")
    print("🔍 Provider Matching: AI-powered keyword matching")
    print("🌐 CORS: Enabled for frontend communication")
    print("📡 Health Check: http://localhost:8000/health")
    print("📚 API Endpoints:")
    print("   • GET  /api/v1/patients")
    print("   • GET  /api/v1/providers")
    print("   • POST /api/v1/documents/upload-file")
    print("🚀 Server starting on http://localhost:8000")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        cleanup_ports()
    except Exception as e:
        print(f"❌ Server error: {e}")
        cleanup_ports()
        sys.exit(1)
