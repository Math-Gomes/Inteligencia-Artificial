import numpy as np
import pandas as pd
from random import random
from sklearn import datasets
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import euclidean_distances, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

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
            chances = list(map(lambda k: k/sum(row), row))
            chances = list(zip(chances, range(len(chances))))
            chances.sort()
            c_ = accumulate(list(map(lambda k: k[0], chances)))
            chances = list(zip(c_, list(map(lambda k: k[1], chances))))
            self.rules.append(chances)

    def predict(self, X):
        X = self.discret.fit_transform(X)
        column = X.T[self.best_feat]
        result = []
        for e in column.astype(int):
            r = random()
            for (chance, class_) in self.rules[e]:
                if r < chance:
                    result.append(class_)
                    break
        return result

if __name__ == "__main__":
    nn = OneRProbabilistic()

    base = datasets.load_iris()
    # base = datasets.load_digits()
    # base = datasets.load_wine()
    # base = datasets.load_breast_cancer()

    x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)

    nn.fit(x_train, y_train)
    y_pred = nn.predict(x_test)

    # scores = cross_val_score(nn, base.data, base.target, cv = 10)
    # print ('CV Accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
    # print(scores)
