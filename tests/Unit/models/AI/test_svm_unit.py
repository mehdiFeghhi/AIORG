import pytest
from sklearn.svm import SVC
from app.models.AI.svm import SVMModel  # Adjust the import path as needed

def test_svm_model_default_param_grid():
    """
    Test SVMModel initialization with the default parameter grid.
    """
    model = SVMModel()  # Initialize without custom parameters
    default_param_grid = {
        'C': [0.1, 1.0, 10.0],
        'gamma': ['scale', 'auto'],
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid']
    }
    assert model.param_grid == default_param_grid
    # Check that the model's class name is set to 'SVM'
    assert model.model.__class__.__name__ == 'SVM'
    # Verify that the underlying model is an instance of SVC
    assert isinstance(model.model, SVC)

def test_svm_model_custom_param_grid():
    """
    Test SVMModel initialization with a custom parameter grid.
    """
    custom_param_grid = {
        'C': [0.5, 2.0],
        'kernel': ['rbf']
    }
    model = SVMModel(param_grid=custom_param_grid)
    assert model.param_grid == custom_param_grid
    # Check that the model's class name is set to 'SVM'
    assert model.model.__class__.__name__ == 'SVM'
    # Verify that the underlying model is an instance of SVC
    assert isinstance(model.model, SVC)

def test_svm_model_methods_exist():
    """
    Verify that SVMModel has the key methods inherited from BaseModel.
    """
    model = SVMModel()
    # Assuming BaseModel implements train, predict, and evaluate methods
    assert hasattr(model, "train")
    assert hasattr(model, "predict")
    assert hasattr(model, "evaluate")
