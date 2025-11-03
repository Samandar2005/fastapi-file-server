from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from tortoise.transactions import in_transaction
from app.models.file import File as FileModel
from app.schemas.file import FileCreate
from app.utils.file import save_file_to_disk, save_to_excel, validate_file, ALLOWED_EXTENSIONS
from app.utils.security import verify_token, decrypt_file
import fastapi_limiter
from fastapi_limiter.depends import RateLimiter
import os
import uuid
from datetime import datetime
import hashlib
import traceback
import os


router = APIRouter()

UPLOAD_FOLDER = "app/uploaded_files"
EXCEL_PATH = "app/file_records.xlsx"
DEFAULT_SERVER = "localhost"


@router.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        token: dict = Depends(verify_token),
        rate_limiter: None = Depends(RateLimiter(times=10, seconds=60))  # 10 requests per minute
):
    try:
        file_data = await file.read()
        
        # Fayl turini va hajmini tekshirish
        validate_file(file.content_type, len(file_data))
        
        hash_code = hash_file(file_data)

        existing_file = await FileModel.filter(hash_code=hash_code).first()
        if existing_file:
            duplicate_file_info = FileCreate(
                name=file.filename,
                saved_name=existing_file.saved_name,
                path=existing_file.path,
                hash_code=hash_code,
                server=DEFAULT_SERVER,
                shareable=True,
                public=True,
                size=len(file_data),
                format=file.content_type
            )
            async with in_transaction() as connection:
                await FileModel.create(**duplicate_file_info.dict(), using_db=connection)
            saved_date = existing_file.path.split(os.sep)[-2]
            return {
                "message": "File already exists",
                "url": f"/{saved_date}/{existing_file.saved_name}"
            }

        current_date = datetime.now().strftime("%Y-%m-%d")
        daily_folder = os.path.join(UPLOAD_FOLDER, current_date)
        if not os.path.exists(daily_folder):
            os.makedirs(daily_folder)

        unique_filename = f"{uuid.uuid4().hex}"

        saved_name, file_path = save_file_to_disk(daily_folder, file_data, unique_filename)
        file_size = len(file_data)

        file_info = FileCreate(
            name=file.filename,
            saved_name=saved_name,
            path=file_path,
            hash_code=hash_code,
            server=DEFAULT_SERVER,
            shareable=True,
            public=True,
            size=file_size,
            format=file.content_type
        )

        async with in_transaction() as connection:
            db_file = await FileModel.create(**file_info.dict(), using_db=connection)
        save_to_excel(file_info.dict(), EXCEL_PATH)

        return {
            "message": "File uploaded successfully",
            "url": f"/{current_date}/{saved_name}"
        }
    except Exception as e:
        # During testing include the full traceback in the response to aid debugging
        if os.environ.get("TESTING"):
            tb = traceback.format_exc()
            raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{date}/{filename}")
async def get_file(
    date: str, 
    filename: str,
    token: dict = Depends(verify_token),
    rate_limiter: None = Depends(RateLimiter(times=30, seconds=60))  # 30 requests per minute
):
    file_path = os.path.join(UPLOAD_FOLDER, date, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Faylni o'qish va decrypt qilish
    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    
    decrypted_data = decrypt_file(encrypted_data)
    
    def iterfile():
        yield decrypted_data

    # Fayl turini aniqlash
    file_extension = filename.split('.')[-1].lower()
    content_type = next((mime for ext, mime in ALLOWED_EXTENSIONS.items() if ext == file_extension), 'application/octet-stream')
    
    return StreamingResponse(
        iterfile(),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


def hash_file(file_data: bytes):
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest()
