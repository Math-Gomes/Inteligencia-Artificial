import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_X_y

class ZeroR(BaseEstimator, ClassifierMixin):
    def __init__(self, demo_param = 'demo'):
        self.demo_param = demo_param
    
    def get_params(self, deep = True):
        return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)
        self.c = np.argmax(np.bincount(y))

    def predict(self, X):
        n, _ = X.shape
        return self.c * np.ones(n)