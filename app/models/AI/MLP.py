from sklearn.neural_network import MLPClassifier
from .base_model import BaseModel
import os
import numpy as np


class MLPModel(BaseModel):
    def __init__(self, param_grid=None, **kwargs):
        """
        Initialize the MLP model with custom parameters. Inherits from BaseModel.
        
        param_grid (dict): Dictionary of hyperparameters for MLPClassifier or for GridSearchCV.
        **kwargs: Additional keyword arguments for MLPClassifier initialization (e.g., hidden_layer_sizes, activation, etc.)
        """
        # Default parameter grid for MLPClassifier if not provided
        default_param_grid = {
            'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
            'activation': ['relu', 'tanh', 'logistic'],
            'solver': ['adam', 'sgd'],
            'learning_rate': ['constant', 'adaptive'],
            'alpha': [0.0001, 0.001, 0.01]
        }
        
        # If a custom param_grid is provided, merge it with the default
        if param_grid is None:
            param_grid = default_param_grid
        self.param_grid = param_grid
        
        # Call the parent class constructor to initialize the model
        super().__init__(MLPClassifier, param_grid, **kwargs)
        self.model.__class__.__name__ = 'MLP'

