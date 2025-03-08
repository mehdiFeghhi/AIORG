import os
import pytest
from fastapi import UploadFile
from io import BytesIO
from app.services import file_service  # Import the whole module

@pytest.fixture
def temp_upload_dir(tmp_path, monkeypatch):
    """
    Fixture to override the UPLOAD_DIR for testing.
    """
    monkeypatch.setattr(file_service, "UPLOAD_DIR", str(tmp_path))  # Patch UPLOAD_DIR
    return str(tmp_path)

def test_ensure_directory_exists(temp_upload_dir):
    """
    Test that the function correctly creates a directory.
    """
    test_dir = os.path.join(temp_upload_dir, "test_folder")
    assert not os.path.exists(test_dir)

    file_service.ensure_directory_exists(test_dir)
    assert os.path.exists(test_dir)

def test_get_upload_path(temp_upload_dir):
    """
    Test that get_upload_path correctly constructs the directory path.
    """
    title = "test_title"
    expected_path = os.path.join(temp_upload_dir, title)

    assert file_service.get_upload_path(title) == expected_path

def test_save_file_to_disk(temp_upload_dir):
    """
    Test that save_file_to_disk correctly saves a file to the expected directory.
    """
    test_title = "test_upload"
    test_filename = "test.txt"
    test_content = b"Hello, this is a test file."

    file = UploadFile(filename=test_filename, file=BytesIO(test_content))
    
    saved_path = file_service.save_file_to_disk(file, test_title)
    expected_path = os.path.join(temp_upload_dir, test_title, test_filename)

    assert saved_path == expected_path
    assert os.path.exists(expected_path)

    with open(expected_path, "rb") as f:
        assert f.read() == test_content
