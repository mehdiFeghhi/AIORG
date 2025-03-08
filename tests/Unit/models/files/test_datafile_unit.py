import pytest
from io import BytesIO
from datetime import datetime
from unittest.mock import MagicMock
from app.models.files.data_file import DataFile
from khayyam import JalaliDatetime

def test_add_file_success(monkeypatch, db_session):
    """Test adding a file successfully using a patched save_file_to_disk function."""
    # Create a BytesIO object to simulate an uploaded file
    file_content = b"dummy content"
    mock_file = BytesIO(file_content)
    mock_file.filename = "test_file.txt"
    # Simulate an UploadFile-like object by adding a 'file' attribute
    mock_file.file = mock_file

    # Define a fake save_file_to_disk function that returns the expected path
    def fake_save_file_to_disk(file, prefix):
        return "/path/to/test_file.txt"

    # Patch the save_file_to_disk function imported in the DataFile module
    monkeypatch.setattr("app.models.files.data_file.save_file_to_disk", fake_save_file_to_disk)

    # Define a valid Persian date string
    persian_date = "1402/11/25"

    # Call the add_file method from DataFile
    data_file = DataFile.add_file(db_session, file=mock_file, exam_id=1, created_at=persian_date)

    # Assert that the file record was added successfully
    assert data_file.id is not None
    assert data_file.name == "test_file.txt"
    assert data_file.path == "/path/to/test_file.txt"
    assert data_file.exam_id == 1
    assert isinstance(data_file.created_at, datetime)

def test_add_file_invalid_date(db_session):
    """Test adding a file with an invalid Persian date format."""
    mock_file = MagicMock()
    mock_file.filename = "test_file.txt"

    with pytest.raises(ValueError, match="Invalid Persian calendar datetime format. Use YYYY/MM/DD ."):
        DataFile.add_file(db_session, file=mock_file, exam_id=1, created_at="InvalidDate")

def test_get_files_by_exam_id(db_session):
    """Test retrieving files grouped by Persian year."""
    # Create two DataFile records with different Persian years
    file1 = DataFile(
        name="file1.txt",
        path="/path/file1.txt",
        created_at=JalaliDatetime(1402, 10, 15).todatetime(),
        exam_id=1
    )
    file2 = DataFile(
        name="file2.txt",
        path="/path/file2.txt",
        created_at=JalaliDatetime(1401, 5, 10).todatetime(),
        exam_id=1
    )
    db_session.add_all([file1, file2])
    db_session.commit()

    files_by_year = DataFile.get_files_by_exam_id(db_session, exam_id=1)

    assert 1402 in files_by_year
    assert "/path/file1.txt" in files_by_year[1402]
    
    assert 1401 in files_by_year
    assert "/path/file2.txt" in files_by_year[1401]
