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



