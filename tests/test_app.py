import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
import pytest_asyncio
from httpx import AsyncClient
import os
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import asyncio as aioredis
from app.main import app

import asyncio
from tortoise import Tortoise


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    os.environ["TESTING"] = "1"
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

    # 🟢 Tortoise init & startup (in-memory sqlite for tests)
    await Tortoise.init(
        config={
            "connections": {"default": "sqlite://:memory:"},
            "apps": {
                "models": {
                    "models": ["app.models.file"],
                    "default_connection": "default",
                }
            },
        }
    )
    await Tortoise.generate_schemas()

    yield

    # 🧹 Cleanup
    await Tortoise.close_connections()
    await redis.close()
    os.environ.pop("TESTING", None)

import os
import json
from pathlib import Path


# Test ma'lumotlari
TEST_USERNAME = "test"
TEST_PASSWORD = "test"
TEST_FILE_CONTENT = b"Test file content"
TEST_FILE_NAME = "test.txt"

async def get_test_token():
    """Test uchun token olish (async)"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/token",
            json={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_root():
    """Asosiy endpoint testi"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Project is working!"

@pytest.mark.asyncio
async def test_login():
    """Login testi"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # To'g'ri ma'lumotlar bilan
        response = await ac.post(
            "/token",
            json={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

        # Noto'g'ri ma'lumotlar bilan
        response = await ac.post(
            "/token",
            json={"username": "wrong", "password": "wrong"}
        )
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_without_token():
    """Tokensiz fayl yuklash testi"""
    files = {"file": ("test.txt", TEST_FILE_CONTENT)}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload/", files=files)
    # FastAPI security xatosi 403 qaytaradi
    assert response.status_code in [401, 403]  # Both are acceptable for authentication errors

@pytest.mark.asyncio
async def test_upload_with_token():
    """Token bilan fayl yuklash testi"""
    token = await get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Ruxsat etilgan fayl turi
        files = {"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")}
        response = await ac.post("/upload/", headers=headers, files=files)
        # If the server returned an error, print the body for debugging (contains traceback when TESTING=1)
        if response.status_code != 200:
            print("UPLOAD ERROR RESPONSE STATUS:", response.status_code)
            try:
                print("UPLOAD ERROR RESPONSE TEXT:", response.text)
            except Exception:
                print("(could not read response.text)")
        assert response.status_code == 200
        assert "url" in response.json()
        
        # File path ni saqlab olish
        file_url = response.json()["url"]
        
        # Ruxsat etilmagan fayl turi
        files = {"file": ("test.exe", TEST_FILE_CONTENT, "application/x-msdownload")}
        response = await ac.post("/upload/", headers=headers, files=files)
        assert response.status_code == 400
        assert "File type not allowed" in response.json()["detail"]
        
        return file_url

@pytest.mark.asyncio
async def test_download_file():
    """Fayl yuklab olish testi"""
    token = await get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Avval faylni yuklash
    file_url = await test_upload_with_token()
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Faylni yuklab olish
        response = await ac.get(file_url, headers=headers)
        assert response.status_code == 200
        
        # Tokensiz urinish
        response = await ac.get(file_url)
        assert response.status_code in [401, 403]
        
        # Mavjud bo'lmagan fayl
        response = await ac.get("/2025-11-03/nonexistent.txt", headers=headers)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_rate_limiting():
    """Rate limiting testi"""
    token = await get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")}
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 10 ta so'rov yuborish (limit: 10 req/min)
        for _ in range(10):
            response = await ac.post("/upload/", headers=headers, files=files)
            assert response.status_code == 200
        
        # 11-so'rov rate limit xatosini berishi kerak
        response = await ac.post("/upload/", headers=headers, files=files)
        assert response.status_code == 429

@pytest.mark.asyncio
async def test_duplicate_file():
    """Bir xil faylni qayta yuklash testi"""
    token = await get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (TEST_FILE_NAME, TEST_FILE_CONTENT, "text/plain")}
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Birinchi yuklash
        response1 = await ac.post("/upload/", headers=headers, files=files)
        assert response1.status_code == 200
        url1 = response1.json()["url"]
        
        # Xuddi o'sha faylni qayta yuklash
        response2 = await ac.post("/upload/", headers=headers, files=files)
        assert response2.status_code == 200
        assert "File already exists" in response2.json()["message"]
        url2 = response2.json()["url"]
        
        # URL lar bir xil bo'lishi kerak
        assert url1 == url2

@pytest.mark.asyncio
async def test_file_size_limit():
    """Fayl hajmi cheklovi testi"""
    token = await get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 51MB hajmli fayl (limit: 50MB)
    large_content = b"0" * (51 * 1024 * 1024)
    files = {"file": ("large.txt", large_content, "text/plain")}
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/upload/", headers=headers, files=files)
        assert response.status_code == 400
        assert "File size too large" in response.json()["detail"]

@pytest.mark.asyncio
async def test_cleanup():
    """Test fayllarini tozalash"""
    uploaded_files_dir = Path("app/uploaded_files")
    if uploaded_files_dir.exists():
        for date_dir in uploaded_files_dir.iterdir():
            if date_dir.is_dir():
                for file in date_dir.iterdir():
                    if file.name.startswith("test"):
                        file.unlink()
                if not any(date_dir.iterdir()):
                    date_dir.rmdir()