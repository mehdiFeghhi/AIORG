import pytest
from app.models.files.exam_info import ExamDetails

def test_add_exam(db_session):
    """Test adding a new exam using the add_exam method."""
    new_exam = ExamDetails.add_exam(db_session, title="Physics Exam", creator_name="Dr. Smith", description="Advanced Physics test")

    assert new_exam is not None
    assert new_exam.title == "Physics Exam"
    assert new_exam.creator_name == "Dr. Smith"
    assert new_exam.description == "Advanced Physics test"


def test_get_exam_list(db_session):
    """Test retrieving a list of exams using get_exam_list."""
    exam1 = ExamDetails.add_exam(db_session, title="Math Exam", creator_name="Alice")
    exam2 = ExamDetails.add_exam(db_session, title="History Exam", creator_name="Bob")

    exam_list = ExamDetails.get_exam_list(db_session)

    # Verify that the exam titles exist in the retrieved list
    assert (exam1.id, "Math Exam") in exam_list
    assert (exam2.id, "History Exam") in exam_list

