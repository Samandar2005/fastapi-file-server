from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProjectBase(BaseModel):
    title: str
    body: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    logo: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True
