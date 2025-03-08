import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from app.services.pre_processing_data_service import (
    make_dataset,
    fetch_performance_data,
    fetch_file_data,
    process_data,
    process_file,
    find_all_similar_job
)


@pytest.fixture
def mock_db():
    """Fixture for a mock database session."""
    return MagicMock()


@pytest.fixture
def mock_performance_data():
    """Mock performance data grouped by year."""
    return {
        "1401": [{"person_id": 1, "performance_value": 85}, {"person_id": 2, "performance_value": 90}],
        "1402": [{"person_id": 1, "performance_value": 88}]
    }


@pytest.fixture
def mock_file_data():
    """Mock file data grouped by Persian calendar year."""
    return {
        "1401": ["mock_file_1401.csv"],
        "1402": ["mock_file_1402.csv"]
    }


@pytest.fixture
def mock_csv_data():
    """Mock DataFrame for CSV file."""
    return pd.DataFrame({
        "person_id": [1, 2],
        "feature1": [10, 20],
        "feature2": [30, 40]
    })


@patch("app.models.job_performance.job_performance.JobPerformance.get_performance_by_jobs_and_date")
def test_fetch_performance_data(mock_get_performance, mock_db, mock_performance_data):
    """Test fetching performance data."""
    mock_get_performance.return_value = mock_performance_data
    result = fetch_performance_data(mock_db, ["job1"], "job_efficiency_rank")

    assert result == mock_performance_data
    mock_get_performance.assert_called_once_with(db=mock_db, job_ids=["job1"], performance_metric="job_efficiency_rank")


@patch("app.models.files.data_file.DataFile.get_files_by_exam_id")
def test_fetch_file_data(mock_get_files, mock_db, mock_file_data):
    """Test fetching file data."""
    mock_get_files.return_value = mock_file_data
    result = fetch_file_data(mock_db, "exam123")

    assert result == mock_file_data
    mock_get_files.assert_called_once_with(db=mock_db, exam_id="exam123")


@patch("pandas.read_csv")
def test_process_file(mock_read_csv, mock_performance_data, mock_csv_data):
    """Test processing a file."""
    mock_read_csv.return_value = mock_csv_data
    combined_features, combined_labels = process_file("mock_file_1401.csv", mock_performance_data["1401"], [], [])

    assert len(combined_features) == 2
    assert len(combined_labels) == 2
    assert combined_labels == [85, 90]
    mock_read_csv.assert_called_once_with("mock_file_1401.csv")


def test_find_all_similar_job():
    """Test finding similar jobs."""
    assert find_all_similar_job("job1") == ["job1"]


@patch("app.services.pre_processing_data_service.process_file")
def test_process_data(mock_process_file, mock_performance_data, mock_file_data):
    """Test processing data aggregation."""
    mock_process_file.side_effect = lambda file_path, records, feats, labels: (feats + [[10, 20]], labels + [85])

    X, Y = process_data(mock_performance_data, mock_file_data, "job_efficiency_rank")

    # Debugging output
    print(f"X: {X}, Y: {Y}")
    print(f"Length of X: {len(X)}, Expected: 1")
    print(f"Length of Y: {len(Y)}, Expected: 1")
    print(f"process_file call count: {mock_process_file.call_count}")
    print(f"mock_file_data: {mock_file_data}")
    print(f"mock_performance_data: {mock_performance_data}")

    assert isinstance(X, pd.DataFrame)
    assert isinstance(Y, pd.Series)
    assert len(X) == 2

    assert len(Y) == 2
    assert Y.iloc[0] == 85
    