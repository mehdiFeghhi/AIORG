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
from app.utils.train_helper_method import ModelName
from app.models.files.exam_info import ExamDetails
import pandas as pd

# --- Fixtures ---

@pytest.fixture(scope="module")
def db_session():
    """Provide a SQLAlchemy session for tests (bind to test DB)."""
    from app.database import SessionLocal, engine
    SessionLocal.configure(bind=engine)
    db = SessionLocal()

    # Ensure a related exam record exists to satisfy foreign key constraint
    exam = db.query(ExamDetails).filter_by(id=1).first()
    if not exam:
        exam = ExamDetails(
            id=1,
            title="Sample Exam",  # Adjust fields according to your model
            description="This is a test exam",
            creator_name="Mehdi",  # if your model requires a date
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

@pytest.fixture
def mock_make_dataset(monkeypatch):
    """Monkey-patch make_dataset to return dummy features and labels."""
    """Monkey-patch make_dataset to return a realistic dummy dataset."""

    def fake_make_dataset(job_id, exam_id, target_col, db):
        np.random.seed(42)  # reproducibility
        num_samples = 100
        num_features = 6

        # ساخت دیتافریم با مقادیر تصادفی برای ویژگی‌ها
        X = pd.DataFrame(
            np.random.rand(num_samples, num_features),
            columns=[f"feature_{i}" for i in range(num_features)]
        )

        # ساخت برچسب باینری یا عددی برای ستون هدف
        if target_col in ["satisfaction_score", "job_improvement"]:
            y = pd.Series(np.random.randint(0, 100, size=num_samples))  
        elif target_col == "job_performance":
            y = pd.Series(np.random.randint(0, 100, size=num_samples))  
        else:
            y = pd.Series(np.random.randint(0, 100, size=num_samples))

        return X, y

    monkeypatch.setattr(
        # "app.services.pre_processing_data_service.make_dataset",
        "app.api.model.make_dataset",
        fake_make_dataset
    )

# --- Test Client ---
client = TestClient(app)

# --- Parameterized Tests ---

@pytest.mark.parametrize("endpoint", [
    "/model/train_job_satisfaction",
    "/model/train_job_improvement",
    "/model/train_job_performance",
])
@pytest.mark.parametrize("model_name_enum", list(ModelName))
def test_train_routes_success(endpoint, model_name_enum, mock_make_dataset):
    """Ensure each train endpoint returns 200 and triggers real train_model."""
    payload = {
        "job_id": 1,
        "exam_id": 1,
        "model_name": model_name_enum.value,
        "num_classes": 3
    }
    response = client.post(endpoint, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Model trained and saved successfully"}

def test_invalid_model_name(mock_make_dataset):
    """Passing an invalid model_name should result in a 422 validation error."""
    response = client.post(
        "/model/train_job_satisfaction",
        json={
            "job_id": 1,
            "exam_id": 1,
            "model_name": "UNKNOWN",
            "num_classes": 2
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
