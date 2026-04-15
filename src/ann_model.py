import numpy as np

class ANN:
    """
    Artificial Neural Network for binary classification
    Architecture: Input -> Hidden Layer -> Output Layer
    """
    
    def __init__(self, hidden_units=64, lr=0.01, epochs=500, batch_size=32):
        """
        Initialize ANN
        
        Args:
            hidden_units: Number of neurons in hidden layer
            lr: Learning rate
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        self.hidden_units = hidden_units
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        
        # Weights and biases (will be initialized in fit)
        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None
    
    def relu(self, z):
        """ReLU activation function"""
        return np.maximum(0, z)
    
    def relu_derivative(self, z):
        """Derivative of ReLU"""
        return (z > 0).astype(float)
    
    def sigmoid(self, z):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-z))
    
    def sigmoid_derivative(self, z):
        """Derivative of sigmoid"""
        s = self.sigmoid(z)
        return s * (1 - s)
    
    def forward(self, X):
        """
        Forward propagation
        
        Returns:
            z1: Linear output from hidden layer
            a1: Activated output from hidden layer
            z2: Linear output from output layer
            a2: Activated output from output layer (predictions)
        """
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        
        return self.z1, self.a1, self.z2, self.a2
    
    def backward(self, X, y, z1, a1, z2, a2, batch_size):
        """
        Backward propagation
        
        Returns:
            dW1, db1, dW2, db2: Gradients
        """
        # Output layer error
        dz2 = a2 - y
        dW2 = (1/batch_size) * np.dot(a1.T, dz2)
        db2 = (1/batch_size) * np.sum(dz2, axis=0, keepdims=True)
        
        # Hidden layer error
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self.relu_derivative(z1)
        dW1 = (1/batch_size) * np.dot(X.T, dz1)
        db1 = (1/batch_size) * np.sum(dz1, axis=0, keepdims=True)
        
        return dW1, db1, dW2, db2
    
    def fit(self, X, y):
        """
        Train the neural network
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training labels (n_samples, 1)
        """
        n_samples, n_features = X.shape
        
        # Initialize weights with Xavier initialization
        self.W1 = np.random.randn(n_features, self.hidden_units) * np.sqrt(1 / n_features)
        self.b1 = np.zeros((1, self.hidden_units))
        self.W2 = np.random.randn(self.hidden_units, 1) * np.sqrt(1 / self.hidden_units)
        self.b2 = np.zeros((1, 1))
        
        # Reshape y to (n_samples, 1) if needed
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)
        
        # Training loop
        for epoch in range(self.epochs):
            # Shuffle data
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            
            # Mini-batch training
            for i in range(0, n_samples, self.batch_size):
                X_batch = X_shuffled[i:i+self.batch_size]
                y_batch = y_shuffled[i:i+self.batch_size]
                
                # Forward propagation
                z1, a1, z2, a2 = self.forward(X_batch)
                
                # Backward propagation
                dW1, db1, dW2, db2 = self.backward(X_batch, y_batch, z1, a1, z2, a2, len(X_batch))
                
                # Update weights
                self.W1 -= self.lr * dW1
                self.b1 -= self.lr * db1
                self.W2 -= self.lr * dW2
                self.b2 -= self.lr * db2
    
    def predict_proba(self, X):
        """
        Predict probability for binary classification
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Probabilities (n_samples,)
        """
        _, _, _, a2 = self.forward(X)
        return a2.ravel()
    
    def predict(self, X):
        """
        Predict class labels
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Binary predictions (n_samples,)
        """
        probs = self.predict_proba(X)
        return (probs >= 0.5).astype(int)
    
    def save_model(self, path):
        """
        Save model weights to file
        
        Args:
            path: Path to save the model
        """
        np.savez(path,
                 W1=self.W1,
                 b1=self.b1,
                 W2=self.W2,
                 b2=self.b2,
                 hidden_units=self.hidden_units)
    
    def load_model(self, path):
        """
        Load model weights from file
        
        Args:
            path: Path to load the model
        """
        data = np.load(path)
        self.W1 = data["W1"]
        self.b1 = data["b1"]
        self.W2 = data["W2"]
        self.b2 = data["b2"]
        self.hidden_units = int(data["hidden_units"])
