from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.features.auth.router import router as auth_router
from app.features.health.router import router as health_router
from app.features.users.router import router as users_router

app = FastAPI(
    title="HomeHealth API",
    description="Feature-based FastAPI backend for HomeHealth",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Feature-based routing
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "HomeHealth API is running"}

@app.get("/health-check")
async def health_check():
    return {"status": "healthy"} 