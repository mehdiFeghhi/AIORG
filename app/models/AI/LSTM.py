import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from .base_model import BaseModel  # Assuming the BaseModel is in base_model.py


class LSTM(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=64,num_layers=1, dropout=0.2):
        super(LSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, dropout=dropout, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Last timestep
        return torch.sigmoid(out) if self.fc.out_features == 1 else torch.softmax(out, dim=1)


class LSTMModel(BaseModel):
    def __init__(self,output_size, model=LSTM,param_grid=None, **kwargs):
        """
        Initialize the LSTMModel using the BaseModel class.
        - model: Pass the LSTM class (or any PyTorch model class).
        - kwargs: Pass the architecture-specific parameters like input_size, hidden_size, etc.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loss_function = nn.BCELoss() if output_size == 1 else nn.CrossEntropyLoss()
        self.optimizer = None  # Initialize later after the model is created
        kwargs['output_size'] = output_size
        # Instantiate the model using BaseModel
        super().__init__(model=model, param_grid=param_grid, **kwargs)
        self.model.__class__.__name__ = 'LSTM'
        # Move the model to the appropriate device
        self.model = self.model.to(self.device)

    def train(self, X_train, y_train, epochs=10, batch_size=32, learning_rate=0.001):
        """
        Train the model using PyTorch.
        """
        self.model.train()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Convert data to PyTorch tensors
        X_train = torch.tensor(X_train, dtype=torch.float32).to(self.device)
        y_train = torch.tensor(y_train, dtype=torch.float32 if self.model.fc.out_features == 1 else torch.long).to(self.device)

        for epoch in range(epochs):
            permutation = torch.randperm(X_train.size(0))
            for i in range(0, X_train.size(0), batch_size):
                indices = permutation[i:i + batch_size]
                batch_x, batch_y = X_train[indices], y_train[indices]

                # Forward pass
                self.optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = self.loss_function(outputs.squeeze(), batch_y)
                
                # Backward pass
                loss.backward()
                self.optimizer.step()

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")
        print("Training complete.")

    
    def predict(self, X):
        """
        Custom predict method for the PyTorch model.
        Converts input to a tensor, evaluates the model, and returns predictions.
        """
        self.model.eval()  # Set model to evaluation mode
        X = torch.tensor(X, dtype=torch.float32).to(self.device)

        with torch.no_grad():
            outputs = self.model(X)
            # For multi-class classification, take argmax; for binary, use a threshold
            if outputs.size(1) > 1:  # Multi-class
                predicted = torch.argmax(outputs, dim=1)
            else:  # Binary classification
                predicted = (outputs.squeeze() > 0.5).float()

        return predicted.cpu().numpy()


    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data.
        """
        self.model.eval()
        X_test = torch.tensor(X_test, dtype=torch.float32).to(self.device)
        y_test = torch.tensor(y_test, dtype=torch.float32 if self.model.fc.out_features == 1 else torch.long).to(self.device)

        with torch.no_grad():
            outputs = self.model(X_test)
            predicted = (outputs.squeeze() > 0.5).float() if self.model.fc.out_features == 1 else torch.argmax(outputs, dim=1)
            accuracy = (predicted == y_test).sum().item() / len(y_test)

        print(f"Test Accuracy: {accuracy:.4f}")
        return accuracy

# if __name__ == "__main__":
    
#     # Define the base directory for saving models
#     base_directory_model = os.path.expanduser("~/Documents/AIOrganization/Models_save")

#     # Set the folder name for saving the model (optional)
#     name_position = "Test"

#     # Generate example feature data and labels
#     X = np.random.rand(100, 10, 5)  # 100 samples, 10 time steps, 5 features each
#     y = np.random.randint(0, 3, 100)  # Multi-class labels (e.g., 0, 1, 2)

#     # Initialize the LSTM model
#     model = LSTMModel(
#         model=LSTM,       # Pass the LSTM class
#         input_size=5,    # Number of features per timestep
#         output_size=3,    # Number of output classes
#         hidden_size=64,   # Hidden layer size
#         num_layers=2,     # Number of LSTM layers
#         dropout=0.3,      # Dropout rate
#         param_grid=None   # No hyperparameter grid for simplicity
#     )

#     # Train, evaluate, and save the model along with metadata
#     model.save_model_with_card(X, y, base_directory_model, name_position)
