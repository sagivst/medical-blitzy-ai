#!/usr/bin/env python3
"""
Complete workflow test for Medical Blitzy AI
Tests the end-to-end MRI document processing workflow
"""

import requests
import json
import time
import sys

def test_backend_health():
    """Test if backend is running"""
    try:
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_provider_search():
    """Test provider search with keywords"""
    try:
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.get(f"http://localhost:{port}/api/v1/providers?keywords=brain,mri,neurological", timeout=10)
        if response.status_code == 200:
            data = response.json()
            providers = data.get("providers", [])
            print(f"✅ Provider search returned {len(providers)} providers")
            if providers:
                print(f"   First provider: {providers[0].get('name')} - {providers[0].get('specialty')}")
            return True
        else:
            print(f"❌ Provider search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Provider search error: {e}")
        return False

def test_document_upload():
    """Test document upload with simulated file"""
    try:
        test_content = b"MRI Brain Scan Report - Patient shows neurological symptoms with headache"
        files = {'file': ('test_mri.txt', test_content, 'text/plain')}
        
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.post(f"http://localhost:{port}/api/v1/documents/upload-file", files=files, timeout=15)
        if response.status_code == 200:
            data = response.json()
            document = data.get("document", {})
            matched_providers = data.get("matched_providers", [])
            print(f"✅ Document upload successful")
            print(f"   OCR extracted keywords: {document.get('extracted_keywords', [])}")
            print(f"   Matched providers: {len(matched_providers)}")
            return True, document.get("id")
        else:
            print(f"❌ Document upload failed: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ Document upload error: {e}")
        return False, None

def test_document_based_provider_search(document_id):
    """Test provider search based on specific document"""
    if not document_id:
        print("⚠️  Skipping document-based search (no document ID)")
        return False
    
    try:
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.get(f"http://localhost:{port}/api/v1/documents/{document_id}/providers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            providers = data.get("recommended_providers", [])
            print(f"✅ Document-based provider search returned {len(providers)} providers")
            return True
        else:
            print(f"❌ Document-based provider search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document-based provider search error: {e}")
        return False

def test_translation_service():
    """Test translation service"""
    try:
        payload = {
            "text": "brain MRI scan",
            "source_lang": "en",
            "target_lang": "he"
        }
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.post(f"http://localhost:{port}/api/v1/translate", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Translation service working")
            print(f"   Translated: '{payload['text']}' -> '{data.get('translated_text')}'")
            return True
        else:
            print(f"❌ Translation service failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Translation service error: {e}")
        return False

def test_communication_service():
    """Test communication service"""
    try:
        payload = {
            "type": "provider_match",
            "recipient_id": "test_patient",
            "message": "Test notification"
        }
        import os
        port = os.environ.get("PORT", "8001")
        response = requests.post(f"http://localhost:{port}/api/v1/communications/notify", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Communication service working")
            print(f"   Notification ID: {data.get('notification_id')}")
            return True
        else:
            print(f"❌ Communication service failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Communication service error: {e}")
        return False

def main():
    """Run complete workflow test"""
    print("🏥 Medical Blitzy AI - Complete Workflow Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    if test_backend_health():
        tests_passed += 1
    
    if test_provider_search():
        tests_passed += 1
    
    upload_success, document_id = test_document_upload()
    if upload_success:
        tests_passed += 1
    
    if test_document_based_provider_search(document_id):
        tests_passed += 1
    
    if test_translation_service():
        tests_passed += 1
    
    if test_communication_service():
        tests_passed += 1
    
    print("=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Medical Blitzy AI is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
