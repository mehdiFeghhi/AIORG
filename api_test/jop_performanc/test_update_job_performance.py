import pytest
import sys
import os
from fastapi.testclient import TestClient
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.database import SessionLocal, engine
from app.models.job_performance.job_performance import JobPerformance

@pytest.fixture(scope="module")
def db_session():
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_update_job_performance(db_session):
    # Define the test timestamp
    test_created_at = "2025-04-07 00:00:00"
    dt_created_at = datetime.strptime(test_created_at, "%Y-%m-%d %H:%M:%S")

    # Insert initial job performance record
    new_record = JobPerformance(
        person_id=4,
        job_efficiency_rank=60.0,
        improvement_rank=65.0,
        satisfaction_score=70.0,
        job_id=5,
        created_at=dt_created_at
    )
    db_session.add(new_record)
    db_session.commit()

    # Prepare client and update request
    client = TestClient(app)
    update_params = {
        "created_at": "1404/01/19",
        "job_efficiency_rank": 62.0,
        "improvement_rank": 67.0,
        "satisfaction_score": 72.0
    }

    response = client.put("/job_performance/update/4/5", params=update_params)
    assert response.status_code == 200

    data = response.json()
    assert data["person_id"] == 4
    assert data["job_id"] == 5
    assert data["job_efficiency_rank"] == 62.0
    assert data["improvement_rank"] == 67.0
    assert data["satisfaction_score"] == 72.0
    assert data["created_at"] == test_created_at
