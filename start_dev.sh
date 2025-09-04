#!/bin/bash

echo "🏥 Starting Medical Blitzy AI Development Environment..."

if [ "$CODESPACES" = "true" ]; then
    echo "📍 Running in GitHub Codespaces"
    BACKEND_DIR="/workspaces/medical-blitzy-ai/backend"
    FRONTEND_DIR="/workspaces/medical-blitzy-ai/frontend"
else
    echo "📍 Running locally"
    BACKEND_DIR="./backend"
    FRONTEND_DIR="./frontend"
fi

check_service() {
    if pgrep -f "$1" > /dev/null; then
        echo "✅ $1 is running"
        return 0
    else
        echo "❌ $1 is not running"
        return 1
    fi
}

echo "🚀 Starting Backend (Flask)..."
cd "$BACKEND_DIR"

if [ requirements.txt -nt .requirements_installed ] || [ ! -f .requirements_installed ]; then
    echo "📦 Installing/updating Python dependencies..."
    pip install -r requirements.txt
    touch .requirements_installed
fi

python app/main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

echo "⏳ Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend is responding"
        break
    fi
    sleep 1
done

echo "⚛️ Starting Frontend (React)..."
cd "$FRONTEND_DIR"

if [ package.json -nt .packages_installed ] || [ ! -f .packages_installed ]; then
    echo "📦 Installing/updating Node.js dependencies..."
    npm install
    touch .packages_installed
fi

npm start &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo "⏳ Waiting for frontend to start..."
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null; then
        echo "✅ Frontend is responding"
        break
    fi
    sleep 1
done

echo ""
echo "🎉 Medical Blitzy AI is now running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Access Points:"
if [ "$CODESPACES" = "true" ]; then
    echo "   🌐 Frontend:     Check 'Ports' tab for port 3000"
    echo "   🔗 Backend API:  Check 'Ports' tab for port 8000"
    echo "   📚 API Docs:     Backend URL + /docs"
else
    echo "   🌐 Frontend:     http://localhost:3000"
    echo "   🔗 Backend API:  http://localhost:8000"
    echo "   📚 API Docs:     http://localhost:8000/docs"
fi
echo ""
echo "🧪 Test Commands:"
echo "   curl http://localhost:8000/health"
echo "   python3 medical_terminal.py"
echo "   python3 test_terminal_only.py"
echo ""
echo "🛑 To stop services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cleanup() {
    echo ""
    echo "🛑 Stopping Medical Blitzy AI services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "📊 Monitoring services (Ctrl+C to stop)..."
echo "Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"

wait $BACKEND_PID $FRONTEND_PID
