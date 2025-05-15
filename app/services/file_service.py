import os
from fastapi import UploadFile

# تعیین مسیر اصلی برنامه (دایرکتوری جاری فایل پایتون)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مسیر دایرکتوری آپلود (بدون استفاده از فایل env)
UPLOAD_DIR_NAME = "uploaded_files"

# مسیر کامل برای ذخیره‌سازی فایل‌ها
UPLOAD_DIR = os.path.join(BASE_DIR, UPLOAD_DIR_NAME)


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure the given directory exists; create it if necessary.
    """
    os.makedirs(directory, exist_ok=True)

def get_upload_path(title: str) -> str:
    """
    Generate the upload path for a given title.
    """
    return os.path.join(UPLOAD_DIR, title)

def save_file_to_disk(file: UploadFile, title: str) -> str:
    """
    Save the uploaded file to the disk inside a designated directory and return the file path.
    """
    try:
        upload_path = get_upload_path(title)
        ensure_directory_exists(upload_path)

        file_path = os.path.join(upload_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to save file: {str(e)}")
