from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.files.data_file import DataFile
from app.models.files.exam_info import ExamDetails
from typing import List, Dict, Union
from app.database import get_db

router = APIRouter()


@router.post("/upload_file", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str | int])
async def upload_file(
    file: UploadFile = File(...),
    exam_id: int = Form(...),
    created_at: str = Form(...),
    db: Session = Depends(get_db)
) -> Dict[str, str | int]:
    """
    Upload a file, save it to disk, and associate it with an exam.
    """
    try:
        # Call the DataFile class method to handle file upload and save
        data_file = DataFile.add_file(db, file, exam_id, created_at)

        return {"message": "File uploaded successfully", "data_file_id": data_file.id}

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(re)
        )



@router.post("/add_exam", status_code=status.HTTP_201_CREATED)
async def add_exam(
    title: str = Form(...),
    creator_name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Add a new exam to the database using the ExamDetails class method.

    Args:
        title (str): The title of the exam.
        creator_name (str): The name of the creator of the exam.
        description (str, optional): The description of the exam.
        db (Session): The database session.

    Returns:
        dict: Success message with the newly created exam ID.
    """
    try:
        # Call the class method to add the exam
        new_exam = ExamDetails.add_exam(db, title, creator_name, description)

        return {
            "message": "Exam added successfully",
            "exam_id": new_exam.id
        }

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while adding the exam: {str(e)}"
        )

@router.get("/exam_name", status_code=status.HTTP_200_OK, response_model=Dict[str, Union[str, List[Dict[str, Union[int, str]]]]])
async def get_exam_id_name(db: Session = Depends(get_db)) -> Dict[str, Union[str, List[Dict[str, Union[int, str]]]]]:

    """
    Retrieve a list of all exams as dictionaries with their ID and name.
    """
    try:
        # Call the class method to retrieve the list of exams
        exams = ExamDetails.get_exam_list(db)

        if not exams:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No exams found"
            )

        # Convert the result into a list of dictionaries
        exams_list = [{"id": exam[0], "title": exam[1]} for exam in exams]

        return {
            "message": "Exams retrieved successfully",
            "exams": exams_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
