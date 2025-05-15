from sklearn.tree import DecisionTreeClassifier
from .base_model import BaseModel
import numpy as np

class DecisionTreeModel(BaseModel):
    def __init__(self, param_grid=None, num_classes=None, **kwargs):
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
        super().__init__(DecisionTreeClassifier, param_grid, num_classes=num_classes, **kwargs)
        self.model.__class__.__name__ = 'DecisionTree'

