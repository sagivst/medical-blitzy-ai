# מדריך התקנה מלא - Medical Blitzy AI (IHN)

## דרישות מקדימות

### 1. תוכנות נדרשות
```bash
# Python 3.12+
python --version

# Node.js 18+ ו-npm
node --version
npm --version

# Git
git --version

# Docker (אופציונלי למסדי נתונים)
docker --version
```

### 2. מסדי נתונים
- **MongoDB** (לאחסון מסמכים)
- **PostgreSQL** (למשאבי FHIR)
- **Redis** (לקאש וסשנים)

## התקנת Backend (FastAPI)

### 1. הכנת הסביבה
```bash
# יצירת תיקיית הפרויקט
mkdir medical-blitzy-ai
cd medical-blitzy-ai

# יצירת סביבה וירטואלית
python -m venv venv

# הפעלת הסביבה הוירטואלית
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. התקנת תלויות Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. הגדרת משתני סביבה
צור קובץ `.env` בתיקיית `backend/`:

```env
# הגדרות בסיסיות
APP_NAME="Medical Blitzy AI"
DEBUG=True
SECRET_KEY="your-super-secret-key-here"
API_V1_STR="/api/v1"

# מסדי נתונים
MONGODB_URL="mongodb://localhost:27017"
MONGODB_DB_NAME="medical_blitzy"
POSTGRES_URL="postgresql://user:password@localhost:5432/medical_blitzy"
REDIS_URL="redis://localhost:6379"

# אבטחה
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM="HS256"

# שירותי OCR
TESSERACT_PATH="/usr/bin/tesseract"
POPPLER_PATH="/usr/bin"

# שירותי תרגום
GOOGLE_TRANSLATE_API_KEY="your-google-translate-key"

# שירותי ביטוח
INSURANCE_API_BASE_URL="https://api.insurance-provider.com"
INSURANCE_API_KEY="your-insurance-api-key"

# FHIR
FHIR_SERVER_URL="https://hapi.fhir.org/baseR5"

# Celery
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

### 4. התקנת תלויות מערכת
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-heb poppler-utils

# macOS
brew install tesseract poppler

# Windows
# הורד Tesseract מ: https://github.com/UB-Mannheim/tesseract/wiki
# הורד Poppler מ: https://blog.alivate.com.au/poppler-windows/
```

### 5. הפעלת השרת
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

השרת יהיה זמין ב: `http://localhost:8000`
תיעוד API: `http://localhost:8000/docs`

## התקנת Frontend (React)

### 1. התקנת תלויות
```bash
cd frontend
npm install
```

### 2. הגדרת משתני סביבה
צור קובץ `.env` בתיקיית `frontend/`:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_API_VERSION=v1
REACT_APP_APP_NAME="Medical Blitzy AI"
```

### 3. הפעלת שרת הפיתוח
```bash
npm start
```

האפליקציה תהיה זמינה ב: `http://localhost:3000`

## הגדרת מסדי נתונים

### 1. MongoDB
```bash
# התקנה עם Docker
docker run -d --name mongodb -p 27017:27017 mongo:latest

# או התקנה מקומית
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community

# Windows
# הורד מ: https://www.mongodb.com/try/download/community
```

### 2. PostgreSQL
```bash
# התקנה עם Docker
docker run -d --name postgres \
  -e POSTGRES_DB=medical_blitzy \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

# או התקנה מקומית
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# הורד מ: https://www.postgresql.org/download/windows/
```

### 3. Redis
```bash
# התקנה עם Docker
docker run -d --name redis -p 6379:6379 redis:latest

# או התקנה מקומית
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# הורד מ: https://github.com/microsoftarchive/redis/releases
```

## הפעלת Celery (עיבוד רקע)

### 1. הפעלת Celery Worker
```bash
cd backend
celery -A app.tasks.celery worker --loglevel=info
```

### 2. הפעלת Celery Beat (משימות מתוזמנות)
```bash
cd backend
celery -A app.tasks.celery beat --loglevel=info
```

### 3. ניטור Celery (אופציונלי)
```bash
cd backend
celery -A app.tasks.celery flower
```

ממשק הניטור יהיה זמין ב: `http://localhost:5555`

## בדיקת התקנה

### 1. בדיקת Backend
```bash
# בדיקת בריאות השרת
curl http://localhost:8000/health

# בדיקת API
curl http://localhost:8000/api/v1/patients/
```

### 2. בדיקת Frontend
פתח דפדפן וגש ל: `http://localhost:3000`
ודא שהדפים הבאים עובדים:
- Dashboard
- Patient Profile
- Document Upload
- Provider Search
- Insurance Claims

## פתרון בעיות נפוצות

### 1. שגיאות התקנה
```bash
# אם יש בעיות עם pip
pip install --upgrade pip

# אם יש בעיות עם npm
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 2. שגיאות מסד נתונים
```bash
# בדיקת חיבור MongoDB
mongosh --eval "db.adminCommand('ismaster')"

# בדיקת חיבור PostgreSQL
psql -h localhost -U user -d medical_blitzy -c "SELECT version();"

# בדיקת חיבור Redis
redis-cli ping
```

### 3. שגיאות OCR
```bash
# בדיקת Tesseract
tesseract --version

# בדיקת שפות זמינות
tesseract --list-langs
```

## הגדרות פיתוח

### 1. הפעלת מצב Debug
ב-`.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### 2. הפעלת Hot Reload
```bash
# Backend
uvicorn app.main:app --reload

# Frontend
npm start
```

### 3. בדיקות איכות קוד
```bash
# Backend
cd backend
black . --check
flake8 .
mypy app/

# Frontend
cd frontend
npm run lint
npm run type-check
```

## פריסה לייצור

### 1. הכנה לייצור
```bash
# Backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
```

### 2. Docker
```dockerfile
# Dockerfile לBackend
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

# Dockerfile לFrontend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
```

### 3. Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - POSTGRES_URL=postgresql://postgres:password@postgres:5432/medical_blitzy
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mongodb
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=medical_blitzy
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

## אבטחה וציות

### 1. הגדרות HIPAA
- הצפנת נתונים ב-AES-256
- אימות דו-שלבי
- רישום ביקורת מלא
- גיבויים מוצפנים

### 2. הגדרות SSL/TLS
```bash
# יצירת תעודות SSL
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### 3. משתני סביבה בטוחים
```env
# השתמש במפתחות חזקים
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_PASSWORD=$(openssl rand -base64 32)
```

## תמיכה ותחזוקה

### 1. לוגים
```bash
# צפייה בלוגים
tail -f backend/logs/app.log
tail -f frontend/logs/access.log
```

### 2. ניטור ביצועים
- השתמש ב-Prometheus + Grafana
- הגדר התראות על שגיאות
- עקוב אחר זמני תגובה

### 3. גיבויים
```bash
# גיבוי MongoDB
mongodump --db medical_blitzy --out backup/

# גיבוי PostgreSQL
pg_dump medical_blitzy > backup/postgres_backup.sql
```

## קישורים שימושיים

- [תיעוד FastAPI](https://fastapi.tiangolo.com/)
- [תיעוד React](https://react.dev/)
- [תיעוד FHIR](https://hl7.org/fhir/)
- [תיעוד MongoDB](https://docs.mongodb.com/)
- [תיעוד PostgreSQL](https://www.postgresql.org/docs/)

---

**הערה**: מדריך זה מכסה התקנה בסיסית. לפריסה בייצור, יש להתייעץ עם מומחה DevOps ולהגדיר אמצעי אבטחה נוספים.
