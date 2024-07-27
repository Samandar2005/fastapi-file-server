from sqlalchemy.orm import Session
from app.models.file import File
from app.schemas.file import FileCreate
import hashlib


def get_file_by_hash(db: Session, hash_code: str):
    return db.query(File).filter(File.hash_code == hash_code).first()


def create_file(db: Session, file: FileCreate):
    db_file = File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def hash_file(file_data: bytes):
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest()
