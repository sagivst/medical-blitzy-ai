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
