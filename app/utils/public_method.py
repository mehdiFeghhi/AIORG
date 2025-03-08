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




