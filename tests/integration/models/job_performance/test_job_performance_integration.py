import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models.job_performance.job_performance import JobPerformance
from app.database import Base
from khayyam import JalaliDatetime

# --- Pytest fixture for a temporary in-memory database session ---

@pytest.fixture(scope="function")
def db_session():
    """
    Create an in-memory SQLite database, create all tables, and yield a session.
    After the test, the session is closed and tables dropped.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

# --- Integration tests ---

def test_add_performance_integration(db_session):
    """
    Test that add_performance correctly converts a Jalali date string,
    creates a JobPerformance record, and stores a Gregorian datetime.
    """
    created_at = "1403/11/10"  # Jalali date string
    performance = JobPerformance.add_performance(
        db=db_session,
        person_id=1,
        job_efficiency_rank=8.5,
        improvement_rank=7.0,
        satisfaction_score=9.0,
        job_id=101,
        created_at=created_at
    )
    # Query the record from the database
    result = db_session.query(JobPerformance).filter_by(id=performance.id).first()
    assert result is not None
    assert result.person_id == 1
    assert result.job_efficiency_rank == 8.5
    assert result.improvement_rank == 7.0
    assert result.satisfaction_score == 9.0
    assert result.job_id == 101
    # Verify that the created_at field is now a Gregorian datetime
    assert isinstance(result.created_at, datetime)

def test_get_performance_by_job_and_date_integration(db_session):
    """
    Insert two records for the same job_id and verify that get_performance_by_job_and_date
    groups the results by Persian calendar year.
    """
    # Insert two records with created_at values that convert to a Persian year.
    perf1 = JobPerformance.add_performance(
        db=db_session,
        person_id=1,
        job_efficiency_rank=8.0,
        improvement_rank=7.5,
        satisfaction_score=9.0,
        job_id=101,
        created_at="1403/01/10"
    )
    perf2 = JobPerformance.add_performance(
        db=db_session,
        person_id=2,
        job_efficiency_rank=7.5,
        improvement_rank=8.0,
        satisfaction_score=8.5,
        job_id=101,
        created_at="1403/06/15"
    )

    # Call the method under test
    result = JobPerformance.get_performance_by_job_and_date(
        db=db_session,
        job_id=101,
        performance_metric="job_efficiency_rank"
    )
    # Determine the expected Persian year from one of the records.
    expected_year = JalaliDatetime(perf1.created_at).year
    assert isinstance(result, dict)
    assert expected_year in result
    # Two records should be grouped under the expected year
    assert len(result[expected_year]) == 2

    # Validate one of the record's data
    first_entry = result[expected_year][0]
    assert 'person_id' in first_entry
    assert 'performance_value' in first_entry

def test_get_performance_by_jobs_and_date_integration(db_session):
    """
    Insert two records with different job_ids and verify that get_performance_by_jobs_and_date
    groups the results by Persian calendar year.
    """
    perf1 = JobPerformance.add_performance(
        db=db_session,
        person_id=1,
        job_efficiency_rank=8.0,
        improvement_rank=7.5,
        satisfaction_score=9.0,
        job_id=101,
        created_at="1403/03/05"
    )
    perf2 = JobPerformance.add_performance(
        db=db_session,
        person_id=2,
        job_efficiency_rank=7.5,
        improvement_rank=8.0,
        satisfaction_score=8.5,
        job_id=102,
        created_at="1403/06/15"
    )

    result = JobPerformance.get_performance_by_jobs_and_date(
        db=db_session,
        job_ids=[101, 102],
        performance_metric="job_efficiency_rank"
    )
    # Determine the expected Persian year from one of the records.
    expected_year = JalaliDatetime(perf1.created_at).year
    assert isinstance(result, dict)
    assert expected_year in result
    # Expect two records in the grouping.
    assert len(result[expected_year]) == 2

    # Validate each record's details.
    rec0, rec1 = result[expected_year]
    # Since order might not be guaranteed, check that both job_ids are present.
    job_ids = {rec0['job_id'], rec1['job_id']}
    assert job_ids == {101, 102}

def test_invalid_performance_metric_integration(db_session):
    """
    Verify that an invalid performance_metric raises a ValueError.
    """
    with pytest.raises(ValueError):
        JobPerformance.get_performance_by_job_and_date(
            db=db_session,
            job_id=101,
            performance_metric="invalid_metric"
        )
