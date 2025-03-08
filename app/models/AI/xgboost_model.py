import os
import numpy as np
import xgboost as xgb
from .base_model import BaseModel  # Ensure BaseModel is implemented correctly

class XGBoostModel(BaseModel):
    def __init__(self, param_grid=None, **kwargs):
        """
        Initialize the XGBoost model with custom hyperparameters.

        Args:
            param_grid (dict, optional): Dictionary specifying hyperparameter ranges for GridSearchCV.
                                         If None, a default parameter grid is used.
            **kwargs: Additional keyword arguments for initializing the XGBClassifier.
        """
        # Define a default parameter grid for hyperparameter tuning
        default_param_grid = {
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'n_estimators': [50, 100, 200],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
        }

        # Use the provided param_grid or fall back to the default
        self.param_grid = param_grid or default_param_grid
        xgb.XGBRFClassifier
        # Initialize the BaseModel with XGBClassifier as the base estimator
        super().__init__(xgb.XGBClassifier, self.param_grid, **kwargs)
        self.model.__class__.__name__ = 'XGB'
# Usage example
if __name__ == "__main__":
    # Define the base directory for saving models
    base_directory_model = os.path.expanduser("~/Documents/AIOrganization/Models_save")
    name_position = "Test"  # Optional subdirectory name for saving models

    # Generate synthetic data for demonstration
    X = np.random.rand(100, 5)  # Example feature matrix (100 samples, 5 features)
    y = np.random.randint(0, 2, size=100)  # Example binary target labels

    # Instantiate the XGBoost model
    model = XGBoostModel()

    # Save the model and its associated metadata (assumes save_model_with_card is implemented in BaseModel)
    model.save_model_with_card(X, y, base_directory_model, name_position)
