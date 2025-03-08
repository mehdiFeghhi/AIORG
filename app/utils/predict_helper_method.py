import pandas as pd
from typing import Dict, Tuple
import json
import joblib
from pathlib import Path
from app.models.AI.ModelDetails import ModelDetails  # Assuming ModelDetails is in app.models

def find_person_feature_last_exam(person_id: int, files_by_year: Dict[int, list]) -> Tuple[Dict, bool]:
    """
    Finds the row corresponding to the given person_id in the newest available CSV file,
    searching from the most recent year to older years.

    Args:
        person_id (int): The ID of the person to search for.
        files_by_year (Dict[int, list]): A dictionary with years as keys and lists of file paths as values.

    Returns:
        Tuple[Dict, bool]: A tuple containing the data (as a dictionary) of the found row and a boolean flag indicating success.
    """
    # Sort the years in descending order
    sorted_years = sorted(files_by_year.keys(), reverse=True)

    # Iterate through each year from newest to oldest
    for year in sorted_years:
        # Get the list of CSV files for the current year
        files = files_by_year[year]

        # Iterate through each file and search for the person_id
        for file_path in files:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)

            # Check if the person_id is in the DataFrame
            person_row = df[df['person_id'] == person_id]

            if not person_row.empty:
                # Convert the row to a dictionary and return it with the success flag
                return person_row.to_dict(orient='records')[0], True

    # If the person_id was not found in any file, return empty data and a failure flag
    return {}, False




def find_essential_parameter(model_id: int, db):
    # Step 1: Find the model by ID
    model_card = ModelDetails.find_model_by_id(db, model_id)
    if not model_card:
        raise ValueError(f"Model with ID {model_id} not found.")

    # Step 2: Extract feature engineering details address
    feature_engineering_details_address = model_card.feature_engineering_details_address

    # Step 3: Read the JSON file at the feature engineering details address
    feature_details_path = Path(feature_engineering_details_address)
    try:
        with feature_details_path.open('r') as file:
            feature_details = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Feature engineering details file not found at {feature_engineering_details_address}.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from file at {feature_engineering_details_address}.")

    # Extract the necessary values from the JSON file
    base_feature = feature_details.get("base_feature")
    normalization_params = feature_details.get("normalization_params")
    one_hot_mappings = feature_details.get("one_hot_mappings")
    feature_order = feature_details.get("feature_order")

    # Step 4: Load the model from the .joblib file
    model_path = Path(model_card.address)
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_card.address}.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the model: {e}")

    # Step 5: Return the required values
    return {
        "name_object_predict_in_card":model_card.name_object_predict,
        "base_feature": base_feature,
        "normalization_params": normalization_params,
        "one_hot_mappings": one_hot_mappings,
        "feature_order": feature_order,
        "model": model,
        "number_of_labels": model_card.number_of_labels
    }
