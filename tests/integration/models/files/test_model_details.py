import pytest
from app.models.files.exam_info import ExamDetails

def test_exam_details_integration(db_session):
    """Full CRUD integration test for ExamDetails."""
    exam = ExamDetails(title="History Exam", date="2025-05-20", duration=90)
    db_session.add(exam)
    db_session.commit()

    retrieved = db_session.query(ExamDetails).filter_by(title="History Exam").first()
    assert retrieved is not None

    retrieved.duration = 100
    db_session.commit()

    updated = db_session.query(ExamDetails).filter_by(title="History Exam").first()
    assert updated.duration == 100

    db_session.delete(updated)
    db_session.commit()

    deleted = db_session.query(ExamDetails).filter_by(title="History Exam").first()
    assert deleted is None
