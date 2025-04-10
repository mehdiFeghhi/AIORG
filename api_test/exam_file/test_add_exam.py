# exam_file/test_add_exam.py
import pytest
import sys
import os
from fastapi.testclient import TestClient


# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app  # Now this will work
from app.database import SessionLocal, engine
from app.models.files.exam_info import ExamDetails


@pytest.fixture(scope="module")
def db_session():
    # ساخت دیتابیس برای تست
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# تست اضافه کردن یک آزمون جدید
def test_add_exam(db_session):
    # ساخت تست کلاینت FastAPI
    client = TestClient(app)
    
    # ارسال داده برای افزودن آزمون جدید
    response = client.post(
        "/files/add_exam",
        data={
            "title": "Test Exam",
            "creator_name": "John Doe",
            "description": "This is a test exam."
        }
    )

    # بررسی وضعیت پاسخ
    assert response.status_code == 201
    data = response.json()
    exam_id = data["exam_id"]

    # بررسی ذخیره شدن داده در دیتابیس
    exam = db_session.query(ExamDetails).filter(ExamDetails.id == exam_id).first()
    assert exam is not None
    assert exam.title == "Test Exam"
    assert exam.creator_name == "John Doe"
    assert exam.description == "This is a test exam."



def test_add_exam_missing_title(db_session):
    client = TestClient(app)
    response = client.post(
        "/files/add_exam",
        data={
            "creator_name": "Dr. Smith",
            "description": "Missing title test"
        }
    )
    assert response.status_code == 422  # FastAPI validation error

