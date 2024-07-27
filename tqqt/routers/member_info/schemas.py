from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MemberInfoBase(BaseModel):
    first_name: str
    last_name: str
    title: str
    member_id: int
    description: Optional[str] = None


class MemberInfoCreate(MemberInfoBase):
    pass


class MemberInfo(MemberInfoBase):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
