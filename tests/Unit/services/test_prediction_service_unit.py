import pytest
import numpy as np
import pandas as pd
from app.services.prediction_service import predict_job_utils

pytest_plugins = ["pytest_mock"]

def test_empty_data_person_raises_error():
    """Test that a ValueError is raised when data_person is empty."""
    with pytest.raises(ValueError) as exc_info:
        predict_job_utils("test_object", {}, 1, None)
    assert "The input data contains no columns." in str(exc_info.value)

def test_name_object_mismatch_raises_error(mocker):
    """Test ValueError when name_object_predict doesn't match the model's learned object."""
    mocker.patch(
        'app.services.prediction_service.find_essential_parameter',
        return_value=("wrong_object", [], {}, {}, [], None, 0)
    )
    data_person = {"age": 30}
    with pytest.raises(ValueError) as exc_info:
        predict_job_utils("test_object", data_person, 1, None)
    assert "not learn by this model" in str(exc_info.value)

def test_missing_base_feature_raises_error(mocker):
    """Test ValueError when data_person is missing a required base feature."""
    mocker.patch(
        'app.services.prediction_service.find_essential_parameter',
        return_value=("test_object", ["required_feature"], {}, {}, [], None, 0)
    )
    data_person = {"other_feature": 5}
    with pytest.raises(ValueError) as exc_info:
        predict_job_utils("test_object", data_person, 1, None)
    assert "missing the required feature: required_feature" in str(exc_info.value)

def test_successful_prediction(mocker):
    """Test a successful prediction with proper data processing and model interaction."""
    # Setup mock model and parameters
    mock_model = mocker.Mock()
    mock_model.predict.return_value = np.array([[0.8]])
    mocker.patch(
        'app.services.prediction_service.find_essential_parameter',
        return_value=(
            "correct_object",
            ["age", "gender"],
            {"age": {"min": 0, "max": 100}},
            {"gender": ["M", "F"]},
            ["age", "gender_M", "gender_F"],
            mock_model,
            3
        )
    )
    mock_get_pred = mocker.patch(
        'app.services.prediction_service.get_prediction_range',
        return_value="High"
    )

    # Execute function with valid data
    data_person = {"age": 25, "gender": "M"}
    result = predict_job_utils("correct_object", data_person, 1, None)

    # Verify result
    assert result == "High"

    # Verify model input processing
    expected_input = np.array([[0.25, 1.0, 0.0]])
    actual_input = mock_model.predict.call_args[0][0]
    np.testing.assert_array_almost_equal(actual_input, expected_input)

    # Verify prediction range call
    mock_get_pred.assert_called_once_with(num_classes=3, prediction=np.array([[0.8]]))

def test_normalization_and_encoding(mocker):
    """Test numerical normalization and categorical encoding are applied correctly."""
    mock_model = mocker.Mock()
    mock_model.predict.return_value = np.array([[0.5]])
    mocker.patch(
        'app.services.prediction_service.find_essential_parameter',
        return_value=(
            "correct_object",
            ["age", "gender"],
            {"age": {"min": 20, "max": 80}},  # age normalized as (value - 20)/60
            {"gender": ["F"]},  # One-hot encode 'F' only
            ["age", "gender_F"],
            mock_model,
            2
        )
    )
    mocker.patch(
        'app.services.prediction_service.get_prediction_range', 
        return_value="Medium"
    )

    data_person = {"age": 50, "gender": "F"}
    result = predict_job_utils("correct_object", data_person, 1, None)

    assert result == "Medium"
    expected_input = np.array([[(50-20)/(80-20), 1.0]])
    actual_input = mock_model.predict.call_args[0][0]
    np.testing.assert_array_almost_equal(actual_input, expected_input)