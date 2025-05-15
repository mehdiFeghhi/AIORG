from typing import Tuple, Dict
import numpy as np
import joblib
import numpy as np

def find_structure_input(model_address: str) -> Tuple[Dict,Dict,list,list,str]:

    return

def find_works_main_propertis(propertis:list):

    return

def create_dataset(list_of_common_works:list,group_feature_for_training_id:str,purpose:str):

    return


def data_preprocess(data_person: dict,
                    model_structure_input_default: dict,
                    one_hot_variable: dict,
                    numberal_variable_with_order_for_normalization: list,
                    order_feature: list,
                    normalization_address: str) -> np.ndarray:
    """
    Preprocesses input data for a predictive model.
    
    Parameters:
        data_person (dict): A dictionary containing personal data to preprocess.
        model_structure_input_default (dict): A default structure for input features.
        one_hot_variable (dict): A mapping of categorical features to their possible values for one-hot encoding.
        numberal_variable_with_order_for_normalization (list): List of numerical variables for normalization.
        order_feature (list): Desired order of features in the final output.
        normalization_address (str): File path to the normalization parameters.
    
    Returns:
        np.ndarray: A preprocessed numpy array ready for model input.
    """
    new_dict = {}
    for key, value in one_hot_variable:

        person_properti = data_person.get(key,model_structure_input_default.get(key,None))

        for item in value:
            if  person_properti is not None and person_properti == item:
                new_dict[item] = 1
            else:
                new_dict[item] = 0

    list_numerical_for_normalization = []
    for item in numberal_variable_with_order_for_normalization:

        value = data_person.get(item,model_structure_input_default.get(key))
        list_numerical_for_normalization.append(value)
    
    scaler = joblib.load(normalization_address)
    numeric_data_scaled = scaler.transform([list_numerical_for_normalization])

    for idx,item in enumerate(numberal_variable_with_order_for_normalization):

        new_dict[item] = numeric_data_scaled[idx]

    list_output = []
    
    for item in order_feature:

        list_output.append(new_dict[item])
    
    return np.array(list_output).reshape(1, -1)



def check_structure(model_structure_input: dict, data_person: dict) -> bool:
    total_keys = len(model_structure_input)  # Total number of keys in model_structure_input
    matched_keys = 0  # Counter for matched keys
    
    for key, value_type in model_structure_input.items():
        # Check if the key exists in data_person and if the type matches
        if key in data_person and isinstance(data_person[key], eval(value_type)):
            matched_keys += 1
    
    # Check if 80% of the keys match
    if matched_keys / total_keys >= 0.8:
        return True
    return False
