import pytest
import numpy as np
from app.models.AI.xgboost_model import XGBoostModel  # Adjust the import path as needed

@pytest.fixture
def binary_classification_data():
    """
    Fixture that generates random binary classification data.
    - X: Feature array with shape [samples, n_features]
    - y: Binary labels (0 or 1)
    """
    X_train = np.random.rand(100, 10)      # 100 samples, 10 features
    y_train = np.random.randint(0, 2, 100)   # Binary labels for training
    X_test = np.random.rand(20, 10)          # 20 test samples, 10 features
    y_test = np.random.randint(0, 2, 20)       # Binary labels for testing
    return X_train, y_train, X_test, y_test

def test_xgboost_training_prediction_evaluation(binary_classification_data):
    """
    Integration test for XGBoostModel:
    - Train the model on training data.
    - Make predictions on test data.
    - Evaluate the model's accuracy (should be between 0 and 1).
    """
    X_train, y_train, X_test, y_test = binary_classification_data
    model = XGBoostModel()
    
    # Train the model (assuming BaseModel implements the train method)
    model.train(X_train, y_train)
    
    # Make predictions on test data
    predictions = model.predict(X_test)
    assert predictions.shape[0] == X_test.shape[0]
    
    # Evaluate the model and verify the accuracy is between 0 and 1.
    accuracy = model.evaluate(X_test, y_test)
    assert 0 <= accuracy <= 1
