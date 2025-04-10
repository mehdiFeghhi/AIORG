# exam_file/test_upload_file.py
import pytest
import sys
import os
from fastapi.testclient import TestClient
from datetime import datetime
from khayyam import JalaliDatetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.database import SessionLocal, engine
from app.models.files.exam_info import ExamDetails
from app.models.files.data_file import DataFile


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_exam(db_session):
    exam = ExamDetails.add_exam(
        db=db_session,
        title="Upload Test Exam",
        creator_name="Test User"
    )
    yield exam.id
    # Cleanup
    db_session.query(DataFile).filter(DataFile.exam_id == exam.id).delete()
    db_session.delete(db_session.query(ExamDetails).get(exam.id))
    db_session.commit()

def test_upload_file_success(test_client, db_session, test_exam):
    # Create a Persian calendar date string
    persian_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    
    test_file = ("test.txt", b"test content")
    response = test_client.post(
        "/files/upload_file",
        files={"file": test_file},
        data={
            "exam_id": test_exam,
            "created_at": persian_date  # Now using correct format
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert db_session.query(DataFile).get(data["data_file_id"]) is not None

def test_upload_file_invalid_exam(test_client):
    # Create a Persian calendar date string
    persian_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    
    response = test_client.post(
        "/files/upload_file",
        files={"file": ("dummy.txt", b"content")},
        data={
            "exam_id": 99999,  # Non-existent exam
            "created_at": persian_date  # Using correct format
        }
    )
    assert response.status_code == 422

def test_upload_file_invalid_date_format(test_client, test_exam):
    response = test_client.post(
        "/files/upload_file",
        files={"file": ("dummy.txt", b"content")},
        data={
            "exam_id": test_exam,
            "created_at": "2023-12-31"  # Wrong format (Gregorian ISO)
        }
    )
    assert response.status_code == 422