from tortoise.transactions import in_transaction
from app.models.file import File
from app.schemas.file import FileCreate
import hashlib


async def get_file_by_hash(hash_code: str):
    return await File.filter(hash_code=hash_code).first()


async def create_file(file: FileCreate):
    async with in_transaction() as connection:
        db_file = File(**file.dict())
        await db_file.save(using_db=connection)
        return db_file


def hash_file(file_data: bytes):
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest()
