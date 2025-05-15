import json


def load_json(file_path: str):
    
    # Ensure the file path ends with '.json'
    if not file_path.endswith('.json'):
        file_path += '.json'
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data from the file
        return data
    except FileNotFoundError:
        raise(f"The file at {file_path} was not found.")
        
    except json.JSONDecodeError:
        raise ("Failed to decode JSON. The file may be corrupted or improperly formatted.")
        r
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def number_validation(job_efficiency_rank, improvement_rank, satisfaction_score, lower_bond, uper_bond):
    """
    Validates that the provided numerical parameters are within the given bounds.

    Parameters:
        job_efficiency_rank (int|float): Job efficiency rank value.
        improvement_rank (int|float): Improvement rank value.
        satisfaction_score (int|float): Satisfaction score value.
        lower_bond (int|float): Lower bound (inclusive).
        uper_bond (int|float): Upper bound (inclusive).

    Returns:
        bool: True if all values are within bounds, otherwise raises a ValueError.
    """
    # Validate that each value is a number and is within the specified bounds.
    for value, name in zip(
        (job_efficiency_rank, improvement_rank, satisfaction_score),
        ("job_efficiency_rank", "improvement_rank", "satisfaction_score")
    ):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number. Got {type(value)} instead.")
        if value < lower_bond or value > uper_bond:
            return False
    return True



