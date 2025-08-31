#!/usr/bin/env python3
"""
Test script to verify Flask imports and basic functionality
"""

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import flask
        print(f"✅ Flask {flask.__version__} imported successfully")
        
        import flask_cors
        print("✅ Flask-CORS imported successfully")
        
        import pymongo
        print(f"✅ PyMongo {pymongo.version} imported successfully")
        
        import jwt
        print("✅ PyJWT imported successfully")
        
        import requests
        print(f"✅ Requests {requests.__version__} imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_flask_app():
    """Test basic Flask app creation"""
    try:
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/test')
        def test():
            return jsonify({"status": "ok", "message": "Flask test successful"})
        
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Medical Blitzy AI minimal requirements...")
    print("=" * 50)
    
    imports_ok = test_imports()
    app_ok = test_flask_app()
    
    if imports_ok and app_ok:
        print("=" * 50)
        print("✅ ALL TESTS PASSED! Ready to run Flask server.")
    else:
        print("=" * 50)
        print("❌ Some tests failed. Check requirements installation.")
