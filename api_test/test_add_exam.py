# app/tests/test_exam.py
import pytest
from fastapi.testclient import TestClient
from ..app.main import app  # فرض بر این است که FastAPI app در این مسیر باشد
from ..app.database import SessionLocal, engine
from ..app.models.files.exam_info import ExamDetails
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))


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
        "/add_exam",
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

