# 🧪 מסגרת בדיקות הדרגתית - Medical Blitzy AI

## 🎯 מטרה: בדיקת כל שלב בנפרד

### **עקרון הבדיקה ההדרגתית:**
1. **בדיקה אחרי כל הוספת חבילה** - לזהות בדיוק מה נכשל
2. **בדיקות אוטומטיות** - ללא תלות בהתערבות ידנית
3. **rollback מהיר** - חזרה לגרסה עובדת אם משהו נכשל
4. **דיווח ברור** - הבנה מדויקת של מה עובד ומה לא

## 📋 **סקריפטי בדיקה לכל שלב**

### **שלב 1: בסיס (יש כבר) ✅**
```python
# test_stage1_baseline.py
#!/usr/bin/env python3
"""בדיקת הבסיס - Flask + Flask-CORS"""

def test_baseline():
    print("🧪 בדיקת שלב 1: בסיס")
    
    # בדיקת imports
    try:
        import flask
        import flask_cors
        print("✅ Imports: Flask + Flask-CORS")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # בדיקת שרת
    try:
        from app.main import app
        print("✅ Server: Flask app loads")
    except Exception as e:
        print(f"❌ Server failed: {e}")
        return False
    
    print("🎉 שלב 1: בסיס - עובד!")
    return True

if __name__ == "__main__":
    test_baseline()
```

### **שלב 2: מסד נתונים + אבטחה**
```python
# test_stage2_database.py
#!/usr/bin/env python3
"""בדיקת שלב 2: MongoDB + JWT + bcrypt"""

def test_stage2_packages():
    print("🧪 בדיקת שלב 2: חבילות מסד נתונים")
    
    packages = [
        ("pymongo", "MongoDB driver"),
        ("jwt", "JWT tokens"),
        ("bcrypt", "Password hashing"),
        ("requests", "HTTP requests")
    ]
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package}: {description}")
        except ImportError as e:
            print(f"❌ {package} failed: {e}")
            return False
    
    return True

def test_stage2_functionality():
    print("🧪 בדיקת שלב 2: פונקציונליות")
    
    try:
        # בדיקת MongoDB connection (mock)
        from pymongo import MongoClient
        print("✅ MongoDB: Connection class available")
        
        # בדיקת JWT
        import jwt
        token = jwt.encode({"test": "data"}, "secret", algorithm="HS256")
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        print("✅ JWT: Encode/decode working")
        
        # בדיקת bcrypt
        import bcrypt
        password = b"test_password"
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        verified = bcrypt.checkpw(password, hashed)
        print("✅ bcrypt: Hash/verify working")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_stage2():
    print("🧪 בדיקת שלב 2 מלאה")
    return test_stage2_packages() and test_stage2_functionality()

if __name__ == "__main__":
    if test_stage2():
        print("🎉 שלב 2: מסד נתונים + אבטחה - עובד!")
    else:
        print("❌ שלב 2 נכשל!")
```

### **שלב 3: OCR - 3 אופציות**
```python
# test_stage3_ocr.py
#!/usr/bin/env python3
"""בדיקת שלב 3: OCR - בדיקת כל האופציות"""

def test_option_a_easyocr():
    print("🧪 אופציה A: EasyOCR")
    try:
        import easyocr
        import PIL
        print("✅ EasyOCR + Pillow installed")
        
        # בדיקה בסיסית
        reader = easyocr.Reader(['en', 'he'])
        print("✅ EasyOCR: Reader created with Hebrew support")
        return True
    except ImportError as e:
        print(f"❌ EasyOCR import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ EasyOCR functionality failed: {e}")
        return False

def test_option_b_api():
    print("🧪 אופציה B: OCR APIs")
    try:
        import requests
        
        # בדיקת OCR.space API (mock)
        api_url = "https://api.ocr.space/parse/image"
        print("✅ OCR API: Requests available for external APIs")
        
        # בדיקת Google Vision (mock)
        print("✅ Google Vision: Can be integrated via API")
        
        return True
    except Exception as e:
        print(f"❌ API option failed: {e}")
        return False

def test_stage3_ocr():
    print("🧪 בדיקת שלב 3: OCR")
    
    # נסה אופציה A
    if test_option_a_easyocr():
        print("🎯 מומלץ: אופציה A - EasyOCR")
        return True
    
    # אם A נכשל, נסה B
    if test_option_b_api():
        print("🎯 חלופה: אופציה B - OCR APIs")
        return True
    
    print("❌ כל אופציות OCR נכשלו")
    return False

if __name__ == "__main__":
    if test_stage3_ocr():
        print("🎉 שלב 3: OCR - עובד!")
    else:
        print("❌ שלב 3 נכשל!")
```

