from fastapi import FastAPI
from app.database import init, close_db_connection
from tortoise.contrib.fastapi import register_tortoise
from app.routers import file
from fastapi.responses import JSONResponse

from app.database import TORTOISE_ORM

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init()


@app.on_event("shutdown")
async def shutdown_event():
    await close_db_connection()


app.include_router(file.router)


@app.get("/")
async def root():
    message = f"Project is working!"
    return JSONResponse(content={"message": message})


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
