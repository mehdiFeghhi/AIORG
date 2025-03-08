from sklearn.svm import SVC
from .base_model import BaseModel
import os
import numpy as np

class SVMModel(BaseModel):
    def __init__(self, param_grid=None, **kwargs):
        """
        Initialize the SVM model with custom parameters. Inherits from BaseModel.
        
        param_grid (dict): Dictionary of hyperparameters for SVC or for GridSearchCV.
        **kwargs: Additional keyword arguments for SVC initialization (e.g., C, gamma, kernel, etc.)
        """
        # Default parameter grid for SVC if not provided
        default_param_grid = {
            'C': [0.1, 1.0, 10.0],
            'gamma': ['scale', 'auto'],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid']
        }
        
        # If a custom param_grid is provided, merge it with the default
        if param_grid is None:
            param_grid = default_param_grid
        self.param_grid = param_grid
        
        # Call the parent class constructor to initialize the model
        super().__init__(SVC, param_grid, **kwargs)
        self.model.__class__.__name__ = 'SVM'



# Usage example
if __name__ == "__main__":
    base_directory_model = os.path.expanduser("~/Documents/AIOrganization/Models_save")  # The base directory for saving models
    name_position = "Test"  # This can be set to a specific folder name if needed
    X = np.random.rand(100, 5)  # Example feature data
    y = np.random.randint(0, 2, 100)  # Example binary labels

    model = SVMModel()
    model.save_model_with_card(X, y, base_directory_model, name_position)
