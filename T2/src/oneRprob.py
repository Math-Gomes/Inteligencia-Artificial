import numpy as np
from random import random
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_X_y

from itertools import accumulate

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class OneRProbabilistic(BaseEstimator, ClassifierMixin):
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
        self.rules = []
        for row in tables[self.best_feat]:
            if sum(row) == 0:
                row = [1]*len(row)
            chances = list(map(lambda k: k/sum(row), row))
            chances = list(zip(chances, range(len(chances))))
            chances.sort()
            c_ = accumulate(list(map(lambda k: k[0], chances)))
            chances = list(zip(c_, list(map(lambda k: k[1], chances))))
            self.rules.append(chances)

    def predict(self, X):
        X = self.discret.fit_transform(X)
        result = []
        for e in X.T[self.best_feat].astype(int):
            r = random()
            for (chance, class_) in self.rules[e]:
                if r < chance:
                    result.append(class_)
                    break
        return result