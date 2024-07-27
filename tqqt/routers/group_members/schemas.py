from pydantic import BaseModel
from datetime import datetime


class GroupMemberBase(BaseModel):
    group_id: int
    member_id: int


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMember(GroupMemberBase):
    created_date: datetime
    updated_date: datetime

    class Config:
        orm_mode = True
