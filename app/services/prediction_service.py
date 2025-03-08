from app.utils.model_loader import get_prediction_range
# from app.schemas import data_loader
from app.utils.predict_helper_method import find_essential_parameter
import pandas as pd



def predict_job_utils(name_object_predict:str,data_person: dict, model_id: int, db) -> str:
    """
    Predicts job utility metrics for a given person's data using a pre-trained model.

    Parameters:
        data_person (dict): Dictionary containing the person's data.
        model_id (int): The ID of the model to use for prediction.
        db: Database connection or handler to fetch model parameters.
    
    Returns:
        str: The prediction result.
    
    Raises:
        ValueError: If `data_person_df` has no columns or is missing required features.
    """
    # Convert data_person to a DataFrame for easier processing
    data_person_df = pd.DataFrame([data_person])
    
    # Check if the DataFrame has no columns
    if data_person_df.empty or len(data_person_df.columns) == 0:
        raise ValueError("The input data contains no columns.")
    
    # Retrieve essential parameters for the model from the database
    name_object_predict_in_card,base_feature, normalization_params, one_hot_mappings, feature_order, model, number_of_label = find_essential_parameter(model_id, db)
    
    if name_object_predict_in_card != name_object_predict:
        raise ValueError(f"The Object you want to predict :{name_object_predict} is not learn by this model.")



    # Ensure all base features are present in data_person, raise error if not
    for feature in base_feature:
        if feature not in data_person_df.columns:
            raise ValueError(f"The input data is missing the required feature: {feature}")
    
    # Normalize numerical columns using normalization parameters
    for col, params in normalization_params.items():
        data_person_df[col] = (data_person_df[col] - params['min']) / (params['max'] - params['min'])
        data_person_df[col].fillna(0, inplace=True)  # Fill missing values with 0 after normalization
    
    # One-hot encode categorical columns using the provided mappings
    encoded_columns = []
    for col, categories in one_hot_mappings.items():
        for category in categories:
            encoded_col = f"{col}_{category}"
            data_person_df[encoded_col] = (data_person_df[col] == category).astype(int)
            encoded_columns.append(encoded_col)
    
    # Drop original categorical columns
    data_person_df.drop(columns=one_hot_mappings.keys(), inplace=True)
    
    # Reindex columns to match the feature order expected by the model
    data_person_df = data_person_df.reindex(columns=feature_order, fill_value=0)
    
    # Convert the DataFrame to a NumPy array for model input
    data_person_numpy = data_person_df.to_numpy()
    
    # Make prediction using the model
    prediction = model.predict(data_person_numpy)
    
    # Get the prediction range from the model loader
    result = get_prediction_range(num_classes=number_of_label, prediction=prediction)
    
    return result
