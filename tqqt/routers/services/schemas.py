from pydantic import BaseModel
from typing import Optional


class ServiceBase(BaseModel):
    service_name: str
    image: Optional[str] = None
    short_description: Optional[str] = None
    full_info_link: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True
