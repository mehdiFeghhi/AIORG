from sklearn.tree import DecisionTreeClassifier
from .base_model import BaseModel
import numpy as np

class DecisionTreeModel(BaseModel):
    def __init__(self, param_grid=None, **kwargs):
        """
        Initialize the DecisionTreeClassifier model with custom parameters.
        
        param_grid (dict): Dictionary of hyperparameters for DecisionTreeClassifier or GridSearchCV.
        **kwargs: Additional keyword arguments for DecisionTreeClassifier initialization (e.g., max_depth, criterion, etc.)
        """
        # Default parameter grid for DecisionTreeClassifier if not provided
        default_param_grid = {
            'max_depth': [None, 10, 20, 30],
            'criterion': ['gini', 'entropy'],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': [None, 'sqrt', 'log2']
        }

        # If a custom param_grid is provided, merge it with the default
        if param_grid is None:
            param_grid = default_param_grid
        self.param_grid = param_grid

        # Call the parent class constructor to initialize the model
        super().__init__(DecisionTreeClassifier, param_grid, **kwargs)
        self.model.__class__.__name__ = 'DecisionTree'


# Usage example
if __name__ == "__main__":
    base_directory_model = "/home/mehdi/Documents/AIOrganization/Models_save"  # The base directory for saving models
    name_position = "Test"  # This can be set to a specific folder name if needed
    X = np.random.rand(100, 5)  # Example feature data
    y = np.random.randint(0, 2, 100)  # Example binary labels

    model = DecisionTreeModel()
    model.save_model_with_card(X, y, base_directory_model, name_position)