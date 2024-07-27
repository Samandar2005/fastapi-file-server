from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "The project is working!"}
