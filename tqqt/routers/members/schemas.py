from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MemberBase(BaseModel):
    full_name: str
    image: Optional[str] = None
    short_description: Optional[str] = None
    full_info_link: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
