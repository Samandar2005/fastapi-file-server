import os
import sys
import pytest
import pytest_asyncio
import asyncio
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

# Loyiha root papkasini Python pathga qo'shish
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

# Test rejimida ekanligimizni belgilang (Tortoise uchun in-memory sqlite ishlatamiz)
os.environ.setdefault("TESTING", "1")

@pytest_asyncio.fixture(autouse=True)
async def setup_redis():
    """Test muhiti uchun Redis ni ulash"""
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield redis
    await redis.close()