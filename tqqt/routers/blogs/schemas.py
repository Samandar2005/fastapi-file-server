from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogBase(BaseModel):
    title: str
    short_info: Optional[str] = None
    logo: Optional[str] = None
    blog_link: Optional[str] = None


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
