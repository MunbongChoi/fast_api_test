import os
import uuid
from typing import Tuple

STORAGE_DIR = "uploaded_files"

def save_file(file_bytes: bytes, filename: str = None) -> Tuple[str, str]:
    """
    :return: (저장된 파일 경로, 실제 저장된 파일명)
    """
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    if filename is None:
        filename = str(uuid.uuid4())  # 유니크한 파일명

    file_path = os.path.join(STORAGE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path, filename

def get_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()
