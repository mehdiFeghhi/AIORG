import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.job_performance.job_performance import JobPerformance
from khayyam import JalaliDatetime

@pytest.fixture
def mock_session():
    """Fixture to provide a mocked SQLAlchemy session."""
    return MagicMock(spec=Session)

def test_add_performance(mock_session):
    # Define the input data
    person_id = 1
    job_efficiency_rank = 8.5
    improvement_rank = 7.0
    satisfaction_score = 9.0
    job_id = 101
    created_at = "1403/11/10"  # Persian date string

    # Set up the session mocks for add, commit, and refresh
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Invoke the method under test
    new_performance = JobPerformance.add_performance(
        db=mock_session,
        person_id=person_id,
        job_efficiency_rank=job_efficiency_rank,
        improvement_rank=improvement_rank,
        satisfaction_score=satisfaction_score,
        job_id=job_id,
        created_at=created_at
    )

    # Verify that the session's methods were called correctly
    mock_session.add.assert_called_once_with(new_performance)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_performance)

    # Verify that the new record has the expected attribute values
    assert new_performance.person_id == person_id
    assert new_performance.job_efficiency_rank == job_efficiency_rank
    assert new_performance.improvement_rank == improvement_rank
    assert new_performance.satisfaction_score == satisfaction_score
    assert new_performance.job_id == job_id
    # Ensure the created_at field is now a Gregorian datetime
    assert isinstance(new_performance.created_at, datetime)


def test_get_performance_by_jobs_and_date(mock_session):
    # Create two mock records with different job_ids
    record1 = JobPerformance(
        person_id=1,
        job_efficiency_rank=8.0,
        improvement_rank=7.5,
        satisfaction_score=9.0,
        job_id=101,
        created_at=datetime(2023, 3, 5)
    )
    record2 = JobPerformance(
        person_id=2,
        job_efficiency_rank=7.5,
        improvement_rank=8.0,
        satisfaction_score=8.5,
        job_id=102,
        created_at=datetime(2023, 6, 15)
    )
    mock_records = [record1, record2]

    # Configure the mock query
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = mock_records
    mock_session.query.return_value = mock_query

    # Invoke the method under test
    result = JobPerformance.get_performance_by_jobs_and_date(
        db=mock_session,
        job_ids=[101, 102],
        performance_metric="job_efficiency_rank"
    )

    # Assert the result structure and content
    assert isinstance(result, dict)
    print("for test")
    print(result)
    assert 1401 in result
    assert len(result[1401]) == 1
    assert len(result[1402]) == 1

    # Validate each record's details
    rec0 = result[1401][0]
    print(rec0)
    assert rec0['job_id'] == 101
    assert rec0['person_id'] == 1
    assert rec0['performance_value'] == 8.0
    
    rec1 = result[1402][0]
    assert rec1['job_id'] == 102
    assert rec1['person_id'] == 2
    assert rec1['performance_value'] == 7.5
def test_invalid_performance_metric(mock_session):
    # When an invalid performance metric is provided, a ValueError should be raised
    with pytest.raises(ValueError):
        JobPerformance.get_performance_by_job_and_date(
            db=mock_session,
            job_id=101,
            performance_metric="invalid_metric"
        )
