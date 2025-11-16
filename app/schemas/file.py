from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class FileCreate(BaseModel):
    name: str
    saved_name: str
    path: str
    hash_code: str
    server: str
    shareable: bool
    public: bool
    size: int
    format: str


class FileUpdate(BaseModel):
    name: Optional[str] = None
    shareable: Optional[bool] = None
    public: Optional[bool] = None


class File(BaseModel):
    id: int
    date: datetime
    name: str
    saved_name: str
    path: str
    hash_code: str
    server: str
    is_used_by_other_servers: bool
    shareable: bool
    public: bool
    size: int
    format: str

    class Config:
        from_attributes = True


class FileResponse(BaseModel):
    """Fayl ro'yxati uchun response model"""
    id: int
    date: datetime
    name: str
    saved_name: str
    hash_code: str
    server: str
    shareable: bool
    public: bool
    size: int
    format: str
    url: str  # Fayl URL'i

    class Config:
        from_attributes = True


class SortField(str, Enum):
    """Sorting maydonlari"""
    date = "date"
    name = "name"
    size = "size"
    format = "format"


class SortOrder(str, Enum):
    """Sorting tartibi"""
    asc = "asc"
    desc = "desc"


class PaginationParams(BaseModel):
    """Pagination parametrlari"""
    page: int = Field(default=1, ge=1, description="Sahifa raqami")
    page_size: int = Field(default=10, ge=1, le=100, description="Sahifadagi elementlar soni")
    search: Optional[str] = Field(default=None, description="Qidiruv matni (fayl nomi bo'yicha)")
    format: Optional[str] = Field(default=None, description="Fayl formati bo'yicha filter")
    shareable: Optional[bool] = Field(default=None, description="Shareable bo'yicha filter")
    public: Optional[bool] = Field(default=None, description="Public bo'yicha filter")
    sort_by: Optional[SortField] = Field(default=SortField.date, description="Sorting maydoni")
    sort_order: Optional[SortOrder] = Field(default=SortOrder.desc, description="Sorting tartibi")


class FileListResponse(BaseModel):
    """Fayllar ro'yxati response modeli"""
    items: List[FileResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
