import pandas as pd
import pytest

# Import the integration function.
from app.services.enhance_training_data_service import enhance_dataset

def test_enhance_dataset():
    """
    Integration test for `enhance_dataset`.
    Uses a small sample DataFrame with numerical and categorical columns along with a target Series.
    Verifies that:
      - The train/test split is correct.
      - Numerical features are scaled to the [0, 1] range.
      - Categorical features are one-hot encoded (and the original categorical column is dropped).
      - The parameters dictionary contains expected keys.
      - The target variable is categorized correctly.
    """
    # Create a sample DataFrame and target Series.
    df = pd.DataFrame({
        'num1': [0, 50, 100, 25, 75],
        'cat1': ['A', 'B', 'A', 'B', 'C']
    })
    Y = pd.Series([10, 40, 70, 20, 90])
    num_classes = 5
    # Use a test_size of 0.4 for clarity and a fixed random state for reproducibility.
    X_train, X_test, Y_train, Y_test, params = enhance_dataset(
        df, Y, num_classes, test_size=0.4, random_state=1
    )

    # --- Train/Test Split ---
    # Check that total number of rows equals original
    print(len(X_train))
    print(len(X_test))
    assert len(X_train) + len(X_test) == len(df)
    
    # --- Categorical Encoding ---
    # Original categorical column should be dropped.
    assert 'cat1' not in X_train.columns
    # There should be one-hot encoded columns (names typically start with the original column name)
    one_hot_columns = [col for col in X_train.columns if col.startswith('cat1_')]
    assert len(one_hot_columns) > 0

    # --- Normalization ---
    # Check that the numerical column 'num1' in the training set is scaled to [0, 1].
    assert X_train['num1'].min() >= 0
    assert X_train['num1'].max() <= 1

    # --- Parameters Dictionary ---
    # Ensure the dictionary contains all expected keys.
    expected_param_keys = {"base_feature", "normalization_params", "one_hot_mappings", "feature_order"}
    assert expected_param_keys.issubset(params.keys())
    
    # Check that normalization parameters include 'num1'
    normalization_params = params["normalization_params"]
    assert "num1" in normalization_params
    
    # Check that one-hot mappings include 'cat1'
    one_hot_mappings = params["one_hot_mappings"]
    assert "cat1" in one_hot_mappings

    # Check that the feature order includes both the numerical column and the new one-hot columns.
    feature_order = params["feature_order"]
    assert 'num1' in feature_order
    for col in one_hot_columns:
        assert col in feature_order

    # --- Target Categorization ---
    # The target should now be integer classes in the range [0, num_classes - 1]
    assert Y_train.min() >= 0 and Y_train.max() < num_classes
    assert Y_test.min() >= 0 and Y_test.max() < num_classes


def test_integration_pipeline():
    """
    A more comprehensive integration test that uses a DataFrame with multiple numerical and 
    categorical columns and a target variable. This test ensures that the entire pipeline (splitting, 
    normalization, encoding, and parameter extraction) works together as expected.
    """
    # Construct a more complex dataset.
    data = {
        'num1': [10, 20, 30, 40, 50, 60, 70, 80],
        'num2': [100, 200, 300, 400, 500, 600, 700, 800],
        'cat1': ['X', 'Y', 'X', 'Z', 'Y', 'X', 'Z', 'Y'],
        'cat2': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    }
    df = pd.DataFrame(data)
    Y = pd.Series([5, 15, 25, 35, 45, 55, 65, 75])
    num_classes = 4

    # Run the enhancement function with a 25% test split.
    X_train, X_test, Y_train, Y_test, params = enhance_dataset(
        df, Y, num_classes, test_size=0.25, random_state=123
    )

    # Verify that both train and test feature DataFrames have the exact columns as specified in 'feature_order'.
    assert set(X_train.columns) == set(params['feature_order'])
    assert set(X_test.columns) == set(params['feature_order'])

    # Check that numerical features remain scaled between 0 and 1 in the training set.
    for col in ['num1', 'num2']:
        if col in X_train.columns:
            assert X_train[col].min() >= 0
            assert X_train[col].max() <= 1

    # Original categorical columns should not appear after one-hot encoding.
    for col in ['cat1', 'cat2']:
        assert col not in X_train.columns

    # Verify that the target series (Y_train and Y_test) have been categorized properly.
    assert Y_train.min() >= 0 and Y_train.max() < num_classes
    assert Y_test.min() >= 0 and Y_test.max() < num_classes
