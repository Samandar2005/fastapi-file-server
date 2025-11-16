from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
from tortoise.transactions import in_transaction
from app.models.file import File as FileModel
from app.schemas.file import (
    FileCreate, FileUpdate, FileResponse, FileListResponse, 
    PaginationParams, SortField, SortOrder
)
from app.utils.file import save_file_to_disk, save_to_excel, validate_file, ALLOWED_EXTENSIONS
from app.utils.security import verify_token, decrypt_file
from app.crud.file import get_files, get_file_by_id, update_file, delete_file
import fastapi_limiter
from fastapi_limiter.depends import RateLimiter
import os
import uuid
from datetime import datetime
import hashlib
import traceback
import math


router = APIRouter()

UPLOAD_FOLDER = "app/uploaded_files"
EXCEL_PATH = "app/file_records.xlsx"
DEFAULT_SERVER = "localhost"


# ============ Fayllarni boshqarish API endpointlari ============

@router.get("/files", response_model=FileListResponse)
async def list_files(
    page: int = Query(default=1, ge=1, description="Sahifa raqami"),
    page_size: int = Query(default=10, ge=1, le=100, description="Sahifadagi elementlar soni"),
    search: str = Query(default=None, description="Qidiruv matni (fayl nomi bo'yicha)"),
    format: str = Query(default=None, description="Fayl formati bo'yicha filter"),
    shareable: bool = Query(default=None, description="Shareable bo'yicha filter"),
    public: bool = Query(default=None, description="Public bo'yicha filter"),
    sort_by: SortField = Query(default=SortField.date, description="Sorting maydoni"),
    sort_order: SortOrder = Query(default=SortOrder.desc, description="Sorting tartibi"),
    token: dict = Depends(verify_token),
    rate_limiter: None = Depends(RateLimiter(times=30, seconds=60))
):
    """
    Fayllar ro'yxatini olish (pagination, filtering, sorting bilan)
    
    - **page**: Sahifa raqami (1 dan boshlanadi)
    - **page_size**: Sahifadagi elementlar soni (1-100 oraliq)
    - **search**: Fayl nomi bo'yicha qidiruv
    - **format**: Fayl formati bo'yicha filter (masalan: "text/plain", "image/png")
    - **shareable**: Shareable bo'yicha filter (true/false)
    - **public**: Public bo'yicha filter (true/false)
    - **sort_by**: Sorting maydoni (date, name, size, format)
    - **sort_order**: Sorting tartibi (asc, desc)
    """
    try:
        params = PaginationParams(
            page=page,
            page_size=page_size,
            search=search,
            format=format,
            shareable=shareable,
            public=public,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        files, total = await get_files(params)
        
        # FileResponse ga aylantirish (URL qo'shish)
        file_responses = []
        for file in files:
            # URL ni yaratish (path dan date va saved_name ni olish)
            path_parts = file.path.split(os.sep)
            if len(path_parts) >= 2:
                date_part = path_parts[-2]  # YYYY-MM-DD
                file_url = f"/{date_part}/{file.saved_name}"
            else:
                file_url = f"/{file.saved_name}"
            
            file_response = FileResponse(
                id=file.id,
                date=file.date,
                name=file.name,
                saved_name=file.saved_name,
                hash_code=file.hash_code,
                server=file.server,
                shareable=file.shareable,
                public=file.public,
                size=file.size,
                format=file.format,
                url=file_url
            )
            file_responses.append(file_response)
        
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        return FileListResponse(
            items=file_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        if os.environ.get("TESTING"):
            tb = traceback.format_exc()
            raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/files/{file_id}", response_model=FileResponse)
async def get_file_by_id_endpoint(
    file_id: int,
    token: dict = Depends(verify_token),
    rate_limiter: None = Depends(RateLimiter(times=30, seconds=60))
):
    """
    ID bo'yicha fayl ma'lumotlarini olish
    
    - **file_id**: Fayl ID si
    """
    try:
        file = await get_file_by_id(file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # URL ni yaratish
        path_parts = file.path.split(os.sep)
        if len(path_parts) >= 2:
            date_part = path_parts[-2]  # YYYY-MM-DD
            file_url = f"/{date_part}/{file.saved_name}"
        else:
            file_url = f"/{file.saved_name}"
        
        return FileResponse(
            id=file.id,
            date=file.date,
            name=file.name,
            saved_name=file.saved_name,
            hash_code=file.hash_code,
            server=file.server,
            shareable=file.shareable,
            public=file.public,
            size=file.size,
            format=file.format,
            url=file_url
        )
    except HTTPException:
        raise
    except Exception as e:
        if os.environ.get("TESTING"):
            tb = traceback.format_exc()
            raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/files/{file_id}", response_model=FileResponse)
async def update_file_endpoint(
    file_id: int,
    file_update: FileUpdate,
    token: dict = Depends(verify_token),
    rate_limiter: None = Depends(RateLimiter(times=20, seconds=60))
):
    """
    Fayl ma'lumotlarini yangilash (metadata o'zgartirish)
    
    - **file_id**: Fayl ID si
    - Yangilash mumkin bo'lgan maydonlar: name, shareable, public
    """
    try:
        updated_file = await update_file(file_id, file_update)
        if not updated_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # URL ni yaratish
        path_parts = updated_file.path.split(os.sep)
        if len(path_parts) >= 2:
            date_part = path_parts[-2]  # YYYY-MM-DD
            file_url = f"/{date_part}/{updated_file.saved_name}"
        else:
            file_url = f"/{updated_file.saved_name}"
        
        return FileResponse(
            id=updated_file.id,
            date=updated_file.date,
            name=updated_file.name,
            saved_name=updated_file.saved_name,
            hash_code=updated_file.hash_code,
            server=updated_file.server,
            shareable=updated_file.shareable,
            public=updated_file.public,
            size=updated_file.size,
            format=updated_file.format,
            url=file_url
        )
    except HTTPException:
        raise
    except Exception as e:
        if os.environ.get("TESTING"):
            tb = traceback.format_exc()
            raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/files/{file_id}")
async def delete_file_endpoint(
    file_id: int,
    token: dict = Depends(verify_token),
    rate_limiter: None = Depends(RateLimiter(times=10, seconds=60))
):
    """
    Faylni o'chirish (fizik fayl va DB yozuvi)
    
    - **file_id**: Fayl ID si
    
    Muvaffaqiyatli o'chirilganda: `{"message": "File deleted successfully", "file_id": file_id}`
    """
    try:
        success, error_message = await delete_file(file_id)
        if not success:
            if error_message == "File not found":
                raise HTTPException(status_code=404, detail=error_message)
            raise HTTPException(status_code=500, detail=error_message)
        
        return {
            "message": "File deleted successfully",
            "file_id": file_id
        }
    except HTTPException:
        raise
    except Exception as e:
        if os.environ.get("TESTING"):
            tb = traceback.format_exc()
            raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ============ Fayl yuklash va yuklab olish endpointlari ============


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
