# 🏥 Medical Blitzy AI - Integrated Health Navigator (IHN)

## 🚀 Quick Start with GitHub Codespaces (Recommended)

### Option 1: GitHub Codespaces (Zero Setup!)

1. **Fork this repository** to your GitHub account
2. **Click "Code" → "Codespaces" → "Create codespace"**
3. **Wait 2-3 minutes** for automatic setup
4. **Run the application:**
   ```bash
   ./start_dev.sh
   ```
5. **Access the application:**
   - 🌐 Frontend: Click the "Open in Browser" notification for port 3000
   - 🔗 Backend API: Click the "Open in Browser" notification for port 8000
   - 📚 API Docs: Backend URL + `/docs`

### ✅ What's Pre-Configured in Codespaces:

- ✅ **Python 3.11** (no more Python 3.13 issues!)
- ✅ **All dependencies** installed automatically
- ✅ **MongoDB & Redis** running
- ✅ **Tesseract OCR** with Hebrew support
- ✅ **VS Code** with all extensions
- ✅ **Environment variables** configured
- ✅ **Port forwarding** set up

## 🎯 System Overview

Medical Blitzy AI is a comprehensive Integrated Health Navigator (IHN) platform that provides:

### 🏥 Core Features
- **Patient Management** - Complete patient profiles and medical history
- **Document Processing** - OCR for medical documents with Hebrew support
- **AI Provider Matching** - Intelligent healthcare provider recommendations
- **Insurance Claims** - Automated claims processing and tracking
- **Multilingual Support** - Hebrew, Arabic, and English interfaces

### 🔧 Technical Stack
- **Backend**: Flask with Python 3.11
- **Frontend**: React with TypeScript and Tailwind CSS
- **Database**: MongoDB for documents
- **Caching**: Redis for session management
- **AI/ML**: OpenAI API, EasyOCR, scikit-learn
- **Security**: JWT authentication, bcrypt encryption

## 📋 Local Development (Alternative)

If you prefer local development:

### Prerequisites
- Python 3.11+ (avoid Python 3.13)
- Node.js 18+
- MongoDB
- Redis
- Tesseract OCR

### Installation
```bash
# Clone repository
git clone https://github.com/your-username/medical-blitzy-ai
cd medical-blitzy-ai

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Start services
./start_dev.sh
```

## 🧪 Testing

### Run All Tests
```bash
# Backend tests
cd backend
python test_ultra_minimal.py

# Frontend tests
cd frontend
npm test
```

### Test Individual Components
```bash
# Test OCR functionality
python -c "import easyocr; print('OCR Ready!')"

# Test AI matching
python -c "import openai; print('AI Ready!')"
```

## 🌐 API Endpoints

### Health & Status
- `GET /health` - System health check
- `GET /` - API information

### Patient Management
- `GET /api/v1/patients` - List all patients
- `POST /api/v1/patients` - Create new patient
- `GET /api/v1/patients/{id}` - Get patient details

### Document Processing
- `POST /api/v1/documents` - Upload and process document
- `GET /api/v1/documents` - List documents

### Provider Matching
- `GET /api/v1/providers` - Search providers

### Insurance Claims
- `POST /api/v1/insurance` - Submit insurance claim
- `GET /api/v1/insurance` - List claims

## 🔐 Security & Compliance

### HIPAA Compliance
- ✅ **Data Encryption** - AES-256 encryption at rest and in transit
- ✅ **Access Controls** - Role-based access with JWT tokens
- ✅ **Audit Logging** - Complete audit trail for all operations
- ✅ **Secure Communication** - HTTPS/TLS for all API calls

## 🌍 Multilingual Support

### Supported Languages
- 🇮🇱 **Hebrew** (עברית) - Primary interface
- 🇸🇦 **Arabic** (العربية) - Full support
- 🇺🇸 **English** - International standard

### OCR Language Support
```python
# Configure OCR languages
OCR_LANGUAGES = ["eng", "heb", "ara"]
```

## 📊 Performance Metrics

### Target Performance
- **Document Upload**: < 2 seconds
- **OCR Processing**: < 30 seconds
- **Provider Matching**: < 5 seconds
- **API Response Time**: < 500ms

## 🚀 Deployment

### Production Deployment
```bash
# Using Docker
docker-compose up -d

# Using Railway
railway deploy
```

### Environment Variables
```bash
# Required for production
MONGODB_URL=mongodb://production-server:27017/medical_blitzy
REDIS_URL=redis://production-server:6379
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-openai-api-key
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- 📧 **Email**: support@medical-blitzy.ai
- 📖 **Documentation**: Complete API documentation available
- 🐛 **Issues**: GitHub Issues for bug reports

### Common Issues
- **Python 3.13 Issues**: Use GitHub Codespaces with Python 3.11
- **OCR Not Working**: Ensure Tesseract is installed with Hebrew support
- **MongoDB Connection**: Check MongoDB service is running

---

**🏥 Medical Blitzy AI - Revolutionizing Healthcare Navigation with AI** 🚀
