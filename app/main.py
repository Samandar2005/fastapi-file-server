from fastapi import FastAPI
from app.database import init, close_db_connection
from tortoise.contrib.fastapi import register_tortoise
from app.routers import file, auth
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis
import fastapi_limiter
from fastapi_limiter.depends import RateLimiter

from app.database import TORTOISE_ORM

app = FastAPI()


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init()
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await fastapi_limiter.FastAPILimiter.init(redis)
    
    yield
    
    # Shutdown
    await close_db_connection()
    await redis.close()
    await fastapi_limiter.FastAPILimiter.reset()

app = FastAPI(lifespan=lifespan)


app.include_router(auth.router)
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
