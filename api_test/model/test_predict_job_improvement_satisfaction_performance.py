import os
import sys
import pytest
from fastapi import status
from fastapi.testclient import TestClient

# Add project root to path so app imports work
tail = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, tail)

import numpy as np
import pandas as pd
from app.main import app
from app.database import get_db
from app.models.files.exam_info import ExamDetails

# --- Fixtures for DB setup (reuse from train tests) ---

@pytest.fixture(scope="module")
def db_session():
    from app.database import SessionLocal, engine
    SessionLocal.configure(bind=engine)
    db = SessionLocal()

    exam = db.query(ExamDetails).filter_by(id=1).first()
    if not exam:
        exam = ExamDetails(
            id=1,
            title="Sample Exam",
            description="This is a test exam",
            creator_name="Mehdi",
        )
        db.add(exam)
        db.commit()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_test_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

# --- Fixtures to monkey-patch prediction logic ---

@pytest.fixture
def mock_predict_utils_and_loader(monkeypatch):
    """
    - Always find the person
    - Always return "dummy_result"
    """
    # Always “find” the person
    def fake_find(person_id, files_by_year):
        return ({"foo": 1, "bar": 2}, True)
    monkeypatch.setattr("app.api.model.find_person_feature_last_exam", fake_find)

    # Always return a dummy result
    def fake_predict(name_object, data_person, model_id, db):
        return "dummy_result"
    monkeypatch.setattr("app.api.model.predict_job_utils", fake_predict)

@pytest.fixture
def mock_person_not_found(monkeypatch):
    def fake_find(person_id, files_by_year):
        return ({}, False)
    monkeypatch.setattr("app.api.model.find_person_feature_last_exam", fake_find)

@pytest.fixture
def mock_predict_value_error(monkeypatch):
    # Person is found
    def fake_find(person_id, files_by_year):
        return ({"foo": 1}, True)
    monkeypatch.setattr("app.api.model.find_person_feature_last_exam", fake_find)

    # predict_job_utils raises ValueError
    def fake_predict(name_object, data_person, model_id, db):
        raise ValueError("bad input")
    monkeypatch.setattr("app.api.model.predict_job_utils", fake_predict)

@pytest.fixture
def mock_predict_exception(monkeypatch):
    # Person is found
    def fake_find(person_id, files_by_year):
        return ({"foo": 1}, True)
    monkeypatch.setattr("app.api.model.find_person_feature_last_exam", fake_find)

    # predict_job_utils raises generic Exception
    def fake_predict(name_object, data_person, model_id, db):
        raise RuntimeError("something broke")
    monkeypatch.setattr("app.api.model.predict_job_utils", fake_predict)

# --- Tests ---

@pytest.mark.parametrize("endpoint", [
    "/model/predict_job_satisfaction",
    "/model/predict_job_improvement",
    "/model/predict_job_performance",
])
def test_predict_routes_success(endpoint, mock_predict_utils_and_loader):
    """All prediction endpoints return 200 with dummy_result."""
    response = client.post(
        endpoint,
        params={"person_id": 1, "model_id": 42, "exam_id": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Prediction successful",
        "result": "dummy_result"
    }

@pytest.mark.parametrize("endpoint", [
    "/model/predict_job_satisfaction",
    "/model/predict_job_improvement",
    "/model/predict_job_performance",
])
def test_predict_person_not_found(endpoint, mock_person_not_found):
    """When the person isn’t in any file, should return the “not involved” message."""
    response = client.post(
        endpoint,
        params={"person_id": 999, "model_id": 42, "exam_id": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Prediction faild",
        "result": "This person don't involve in this exam before."
    }

@pytest.mark.parametrize("endpoint", [
    "/model/predict_job_satisfaction",
    "/model/predict_job_improvement",
    "/model/predict_job_performance",
])
def test_predict_validation_error(endpoint, mock_predict_value_error):
    """A ValueError in predict_job_utils should yield a 422."""
    response = client.post(
        endpoint,
        params={"person_id": 1, "model_id": 42, "exam_id": 1}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Validation error: bad input" in response.json()["detail"]

@pytest.mark.parametrize("endpoint", [
    "/model/predict_job_satisfaction",
    "/model/predict_job_improvement",
    "/model/predict_job_performance",
])
def test_predict_generic_exception(endpoint, mock_predict_exception):
    """A generic exception in predict_job_utils should yield a 500."""
    response = client.post(
        endpoint,
        params={"person_id": 1, "model_id": 42, "exam_id": 1}
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Prediction error: something broke" in response.json()["detail"]
