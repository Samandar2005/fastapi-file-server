from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GroupBase(BaseModel):
    title: str
    logo: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
