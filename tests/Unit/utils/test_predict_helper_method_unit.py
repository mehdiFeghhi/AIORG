# test_unit_functions.py
import json
import joblib
import pandas as pd
import pytest
from pathlib import Path

# Import the functions to test:
from app.utils.predict_helper_method import find_person_feature_last_exam, find_essential_parameter
from app.models.AI.ModelDetails import ModelDetails  # For monkeypatching

# ---------------------------
# Unit Tests for find_person_feature_last_exam
# ---------------------------

def fake_read_csv(file_path):
    """A fake pd.read_csv that returns a DataFrame based on the file_path."""
    if file_path == "file1.csv":
        return pd.DataFrame({"person_id": [1, 2], "value": [10, 20]})
    elif file_path == "file2.csv":
        return pd.DataFrame({"person_id": [3, 4], "value": [30, 40]})
    else:
        return pd.DataFrame()

def test_find_person_feature_found(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", fake_read_csv)
    files_by_year = {2022: ["file1.csv"], 2021: ["file2.csv"]}
    
    # person_id 1 is in file1.csv (year 2022)
    data, found = find_person_feature_last_exam(1, files_by_year)
    assert found is True
    assert data["person_id"] == 1
    assert data["value"] == 10

def test_find_person_feature_found_in_later_year(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", fake_read_csv)
    # Although file1.csv (year 2022) doesn’t contain person_id 2 in this test order,
    # file1.csv does (in our fake, it does); you can change the order to simulate the search.
    files_by_year = {2022: ["file2.csv"], 2021: ["file1.csv"]}
    # person_id 2 is not in file2.csv but is in file1.csv (year 2021)
    data, found = find_person_feature_last_exam(2, files_by_year)
    assert found is True
    assert data["person_id"] == 2
    assert data["value"] == 20

def test_find_person_feature_not_found(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", fake_read_csv)
    files_by_year = {2022: ["file1.csv"], 2021: ["file2.csv"]}
    data, found = find_person_feature_last_exam(5, files_by_year)
    assert found is False
    assert data == {}

# ---------------------------
# Unit Tests for find_essential_parameter
# ---------------------------

# A dummy model card for testing purposes.
class DummyModelCard:
    def __init__(self, feature_engineering_details_address, address, name_object_predict, number_of_labels):
        self.feature_engineering_details_address = feature_engineering_details_address
        self.address = address
        self.name_object_predict = name_object_predict
        self.number_of_labels = number_of_labels

# A dummy model object (could be any object).
class DummyModel:
    pass

def dummy_find_model_by_id(db, model_id):
    if model_id == 1:
        return DummyModelCard("dummy_feature.json", "dummy_model.joblib", "dummy_predict", 3)
    return None

def fake_joblib_load(path):
    if str(path) == "dummy_model.joblib":
        return DummyModel()
    else:
        raise FileNotFoundError

def test_find_essential_parameter_success(monkeypatch, tmp_path):
    # Create a temporary JSON file with valid feature details.
    json_data = {
        "base_feature": "feature_base",
        "normalization_params": {"a": 1},
        "one_hot_mappings": {"b": 2},
        "feature_order": ["f1", "f2"]
    }
    json_file = tmp_path / "dummy_feature.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    # Create a temporary joblib file for the model.
    dummy_model = DummyModel()
    model_file = tmp_path / "dummy_model.joblib"
    joblib.dump(dummy_model, model_file)
    
    # Create a dummy model card with the temporary file paths.
    dummy_card = DummyModelCard(str(json_file), str(model_file), "dummy_predict", 3)
    
    # Monkeypatch ModelDetails.find_model_by_id and joblib.load
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card if model_id == 1 else None)
    monkeypatch.setattr(joblib, "load", lambda path: dummy_model if str(path) == str(model_file) else None)
    
    result = find_essential_parameter(1, db={})
    assert result["name_object_predict_in_card"] == "dummy_predict"
    assert result["base_feature"] == "feature_base"
    assert result["normalization_params"] == {"a": 1}
    assert result["one_hot_mappings"] == {"b": 2}
    assert result["feature_order"] == ["f1", "f2"]
    assert result["model"] == dummy_model
    assert result["number_of_labels"] == 3

def test_find_essential_parameter_model_not_found(monkeypatch):
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: None)
    with pytest.raises(ValueError, match="Model with ID 999 not found."):
        find_essential_parameter(999, db={})

def test_find_essential_parameter_json_file_not_found(monkeypatch):
    dummy_card = DummyModelCard("non_existent.json", "dummy_model.joblib", "dummy_predict", 3)
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card)
    with pytest.raises(FileNotFoundError, match="Feature engineering details file not found"):
        find_essential_parameter(1, db={})

def test_find_essential_parameter_json_decode_error(monkeypatch, tmp_path):
    # Create a file with invalid JSON.
    bad_json_path = tmp_path / "bad_feature.json"
    with open(bad_json_path, "w") as f:
        f.write("Not a JSON")
    dummy_card = DummyModelCard(str(bad_json_path), "dummy_model.joblib", "dummy_predict", 3)
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card)
    with pytest.raises(ValueError, match="Error decoding JSON"):
        find_essential_parameter(1, db={})

def test_find_essential_parameter_joblib_load_error(monkeypatch, tmp_path):
    # Create a valid JSON file.
    json_data = {
        "base_feature": "feature_base",
        "normalization_params": {"a": 1},
        "one_hot_mappings": {"b": 2},
        "feature_order": ["f1", "f2"]
    }
    json_file = tmp_path / "dummy_feature.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    # Dummy card points to a non-existent model file.
    dummy_card = DummyModelCard(str(json_file), "non_existent_model.joblib", "dummy_predict", 3)
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card)
    with pytest.raises(FileNotFoundError, match="Model file not found"):
        find_essential_parameter(1, db={})

def test_find_essential_parameter_joblib_other_error(monkeypatch, tmp_path):
    # Create a valid JSON file.
    json_data = {
        "base_feature": "feature_base",
        "normalization_params": {"a": 1},
        "one_hot_mappings": {"b": 2},
        "feature_order": ["f1", "f2"]
    }
    json_file = tmp_path / "dummy_feature.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f)
        
    dummy_card = DummyModelCard(str(json_file), "dummy_model.joblib", "dummy_predict", 3)
    monkeypatch.setattr(ModelDetails, "find_model_by_id", lambda db, model_id: dummy_card)
    
    # Monkey-patch joblib.load to raise a generic exception.
    def fake_joblib_load_error(path):
        raise Exception("Some other error")
    monkeypatch.setattr(joblib, "load", fake_joblib_load_error)
    
    with pytest.raises(RuntimeError, match="An error occurred while loading the model"):
        find_essential_parameter(1, db={})
