import os
from typing import Tuple
import pandas as pd
from datetime import datetime


def save_file_to_disk(upload_folder: str, file_data: bytes, filename: str) -> Tuple[str, str]:
    """
    Save a file to disk with a unique name.

    Args:
        upload_folder (str): The folder to save the file.
        file_data (bytes): The file data in bytes.
        filename (str): The original file name.

    Returns:
        Tuple[str, str]: A tuple containing the unique name and file path.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
    file_path = os.path.join(upload_folder, unique_name)

    with open(file_path, "wb") as f:
        f.write(file_data)

    return unique_name, file_path


def save_to_excel(file_data: dict, excel_path: str):
    """
    Save data to an Excel file. If the file already exists, append the data.

    Args:
        file_data (dict): The data to be saved.
        excel_path (str): The path to the Excel file.
    """
    new_data = pd.DataFrame([file_data])

    if not os.path.isfile(excel_path):
        new_data.to_excel(excel_path, index=False)
    else:
        df = pd.read_excel(excel_path)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(excel_path, index=False)