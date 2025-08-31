#!/bin/bash

echo "🏥 Setting up Medical Blitzy AI Development Environment..."

sudo apt-get update

echo "📦 Installing system dependencies..."
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-heb \
    tesseract-ocr-ara \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    wget \
    gnupg

echo "🗄️ Installing MongoDB..."
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

echo "🔴 Installing Redis..."
sudo apt-get install -y redis-server

sudo mkdir -p /data/db
sudo chown -R vscode:vscode /data/db

echo "🐍 Setting up Python environment..."
cd /workspaces/medical-blitzy-ai/backend

python3 -m pip install --upgrade pip

echo "📦 Installing Python dependencies..."
pip install \
    flask==3.0.0 \
    flask-cors==4.0.0 \
    pymongo==4.6.0 \
    pyjwt==2.8.0 \
    bcrypt==4.1.2 \
    requests==2.31.0 \
    python-multipart==0.0.6 \
    openai==1.3.0 \
    easyocr==1.7.0 \
    pillow==10.1.0 \
    pytesseract==0.3.10 \
    scikit-learn==1.3.2 \
    pandas==2.1.4 \
    numpy==1.24.4 \
    python-dotenv==1.0.0 \
    celery==5.3.4 \
    redis==5.0.1

echo "⚛️ Setting up Frontend..."
cd /workspaces/medical-blitzy-ai/frontend

npm install

echo "📝 Creating environment files..."

cat > /workspaces/medical-blitzy-ai/backend/.env << EOF
MONGODB_URL=mongodb://localhost:27017/medical_blitzy_ai
REDIS_URL=redis://localhost:6379

SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

OPENAI_API_KEY=your-openai-api-key
GOOGLE_TRANSLATE_API_KEY=your-google-translate-api-key

OCR_LANGUAGE=eng+heb
TESSERACT_CMD=/usr/bin/tesseract

DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=["*"]
EOF

cat > /workspaces/medical-blitzy-ai/frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
EOF

echo "🚀 Starting services..."

sudo systemctl start mongod
sudo systemctl enable mongod

sudo systemctl start redis-server
sudo systemctl enable redis-server

cat > /workspaces/medical-blitzy-ai/start_dev.sh << 'EOF'
#!/bin/bash

echo "🏥 Starting Medical Blitzy AI Development Environment..."

sudo systemctl start mongod
sudo systemctl start redis-server

echo "🚀 Starting Backend (Flask)..."
cd /workspaces/medical-blitzy-ai/backend
python app/main.py &
BACKEND_PID=$!

sleep 3

echo "⚛️ Starting Frontend (React)..."
cd /workspaces/medical-blitzy-ai/frontend
npm start &
FRONTEND_PID=$!

echo "✅ Services started!"
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📍 API Docs: http://localhost:8000/docs"

wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x /workspaces/medical-blitzy-ai/start_dev.sh

echo "🧪 Running initial tests..."
cd /workspaces/medical-blitzy-ai/backend
python test_ultra_minimal.py

echo "✅ Medical Blitzy AI Development Environment Setup Complete!"
echo ""
echo "🚀 To start the application:"
echo "   ./start_dev.sh"
echo ""
echo "🧪 To run tests:"
echo "   cd backend && python test_ultra_minimal.py"
echo ""
echo "📍 Access points will be:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   MongoDB: localhost:27017"
echo "   Redis: localhost:6379"
