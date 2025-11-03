from fastapi import APIRouter, HTTPException
from app.utils.security import create_access_token
from pydantic import BaseModel

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

# Test uchun oddiy autentifikatsiya
@router.post("/token")
async def login(user: UserLogin):
    # ESLATMA: Bu test uchun. Haqiqiy loyihada to'g'ri autentifikatsiya qo'shish kerak
    if user.username == "test" and user.password == "test":
        return {
            "access_token": create_access_token({"sub": user.username}),
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")