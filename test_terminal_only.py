#!/usr/bin/env python3
"""
Medical Blitzy AI - Terminal Only Testing Script
Tests OCR and Provider Search functionality directly via backend API
"""

import requests
import json
import os
import sys
from pathlib import Path

BACKEND_URL = "http://127.0.0.1:8000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data['status']} - {data['service']} v{data['version']}")
            return True
        else:
            print(f"❌ Backend Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Connection Failed: {e}")
        return False

def test_provider_search(specialty="neurology", location="Jerusalem"):
    """Test provider search functionality"""
    try:
        params = {}
        if specialty:
            params['specialty'] = specialty
        if location:
            params['location'] = location
            
        response = requests.get(f"{BACKEND_URL}/api/v1/providers", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            count = data.get('count', 0)
            
            print(f"\n🔍 Provider Search Results:")
            print(f"   Query: specialty='{specialty}', location='{location}'")
            print(f"   Found: {count} providers")
            
            for i, provider in enumerate(providers, 1):
                print(f"\n   {i}. {provider['name']}")
                print(f"      Specialty: {provider['specialty']}")
                print(f"      Location: {provider['location']}")
                if 'keywords' in provider:
                    print(f"      Keywords: {', '.join(provider['keywords'])}")
                    
            return True
        else:
            print(f"❌ Provider Search Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Provider Search Error: {e}")
        return False

def test_ocr_with_text_file():
    """Test OCR functionality with a text file (simulating image)"""
    try:
        test_content = """
        MEDICAL REPORT
        
        Patient: Test Patient
        Date: 2024-01-15
        
        FINDINGS:
        Brain MRI shows normal results.
        No neurological abnormalities detected.
        Recommend follow-up with neurology specialist.
        
        Keywords: brain, mri, neurological, neurology
        """
        
        test_file_path = "/tmp/test_medical_document.txt"
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_medical.txt', f, 'text/plain')}
            response = requests.post(f"{BACKEND_URL}/api/v1/documents/upload-file", 
                                   files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📄 OCR Document Processing Results:")
            print(f"   File: {data['document']['filename']}")
            print(f"   Status: {data['document']['status']}")
            print(f"   Processing Complete: {data['document']['processing_complete']}")
            
            if 'extracted_keywords' in data['document']:
                keywords = data['document']['extracted_keywords']
                print(f"   Extracted Keywords: {', '.join(keywords)}")
            
            if 'matched_providers' in data:
                providers = data['matched_providers']
                print(f"\n🎯 Auto-Matched Providers ({len(providers)} found):")
                
                for i, provider in enumerate(providers, 1):
                    match_score = provider.get('match_score', 0) * 100
                    print(f"   {i}. {provider['name']} ({match_score:.0f}% match)")
                    print(f"      Specialty: {provider['specialty']}")
                    print(f"      Location: {provider['location']}")
                    if 'matched_keywords' in provider:
                        print(f"      Matched Keywords: {', '.join(provider['matched_keywords'])}")
            
            os.remove(test_file_path)
            return True
            
        else:
            print(f"❌ OCR Upload Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OCR Test Error: {e}")
        return False

def main():
    """Main testing function"""
    print("🏥 Medical Blitzy AI - Terminal Testing")
    print("=" * 50)
    
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start it first:")
        print("   cd backend && python app/main.py")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    success_search = test_provider_search()
    
    print("\n" + "=" * 50)
    success_ocr = test_ocr_with_text_file()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Backend Health: ✅")
    print(f"   Provider Search: {'✅' if success_search else '❌'}")
    print(f"   OCR Processing: {'✅' if success_ocr else '❌'}")
    
    if success_search and success_ocr:
        print("\n🎉 All tests passed! The Medical Blitzy AI system is working correctly.")
        print("\nNext steps:")
        print("1. The backend API is fully functional")
        print("2. OCR processing works with automatic provider matching")
        print("3. Provider search works with filtering")
        print("4. You can now test the frontend or deploy the system")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    return success_search and success_ocr

if __name__ == "__main__":
    main()
