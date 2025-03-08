import pytest
from datetime import datetime
from app.models.AI.ModelDetails import ModelDetails

# A sample card_info dictionary with all required fields.
@pytest.fixture
def sample_card_info():
    return {
        "name_object_predict": "Test Model",
        "address": "/models/test_model.pkl",
        "feature_engineering_details_address": "/features/test_features.json",
        "architecture": "CNN",
        "accuracy_results": {"accuracy": 0.95},
        "f1_score_results": {"f1": 0.94},
        "precision_results": {"precision": 0.93},
        "recall_results": {"recall": 0.92},
        "t_test_results_accuracy": {"t_test": 0.05},
        "t_test_results_f1_score": {"t_test": 0.06},
        "confidence_level_accuracy": 0.95,
        "confidence_level_f1_score": 0.94,
        "num_all_samples": 1000,
        "num_features": 20,
        "split_test": 0.2,
        "n_splits_t_test": 5,
        "number_of_labels": 10,
        "model_evaluation_date": datetime(2023, 1, 1),
        "version": "1.0",
        "exam_id": 1,
        "job_id": 101
    }

def test_add_record_success(db_session, sample_card_info):
    """Test that a new ModelDetails record is added successfully."""
    record = ModelDetails.add_record(db_session, sample_card_info)
    assert record.id is not None
    assert record.name_object_predict == "Test Model"
    assert record.exam_id == 1
    assert record.job_id == 101

def test_find_model_by_id(db_session, sample_card_info):
    """Test retrieving a ModelDetails record by its ID."""
    record = ModelDetails.add_record(db_session, sample_card_info)
    found = ModelDetails.find_model_by_id(db_session, record.id)
    assert found is not None
    assert found.id == record.id

def test_find_models_by_exam_id(db_session, sample_card_info):
    """Test retrieving models by exam_id."""
    # Add two records with the same exam_id
    record1 = ModelDetails.add_record(db_session, sample_card_info)
    sample_card_info["name_object_predict"] = "Test Model 2"
    record2 = ModelDetails.add_record(db_session, sample_card_info)
    results = ModelDetails.find_models_by_exam_id(db_session, exam_id=1)
    # At least two records should match exam_id=1
    assert len(results) >= 2

def test_find_models_by_job_id(db_session, sample_card_info):
    """Test retrieving models by job_id."""
    # Add two records with the same job_id
    record1 = ModelDetails.add_record(db_session, sample_card_info)
    sample_card_info["name_object_predict"] = "Test Model 3"
    record2 = ModelDetails.add_record(db_session, sample_card_info)
    results = ModelDetails.find_models_by_job_id(db_session, job_id=101)
    # At least two records should match job_id=101
    assert len(results) >= 2

def test_find_models_by_exam_and_job_id(db_session, sample_card_info):
    """Test retrieving models by exam_id and job_id simultaneously."""
    record = ModelDetails.add_record(db_session, sample_card_info)
    results = ModelDetails.find_models_by_exam_and_job_id(db_session, exam_id=1, job_id=101)
    assert any(r.id == record.id for r in results)

def test_update_model_success(db_session, sample_card_info):
    """Test updating a ModelDetails record."""
    record = ModelDetails.add_record(db_session, sample_card_info)
    update_info = {"version": "2.0", "architecture": "Transformer"}
    updated = ModelDetails.update_model(db_session, record.id, update_info)
    assert updated.version == "2.0"
    assert updated.architecture == "Transformer"

def test_delete_model_by_id(db_session, sample_card_info):
    """Test deleting a ModelDetails record by ID."""
    record = ModelDetails.add_record(db_session, sample_card_info)
    result = ModelDetails.delete_model_by_id(db_session, record.id)
    assert result is True
    # Verify that the record is actually deleted
    found = ModelDetails.find_model_by_id(db_session, record.id)
    assert found is None
