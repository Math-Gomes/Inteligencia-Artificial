def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import numpy as np
from sklearn import datasets
iris = datasets.load_iris()
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1, metric='euclidean')
knn.fit(X_train, y_train) 
print(knn.predict(X_test))
print(knn.score(X_test, y_test))
print(knn.get_params())
from sklearn.model_selection import cross_val_score
scores = cross_val_score(knn, iris.data, iris.target, cv=5)
print(scores)

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances

class NearestNeighborClassifier(BaseEstimator, ClassifierMixin):
     
    def __init__(self, demo_param='demo'):
         self.demo_param = demo_param

    def fit(self, X, y):

         # Check that X and y have correct shape
         X, y = check_X_y(X, y)
         # Store the classes seen during fit
         self.classes_ = unique_labels(y)

         self.X_ = X
         self.y_ = y
         # Return the classifier
         return self

    def predict(self, X):

         # Check is fit had been called
         #check_is_fitted(self)

         # Input validation
         X = check_array(X)

         closest = np.argmin(euclidean_distances(X, self.X_), axis=1)
         return self.y_[closest]

nn = NearestNeighborClassifier()
nn.fit(X_train, y_train) 
print(nn.predict(X_test))
print(nn.score(X_test, y_test))
print(nn.get_params())
scores = cross_val_score(nn, iris.data, iris.target, cv=5)
print(scores)

