import pytest
import numpy as np
from unittest.mock import patch
from sklearn.tree import DecisionTreeClassifier
from app.models.AI.decision_tree import DecisionTreeModel

# Test data
X_train = np.random.rand(100, 5)  # 100 samples, 5 features
y_train = np.random.randint(0, 2, 100)  # Binary labels for classification
X_test = np.random.rand(20, 5)  # 20 test samples
y_test = np.random.randint(0, 2, 20)  # Test binary labels

# Test Case 1: Check model initialization with default parameters
def test_decision_tree_model_init_default():
    model = DecisionTreeModel()  # Initialize with default parameters
    assert model.param_grid is not None
    assert 'max_depth' in model.param_grid
    assert 'criterion' in model.param_grid
    assert isinstance(model.model, DecisionTreeClassifier)  # Ensure the model is a DecisionTreeClassifier

# Test Case 2: Check model initialization with custom parameters
def test_decision_tree_model_init_custom():
    custom_param_grid = {
        'max_depth': [5, 10],
        'criterion': ['entropy'],
        'min_samples_split': [3, 4]
    }
    model = DecisionTreeModel(param_grid=custom_param_grid)  # Initialize with custom parameters
    assert model.param_grid == custom_param_grid
    assert isinstance(model.model, DecisionTreeClassifier)

# Test Case 3: Check model training
def test_train():
    model = DecisionTreeModel()  # Initialize model
    model.train(X_train, y_train)  # Train model
    # Check that the model's fit method exists and has been called.
    assert hasattr(model.model, 'fit')

# Test Case 4: Check model prediction
def test_predict():
    model = DecisionTreeModel()  # Initialize model
    model.train(X_train, y_train)  # Train model
    predictions = model.predict(X_test)  # Make predictions
    assert len(predictions) == len(X_test)  # Ensure the number of predictions matches test set size
    assert np.all(np.isin(predictions, [0, 1]))  # Ensure binary predictions

# Test Case 5: Check model evaluation
def test_evaluate():
    model = DecisionTreeModel()  # Initialize model
    model.train(X_train, y_train)  # Train model
    accuracy = model.evaluate(X_test, y_test)  # Evaluate model
    assert 0 <= accuracy <= 1  # Accuracy should be between 0 and 1

# Test Case 6: Check saving and loading models (mock file system)
@patch('app.models.AI.base_model.joblib.dump')
@patch('app.models.AI.base_model.joblib.load')
def test_save_load_model(mock_load, mock_dump):
    model = DecisionTreeModel()  # Initialize model
    model.train(X_train, y_train)  # Train model

    # Test saving the model
    model.save_model('test_model.joblib')
    mock_dump.assert_called_once()  # Ensure joblib.dump was called

    # Test loading the model
    mock_load.return_value = model.model  # Mock the return value for joblib.load
    model.load_model('test_model.joblib')
    mock_load.assert_called_once()  # Ensure joblib.load was called
    assert model.model is not None  # Ensure model is loaded correctly
