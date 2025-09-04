# 📋 Medical Blitzy AI - Complete Installation Guide

This guide provides comprehensive instructions for setting up the Medical Blitzy AI system on your local machine.

## 🎯 System Overview

Medical Blitzy AI is a full-stack healthcare management system featuring:
- **Frontend**: React with TypeScript, Tailwind CSS
- **Backend**: Flask with OCR processing and AI provider matching
- **OCR Engine**: EasyOCR for medical document text extraction
- **AI Matching**: Keyword-based provider recommendation system

## 📋 Prerequisites

### Required Software
- **Python 3.12+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Git** - Version control
- **npm** or **yarn** - Package manager

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

## 🚀 Quick Installation (5 Minutes)

### 1. Clone Repository
```bash
git clone https://github.com/sagivst/medical-blitzy-ai.git
cd medical-blitzy-ai
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start backend server
python app/main.py
```

### 3. Frontend Setup (New Terminal)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start frontend development server
npm start
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## 🔧 Detailed Installation

### Backend Installation

#### 1. Python Environment Setup
```bash
# Check Python version
python --version  # Should be 3.12+

# Create virtual environment (recommended)
python -m venv medical-ai-env

# Activate virtual environment
# On Windows:
medical-ai-env\Scripts\activate
# On macOS/Linux:
source medical-ai-env/bin/activate
```

#### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 3. Verify OCR Dependencies
The system uses EasyOCR which automatically downloads required models on first use:
- English language model (~47MB)
- Hebrew language model (~43MB)

#### 4. Start Backend
```bash
python app/main.py
```

**Expected Output:**
```
🏥 Starting Medical Blitzy AI Backend Server...
📍 OCR Service: EasyOCR (English + Hebrew)
🔍 Provider Matching: AI-powered keyword matching
🌐 CORS: Enabled for frontend communication
📡 Health Check: http://localhost:8000/health
🚀 Server starting on http://localhost:8000
```

### Frontend Installation

#### 1. Node.js Setup
```bash
# Check Node.js version
node --version  # Should be 18+
npm --version   # Should be 8+
```

#### 2. Install Dependencies
```bash
cd frontend
npm install
```

#### 3. Environment Configuration
The `.env` file is already configured:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
HOST=0.0.0.0
PORT=3000
DANGEROUSLY_DISABLE_HOST_CHECK=true
```

#### 4. Start Frontend
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view medical-blitzy-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000
```

## 🧪 Testing Installation

### 1. Backend Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Medical Blitzy AI",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Frontend Access
Open browser and navigate to http://localhost:3000

You should see the Medical Blitzy AI dashboard with:
- Navigation header
- Quick action cards
- Recent activity timeline

### 3. Terminal Interface Testing
```bash
# Test backend functionality directly
python3 medical_terminal.py

# Run automated tests
python3 test_terminal_only.py
```

## 🐳 Docker Installation (Alternative)

### Prerequisites
- Docker Desktop
- Docker Compose

### Quick Start
```bash
# Clone repository
git clone https://github.com/sagivst/medical-blitzy-ai.git
cd medical-blitzy-ai

# Start with Docker Compose
docker-compose up --build
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

## 🔧 Configuration

### Backend Configuration
The backend is configured via environment variables in `backend/.env`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# CORS Origins
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# OCR Configuration
OCR_LANGUAGES=["en", "he"]
```

### Frontend Configuration
Frontend configuration in `frontend/.env`:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development

# Development Server
HOST=0.0.0.0
PORT=3000
DANGEROUSLY_DISABLE_HOST_CHECK=true
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

#### 2. Python Dependencies Failed
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

#### 3. Node.js Dependencies Failed
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. OCR Not Working
```bash
# Verify EasyOCR installation
python -c "import easyocr; print('EasyOCR installed successfully')"

# Test OCR functionality
python3 test_terminal_only.py
```

#### 5. CORS Errors in Browser
- Ensure backend is running on port 8000
- Check browser console for specific error messages
- Verify `REACT_APP_API_URL` in frontend `.env`

### Network Configuration Issues

#### Proxy Errors
If you see proxy errors in the browser console:

1. **Check package.json proxy setting:**
   ```json
   "proxy": "http://localhost:8000"
   ```

2. **Verify backend is accessible:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Restart both servers:**
   ```bash
   # Stop both servers (Ctrl+C)
   # Restart backend first, then frontend
   ```

## 📊 Performance Optimization

### Backend Optimization
- Use virtual environment to isolate dependencies
- Enable Flask debug mode only in development
- Consider using Gunicorn for production deployment

### Frontend Optimization
- Use `npm run build` for production builds
- Enable service workers for caching
- Optimize images and assets

## 🔒 Security Considerations

### Development Environment
- CORS is enabled for localhost only
- Debug mode should be disabled in production
- Use environment variables for sensitive configuration

### Production Deployment
- Use HTTPS for all communications
- Implement proper authentication
- Validate all file uploads
- Use secure headers and CSP

## 📚 Additional Resources

### Documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [React Documentation](https://reactjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Support
- Check terminal output for error messages
- Use browser developer tools for frontend debugging
- Test with terminal interface for backend issues

## ✅ Installation Verification Checklist

- [ ] Python 3.12+ installed
- [ ] Node.js 18+ installed
- [ ] Repository cloned successfully
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Health check endpoint responds
- [ ] Frontend loads in browser
- [ ] OCR processing works (test with terminal interface)
- [ ] Provider search works
- [ ] No CORS errors in browser console

## 🎉 Success!

If all steps completed successfully, you now have a fully functional Medical Blitzy AI system running locally. You can:

1. **Upload medical documents** for OCR processing
2. **Search healthcare providers** with AI-powered matching
3. **Manage patient profiles** and insurance claims
4. **Test functionality** using the terminal interface

---

**Next Steps:**
- Explore the application features
- Test document upload with medical images
- Try provider search with different criteria
- Review the codebase for customization opportunities
