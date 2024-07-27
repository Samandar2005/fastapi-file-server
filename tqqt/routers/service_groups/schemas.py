from pydantic import BaseModel
from typing import Optional


class ServiceGroupBase(BaseModel):
    title: str
    logo: Optional[str] = None


class ServiceGroupCreate(ServiceGroupBase):
    pass


class ServiceGroupUpdate(ServiceGroupBase):
    pass


class ServiceGroup(ServiceGroupBase):
    id: int

    class Config:
        orm_mode = True
