import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.database import SessionLocal, engine, get_db
from app.models.AI.ModelDetails import ModelDetails
from app.models.files.exam_info import ExamDetails
from sqlalchemy.orm import Session


@pytest.fixture(scope="module")
def db_session():
    SessionLocal.configure(bind=engine)
    db: Session = SessionLocal()

    # Create exam record
    exam = ExamDetails(
        id=101,
        title="AI Fundamentals Exam",
        creator_name="Dr. Mehdi",
        description="Basic AI evaluation."
    )
    db.add(exam)
    db.commit()

    # Create model records
    model1 = ModelDetails(
        name_object_predict="ModelA",
        address="192.168.1.10",
        feature_engineering_details_address="fe_address1",
        architecture="ResNet",
        accuracy_results={"accuracy": 0.97},
        f1_score_results={"f1": 0.89},
        precision_results={"precision": 0.87},
        recall_results={"recall": 0.88},
        t_test_results_accuracy={"t_stat": 2.1},
        t_test_results_f1_score={"t_stat": 2.0},
        confidence_level_accuracy=0.95,
        confidence_level_f1_score=0.93,
        num_all_samples=1000,
        num_features=30,
        split_test=0.2,
        n_splits_t_test=5,
        number_of_labels=3,
        model_evaluation_date=datetime(2023, 1, 1),
        version="2.0",
        exam_id=101,
        job_id=303
    )

    model2 = ModelDetails(
        name_object_predict="ModelB",
        address="192.168.1.20",
        feature_engineering_details_address="fe_address2",
        architecture="RNN",
        accuracy_results={"accuracy": 0.88},
        f1_score_results={"f1": 0.85},
        precision_results={"precision": 0.84},
        recall_results={"recall": 0.86},
        t_test_results_accuracy={"t_stat": 2.5},
        t_test_results_f1_score={"t_stat": 2.3},
        confidence_level_accuracy=0.94,
        confidence_level_f1_score=0.92,
        num_all_samples=900,
        num_features=25,
        split_test=0.2,
        n_splits_t_test=5,
        number_of_labels=3,
        model_evaluation_date=datetime(2024, 1, 1),
        version="2.1",
        exam_id=101,
        job_id=303
    )

    db.add_all([model1, model2])
    db.commit()
    db.refresh(model1)
    db.refresh(model2)

    yield db, model1.id, model2.id

    db.query(ModelDetails).delete()
    db.query(ExamDetails).delete()
    db.commit()
    db.close()


@pytest.fixture(scope="module")
def client_with_db(db_session):
    db, _, _ = db_session

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_find_model_details_by_id_success(client_with_db, db_session):
    _, model1_id, _ = db_session
    response = client_with_db.get("/search_model/details_by_id", params={"query_id": model1_id})
    # print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "192.168.1.10"
    assert data["architecture"] == "ResNet"
    assert data["accuracy_results"]["accuracy"] == 0.97


def test_find_model_details_by_id_not_found(client_with_db):
    response = client_with_db.get("/search_model/details_by_id", params={"query_id": 999999})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_find_models_by_exam_and_job(client_with_db):
    response = client_with_db.get("/search_model/details_by_exam_and_job", params={"exam_id": 101, "job_id": 303})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    versions = sorted([model["version"] for model in data])
    assert versions == ["2.0", "2.1"]