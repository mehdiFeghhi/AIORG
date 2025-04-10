from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship,Session
from app.database import Base
from typing import Any
from fastapi import UploadFile
from khayyam import JalaliDatetime
from app.services.file_service import save_file_to_disk
from app.models.files.exam_info import ExamDetails
import os


class DataFile(Base):
    __tablename__ = "data_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Foreign key to link with ExamDetails
    exam_id = Column(Integer, ForeignKey('exam_details.id'), nullable=False)


    @classmethod
    def add_file(
        cls,
        db: Session,
        file: UploadFile,
        exam_id: int,
        created_at: str
    ) -> "DataFile":
        """
        Adds a file to the database after saving it to disk with proper validation.

        Args:
            db: SQLAlchemy database session
            file: The uploaded file
            exam_id: ID of the related exam (must exist in database)
            created_at: Persian calendar datetime string in format "YYYY/MM/DD"

        Returns:
            The created DataFile object

        Raises:
            ValueError: For invalid date format or non-existent exam_id
            RuntimeError: For other operational errors
        """
        # Validate exam exists first (before file operations)
        exam = db.query(ExamDetails).get(exam_id)
        if not exam:
            raise ValueError(f"Exam with ID {exam_id} does not exist")

        try:
            # Validate and convert date
            jalali_datetime = JalaliDatetime.strptime(created_at, "%Y/%m/%d")
            gregorian_datetime = jalali_datetime.todatetime()
        except ValueError as e:
            raise ValueError("Invalid Persian calendar datetime format. Use YYYY/MM/DD") from e

        try:
            # Save file to disk
            file_path = save_file_to_disk(file, f"exam_{exam_id}")

            # Create and save record
            data_file = cls(
                name=file.filename,
                path=file_path,
                created_at=gregorian_datetime,
                exam_id=exam_id
            )
            
            db.add(data_file)
            db.commit()
            db.refresh(data_file)
            
            return data_file

        except Exception as e:
            db.rollback()
            # Clean up file if it was saved but DB operation failed
            if 'file_path' in locals():
                try:
                    os.remove(file_path)
                except OSError:
                    pass  # Don't mask original error
            
            raise RuntimeError(f"Failed to add file: {str(e)}") from e


    @classmethod
    def get_files_by_exam_id(cls, db: Session, exam_id: int) -> dict:
        """
        Retrieves all files for a given exam ID, organized by creation year in the Persian calendar.

        Args:
            db (Session): SQLAlchemy database session.
            exam_id (int): The ID of the exam to filter files by.

        Returns:
            dict: A dictionary where the keys are creation years (in the Persian calendar)
                and the values are lists of file paths for that year.
        """
        # Query the database for all files related to the given exam_id
        records = db.query(cls).filter(cls.exam_id == exam_id).all()

        # Organize results into the desired dictionary format
        files_by_year = {}

        for record in records:
            # Extract the creation date and convert to Persian calendar year
            persian_year = JalaliDatetime(record.created_at).year

            # Initialize the year's entry in the dictionary if it doesn't exist
            if persian_year not in files_by_year:
                files_by_year[persian_year] = []

            # Append the file path to the corresponding year
            files_by_year[persian_year].append(record.path)

        return files_by_year
