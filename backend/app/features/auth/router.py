from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.features.auth.schemas import UserCreate, UserLogin, Token, UserResponse
from app.features.auth.service import AuthService

router = APIRouter()
security = HTTPBearer()

# Dependency injection for service
def get_auth_service() -> AuthService:
    return AuthService()

@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    try:
        return await auth_service.register_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login user"""
    try:
        return await auth_service.login_user(credentials)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get current user info"""
    user = await auth_service.get_current_user(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user 