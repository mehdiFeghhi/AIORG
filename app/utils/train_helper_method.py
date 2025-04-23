import os
from enum import Enum

class ModelName(str, Enum):
    SVM = "SVM"
    # LSTM = "LSTM"
    XgBoost = "XgBoost"
    MLP = "MLP"
    DecisionTree = "DecisionTree"





def manage_model_directory(base_directory_model, name_position, model_name):
    """
    Manage the directory and versioning for saving models.
    """
    if name_position:
        model_directory = os.path.join(base_directory_model, name_position, model_name)
    else:
        model_directory = os.path.join(base_directory_model, model_name)
    
    os.makedirs(model_directory, exist_ok=True)
    
    existing_versions = [f for f in os.listdir(model_directory) if f.startswith("model_v")]
    versions = [int(f.split('_v')[1].split('.joblib')[0]) for f in existing_versions if f.endswith('.joblib')]
    next_version = max(versions, default=0) + 1
    
    model_filename = f"model_v{next_version}.joblib"
    card_filename = f"model_card_v{next_version}.json"
    feature_engg_filename = f"feature_engineering_v{next_version}.json"
    
    return model_directory, model_filename, card_filename, feature_engg_filename, next_version


def calculate_confidence_level(p_value):
    """
    Calculate the confidence level based on the p-value from the t-test.

    Args:
        p_value (float): P-value from the t-test.

    Returns:
        float: Confidence level as a percentage.
    """
    return (1 - p_value) * 100




