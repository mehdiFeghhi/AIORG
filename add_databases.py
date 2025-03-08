# create_table.py

from app.database import engine, Base
from app.models.AI.ModelDetails import ModelDetails  # Import your ExamDetails model
from app.models.files.data_file import DataFile
from app.models.files.exam_info import ExamDetails
from app.models.job_performance.job_performance import JobPerformance
# Create all tables (this will create the exam_details table if it doesn't exist)
Base.metadata.create_all(bind=engine)

print("Table created successfully.")
