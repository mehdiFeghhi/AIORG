from typing import Dict, List, Any,Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split


def enhance_dataset(
    X_main: pd.DataFrame,
    Y_main: pd.Series,
    num_classes: int,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, Dict[str, Any]]:
    """
    Enhances the dataset by normalizing numerical features, one-hot encoding categorical features, 
    and splitting the dataset into training and test sets.
    
    Parameters:
        X (pd.DataFrame): The feature data.
        Y (pd.Series): The target variable.
        num_classes (int): Number of classes to categorize Y into.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Controls the shuffling applied to the data before applying the split.
    
    Returns:
        Tuple: Processed training and test feature data, training and test target variable, 
               and a dictionary containing normalization parameters and encoding mappings.
    """
    X = X_main.copy()
    Y = Y_main.copy()

    # Categorize the target variable into discrete classes
    Y = categorize_to_classes(Y, num_classes)
    
    # Split the data into training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=test_size, random_state=random_state
    )

    base_feature = X.columns.to_list()
    # Extract attributes for processing
    attributes = extract_attributes_from_df(X_train)
    
    # Normalize numerical columns
    scaler = MinMaxScaler()
    numerical_cols = attributes['numerical_variables_for_normalization']
    
    X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
    X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])
    
    # Save normalization parameters
    normalization_params = {
        col: {'min': scaler.data_min_[i], 'max': scaler.data_max_[i]}
        for i, col in enumerate(numerical_cols)
    }
    
    # One-hot encode categorical columns
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    categorical_cols = list(attributes['one_hot_mapping'].keys())
    
    encoded_train = encoder.fit_transform(X_train[categorical_cols])
    encoded_test = encoder.transform(X_test[categorical_cols])
    
    # Create DataFrames for encoded categorical columns
    encoded_train_df = pd.DataFrame(encoded_train, columns=encoder.get_feature_names_out(categorical_cols))
    encoded_test_df = pd.DataFrame(encoded_test, columns=encoder.get_feature_names_out(categorical_cols))
    
    # Reset indices to ensure proper alignment
    X_train = X_train.reset_index(drop=True)
    encoded_train_df = encoded_train_df.reset_index(drop=True)

    # Reset indices to ensure proper alignment
    X_test = X_test.reset_index(drop=True)
    encoded_test_df = encoded_test_df.reset_index(drop=True)


    # Drop original categorical columns and concatenate the encoded DataFrames
    X_train = pd.concat([X_train.drop(columns=categorical_cols), encoded_train_df], axis=1)
    X_test = pd.concat([X_test.drop(columns=categorical_cols), encoded_test_df], axis=1)

    print("IM")
    print(len(X_train))
    print(len(X_test))
    print("Portant")

    # Save one-hot encoding mappings
    one_hot_mappings = {col: encoder.categories_[i].tolist() for i, col in enumerate(categorical_cols)}
    
    # Generate the final feature order after encoding
    feature_order = list(attributes['numerical_variables_for_normalization']) + \
                    list(encoded_train_df.columns)
    


    # Reindex the columns in X_train and X_test to match the final feature order
    X_train = X_train.reindex(columns=feature_order, fill_value=0)
    X_test = X_test.reindex(columns=feature_order, fill_value=0)


    # Return the processed datasets, categorized targets, and parameters for future use
    return (
        X_train, X_test, Y_train, Y_test, {
            "base_feature":base_feature,
            "normalization_params": normalization_params,
            "one_hot_mappings": one_hot_mappings,
            "feature_order": feature_order
        }
    )


def extract_attributes_from_df(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extracts attributes required for training from the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing feature data.
    
    Returns:
        dict: A dictionary with extracted attributes.
    """
    # Step 1: Identify categorical and numerical columns
    categorical_columns: List[str] = df.select_dtypes(include=['object']).columns.tolist()
    numerical_columns: List[str] = df.select_dtypes(include=['number']).columns.tolist()

    # Step 2: Map default structure for input features with mode for categorical and mean for numerical
    model_structure_input_default: Dict[str, Any] = {
        col: df[col].mode()[0] if col in categorical_columns else df[col].mean()
        for col in df.columns
    }

    # Step 3: Create one-hot mapping for categorical variables
    one_hot_mapping: Dict[str, List[Any]] = {
        col: df[col].dropna().unique().tolist() for col in categorical_columns
    }

    # Step 4: Define numerical variables for normalization (ordered list)
    numerical_variables_for_normalization: List[str] = numerical_columns


    # Step 6: Return attributes as a dictionary
    return {
        "model_structure_input_default": model_structure_input_default,
        "one_hot_mapping": one_hot_mapping,
        "numerical_variables_for_normalization": numerical_variables_for_normalization,
    }


def categorize_to_classes(Y: pd.Series, num_classes: int) -> pd.Series:
    """
    Categorizes the values of a target variable (Y) into discrete classes based on the number of classes.

    Parameters:
    - Y: pd.Series - The target variable series.
    - num_classes: int - The number of classes to divide Y into.
    
    Returns:
    - pd.Series - The target variable series with categorized class labels.
    """
    # Convert Y to a NumPy array
    np_Y = Y.to_numpy()

    # Calculate the range for each class
    class_range = 100 / num_classes
    
    # Map the values of Y to classes
    class_labels = np.floor(np_Y / class_range).astype(int)

    # Ensure that the maximum value (100) gets assigned the last class
    class_labels[class_labels == num_classes] = num_classes - 1
    
    # Convert back to pd.Series to maintain the original index
    Y_classified = pd.Series(class_labels, index=Y.index)

    return Y_classified

