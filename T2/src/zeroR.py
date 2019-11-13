import numpy as np
from sklearn import datasets
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score, train_test_split
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

if __name__ == "__main__":
    nn = ZeroR()

    base = datasets.load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)

    nn.fit(x_train, y_train)
    y_pred = nn.predict(x_test)

    # print(f1_score(y_test, y_pred, average='macro')) # Original, mas gera warning
    # print(f1_score(y_test, y_pred, labels = np.unique(y_pred), average='macro')) # Não gera warning

    score = cross_val_score(nn, x_train, y_train, cv = 5)
    # print(score)
