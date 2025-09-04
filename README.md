# 🏥 Medical Blitzy AI - Integrated Health Navigator

A comprehensive AI-powered healthcare management system that provides OCR document processing, intelligent provider matching, and insurance claim management.

## 🚀 Features

- **📄 OCR Document Processing**: Upload medical documents and extract text using advanced OCR
- **🤖 AI Provider Matching**: Intelligent matching of medical conditions to healthcare providers
- **🔍 Provider Search**: Search and filter healthcare providers by specialty and location
- **💳 Insurance Management**: Track and manage insurance claims and appeals
- **👤 Patient Profiles**: Comprehensive patient information management
- **🌐 Multi-language Support**: Hebrew and English language support

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Heroicons** for icons
- **Axios** for API communication

### Backend
- **Flask** web framework
- **EasyOCR** for document text extraction
- **PIL (Pillow)** for image processing
- **Flask-CORS** for cross-origin requests
- **Python 3.12** runtime

## 📦 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sagivst/medical-blitzy-ai.git
   cd medical-blitzy-ai
   ```

2. **Start Backend (Terminal 1)**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app/main.py
   ```

3. **Start Frontend (Terminal 2)**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🧪 Testing

### Terminal Interface (No Frontend Required)
```bash
python3 medical_terminal.py
```

### Automated Testing
```bash
python3 test_terminal_only.py
```

## 🐳 Docker Setup

```bash
docker-compose up --build
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION_GUIDE.md) - Detailed setup instructions
- [Quick Start Guide](docs/QUICK_START_GUIDE.md) - 5-minute setup
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## 🏗️ Project Structure

```
medical-blitzy-ai/
├── frontend/              # React TypeScript application
│   ├── src/
│   │   ├── pages/        # Main application pages
│   │   ├── components/   # Reusable components
│   │   └── App.tsx       # Main application component
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
├── backend/              # Flask API application
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── services/    # Business logic services
│   │   ├── models/      # Data models
│   │   └── main.py      # Application entry point
│   └── requirements.txt  # Backend dependencies
├── docs/                 # Documentation
├── docker-compose.yml    # Container orchestration
└── README.md            # This file
```

## 🔧 Key Components

### Frontend Pages
- **Dashboard**: Overview and quick actions
- **Document Upload**: OCR processing with drag-and-drop
- **Provider Search**: AI-powered provider matching
- **Insurance Claims**: Claim tracking and management
- **Patient Profile**: Personal health information

### Backend Services
- **OCR Service**: Medical document text extraction
- **AI Matching Service**: Provider recommendation algorithm
- **File Upload**: Secure document handling
- **Provider Search**: Healthcare provider database

## 🌟 Core Functionality

### Document Processing Workflow
1. Upload medical document (image/PDF)
2. OCR extracts text content
3. AI identifies medical keywords
4. System matches relevant healthcare providers
5. Display recommendations with match scores

### Provider Search
- Filter by specialty (cardiology, neurology, etc.)
- Filter by location (Jerusalem, Tel Aviv, etc.)
- AI-powered relevance scoring
- Contact information and ratings

## 🔒 Security & Privacy

- HIPAA-compliant data handling
- Secure file upload and processing
- No persistent storage of sensitive data
- CORS protection for API endpoints

## 🚀 Deployment

The system supports multiple deployment options:
- Local development setup
- Docker containerization
- Cloud deployment ready

## 📞 Support

For issues or questions:
- Check the [Installation Guide](docs/INSTALLATION_GUIDE.md)
- Review [Common Issues](docs/QUICK_START_GUIDE.md#troubleshooting)
- Test with terminal interface for debugging

## 📄 License

This project is part of the Medical Blitzy AI system.

---

**Link to Devin run**: https://app.devin.ai/sessions/24592c8f93e84e39b00833bed7a73ac8
**Requested by**: @sagivst
