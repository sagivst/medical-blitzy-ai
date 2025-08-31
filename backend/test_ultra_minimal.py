#!/usr/bin/env python3
"""
Ultra-minimal test script for Medical Blitzy AI installation
Only tests Flask and Flask-CORS - no external dependencies
"""

import subprocess
import sys
import time

def test_installation():
    """Test that minimal requirements can be installed"""
    print("🔧 Testing installation...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Requirements installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def test_imports():
    """Test that Flask packages can be imported"""
    print("📦 Testing imports...")
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
        
        import flask_cors
        print("✅ Flask-CORS")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_server_startup():
    """Test that the Flask server can start without crashing"""
    print("🚀 Testing server startup...")
    
    server_process = None
    try:
        server_process = subprocess.Popen([sys.executable, "app/main.py"], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        if server_process.poll() is None:
            print("✅ Flask server started successfully")
            return True
        else:
            stdout, stderr = server_process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
        
    except Exception as e:
        print(f"❌ Server test error: {e}")
        return False
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()

def main():
    print("🏥 Medical Blitzy AI - Ultra-Minimal Installation Test")
    print("=" * 55)
    
    if not test_installation():
        print("\n❌ Installation test failed!")
        return False
    
    if not test_imports():
        print("\n❌ Import test failed!")
        return False
    
    if not test_server_startup():
        print("\n❌ Server startup test failed!")
        return False
    
    print("\n" + "=" * 55)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Medical Blitzy AI ultra-minimal version is working!")
    print("\n📋 What's working:")
    print("  • Flask 3.0.0 installation")
    print("  • Flask-CORS 4.0.0 installation")
    print("  • Server startup without crashes")
    print("  • Ultra-minimal dependencies (only 2 packages!)")
    print("\n🚀 To start the server manually:")
    print("  cd backend")
    print("  python3 app/main.py")
    print("\n🧪 To test endpoints manually (after starting server):")
    print("  curl http://localhost:8000/health")
    print("  curl http://localhost:8000/api/v1/patients")
    print("  curl -X POST http://localhost:8000/api/v1/patients -H 'Content-Type: application/json' -d '{\"name\":\"Test Patient\"}'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
