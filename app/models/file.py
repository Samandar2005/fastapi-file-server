from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    saved_name = Column(String, index=True)
    path = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
    hash_code = Column(String, index=True)
    server = Column(String, index=True)
    is_used_by_other_servers = Column(Boolean, default=False)
    shareable = Column(Boolean, default=True)
    public = Column(Boolean, default=True)
    size = Column(Integer)
    format = Column(String)
