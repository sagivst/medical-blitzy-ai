# 🚀 Medical Blitzy AI - Quick Start Guide

Get Medical Blitzy AI running in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/sagivst/medical-blitzy-ai.git
cd medical-blitzy-ai

# 2. Start Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python app/main.py

# 3. Start Frontend (Terminal 2) 
cd frontend
npm install
npm start

# 4. Open browser to http://localhost:3000
```

## 🎯 What You Get

- **📄 Document Upload**: Drag & drop medical documents for OCR processing
- **🤖 AI Provider Matching**: Automatic healthcare provider recommendations
- **🔍 Provider Search**: Search by specialty, location, and keywords
- **💳 Insurance Management**: Track claims and appeals
- **👤 Patient Profiles**: Comprehensive health information management

## 🧪 Test the System

### Option 1: Web Interface
1. Open http://localhost:3000
2. Navigate to "Documents" page
3. Upload a medical document image
4. View OCR results and provider recommendations

### Option 2: Terminal Interface (No Frontend Required)
```bash
python3 medical_terminal.py
```

### Option 3: Automated Testing
```bash
python3 test_terminal_only.py
```

## 🔧 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Need 3.12+

# Install dependencies with verbose output
pip install -r requirements.txt -v
```

### Frontend Won't Start
```bash
# Check Node.js version
node --version  # Need 18+

# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Port Conflicts
```bash
# Kill processes on ports 3000 and 8000
# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Proxy Errors
If you see "Proxy error: Could not proxy request" in the browser:

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Verify package.json proxy setting:**
   ```json
   "proxy": "http://localhost:8000"
   ```

3. **Restart both servers:**
   ```bash
   # Stop both servers (Ctrl+C)
   # Start backend first, then frontend
   ```

### OCR Not Working
```bash
# Test OCR directly
python3 test_terminal_only.py

# Check EasyOCR installation
python -c "import easyocr; print('EasyOCR OK')"
```

## 🐳 Docker Alternative

```bash
# Start with Docker Compose
docker-compose up --build

# Access points:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## ✅ Success Indicators

- ✅ Backend health check responds: `curl http://localhost:8000/health`
- ✅ Frontend loads without errors: http://localhost:3000
- ✅ No proxy errors in browser console
- ✅ Document upload works with OCR processing
- ✅ Provider search returns results
- ✅ Terminal interface works: `python3 medical_terminal.py`

## 🎉 Next Steps

Once everything is working:

1. **Upload a medical document** to test OCR
2. **Search for providers** by specialty
3. **Explore all pages** (Dashboard, Profile, Insurance)
4. **Try the terminal interface** for direct API access

## 📞 Support

If you encounter issues:
- Check the [Installation Guide](INSTALLATION_GUIDE.md) for detailed setup
- Use the terminal interface to test backend functionality
- Check browser console for frontend errors
- Verify all prerequisites are installed

---

**Estimated Setup Time**: 5-10 minutes
**System Requirements**: Python 3.12+, Node.js 18+, 4GB RAM
