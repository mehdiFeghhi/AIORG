import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.database import SessionLocal, engine
from app.models.job_performance.job_performance import JobPerformance
from khayyam import JalaliDatetime


@pytest.fixture(scope="module")
def db_session():
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_add_job_performance(db_session):
    client = TestClient(app)

    # Jalali date equivalent to 2025-04-07
    test_created_at = "1404/01/19"
    
    response = client.post(
        "/job_performance/add",
        params={
            "person_id": 1,
            "job_efficiency_rank": 88.5,
            "improvement_rank": 90.0,
            "satisfaction_score": 95.0,
            "job_id": 2,
            "created_at": test_created_at
        }
    )
    
    print(response.json())  # Debug output
    assert response.status_code in (200, 201)

    data = response.json()
    job_perf_id = data.get("id")
    assert job_perf_id is not None

    # Verify DB entry
    record = db_session.query(JobPerformance).filter(JobPerformance.id == job_perf_id).first()
    assert record is not None
    assert record.person_id == 1
    assert record.job_efficiency_rank == 88.5
    assert record.improvement_rank == 90.0
    assert record.satisfaction_score == 95.0
    assert record.job_id == 2

    # Check that Jalali conversion matches the input
    created_at_jalali = JalaliDatetime(record.created_at).strftime("%Y/%m/%d")
    assert created_at_jalali == test_created_at
