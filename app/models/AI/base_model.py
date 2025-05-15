import joblib
import inspect

class BaseModel:
    def __init__(self, model_class, param_grid=None, num_classes=None, **kwargs):
        """
        Initialize a base model with a given sklearn or xgboost model and any specific parameters.
        
        model: The machine learning model (e.g., RandomForestClassifier, XGBClassifier, SVC, etc.)
        param_grid: Dictionary of hyperparameters for GridSearchCV (optional, default is None)
        **kwargs: Additional keyword arguments for model initialization (e.g., n_estimators for RandomForest, etc.)
        """

        self.model_class = model_class
        self.param_grid = param_grid or {}
        init_signature = inspect.signature(model_class.__init__)
        if num_classes is not None and 'num_class' in init_signature.parameters:
            kwargs['num_class'] = num_classes
        self.model = self.model_class(**kwargs)
        self.param_grid = param_grid if param_grid is not None else {}
    
    def fit(self, X_train, y_train):
        """
        Train the model on the given dataset.
        """
        self.model.fit(X_train, y_train)
        print(f"{self.model.__class__.__name__} model trained successfully.")

    def predict(self, X):
        """
        Make predictions using the trained model.
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Predict class probabilities for each input sample.
        """
        return self.model.predict_proba(X)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the accuracy of the model on test data.
        """
        accuracy = self.model.score(X_test, y_test)
        return accuracy

    def save_model(self, filepath):
        """
        Save the trained model to a file.
        """
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")


