from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_health_data():
    """Get user health data"""
    return {"message": "Health tracking feature - coming soon"}

@router.post("/")
async def create_health_record():
    """Create new health record"""
    return {"message": "Health record creation - coming soon"} 