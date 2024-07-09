from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    logo: Optional[str] = None
    full_text: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
