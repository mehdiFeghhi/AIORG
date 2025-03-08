# tests/integration/utils/test_predict_helper_method_integration.py
import json
import joblib
import pandas as pd
import pytest
from pathlib import Path

# Import the functions to test:
from app.utils.predict_helper_method import find_person_feature_last_exam, find_essential_parameter
from app.models.AI.ModelDetails import ModelDetails  # For setting up the dummy model card

# ---------------------------
# Integration Tests for find_person_feature_last_exam
# ---------------------------

def create_csv_file(tmp_path, filename, data):
    """Helper to create a CSV file from a dict and return its string path."""
    file_path = tmp_path / filename
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return str(file_path)

def test_integration_find_person_feature(tmp_path):
    # Create two CSV files with actual content.
    file1 = create_csv_file(tmp_path, "file1.csv", {"person_id": [1, 2], "value": [10, 20]})
    file2 = create_csv_file(tmp_path, "file2.csv", {"person_id": [3, 4], "value": [30, 40]})
    
    files_by_year = {
        2022: [file1],
        2021: [file2]
    }
    
    # Test: person_id 1 should be found in file1.csv with value 10.
    data, found = find_person_feature_last_exam(1, files_by_year)
    assert found is True
    assert data["person_id"] == 1
    assert data["value"] == 10
    
    # Test: person_id 2 should be found in file1.csv with value 20.
    data, found = find_person_feature_last_exam(2, files_by_year)
    assert found is True
    assert data["person_id"] == 2
    assert data["value"] == 20  # Updated expectation
    
    # Test: person_id 3 should be found in file2.csv.
    data, found = find_person_feature_last_exam(3, files_by_year)
    assert found is True
    assert data["person_id"] == 3
    assert data["value"] == 30
    
    # Test: person not found.
    data, found = find_person_feature_last_exam(5, files_by_year)
    assert found is False
    assert data == {}

# ---------------------------
# Integration Tests for find_essential_parameter
# ---------------------------

# Dummy classes for integration testing.
class DummyModelCard:
    def __init__(self, feature_engineering_details_address, address, name_object_predict, number_of_labels):
        self.feature_engineering_details_address = feature_engineering_details_address
        self.address = address
        self.name_object_predict = name_object_predict
        self.number_of_labels = number_of_labels

class DummyModel:
    pass

def test_integration_find_essential_parameter(tmp_path, monkeypatch):
    # Create an actual JSON file with feature details.
    json_data = {
        "base_feature": "feature_base_integration",
        "normalization_params": {"x": 100},
        "one_hot_mappings": {"y": 200},
        "feature_order": ["col1", "col2"]
    }
    json_file = tmp_path / "feature_details.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    # Create an actual joblib file for the model.
    dummy_model = DummyModel()
    model_file = tmp_path / "model.joblib"
    joblib.dump(dummy_model, model_file)
    
    # Create a dummy model card with the actual file paths.
    dummy_card = DummyModelCard(str(json_file), str(model_file), "integration_predict", 5)
    
    # Monkey-patch ModelDetails.find_model_by_id to return our dummy card.
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card if model_id == 1 else None)
    
    result = find_essential_parameter(1, db={})
    
    assert result["name_object_predict_in_card"] == "integration_predict"
    assert result["base_feature"] == "feature_base_integration"
    assert result["normalization_params"] == {"x": 100}
    assert result["one_hot_mappings"] == {"y": 200}
    assert result["feature_order"] == ["col1", "col2"]
    
    # Instead of checking for equality, verify the type of the loaded model.
    assert isinstance(result["model"], DummyModel)
    
    assert result["number_of_labels"] == 5
