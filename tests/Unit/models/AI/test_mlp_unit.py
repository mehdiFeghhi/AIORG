import pytest
from sklearn.neural_network import MLPClassifier
from app.models.AI.MLP import MLPModel  # Adjust the import path as needed

def test_mlp_model_default_param_grid():
    """
    Test MLPModel initialization with the default parameter grid.
    """
    model = MLPModel()  # Initialize without a custom parameter grid
    default_param_grid = {
        'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
        'activation': ['relu', 'tanh', 'logistic'],
        'solver': ['adam', 'sgd'],
        'learning_rate': ['constant', 'adaptive'],
        'alpha': [0.0001, 0.001, 0.01]
    }
    # Verify that the parameter grid is set to the default
    assert model.param_grid == default_param_grid
    # Check that the underlying model is an instance of MLPClassifier
    assert isinstance(model.model, MLPClassifier)
    # Check that the model's class name is renamed to 'MLP'
    assert model.model.__class__.__name__ == 'MLP'

def test_mlp_model_custom_param_grid():
    """
    Test MLPModel initialization with a custom parameter grid.
    """
    custom_param_grid = {
        'hidden_layer_sizes': [(75,)],
        'activation': ['tanh'],
        'solver': ['adam'],
        'learning_rate': ['adaptive'],
        'alpha': [0.005]
    }
    model = MLPModel(param_grid=custom_param_grid)
    # Verify that the parameter grid is set to the custom one
    assert model.param_grid == custom_param_grid
    # Check that the underlying model is an instance of MLPClassifier
    assert isinstance(model.model, MLPClassifier)
    # Check that the model's class name is renamed to 'MLP'
    assert model.model.__class__.__name__ == 'MLP'

def test_mlp_model_methods_exist():
    """
    Verify that MLPModel has the key methods inherited from BaseModel.
    """
    model = MLPModel()
    # Assuming BaseModel implements train, predict, and evaluate methods
    assert hasattr(model, "train")
    assert hasattr(model, "predict")
    assert hasattr(model, "evaluate")
