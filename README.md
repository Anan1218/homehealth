# HomeHealth - Feature-Based Monorepo

A scalable healthcare application built with React.js frontend, FastAPI backend, and Supabase database using feature-based architecture and SOLID principles.

## 🏗️ Architecture

**Feature-Based Organization**: Each feature (health records, appointments, patients, etc.) contains its own models, services, API routes, and UI components, promoting modularity and maintainability.

### Project Structure
```
homehealth/
├── frontend/           # React + Vite frontend
│   ├── src/features/   # Feature-based UI components
│   └── ...
├── backend/            # FastAPI backend
│   ├── app/features/   # Feature-based API modules
│   └── ...
└── docker-compose.yml  # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Supabase account

### Setup

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd homehealth
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🛠️ Development

### Running Without Docker
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Docker vs Uvicorn
- **Docker Compose**: Orchestrates the entire application stack (frontend + backend + networking)
- **Uvicorn**: ASGI web server that runs inside the backend container
- They work together: Docker Compose manages containers, Uvicorn serves the FastAPI app

## 🚀 Production Deployment

### **Option 1: Render (Recommended)**
Deploy both frontend and backend on Render:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for production"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Set Environment Variables**
   - Add your Supabase credentials in Render dashboard
   - Update the `envVarGroups` section in `render.yaml`

4. **Deploy**
   - Render will automatically deploy both services
   - Frontend: `https://your-app-name.onrender.com`
   - Backend: `https://your-api-name.onrender.com`

### **Option 2: Vercel + Render**
Best performance for frontend:

1. **Deploy Frontend to Vercel**
   ```bash
   npx vercel --prod
   ```
   
2. **Set Vercel Environment Variables**
   ```bash
   vercel env add VITE_API_URL
   vercel env add VITE_SUPABASE_URL
   vercel env add VITE_SUPABASE_ANON_KEY
   ```

3. **Deploy Backend to Render**
   - Create new Web Service on Render
   - Use `backend/Dockerfile.prod`
   - Set environment variables

### **Option 3: Automated Deployment**
```bash
# Run deployment script
./scripts/deploy.sh
```

### **Production Checklist**

- [ ] **Environment Variables Set**
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY` 
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `VITE_API_URL` (frontend)

- [ ] **Security**
  - Update CORS origins in `backend/app/main.py`
  - Use HTTPS in production
  - Secure API keys

- [ ] **Performance**
  - Frontend assets minified (`npm run build`)
  - Backend health checks enabled
  - CDN for static assets (optional)

- [ ] **Monitoring**
  - Health endpoint: `/health`
  - Error logging
  - Performance monitoring

## 🏛️ SOLID Principles Implementation

- **Single Responsibility**: Each feature module has focused responsibilities
- **Open/Closed**: Services use dependency injection for extensibility
- **Liskov Substitution**: Abstract base classes for consistent interfaces
- **Interface Segregation**: Feature-specific interfaces and schemas
- **Dependency Inversion**: Repository pattern with abstract base classes

## 📁 Feature Structure
Each feature follows this pattern:
```
features/feature_name/
├── __init__.py
├── models.py       # Data models
├── schemas.py      # Pydantic schemas
├── repository.py   # Data access layer
├── service.py      # Business logic
└── router.py       # API endpoints
```

## 🔧 Common Issues

### Backend Won't Start
- **Error**: `email-validator is not installed`
- **Fix**: Rebuild containers: `docker-compose up --build`

### Environment Variables Missing
- **Error**: `SUPABASE_URL variable is not set`
- **Fix**: Copy `.env.example` to `.env` and add your Supabase credentials

### Port Conflicts
- **Error**: `Port already in use`
- **Fix**: Stop other services on ports 5173/8000 or change ports in `docker-compose.yml`

### Production Deployment Issues
- **Error**: Build failures
- **Fix**: Test locally first with `./scripts/deploy.sh`

## 🚀 Next Steps

1. Set up Supabase database tables
2. Add feature-specific components
4. Implement business logic in services
5. Add comprehensive testing
6. Deploy to production

Built with ❤️ using feature-based architecture and SOLID principles. 