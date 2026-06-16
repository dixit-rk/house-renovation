# House Renovation AI - Deployment Guide

**Version:** 1.0.0  
**Last Updated:** 2026-06-16  
**Status:** Ready for Production

---

## 📋 Project Overview

**House Renovation AI** is a full-stack web application that uses AI to help homeowners plan house renovations. Users upload exterior photos, get AI-powered zone detection, choose materials, generate previews, and receive cost estimations.

### Key Features
- 📸 House exterior image upload & validation
- 🤖 AI zone detection (roof, walls, doors, windows using Groq)
- 🎨 Material selection & suggestions
- 🖼️ Renovation preview generation (Hugging Face Stable Diffusion)
- 💰 Cost estimation (materials + labor)
- 📄 PDF report generation
- 📊 Project history & task tracking

### Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite | 18.3.1 + 7.3.5 |
| **Backend** | FastAPI | 0.111.0 |
| **Database** | PostgreSQL | 14+ |
| **Cache** | Redis | 6+ |
| **Job Queue** | Celery | 5.4.0 |
| **AI Vision** | Groq API | llama-4-scout |
| **Image Gen** | Hugging Face Diffusers | 0.27.2 |

---

## 📁 Project Structure

```
house-renovation/
├── frontend/                          # React + Vite frontend
│   ├── src/
│   │   ├── components/               # React components (5-step wizard)
│   │   │   ├── upload/              # Step 1: Image upload
│   │   │   ├── zones/               # Step 2: Zone detection & materials
│   │   │   ├── generation/          # Step 3: Preview generation
│   │   │   ├── estimation/          # Step 4: Cost estimation
│   │   │   └── report/              # Step 5: PDF report
│   │   ├── hooks/
│   │   │   └── useTaskPoller.js     # Poll Celery task status
│   │   ├── services/
│   │   │   └── api.js               # API client (communicates with backend)
│   │   ├── pages/
│   │   │   └── ProjectPage.jsx      # Main page (5-step wizard)
│   │   ├── App.jsx                  # Root component
│   │   ├── main.jsx                 # Entry point
│   │   └── index.css                # Global styles (Tailwind)
│   ├── package.json                 # Dependencies
│   ├── vite.config.js               # Vite build config
│   ├── tailwind.config.js           # Tailwind CSS config
│   ├── index.html                   # HTML template
│   └── .env                         # Environment: VITE_API_BASE_URL
│
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── api/v1/endpoints/        # API routes
│   │   │   ├── project.py           # Create/read projects
│   │   │   ├── image.py             # Upload & process images
│   │   │   ├── zone.py              # Zone detection
│   │   │   ├── catalog.py           # Material catalog
│   │   │   ├── generation.py        # Image generation
│   │   │   ├── estimation.py        # Cost estimation
│   │   │   ├── task.py              # Celery task status
│   │   │   └── report.py            # PDF report generation
│   │   ├── ai/                      # AI integrations
│   │   │   ├── groq_client.py       # Groq vision API
│   │   │   ├── validation/          # Image validation (OpenCV)
│   │   │   ├── zone_detection/      # Zone detection logic
│   │   │   ├── suggestion/          # Material suggestions
│   │   │   ├── generation/          # Image generation (HF)
│   │   │   └── sketch/              # Zone visualization
│   │   ├── crud/                    # Database operations
│   │   │   ├── project_crud.py
│   │   │   ├── image_crud.py
│   │   │   ├── zone_crud.py
│   │   │   ├── estimation_crud.py
│   │   │   ├── task_crud.py
│   │   │   └── report_crud.py
│   │   ├── models/                  # SQLAlchemy models
│   │   │   └── renovation_models.py # 7 database tables
│   │   ├── schemas/                 # Pydantic schemas (request/response)
│   │   ├── db/
│   │   │   ├── database.py          # SQLAlchemy setup
│   │   │   └── session.py           # DB session management
│   │   ├── workers/                 # Celery tasks
│   │   │   ├── celery_app.py        # Celery config
│   │   │   └── ai_worker.py         # Background AI tasks
│   │   ├── core/
│   │   │   └── config.py            # Settings (from .env)
│   │   ├── utils/
│   │   │   ├── cost_calculator.py   # Cost calculation logic
│   │   │   ├── prompt_builder.py    # AI prompt building
│   │   │   └── file_handler.py      # File I/O
│   │   ├── reports/
│   │   │   └── pdf_generator.py     # PDF report generation
│   │   └── catalog/
│   │       ├── materials.json       # Material prices & specs
│   │       └── loader.py            # Load material catalog
│   ├── alembic/                     # Database migrations
│   │   ├── versions/                # Migration scripts
│   │   ├── env.py                   # Migration environment
│   │   └── script.py.mako           # Migration template
│   ├── storage/                     # Local file storage
│   │   ├── uploads/                 # User-uploaded images
│   │   ├── generated/               # Generated previews & sketches
│   │   └── reports/                 # Generated PDF reports
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   └── .env                         # Actual environment variables
│
├── README.md                        # Project overview
├── DEPLOYMENT.md                    # This file
├── package.json                     # Workspace root (placeholder)
└── .gitignore                       # Git ignore rules
```

