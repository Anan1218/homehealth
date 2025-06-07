from typing import Optional
from app.features.auth.schemas import UserCreate, UserLogin, Token, UserResponse
from app.core.supabase import get_supabase_admin
from supabase import Client


class AuthService:
    """Authentication service following Single Responsibility Principle"""
    
    def __init__(self, supabase: Client = None):
        self.supabase = supabase or get_supabase_admin()
    
    async def register_user(self, user_data: UserCreate) -> Token:
        """Register a new user"""
        response = self.supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "full_name": user_data.full_name
                }
            }
        })
        
        if response.user:
            return Token(
                access_token=response.session.access_token,
                token_type="bearer",
                expires_at=response.session.expires_at,
                user=UserResponse(
                    id=response.user.id,
                    email=response.user.email,
                    full_name=response.user.user_metadata.get("full_name"),
                    created_at=response.user.created_at
                )
            )
        raise Exception("Failed to create user")
    
    async def login_user(self, credentials: UserLogin) -> Token:
        """Authenticate user and return token"""
        response = self.supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if response.user:
            return Token(
                access_token=response.session.access_token,
                token_type="bearer",
                expires_at=response.session.expires_at,
                user=UserResponse(
                    id=response.user.id,
                    email=response.user.email,
                    full_name=response.user.user_metadata.get("full_name"),
                    created_at=response.user.created_at
                )
            )
        raise Exception("Invalid credentials")
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Get current user from token"""
        try:
            response = self.supabase.auth.get_user(token)
            if response.user:
                return UserResponse(
                    id=response.user.id,
                    email=response.user.email,
                    full_name=response.user.user_metadata.get("full_name"),
                    created_at=response.user.created_at
                )
        except Exception:
            return None 