import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from app.services.pre_processing_data_service import make_dataset

@pytest.fixture
def mock_db():
    """Fixture for a mock database session."""
    return MagicMock()


@patch("app.models.job_performance.job_performance.JobPerformance.get_performance_by_jobs_and_date")
@patch("app.models.files.data_file.DataFile.get_files_by_exam_id")
@patch("pandas.read_csv")
def test_make_dataset(mock_read_csv, mock_get_files, mock_get_performance, mock_db):
    """Integration test for make_dataset()."""
    
    # Mock performance data
    mock_get_performance.return_value = {
        "1401": [{"person_id": 1, "performance_value": 85}],
        "1402": [{"person_id": 2, "performance_value": 90}]
    }

    # Mock file data
    mock_get_files.return_value = {
        "1401": ["mock_file_1401.csv"],
        "1402": ["mock_file_1402.csv"]
    }

    # Mock CSV file
    mock_read_csv.return_value = pd.DataFrame({
        "person_id": [1, 2],
        "feature1": [10, 20],
        "feature2": [30, 40]
    })

    # Call function
    X, Y = make_dataset("job1", "exam123", "job_efficiency_rank", mock_db)

    # Assertions
    assert isinstance(X, pd.DataFrame)
    assert isinstance(Y, pd.Series)
    assert len(X) == 2  # Only one matching person_id should be processed
    assert len(Y) == 2
    assert Y.iloc[0] == 85
