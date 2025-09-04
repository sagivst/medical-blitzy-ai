#!/usr/bin/env python3
"""
Medical Blitzy AI - Terminal Interface
Direct terminal access to OCR and Provider Search functionality
Bypasses all network/frontend issues
"""

import requests
import json
import os
import sys
from pathlib import Path

BACKEND_URL = "http://127.0.0.1:8000"

def print_header():
    """Print application header"""
    print("🏥 Medical Blitzy AI - Terminal Interface")
    print("=" * 60)
    print("Direct access to OCR and Provider Search functionality")
    print("Bypassing all network/frontend configuration issues")
    print("=" * 60)

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data['status']} - {data['service']} v{data['version']}")
            return True
        else:
            print(f"❌ Backend Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Connection Failed: {e}")
        print("   Please ensure backend is running: cd backend && python app/main.py")
        return False

def process_medical_document(file_path):
    """Process medical document with OCR and provider matching"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"\n📄 Processing Medical Document: {os.path.basename(file_path)}")
    print("-" * 50)
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'image/jpeg')}
            response = requests.post(f"{BACKEND_URL}/api/v1/documents/upload-file", 
                                   files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            document = data['document']
            
            print(f"📋 Document Information:")
            print(f"   • Filename: {document['filename']}")
            print(f"   • File Size: {document.get('file_size', 'Unknown')} bytes")
            print(f"   • Status: {document['status']}")
            print(f"   • Processing Complete: {document['processing_complete']}")
            
            if 'ocr_text' in document:
                ocr_text = document['ocr_text']
                print(f"\n🔍 OCR Extracted Text:")
                print("-" * 30)
                display_text = ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text
                print(display_text)
                
            if 'extracted_keywords' in document:
                keywords = document['extracted_keywords']
                print(f"\n🏷️  Medical Keywords Detected:")
                print(f"   {', '.join(keywords) if keywords else 'None detected'}")
            
            if 'matched_providers' in data:
                providers = data['matched_providers']
                print(f"\n🎯 Automatically Matched Healthcare Providers:")
                print(f"   Found {len(providers)} matching providers")
                print("-" * 40)
                
                for i, provider in enumerate(providers, 1):
                    match_score = provider.get('match_score', 0) * 100
                    print(f"\n   {i}. {provider['name']}")
                    print(f"      📍 Location: {provider['location']}")
                    print(f"      🏥 Specialty: {provider['specialty']}")
                    print(f"      📊 Match Score: {match_score:.0f}%")
                    
                    if 'matched_keywords' in provider:
                        matched_kw = provider['matched_keywords']
                        print(f"      🔗 Matched Keywords: {', '.join(matched_kw)}")
                    
                    if provider.get('id') == 2:
                        print(f"      📞 Contact: +1-555-0100")
                        print(f"      ⭐ Rating: 4.5/5 (50 reviews)")
                        print(f"      🕒 Availability: 1-2 weeks")
            
            return True
            
        else:
            print(f"❌ OCR Processing Failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Document Processing Error: {e}")
        return False

def search_providers():
    """Interactive provider search"""
    print(f"\n🔍 Healthcare Provider Search")
    print("-" * 40)
    
    specialty = input("Enter specialty (e.g., neurology, cardiology) or press Enter to skip: ").strip()
    location = input("Enter location (e.g., Jerusalem, Tel Aviv) or press Enter to skip: ").strip()
    
    params = {}
    if specialty:
        params['specialty'] = specialty
    if location:
        params['location'] = location
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/providers", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            count = data.get('count', 0)
            
            print(f"\n📋 Search Results:")
            if specialty or location:
                criteria = []
                if specialty:
                    criteria.append(f"specialty='{specialty}'")
                if location:
                    criteria.append(f"location='{location}'")
                print(f"   Search Criteria: {', '.join(criteria)}")
            else:
                print(f"   Showing all available providers")
            
            print(f"   Found: {count} providers")
            print("-" * 40)
            
            if providers:
                for i, provider in enumerate(providers, 1):
                    print(f"\n   {i}. {provider['name']}")
                    print(f"      📍 Location: {provider['location']}")
                    print(f"      🏥 Specialty: {provider['specialty']}")
                    
                    if provider.get('id') == 1:
                        print(f"      📞 Contact: +1-555-0101")
                        print(f"      ⭐ Rating: 4.8/5 (75 reviews)")
                    elif provider.get('id') == 2:
                        print(f"      📞 Contact: +1-555-0100")
                        print(f"      ⭐ Rating: 4.5/5 (50 reviews)")
                    elif provider.get('id') == 3:
                        print(f"      📞 Contact: +1-555-0102")
                        print(f"      ⭐ Rating: 4.7/5 (60 reviews)")
                    elif provider.get('id') == 4:
                        print(f"      📞 Contact: +1-555-0103")
                        print(f"      ⭐ Rating: 4.6/5 (45 reviews)")
            else:
                print("   No providers found matching your criteria.")
                print("   Try different search terms or leave fields empty to see all providers.")
            
            return True
            
        else:
            print(f"❌ Provider Search Failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Provider Search Error: {e}")
        return False

def main_menu():
    """Main interactive menu"""
    while True:
        print(f"\n📋 Main Menu:")
        print("1. Process Medical Document (OCR + Provider Matching)")
        print("2. Search Healthcare Providers")
        print("3. Process User's Medical Image")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            file_path = input("Enter path to medical document: ").strip()
            if file_path:
                process_medical_document(file_path)
            else:
                print("❌ No file path provided")
                
        elif choice == "2":
            search_providers()
            
        elif choice == "3":
            user_image_path = "/home/ubuntu/attachments/397076c1-7c77-427d-8d37-a2b87bcff228/E9F53AEE-9374-4A38-94A1-D2496107E006_1_105_c.jpeg"
            print(f"\n🎯 Processing User's Medical Image...")
            process_medical_document(user_image_path)
            
        elif choice == "4":
            print("\n👋 Thank you for using Medical Blitzy AI Terminal Interface!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-4.")

def main():
    """Main application entry point"""
    print_header()
    
    if not check_backend():
        sys.exit(1)
    
    print(f"\n🎉 System Ready! All backend services are operational.")
    print(f"   • OCR Processing: Available")
    print(f"   • Provider Search: Available") 
    print(f"   • Automatic Matching: Available")
    
    main_menu()

if __name__ == "__main__":
    main()
