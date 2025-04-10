# tests/exams/test_get_exams.py
import pytest
import sys
import os
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.database import SessionLocal, engine, get_db
from app.models.files.exam_info import ExamDetails

@pytest.fixture(scope="module")
def db_session():
    # Create a new transaction for each test module
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    # Apply migrations or create tables if needed
    # Base.metadata.create_all(bind=connection)
    
    yield session
    
    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def test_client(db_session):
    # Override the database dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session here
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def test_exam(db_session):
    exam = ExamDetails(
        title="Test Exam",
        creator_name="Tester"
    )
    db_session.add(exam)
    db_session.commit()
    db_session.refresh(exam)
    yield exam
    db_session.delete(exam)
    db_session.commit()

def test_get_exam_id_name_success(test_client, test_exam):
    response = test_client.get("/files/exam_name")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["message"] == "Exams retrieved successfully"
    assert len(data["exams"]) >= 1
    assert any(e["id"] == test_exam.id and e["title"] == test_exam.title 
              for e in data["exams"])

def test_get_exam_id_name_no_exams(test_client, db_session):
    # Clear exams using the same session
    db_session.query(ExamDetails).delete()
    db_session.commit()
    
    response = test_client.get("/files/exam_name")
    # print(response.json()["detail"])
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No exams found"

def test_get_exam_id_name_database_error(test_client, db_session, monkeypatch):
    # Monkeypatch to simulate database failure
    def mock_get_exam_list(db):
        raise Exception("Simulated database error")
    
    monkeypatch.setattr(ExamDetails, "get_exam_list", mock_get_exam_list)
    
    response = test_client.get("/files/exam_name")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Simulated database error" in response.json()["detail"]