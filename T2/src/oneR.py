import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import euclidean_distances, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

class OneR(BaseEstimator, ClassifierMixin):
    # def __init__(self, demo_param = 'demo'):
    #     self.demo_param = demo_param
    
    def get_params(self, deep = True):
        return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)

        self.disc = KBinsDiscretizer(n_bins = len(np.unique(y)), encode = 'ordinal', strategy = 'quantile')
        X = self.disc.fit_transform(X)

        ct_list, values = [], []

        for (i, j) in enumerate(X.T):
            ct = pd.crosstab(j, y)
            ct_list.append(ct)

            # Soma dos maiores elementos de cada linha da tabela de contingência.
            sum_ = sum(max(list(ct.loc[k,:])) for k in range(ct.shape[1]))

            values.append(sum_)

        self.c = np.argmax(values)
        tb = ct_list[self.c]
        self.rules = list(zip(np.array(tb.index), [np.argmax(t) for t in tb.values]))

    def predict(self, X):
        X = self.disc.fit_transform(X)
        col = X.T[self.c]
        # list_ = []
        # for e in col:
        #     entrou = False
        #     for (v, c) in self.rules:
        #         if v == e:
        #             list_.append(c)
        #             entrou = True
        #             break
        #     if not entrou:
        #         list_.append(0)

        return [c for e in col for (v, c) in self.rules if v == e]

if __name__ == "__main__":
    nn = OneR()

    base = datasets.load_digits()
    x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)

    nn.fit(x_train, y_train)
    y_pred = nn.predict(x_test)

    # print(x_test)
    print(y_pred)
    print()
    print(y_test)
    print()

    # print(f1_score(y_test, y_pred, average='macro')) # Original, mas gera warning
    # print(f1_score(y_test, y_pred, labels = np.unique(y_pred), average='macro')) # Não gera warning

    score = cross_val_score(nn, base.data, base.target, cv = 10)
    print(score)
