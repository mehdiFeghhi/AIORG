import pytest
from datetime import datetime
from app.models.AI.ModelDetails import ModelDetails

def test_modeldetails_crud_integration(db_session):
    """Integration test covering create, read, update, and delete operations."""
    # Prepare a card_info dictionary with model details
    card_info = {
        "name_object_predict": "Integration Model",
        "address": "/models/integration_model.pkl",
        "feature_engineering_details_address": "/features/integration_features.json",
        "architecture": "RNN",
        "accuracy_results": {"accuracy": 0.90},
        "f1_score_results": {"f1": 0.89},
        "precision_results": {"precision": 0.88},
        "recall_results": {"recall": 0.87},
        "t_test_results_accuracy": {"t_test": 0.04},
        "t_test_results_f1_score": {"t_test": 0.03},
        "confidence_level_accuracy": 0.90,
        "confidence_level_f1_score": 0.89,
        "num_all_samples": 500,
        "num_features": 15,
        "split_test": 0.3,
        "n_splits_t_test": 3,
        "number_of_labels": 5,
        "model_evaluation_date": datetime(2023, 6, 1),
        "version": "1.0",
        "exam_id": 2,
        "job_id": 202
    }
    # Create a new record
    record = ModelDetails.add_record(db_session, card_info)
    assert record.id is not None

    # Read: find the record by its ID
    found = ModelDetails.find_model_by_id(db_session, record.id)
    assert found is not None
    assert found.name_object_predict == "Integration Model"

    # Update: modify some fields
    update_info = {"version": "1.1", "architecture": "Transformer"}
    updated = ModelDetails.update_model(db_session, record.id, update_info)
    assert updated.version == "1.1"
    assert updated.architecture == "Transformer"

    # Query by exam_id and job_id
    models_by_exam = ModelDetails.find_models_by_exam_id(db_session, exam_id=2)
    assert any(m.id == record.id for m in models_by_exam)

    models_by_job = ModelDetails.find_models_by_job_id(db_session, job_id=202)
    assert any(m.id == record.id for m in models_by_job)

    models_by_both = ModelDetails.find_models_by_exam_and_job_id(db_session, exam_id=2, job_id=202)
    assert any(m.id == record.id for m in models_by_both)

    # Delete: remove the record and verify deletion
    result = ModelDetails.delete_model_by_id(db_session, record.id)
    assert result is True
    found_after_delete = ModelDetails.find_model_by_id(db_session, record.id)
    assert found_after_delete is None
