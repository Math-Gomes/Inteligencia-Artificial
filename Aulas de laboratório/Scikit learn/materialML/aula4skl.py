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
knn = KNeighborsClassifier()

from sklearn import preprocessing #discretizer

import pandas as pd  # dataframe

from sklearn.impute import SimpleImputer  #missing values

from sklearn.experimental import enable_iterative_imputer  #missing values
from sklearn.impute import IterativeImputer  #missing values

'''
df = pd.DataFrame([['green', 'M', 10.1, 'class1'], ['red', 'L', 13.5, 'class2'],['blue', 'XL', 15.3, 'class1']])
df.columns = ['color', 'size', 'price', 'classlabel']
print(df)


size_mapping = {'XL': 3, 'L': 2, 'M': 1}
df['size'] = df['size'].map(size_mapping)
print(df)


print(pd.get_dummies(df[['price', 'color', 'size']]))



enc = preprocessing.OrdinalEncoder()
enc.fit(df) 
print(enc.transform(df))

enc = preprocessing.OneHotEncoder()
enc.fit(df) 
print(enc.transform(df).toarray())
print(enc.categories_)


est = preprocessing.KBinsDiscretizer(n_bins=[3, 2, 2, 4], encode='ordinal').fit(X_train)
#est = preprocessing.KBinsDiscretizer(n_bins=[3, 2, 2, 4], encode='ordinal', strategy='quantile').fit(X_train)
X_bin = est.transform(X_train)
print(X_bin)

est = preprocessing.KBinsDiscretizer(n_bins=[3, 2, 2, 4], encode='ordinal', strategy='uniform').fit(X_train)
X_bin = est.transform(X_train)
print(X_bin)

est = preprocessing.KBinsDiscretizer(n_bins=[3, 2, 2, 4], encode='ordinal', strategy='kmeans').fit(X_train)
X_bin = est.transform(X_train)
print(X_bin)


X = [[1, 2], [np.nan, 3], [7, 6]]
print(X)
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
imp.fit(X)  
X_test = [[np.nan, 2], [6, np.nan], [7, 6]]
print(X_test)
print(imp.transform(X_test))   


X = [[1, 2], [-1, 3], [7, 6]]
print(X)
imp = SimpleImputer(missing_values=-1, strategy='mean')
imp.fit(X)  
X_test = [[-1, 2], [6, -1], [7, 6]]
print(X_test)
print(imp.transform(X_test))


df = pd.DataFrame([["a", "x"],
                   [np.nan, "y"],
                   ["a", np.nan],
                   ["b", "y"]], dtype="category")
imp = SimpleImputer(strategy="most_frequent")
print(imp.fit_transform(df))



from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_r = pca.fit(X_train).transform(X_train)
print(X_train, X_r)



from sklearn.feature_selection import VarianceThreshold
X = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 1]]
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
X_t = sel.fit_transform(X)
print(X_t)

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

X_b = SelectKBest(chi2, k=2).fit_transform(X_train, y_train)
print (X_b)

'''



