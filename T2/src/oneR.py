import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_X_y

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class OneR(BaseEstimator, ClassifierMixin):
    def __init__(self, demo_param = 'demo'):
        self.demo_param = demo_param
    
    def get_params(self, deep = True):
        return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes = unique_labels(y)
        self.discret = KBinsDiscretizer(n_bins = len(np.unique(y)), encode = 'ordinal', strategy = 'quantile')
        X = self.discret.fit_transform(X)

        tables, sums = [], []
        values_X = np.unique(X)

        for feat in X.T:
            tb = [[0]*len(self.classes) for _ in range(len(values_X))]
            for j, f_value in enumerate(feat.astype(int)):
                tb[f_value][y[j]] += 1
            s = sum(max(list(tb[k])) for k in range(len(tb)))
            sums.append(s)
            tables.append(tb)

        self.best_feat = np.argmax(sums)
        self.rules = [np.argmax(row) for row in tables[self.best_feat]]

    def predict(self, X):
        X = self.discret.fit_transform(X)
        column = X.T[self.best_feat]
        return [self.rules[e] for e in column.astype(int)]