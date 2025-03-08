import pytest
import numpy as np
from app.models.AI.MLP import MLPModel  # Adjust the import path as needed

@pytest.fixture
def classification_data():
    """
    Fixture that generates random classification data.
    X: Array of input features with shape [samples, n_features]
    y: Binary labels (0 or 1)
    """
    X_train = np.random.rand(100, 5)      # 100 samples, 5 features
    y_train = np.random.randint(0, 2, 100)  # Binary labels for training
    X_test = np.random.rand(20, 5)          # 20 test samples
    y_test = np.random.randint(0, 2, 20)      # Binary labels for testing
    return X_train, y_train, X_test, y_test

def test_mlp_training_prediction_evaluation(classification_data):
    """
    Integration test for MLPModel:
    - Train the model on training data.
    - Make predictions on test data.
    - Evaluate the model's accuracy (should be between 0 and 1).
    """
    X_train, y_train, X_test, y_test = classification_data
    model = MLPModel()  # Instantiate the MLPModel

    # Train the model (assuming BaseModel implements the train method)
    model.train(X_train, y_train)
    
    # Make predictions on the test data
    predictions = model.predict(X_test)
    # Check that the number of predictions matches the number of test samples
    assert predictions.shape[0] == X_test.shape[0]
    
    # Evaluate the model and verify that the accuracy is between 0 and 1
    accuracy = model.evaluate(X_test, y_test)
    assert 0 <= accuracy <= 1
