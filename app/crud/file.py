from tortoise.transactions import in_transaction
from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate, PaginationParams, FileResponse, SortField, SortOrder
import hashlib
from typing import Optional, List, Tuple
import math
import os


async def get_file_by_hash(hash_code: str):
    return await File.filter(hash_code=hash_code).first()


async def get_file_by_id(file_id: int) -> Optional[File]:
    """ID bo'yicha fayl olish"""
    return await File.filter(id=file_id).first()


async def create_file(file: FileCreate):
    async with in_transaction() as connection:
        db_file = File(**file.dict())
        await db_file.save(using_db=connection)
        return db_file


async def get_files(
    params: PaginationParams
) -> Tuple[List[File], int]:
    """
    Fayllarni pagination, filtering va sorting bilan olish
    
    Returns:
        Tuple[List[File], int]: (fayllar ro'yxati, jami soni)
    """
    # Base query
    query = File.all()
    
    # Qidiruv (fayl nomi bo'yicha)
    if params.search:
        query = query.filter(name__icontains=params.search)
    
    # Format bo'yicha filter
    if params.format:
        query = query.filter(format=params.format)
    
    # Shareable bo'yicha filter
    if params.shareable is not None:
        query = query.filter(shareable=params.shareable)
    
    # Public bo'yicha filter
    if params.public is not None:
        query = query.filter(public=params.public)
    
    # Jami soni
    total = await query.count()
    
    # Sorting
    sort_field = params.sort_by.value if params.sort_by else "date"
    if params.sort_order and params.sort_order == SortOrder.desc:
        sort_field = f"-{sort_field}"
    
    query = query.order_by(sort_field)
    
    # Pagination
    offset = (params.page - 1) * params.page_size
    files = await query.offset(offset).limit(params.page_size)
    
    return list(files), total


async def update_file(file_id: int, file_update: FileUpdate) -> Optional[File]:
    """Fayl ma'lumotlarini yangilash"""
    file = await get_file_by_id(file_id)
    if not file:
        return None
    
    update_data = file_update.dict(exclude_unset=True)
    if not update_data:
        return file
    
    async with in_transaction() as connection:
        for field, value in update_data.items():
            setattr(file, field, value)
        await file.save(using_db=connection)
        return file


async def delete_file(file_id: int) -> Tuple[bool, Optional[str]]:
    """
    Faylni o'chirish (fizik fayl va DB yozuvi)
    
    Returns:
        Tuple[bool, Optional[str]]: (muvaffaqiyat, xato xabari)
    """
    file = await get_file_by_id(file_id)
    if not file:
        return False, "File not found"
    
    # Fizik faylni o'chirish
    file_path = file.path
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return False, f"Failed to delete physical file: {str(e)}"
    
    # DB yozuvini o'chirish
    try:
        async with in_transaction() as connection:
            await file.delete(using_db=connection)
        return True, None
    except Exception as e:
        return False, f"Failed to delete database record: {str(e)}"


def hash_file(file_data: bytes):
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest()