---

## 🗄️ Database Schema (7 Tables)

```sql
-- projects: User projects
  id (UUID) | name | status | scale_factor | front_width_ft | created_at | updated_at

-- project_images: Uploaded photos
  id | project_id | image_type | file_path | mime_type | uploaded_at

-- project_zones: Detected zones (roof, walls, door, etc)
  id | project_id | zone_key | label | estimated_sqft | created_at

-- zone_material_assignments: Material choice per zone
  id | zone_id | material_id | assigned_at

-- project_estimations: Cost per zone × material
  id | project_id | zone_id | material_id | area_sqft | material_cost_inr | labour_cost_inr | total_cost_inr

-- task_records: Celery background jobs
  id | project_id | celery_task_id | task_type | status | result | created_at

-- renovation_reports: Generated PDF reports
  id | project_id | file_path | grand_total_inr | total_days | generated_at
```

---

## 🚀 Deployment Targets

### **Frontend: Vercel**
- **URL:** `house-renovation-xyz.vercel.app`
- **Repository:** `dixit-rk/house-renovation` (GitHub)
- **Root Directory:** `./frontend`
- **Framework:** Vite
- **Environment Variable:** `VITE_API_BASE_URL` → Railway backend URL

### **Backend: Railway**
- **Repository:** `dixit-rk/house-renovation` (GitHub)
- **Root Directory:** `./backend`
- **Framework:** FastAPI + Uvicorn
- **Services Included:**
  - FastAPI web service (port 8000)
  - PostgreSQL database
  - Redis cache
  - Celery worker (background jobs)

### **API Endpoints**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/projects/` | Create new project |
| POST | `/api/v1/image/upload` | Upload exterior photo |
| GET | `/api/v1/zone/{project_id}` | Get detected zones |
| POST | `/api/v1/zone/{zone_id}/material` | Assign material |
| POST | `/api/v1/generation/generate-renovation` | Generate preview (Celery task) |
| POST | `/api/v1/estimation/calculate` | Calculate costs |
| GET | `/api/v1/task/{task_id}` | Get task status |
| POST | `/api/v1/report/generate` | Generate PDF report |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger API docs |

---

## 📦 Environment Variables

### **Frontend (.env)**
```env
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app
```

### **Backend (.env)**
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/house_renovation

# Cache
REDIS_URL=redis://host:6379/0

# APIs
GROQ_API_KEY=your_groq_api_key_here
DEBUG=False

# Storage paths (relative to backend/)
STORAGE_UPLOAD_DIR=storage/uploads
STORAGE_GENERATED_DIR=storage/generated
STORAGE_REPORTS_DIR=storage/reports

# AI Models
HF_IMAGE_MODEL=stabilityai/sd-turbo
IMAGE_MAX_SIZE=512
IMAGE_STEPS=4
IMAGE_STRENGTH=0.6
GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

---

## 🔑 API Keys Required

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| **Groq** | Vision API (zone detection) | 30 calls/min free |
| **Hugging Face** | Stable Diffusion models | Free (CPU only) |
| **GitHub** | Repository hosting | Free |

---

## 📊 Data Flow

```
User Browser (React)
    ↓
Vercel (Frontend)
    ↓ (HTTP REST API)
Railway Backend (FastAPI)
    ├→ PostgreSQL (project data)
    ├→ Redis (caching)
    └→ Celery Worker (background tasks)
         ├→ Groq API (zone detection)
         ├→ Hugging Face (image generation)
         └→ Local File Storage
    ↓ (Response)
User Browser (shows results)
```

---

## 🛠️ Local Development Setup

### Prerequisites
```bash
# System packages
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env: VITE_API_BASE_URL=http://localhost:8000
npm run dev
# Runs on http://localhost:5173
```

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with local DB/Redis URLs
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload --port 8000
```

### Celery Worker
```bash
cd backend
source venv/bin/activate
celery -A app.workers.celery_app worker --loglevel=info
```

---

## 🎯 Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "House renovation AI - ready for deployment"
git push origin main
```

### Step 2: Deploy Frontend (Vercel)
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Import project: `dixit-rk/house-renovation`
4. Configure:
   - **Root Directory:** `./frontend`
   - **Framework:** Vite
   - **Environment:** `VITE_API_BASE_URL=<your-railway-url>`
