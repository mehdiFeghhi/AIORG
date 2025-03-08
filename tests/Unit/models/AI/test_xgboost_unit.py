import pytest
import xgboost as xgb
from app.models.AI.xgboost_model import XGBoostModel  # Adjust the import path as needed

def test_xgboost_model_default_param_grid():
    """
    Test XGBoostModel initialization with the default parameter grid.
    """
    model = XGBoostModel()  # Initialize without a custom parameter grid
    default_param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.3],
        'n_estimators': [50, 100, 200],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
    }
    assert model.param_grid == default_param_grid
    # Verify that the model's class name is set to 'XGB'
    assert model.model.__class__.__name__ == 'XGB'
    # Ensure the underlying model is an instance of xgb.XGBClassifier
    assert isinstance(model.model, xgb.XGBClassifier)

def test_xgboost_model_custom_param_grid():
    """
    Test XGBoostModel initialization with a custom parameter grid.
    """
    custom_param_grid = {
        'max_depth': [4, 6],
        'learning_rate': [0.05],
        'n_estimators': [100],
        'subsample': [0.9],
        'colsample_bytree': [0.9],
    }
    model = XGBoostModel(param_grid=custom_param_grid)
    assert model.param_grid == custom_param_grid
    assert model.model.__class__.__name__ == 'XGB'
    assert isinstance(model.model, xgb.XGBClassifier)

def test_xgboost_model_methods_exist():
    """
    Verify that XGBoostModel has the key methods inherited from BaseModel.
    """
    model = XGBoostModel()
    # Assuming BaseModel implements train, predict, and evaluate methods
    assert hasattr(model, "train")
    assert hasattr(model, "predict")
    assert hasattr(model, "evaluate")
