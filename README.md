# HomeHealth - Feature-Based Monorepo

A modern healthcare application built with **feature-based architecture** following **SOLID principles**.

## 🏗️ Architecture Overview

### Monorepo Structure
```
homehealth/
├── README.md                 # This file
├── docker-compose.yml        # Development environment
├── env.example              # Environment template
├── frontend/                # React.js + TypeScript
│   ├── src/
│   │   ├── app/            # App-level config, routing
│   │   ├── shared/         # Shared components, hooks, utils
│   │   └── features/       # Feature modules
│   │       ├── auth/       # Authentication feature
│   │       ├── dashboard/  # Dashboard feature
│   │       ├── health-tracking/
│   │       └── user-profile/
├── backend/                 # FastAPI + Python
│   ├── app/
│   │   ├── core/           # App config, database
│   │   ├── shared/         # Shared utilities
│   │   └── features/       # Feature modules
│   │       ├── auth/       # Auth endpoints & logic
│   │       ├── health/     # Health tracking
│   │       └── users/      # User management
├── shared/                  # Cross-platform types
└── scripts/                # Development scripts
```

## 🎯 Feature-Based Benefits

- **Single Responsibility**: Each feature owns its complete functionality
- **Scalability**: Add features without restructuring
- **Team Ownership**: Teams can own entire feature verticals
- **Code Discovery**: Related code lives together
- **SOLID Compliance**: Clear separation of concerns

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Supabase account

### Setup
```bash
# 1. Clone and setup
git clone <your-repo>
cd homehealth
./scripts/setup.sh

# 2. Configure environment
cp env.example .env
# Update .env with your Supabase credentials

# 3. Start development environment
docker-compose up
```

### Manual Setup (Alternative)
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **React Router** for routing
- **TanStack Query** for state management
- **Supabase JS** for authentication

### Backend
- **FastAPI** with async support
- **Supabase** for database & auth
- **Pydantic** for data validation
- **Python-Jose** for JWT handling

### Infrastructure
- **Docker** for containerization
- **Docker Compose** for development
- **Supabase** as Backend-as-a-Service

## 📁 Feature Structure

### Backend Feature Pattern
```
features/auth/
├── router.py      # FastAPI endpoints
├── service.py     # Business logic
├── repository.py  # Data access (if needed)
├── schemas.py     # Pydantic models
└── models.py      # Database models (if needed)
```

### Frontend Feature Pattern
```
features/auth/
├── components/    # React components
├── hooks/        # Custom hooks
├── services/     # API calls
└── types/        # TypeScript types
```

## 🔧 Development

### Adding New Features

1. **Backend Feature**:
```bash
mkdir -p backend/app/features/new-feature
# Create router.py, service.py, schemas.py
# Add router to main.py
```

2. **Frontend Feature**:
```bash
mkdir -p frontend/src/features/new-feature/{components,hooks,services,types}
# Create feature components and services
```

### API Endpoints
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

### Environment Variables
```bash
# Required in .env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

## 🏥 Current Features

### ✅ Implemented
- **Authentication**: Register, login, logout
- **Project Structure**: Feature-based organization
- **Docker Setup**: Development environment
- **SOLID Architecture**: Clean separation of concerns

### 🚧 Planned
- **Health Tracking**: Vital signs, medications
- **Dashboard**: Health overview and analytics
- **User Profiles**: Personal health information
- **Notifications**: Health reminders

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
# Use Dockerfile for production deployment
```

## 🤝 Contributing

1. Follow feature-based structure
2. Maintain SOLID principles
3. Add tests for new features
4. Update this README for major changes

## 📄 License

MIT License - see LICENSE file for details 