5. Deploy

### Step 3: Deploy Backend (Railway)

1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Create new Project** → "Deploy from GitHub repo"
4. **Select repository:** `dixit-rk/house-renovation`
5. **Configure root directory:** `./backend`
6. **Click Deploy** (will use Procfile automatically)

#### Procfile Configuration
The `backend/Procfile` tells Railway how to run the app:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
worker: celery -A app.workers.celery_app worker --loglevel=info
```

#### Add Database & Cache Services
After deployment starts:
1. Go to Project → Add Service
2. Add **PostgreSQL** plugin
3. Add **Redis** plugin
4. Railway auto-generates connection strings

### Step 4: Set Environment Variables on Railway

Go to Project Settings → Environment Variables and add:

```env
DATABASE_URL=<auto-filled by Railway PostgreSQL>
REDIS_URL=<auto-filled by Railway Redis>
GROQ_API_KEY=your_groq_api_key_here
DEBUG=False
STORAGE_UPLOAD_DIR=storage/uploads
STORAGE_GENERATED_DIR=storage/generated
STORAGE_REPORTS_DIR=storage/reports
HF_IMAGE_MODEL=stabilityai/sd-turbo
```

### Step 5: Deploy Celery Worker

In Railway Project:
1. **Add Service** → GitHub repo
2. Select same `dixit-rk/house-renovation` repo
3. **Root Directory:** `./backend`
4. **Start command:** `celery -A app.workers.celery_app worker --loglevel=info`
5. Deploy as background worker

### Step 6: Update Frontend Environment

1. Go to **Vercel Dashboard**
2. Select **house-renovation** project
3. Go to **Settings** → **Environment Variables**
4. Update `VITE_API_BASE_URL`:
   - Get Railway backend URL from Railway dashboard
   - Format: `https://your-railway-backend.up.railway.app`
5. **Redeploy** Vercel project

#### Example Vercel Environment Update
```env
VITE_API_BASE_URL=https://house-renovation-prod.up.railway.app
```

### Step 7: Verify Deployment

Test the live API:
```bash
curl https://house-renovation-prod.up.railway.app/health
# Should return: {"success": true, "msg": "OK", "data": null}
```

Visit frontend:
```
https://house-renovation-nine.vercel.app/
```

Should now connect to Railway backend! ✅

---

## 🧪 Testing Endpoints

### Create Project
```bash
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}'
```

### Upload Image
```bash
curl -X POST http://localhost:8000/api/v1/image/upload \
  -F "project_id=<uuid>" \
  -F "file=@house.jpg"
```

### Check API Docs
```
http://localhost:8000/docs
```

---

## 📈 Performance Tuning

| Task | Time | Optimization |
|------|------|--------------|
| Image upload | 1s | Reduce image size before upload |
| Zone detection | 6-12s | Done async in Celery |
| Material suggestions | 4s | Cached in Redis |
| Image generation | 3-10s | Runs on CPU (fast on Railway) |
| PDF generation | 5s | Async background job |

---

## 🐛 Debugging

### View Celery logs
```bash
celery -A app.workers.celery_app worker --loglevel=debug
```

### Check database
```bash
psql -U user -d house_renovation
\dt  # List tables
SELECT * FROM projects;  # View projects
```

### View Redis cache
```bash
redis-cli
KEYS *
GET key_name
```

### View API logs (Vercel)
Dashboard → Deployments → Logs

### View API logs (Railway)
Dashboard → Project → Logs

---

## 📝 Important Notes

### Limits & Constraints
- Image upload max: 10MB (configurable)
- Max image size: 512×512px (for generation)
- Celery tasks timeout: 15 minutes
- Free tier Redis: 10K commands/day
- Free tier PostgreSQL: 5GB on Neon, unlimited on Railway

### Security
- ✅ CORS enabled for Vercel domain
- ✅ No hardcoded secrets (use .env)
- ✅ Database passwords hashed
- ✅ API rate limiting (optional, can add)

### Monitoring
- Set up error tracking (Sentry recommended)
- Monitor Celery task queue (Flower recommended)
- Set up database backups (Railway auto-backups)

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Groq API | https://console.groq.com |
| Hugging Face | https://huggingface.co |
| FastAPI Docs | https://fastapi.tiangolo.com |
| Celery Docs | https://docs.celeryproject.io |
| Railway Docs | https://docs.railway.app |
| Vercel Docs | https://vercel.com/docs |

---

## 📞 Support

For issues or questions:
1. Check API docs: `http://backend-url/docs`
2. Review logs (Vercel / Railway dashboard)
3. Check database migrations: `alembic current`
4. Test locally before deploying

---

**Ready to deploy!** 🚀
