import os
import io
import shutil
import pytest
from fastapi import UploadFile
from tempfile import TemporaryDirectory

from app.services.file_service import save_file_to_disk, get_upload_path  # Adjust import based on your actual module name

@pytest.fixture
def temp_upload_dir():
    """Fixture to create a temporary upload directory and clean up afterward."""
    with TemporaryDirectory() as temp_dir:
        os.environ["UPLOAD_DIR"] = temp_dir  # Override the environment variable
        yield temp_dir  # Provide the directory path to the test
        shutil.rmtree(temp_dir, ignore_errors=True)  # Cleanup after test

def test_save_file_to_disk(temp_upload_dir):
    """Integration test for saving an uploaded file."""
    # Simulate an uploaded file
    file_content = b"Test content"
    file_name = "test_file.txt"
    
    # Create a file-like object for UploadFile
    file_obj = io.BytesIO(file_content)
    upload_file = UploadFile(filename=file_name, file=file_obj)

    title = "test_directory"
    saved_file_path = save_file_to_disk(upload_file, title)

    # Verify file was saved in the correct location
    expected_path = os.path.join(get_upload_path(title), file_name)
    assert saved_file_path == expected_path
    assert os.path.exists(saved_file_path)

    # Verify file content
    with open(saved_file_path, "rb") as f:
        assert f.read() == file_content
