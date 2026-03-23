import numpy as np

class MBGDLogisticRegression:

    def __init__(self, lr=0.01, epochs=500, batch_size=32):
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def fit(self, X, y):

        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        for epoch in range(self.epochs):

            indices = np.random.permutation(n_samples)
            X = X[indices]
            y = y[indices]

            for i in range(0, n_samples, self.batch_size):

                X_batch = X[i:i+self.batch_size]
                y_batch = y[i:i+self.batch_size]

                linear = np.dot(X_batch, self.weights) + self.bias
                preds = self.sigmoid(linear)

                dw = (1/len(X_batch)) * np.dot(X_batch.T, (preds-y_batch))
                db = (1/len(X_batch)) * np.sum(preds-y_batch)

                self.weights -= self.lr * dw
                self.bias -= self.lr * db

    def predict_proba(self, X):

        linear = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear)

    def predict(self, X):

        probs = self.predict_proba(X)
        return (probs >= 0.5).astype(int)

    def save_model(self, path):

        np.savez(path,
                 weights=self.weights,
                 bias=self.bias)

    def load_model(self, path):

        data = np.load(path)
        self.weights = data["weights"]
        self.bias = data["bias"]