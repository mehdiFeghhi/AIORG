from starlette.datastructures import UploadFile
import os
import io

from app.models.files.data_file import DataFile
from app.database import SessionLocal

db = SessionLocal()

folder_path = "/app/output_csv"
exam_id = 1

for shamsi_year in range(1393, 1404):
    filename = f"features_{shamsi_year}.csv"
    filepath = os.path.join(folder_path, filename)

    try:
        with open(filepath, "rb") as f:
            file_content = f.read()
            upload_file = UploadFile(
                filename=filename,
                file=io.BytesIO(file_content),
                # content_type="text/csv"
            )

            created_at = f"{shamsi_year}/01/01"  # مثلاً '1402/01/01'

            # اضافه کردن فایل
            data_file = DataFile.add_file(db, upload_file, exam_id, created_at)
            print(f"✅ فایل {filename} اضافه شد.")

    except Exception as e:
        print(f"❌ خطا در پردازش {filename}: {e}")
