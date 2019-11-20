import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import euclidean_distances, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
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


if __name__ == "__main__":
    nn = Centroid()

    # base = datasets.load_iris()
    base = datasets.load_digits()
    # base = datasets.load_wine()
    # base = datasets.load_breast_cancer()

    x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)

    # nn.fit(x_train, y_train)
    # y_pred = nn.predict(x_test)

    scores = cross_val_score(nn, base.data, base.target, cv = 10)
    print ('CV Accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
    print(scores)