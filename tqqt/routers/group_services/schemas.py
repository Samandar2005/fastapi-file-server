from pydantic import BaseModel


class GroupServicesBase(BaseModel):
    group_id: int
    service_id: int


class GroupServicesCreate(GroupServicesBase):
    pass


class GroupServices(GroupServicesBase):
    class Config:
        orm_mode = True
