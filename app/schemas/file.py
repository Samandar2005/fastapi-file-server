from pydantic import BaseModel
from datetime import datetime


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
        orm_mode = True