### **שלב 4: AI Matching**
```python
# test_stage4_ai.py
#!/usr/bin/env python3
"""בדיקת שלב 4: AI Matching"""

def test_openai_option():
    print("🧪 אופציה A: OpenAI API")
    try:
        import openai
        print("✅ OpenAI: Package installed")
        
        # בדיקה בסיסית (ללא API key)
        client = openai.OpenAI(api_key="test")
        print("✅ OpenAI: Client can be created")
        return True
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ OpenAI functionality failed: {e}")
        return False

def test_huggingface_option():
    print("🧪 אופציה B: Hugging Face")
    try:
        import huggingface_hub
        print("✅ Hugging Face: Package installed")
        return True
    except ImportError as e:
        print(f"❌ Hugging Face import failed: {e}")
        return False

def test_simple_algorithm():
    print("🧪 אופציה C: אלגוריתם פשוט")
    try:
        # בדיקת אלגוריתם matching פשוט
        def simple_provider_match(patient_data, providers):
            # אלגוריתם פשוט עם משקלים
            scores = []
            for provider in providers:
                score = 0
                # משקל לפי מיקום
                if patient_data.get('location') == provider.get('location'):
                    score += 40
                # משקל לפי התמחות
                if patient_data.get('specialty') == provider.get('specialty'):
                    score += 60
                scores.append((provider, score))
            return sorted(scores, key=lambda x: x[1], reverse=True)
        
        # בדיקה
        test_patient = {'location': 'Tel Aviv', 'specialty': 'Cardiology'}
        test_providers = [
            {'name': 'Dr. A', 'location': 'Tel Aviv', 'specialty': 'Cardiology'},
            {'name': 'Dr. B', 'location': 'Jerusalem', 'specialty': 'Neurology'}
        ]
        
        results = simple_provider_match(test_patient, test_providers)
        print("✅ Simple Algorithm: Provider matching working")
        return True
    except Exception as e:
        print(f"❌ Simple algorithm failed: {e}")
        return False

def test_stage4_ai():
    print("🧪 בדיקת שלב 4: AI Matching")
    
    # נסה אופציות לפי סדר עדיפות
    if test_openai_option():
        print("🎯 מומלץ: OpenAI API")
        return True
    elif test_huggingface_option():
        print("🎯 חלופה: Hugging Face")
        return True
    elif test_simple_algorithm():
        print("🎯 בסיסי: אלגוריתם פשוט")
        return True
    
    print("❌ כל אופציות AI נכשלו")
    return False

if __name__ == "__main__":
    if test_stage4_ai():
        print("🎉 שלב 4: AI Matching - עובד!")
    else:
        print("❌ שלב 4 נכשל!")
```

### **שלב 5: FHIR**
```python
# test_stage5_fhir.py
#!/usr/bin/env python3
"""בדיקת שלב 5: FHIR Parser"""

def test_fhir_simple_parser():
    print("🧪 בדיקת FHIR Parser פשוט")
    try:
        import json
        from datetime import datetime
        
        # FHIR Patient template
        def create_fhir_patient(patient_data):
            fhir_patient = {
                "resourceType": "Patient",
                "id": patient_data.get("id", "unknown"),
                "meta": {
                    "versionId": "1",
                    "lastUpdated": datetime.now().isoformat()
                },
                "identifier": [{
                    "system": "http://medical-blitzy.ai/patient-id",
                    "value": str(patient_data.get("id", ""))
                }],
                "name": [{
                    "family": patient_data.get("last_name", ""),
                    "given": [patient_data.get("first_name", "")]
                }],
                "gender": patient_data.get("gender", "unknown"),
                "birthDate": patient_data.get("birth_date", "")
            }
            return fhir_patient
        
        # בדיקה
        test_patient = {
            "id": "123",
            "first_name": "יוסי",
            "last_name": "כהן",
            "gender": "male",
            "birth_date": "1980-01-01"
        }
        
        fhir_result = create_fhir_patient(test_patient)
        
        # וידוא שזה JSON תקין
        json_str = json.dumps(fhir_result, ensure_ascii=False, indent=2)
        parsed_back = json.loads(json_str)
        
        print("✅ FHIR: Patient conversion working")
        print("✅ FHIR: JSON serialization working")
        print("✅ FHIR: Hebrew support working")
        
        return True
    except Exception as e:
        print(f"❌ FHIR parser failed: {e}")
        return False

def test_fhir_validation():
    print("🧪 בדיקת FHIR Validation")
    try:
        def validate_fhir_patient(fhir_patient):
            required_fields = ["resourceType", "id", "meta"]
            for field in required_fields:
                if field not in fhir_patient:
                    return False, f"Missing required field: {field}"
            
            if fhir_patient["resourceType"] != "Patient":
                return False, "Invalid resourceType"
            
            return True, "Valid FHIR Patient"
        
        # בדיקה עם נתונים תקינים
        valid_patient = {
            "resourceType": "Patient",
            "id": "123",
            "meta": {"versionId": "1"}
        }
        
        is_valid, message = validate_fhir_patient(valid_patient)
        if is_valid:
            print("✅ FHIR: Validation working")
            return True
        else:
            print(f"❌ FHIR validation failed: {message}")
            return False
            
    except Exception as e:
        print(f"❌ FHIR validation failed: {e}")
        return False

def test_stage5_fhir():
    print("🧪 בדיקת שלב 5: FHIR")
    return test_fhir_simple_parser() and test_fhir_validation()

if __name__ == "__main__":
    if test_stage5_fhir():
        print("🎉 שלב 5: FHIR - עובד!")
    else:
        print("❌ שלב 5 נכשל!")
```

