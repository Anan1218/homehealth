from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    """Get users"""
    return {"message": "User management feature - coming soon"}

@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get specific user"""
    return {"message": f"User {user_id} details - coming soon"} 