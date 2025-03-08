import pytest
from unittest.mock import patch
from app.utils.model_loader import get_prediction_range,find_model
from app.models.AI import decision_tree,LSTM,MLP,svm,xgboost_model
# === Unit Tests ===

def test_get_prediction_range():
    assert get_prediction_range(5, 0) == f"{0} تا {25}"
    assert get_prediction_range(5, 1) == f"{25} تا {50}"
    assert get_prediction_range(5, 2) == f"{50} تا {75}"
    assert get_prediction_range(5, 3) == f"{75} تا {100}"
    
    assert get_prediction_range(3, 0) == f"{0} تا {50}"
    assert get_prediction_range(3, 1) == f"{50} تا {100}"


# Test when the model card is missing or invalid
# def test_find_model_invalid_json():
#     with patch("app.utils.model_loader.load_json", return_value=None):
#         with pytest.raises(Exception, match="There is no model card."):
#             find_model("invalid_path.json")


# # Test when required information is missing in the model card
# def test_find_model_incomplete_json():
#     incomplete_json = {
#         "architecture": "DecisionTree",  # Missing other required fields
#     }
#     with patch("app.utils.model_loader.load_json", return_value=incomplete_json):
#         with pytest.raises(Exception, match="The information about this model is not complete!"):
#             find_model("incomplete_model.json")


# # Test when an unsupported architecture type is provided
# def test_find_model_unsupported_architecture():
#     unsupported_json = {
#         "architecture": "RandomForest",
#         "address": "/path/to/model",
#         "number_of_labels": 3,
#         "num_features": 10
#     }
#     with patch("app.utils.model_loader.load_json", return_value=unsupported_json):
#         with pytest.raises(Exception, match="The architecture name RandomForest is unfamiliar"):
#             find_model("unsupported_architecture.json")


# Test for valid DecisionTree model loading
def test_find_model_decision_tree():
    valid_json = {
        "architecture": "DecisionTree",
        "address": "/path/to/decision_tree_model",
        "number_of_labels": 3,
        "num_features": 10
    }
    with patch("app.utils.model_loader.load_json", return_value=valid_json):
        with patch.object(decision_tree.DecisionTreeModel, 'load_model', return_value=None) as mock_load:
            model, number_of_labels = find_model("decision_tree_model.json")
            mock_load.assert_called_once_with("/path/to/decision_tree_model")
            assert isinstance(model, decision_tree.DecisionTreeModel)
            assert number_of_labels == 3


# Test for valid SVM model loading
def test_find_model_svm():
    valid_json = {
        "architecture": "SVM",
        "address": "/path/to/svm_model",
        "number_of_labels": 2,
        "num_features": 5
    }
    with patch("app.utils.model_loader.load_json", return_value=valid_json):
        with patch.object(svm.SVMModel, 'load_model', return_value=None) as mock_load:
            model, number_of_labels = find_model("svm_model.json")
            mock_load.assert_called_once_with("/path/to/svm_model")
            assert isinstance(model, svm.SVMModel)
            assert number_of_labels == 2


# Test for valid XGBoost model loading
def test_find_model_xgboost():
    valid_json = {
        "architecture": "XGB",
        "address": "/path/to/xgboost_model",
        "number_of_labels": 4,
        "num_features": 20
    }
    with patch("app.utils.model_loader.load_json", return_value=valid_json):
        with patch.object(xgboost_model.XGBoostModel, 'load_model', return_value=None) as mock_load:
            model, number_of_labels = find_model("xgboost_model.json")
            mock_load.assert_called_once_with("/path/to/xgboost_model")
            assert isinstance(model, xgboost_model.XGBoostModel)
            assert number_of_labels == 4


# Test for valid LSTM model loading
def test_find_model_lstm():
    valid_json = {
        "architecture": "LSTM",
        "address": "/path/to/lstm_model",
        "number_of_labels": 3,
        "num_features": 5
    }
    with patch("app.utils.model_loader.load_json", return_value=valid_json):
        with patch.object(LSTM.LSTMModel, 'load_model', return_value=None) as mock_load:
            model, number_of_labels = find_model("lstm_model.json")
            mock_load.assert_called_once_with("/path/to/lstm_model")
            assert isinstance(model, LSTM.LSTMModel)
            assert number_of_labels == 3


# Test for valid MLP model loading
def test_find_model_mlp():
    valid_json = {
        "architecture": "MLP",
        "address": "/path/to/mlp_model",
        "number_of_labels": 5,
        "num_features": 10
    }
    with patch("app.utils.model_loader.load_json", return_value=valid_json):
        with patch.object(MLP.MLPModel, 'load_model', return_value=None) as mock_load:
            model, number_of_labels = find_model("mlp_model.json")
            mock_load.assert_called_once_with("/path/to/mlp_model")
            assert isinstance(model, MLP.MLPModel)
            assert number_of_labels == 5
