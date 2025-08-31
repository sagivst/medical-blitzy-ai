"""
Ultra-minimal Flask server for Medical Blitzy AI - Testing Installation
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

patients_db = []
documents_db = []
providers_db = [
    {"id": 1, "name": "Dr. Sarah Cohen", "specialty": "Cardiology", "location": "Tel Aviv"},
    {"id": 2, "name": "Dr. David Levi", "specialty": "Neurology", "location": "Jerusalem"},
    {"id": 3, "name": "Dr. Rachel Ben-David", "specialty": "Pediatrics", "location": "Haifa"}
]
claims_db = []

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

if __name__ == "__main__":
    print("🚀 Starting Medical Blitzy AI Minimal Server...")
    print("📍 Server will run on: http://localhost:8000")
    print("🔗 API Documentation: http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
