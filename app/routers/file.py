from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import file as crud_file
from app.schemas.file import FileCreate
from app.utils.file import save_file_to_disk, save_to_excel
import os
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_FOLDER = "app/uploaded_files"
EXCEL_PATH = "app/file_records.xlsx"
DEFAULT_SERVER = "localhost"


@router.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        file_data = await file.read()
        hash_code = crud_file.hash_file(file_data)

        existing_file = crud_file.get_file_by_hash(db, hash_code)
        if existing_file:
            duplicate_file_info = FileCreate(
                name=file.filename,
                saved_name=existing_file.saved_name,
                path=existing_file.path,
                hash_code=hash_code,
                server=DEFAULT_SERVER,
                shareable=True,
                public=True,
                size=len(file_data),
                format=file.content_type
            )
            crud_file.create_file(db, duplicate_file_info)
            saved_date = existing_file.path.split(os.sep)[-2]
            return {
                "message": "File already exists",
                "url": f"/{saved_date}/{existing_file.saved_name}"
            }

        current_date = datetime.now().strftime("%Y-%m-%d")
        daily_folder = os.path.join(UPLOAD_FOLDER, current_date)
        if not os.path.exists(daily_folder):
            os.makedirs(daily_folder)

        unique_filename = f"{uuid.uuid4().hex}"

        saved_name, file_path = save_file_to_disk(daily_folder, file_data, unique_filename)
        file_size = len(file_data)

        file_info = FileCreate(
            name=file.filename,
            saved_name=saved_name,
            path=file_path,
            hash_code=hash_code,
            server=DEFAULT_SERVER,
            shareable=True,
            public=True,
            size=file_size,
            format=file.content_type
        )

        db_file = crud_file.create_file(db, file_info)
        save_to_excel(file_info.dict(), EXCEL_PATH)

        return {
            "message": "File uploaded successfully",
            "url": f"/{current_date}/{saved_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{date}/{filename}")
async def get_file(date: str, filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, date, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)