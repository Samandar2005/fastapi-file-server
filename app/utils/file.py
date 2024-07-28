import os
from typing import Tuple
import pandas as pd
from datetime import datetime


def save_file_to_disk(upload_folder: str, file_data: bytes, filename: str) -> Tuple[str, str]:
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
    file_path = os.path.join(upload_folder, unique_name)

    with open(file_path, "wb") as f:
        f.write(file_data)

    return unique_name, file_path


def save_to_excel(file_data: dict, excel_path: str):
    new_data = pd.DataFrame([file_data])

    if not os.path.isfile(excel_path):
        new_data.to_excel(excel_path, index=False)
    else:
        df = pd.read_excel(excel_path)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(excel_path, index=False)