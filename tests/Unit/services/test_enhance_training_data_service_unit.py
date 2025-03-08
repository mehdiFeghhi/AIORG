import pandas as pd
import numpy as np
import pytest

# Import the functions to be tested.
from app.services.enhance_training_data_service import categorize_to_classes, extract_attributes_from_df

def test_categorize_to_classes():
    """
    Unit test for `categorize_to_classes`.
    Given a simple series and a number of classes, verify that the output matches expected classes.
    """
    # Input values
    Y = pd.Series([10, 50, 90, 100])
    num_classes = 5
    # Expected:
    # class_range = 100/5 = 20, so:
    # 10 -> floor(10/20)=0, 50 -> floor(50/20)=2, 90 -> floor(90/20)=4, 
    # and 100 -> floor(100/20)=5 which is then set to 4 (last class)
    expected = pd.Series([0, 2, 4, 4])
    
    result = categorize_to_classes(Y, num_classes)
    pd.testing.assert_series_equal(result, expected)


def test_extract_attributes_from_df():
    """
    Unit test for `extract_attributes_from_df`.
    Creates a small DataFrame with both numerical and categorical columns,
    and verifies that the returned attributes dictionary has the expected keys and values.
    """
    df = pd.DataFrame({
        'age': [25, 30, 35],
        'color': ['red', 'blue', 'red']
    })
    
    attributes = extract_attributes_from_df(df)
    
    # Check that all expected keys are present
    assert 'model_structure_input_default' in attributes
    assert 'one_hot_mapping' in attributes
    assert 'numerical_variables_for_normalization' in attributes

    # Check that the numerical column is listed
    assert 'age' in attributes['numerical_variables_for_normalization']
    
    # For categorical column, ensure the mapping is correct
    assert 'color' in attributes['one_hot_mapping']
    unique_colors = attributes['one_hot_mapping']['color']
    assert set(unique_colors) == {'red', 'blue'}
    
    # Also, check that the default model structure is computed properly.
    # For numerical columns, it's the mean; for categorical, it's the mode.
    assert np.isclose(attributes['model_structure_input_default']['age'], 30)
    assert attributes['model_structure_input_default']['color'] in ['red', 'blue']
