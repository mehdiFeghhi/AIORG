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
from app.models.job_performance.job_performance import JobPerformance

@pytest.fixture(scope="module")
def db_session():
    SessionLocal.configure(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def test_get_performance_by_job(db_session):
    # Insert test record using Gregorian date
    gregorian_created_at = datetime.strptime("2025-04-07 10:00:00", "%Y-%m-%d %H:%M:%S")
    jalali_year = JalaliDatetime(gregorian_created_at).year  # Should be 1404

    new_record = JobPerformance(
        person_id=2,
        job_efficiency_rank=75.0,
        improvement_rank=80.0,
        satisfaction_score=85.0,
        job_id=3,
        created_at=gregorian_created_at
    )
    db_session.add(new_record)
    db_session.commit()

    client = TestClient(app)
    job_id = 3
    performance_metric = "job_efficiency_rank"

    response = client.get(f"/job_performance/performance/{job_id}/{performance_metric}")
    
    print(response.json())  # Debug output

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert str(jalali_year) in data

    performance_data = data[str(jalali_year)]
    assert any(entry["performance_value"] == 75.0 for entry in performance_data)
