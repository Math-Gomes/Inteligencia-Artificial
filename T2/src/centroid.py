import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_X_y
from scipy.spatial.distance import euclidean

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class Centroid(BaseEstimator, ClassifierMixin):
    def __init__(self, demo_param = 'demo'):
        self.demo_param = demo_param
    
    def get_params(self, deep = True):
        return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)
        self.centroids = []
        for c in self.classes_:
            group = [X[j] for (j, c_) in enumerate(y) if c_ == c]
            centr = [np.mean(coord) for coord in zip(*group)]
            self.centroids.append(centr)

    def predict(self, X):
        return [np.argmin([euclidean(e, c) for c in self.centroids]) for e in X]