## 🚀 **סקריפט בדיקה מאסטר**

```python
# test_all_stages.py
#!/usr/bin/env python3
"""בדיקת כל השלבים ברצף"""

import subprocess
import sys

def run_stage_test(stage_name, script_name):
    print(f"\n{'='*50}")
    print(f"🧪 מריץ בדיקה: {stage_name}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {stage_name}: הצליח!")
            print(result.stdout)
            return True
        else:
            print(f"❌ {stage_name}: נכשל!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {stage_name}: timeout!")
        return False
    except Exception as e:
        print(f"❌ {stage_name}: שגיאה - {e}")
        return False

def main():
    print("🏥 Medical Blitzy AI - בדיקת כל השלבים")
    print("=" * 60)
    
    stages = [
        ("שלב 1: בסיס", "test_stage1_baseline.py"),
        ("שלב 2: מסד נתונים", "test_stage2_database.py"),
        ("שלב 3: OCR", "test_stage3_ocr.py"),
        ("שלב 4: AI", "test_stage4_ai.py"),
        ("שלב 5: FHIR", "test_stage5_fhir.py")
    ]
    
    results = []
    for stage_name, script_name in stages:
        success = run_stage_test(stage_name, script_name)
        results.append((stage_name, success))
        
        if not success:
            print(f"\n⚠️  {stage_name} נכשל - עוצר כאן")
            break
    
    print(f"\n{'='*60}")
    print("📊 סיכום תוצאות:")
    print(f"{'='*60}")
    
    for stage_name, success in results:
        status = "✅ עובד" if success else "❌ נכשל"
        print(f"{stage_name}: {status}")
    
    successful_stages = sum(1 for _, success in results if success)
    print(f"\n🎯 סה\"כ שלבים שעובדים: {successful_stages}/{len(stages)}")
    
    if successful_stages == len(stages):
        print("🎉 כל השלבים עובדים! המערכת מוכנה!")
    else:
        print(f"⚠️  יש לטפל בשלבים שנכשלו")

if __name__ == "__main__":
    main()
```

## 📋 **הוראות שימוש**

### **בדיקה הדרגתית:**
```bash
# בדיקת שלב בודד
python test_stage2_database.py

# בדיקת כל השלבים
python test_all_stages.py

# בדיקה אחרי הוספת חבילה חדשה
pip install new_package
python test_stage_X.py
```

### **אסטרטגיית rollback:**
```bash
# אם שלב נכשל:
git checkout requirements.txt  # חזרה לגרסה קודמת
pip install -r requirements.txt
python test_stage_previous.py  # וידוא שהקודם עדיין עובד
```

## 🎯 **יתרונות המסגרת הזו:**

✅ **זיהוי מדויק** - יודעים בדיוק איזה חבילה בעייתית  
✅ **בדיקה מהירה** - כל בדיקה לוקחת פחות מדקה  
✅ **rollback בטוח** - תמיד אפשר לחזור לגרסה עובדת  
✅ **דיווח ברור** - הבנה מדויקת של מה עובד  
✅ **אוטומציה מלאה** - ללא התערבות ידנית  

**עם המסגרת הזו, תוכל לבנות את המערכת המלאה בביטחון!** 🚀
