import os
from typing import Tuple
import pandas as pd
from datetime import datetime
from fastapi import HTTPException
from .security import encrypt_file

# Ruxsat etilgan fayl turlari va maksimal hajm
ALLOWED_EXTENSIONS = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

# Export for tests
__all__ = ['ALLOWED_EXTENSIONS']

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file(content_type: str, file_size: int):
    """Fayl turini va hajmini tekshirish"""
    if content_type not in ALLOWED_EXTENSIONS.values():
        raise HTTPException(status_code=400, detail=f"File type not allowed. Allowed types are: {', '.join(ALLOWED_EXTENSIONS.keys())}")
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB")

def save_file_to_disk(upload_folder: str, file_data: bytes, filename: str) -> Tuple[str, str]:
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
    file_path = os.path.join(upload_folder, unique_name)

    # Faylni shifrlash
    encrypted_data = encrypt_file(file_data)
    
    with open(file_path, "wb") as f:
        f.write(encrypted_data)

    return unique_name, file_path


def save_to_excel(file_data: dict, excel_path: str):
    new_data = pd.DataFrame([file_data])

    if not os.path.isfile(excel_path):
        new_data.to_excel(excel_path, index=False)
    else:
        df = pd.read_excel(excel_path)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(excel_path, index=False)