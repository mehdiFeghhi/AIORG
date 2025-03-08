import pytest
from app.models.files.exam_info import ExamDetails

def test_exam_details_crud_operations(db_session):
    """Integration test for full CRUD operations on ExamDetails."""

    # Create
    exam = ExamDetails.add_exam(db_session, title="Biology Exam", creator_name="Dr. Jane")
    assert exam is not None
    assert exam.title == "Biology Exam"

    # Read
    retrieved_exam = db_session.query(ExamDetails).filter_by(title="Biology Exam").first()
    assert retrieved_exam is not None
    assert retrieved_exam.creator_name == "Dr. Jane"

    # Update
    retrieved_exam.creator_name = "Dr. John"
    db_session.commit()
    
    updated_exam = db_session.query(ExamDetails).filter_by(title="Biology Exam").first()
    assert updated_exam.creator_name == "Dr. John"

    # Delete
    db_session.delete(updated_exam)
    db_session.commit()

    deleted_exam = db_session.query(ExamDetails).filter_by(title="Biology Exam").first()
    assert deleted_exam is None
