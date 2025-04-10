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

def test_get_performance_by_jobs(db_session):
    # Insert a test record
    test_created_at = datetime.strptime("2025-04-07", "%Y-%m-%d")
    new_record = JobPerformance(
        person_id=3,
        job_efficiency_rank=70.0,
        improvement_rank=75.0,
        satisfaction_score=80.0,
        job_id=4,
        created_at=test_created_at
    )
    db_session.add(new_record)
    db_session.commit()

    client = TestClient(app)

    performance_metric = "improvement_rank"
    job_ids_payload = {"list_job_ids": [4]}

    # Send request to the correct endpoint
    response = client.request(
        method="GET",
        url="/job_performance/performance_jobs",
        params={"performance_metric": performance_metric},
        json=job_ids_payload
    )
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 4 in data or any(str(year).isdigit() for year in data.keys())
