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

from sklearn.model_selection import cross_val_score
scores = cross_val_score(knn, iris.data, iris.target, cv = 5)

from sklearn.model_selection import GridSearchCV
grade = {'n_neighbors': [1,3,5]}
gs = GridSearchCV(estimator=knn, param_grid=grade, scoring='accuracy', cv = 10)
gs = gs.fit(X_train, y_train)

# print(gs.best_score_)
# print(gs.best_params_)
# print(gs.cv_results_.keys())

# print(gs.cv_results_['split8_test_score'][0])
# print(gs.cv_results_['split9_test_score']) # (split9 , fold 10)

parciais1 = np.array([gs.cv_results_['split0_test_score'][0],
                      gs.cv_results_['split1_test_score'][0],
                      gs.cv_results_['split2_test_score'][0],
                      gs.cv_results_['split3_test_score'][0],
                      gs.cv_results_['split4_test_score'][0],
                      gs.cv_results_['split5_test_score'][0],
                      gs.cv_results_['split6_test_score'][0],
                      gs.cv_results_['split7_test_score'][0],
                      gs.cv_results_['split8_test_score'][0],
                      gs.cv_results_['split9_test_score'][0]])

parciais2 = np.array([gs.cv_results_['split0_test_score'][1],
                      gs.cv_results_['split1_test_score'][1],
                      gs.cv_results_['split2_test_score'][1],
                      gs.cv_results_['split3_test_score'][1],
                      gs.cv_results_['split4_test_score'][1],
                      gs.cv_results_['split5_test_score'][1],
                      gs.cv_results_['split6_test_score'][1],
                      gs.cv_results_['split7_test_score'][1],
                      gs.cv_results_['split8_test_score'][1],
                      gs.cv_results_['split9_test_score'][1]])

# print(parciais1)
# print(parciais2)

import seaborn as sns
import matplotlib.pyplot as plt

# sns.boxplot(data = [parciais1, parciais2], showmeans = True)
# plt.show()

# data1 = np.array([1,2,1,1,2,1])
# data2 = np.array([3,5,5,5,4,5])
# data3 = np.array([3,1,2,5,4,5])
# data4 = np.array([1,7,4,5,3,9])

# sns.boxplot(data = [data1,data2,data3,data4], showmeans = True)
# plt.show()

grade = {'n_neighbors': [1,3,5]}
gs = GridSearchCV(estimator=knn, param_grid=grade, scoring='accuracy', n_jobs=-1)
scores = cross_val_score(gs, X_train, y_train, scoring='accuracy', cv = 5)

# print('CV Accuracy: %.3f +/- %.3f' %(np.mean(scores), np.std(scores)))
# print(scores)

grade = {'n_neighbors': [1,3,5]}
gs = GridSearchCV(estimator=knn, param_grid=grade, scoring='accuracy', n_jobs=-1, cv=7)
scores = cross_val_score(gs, iris.data, iris.target, scoring='accuracy', cv=10)

# print('CV Accuracy: %.3f +/- %.3f' %(np.mean(scores), np.std(scores)))
# print(scores)

from scipy import stats
from math import sqrt
from numpy import mean
from scipy.stats import t

data1 = np.array([1,2,1,1,2,1])
data2 = np.array([3,5,5,5,4,5])

def dependent_ttest(data1, data2, alpha):
    # calculate means
    mean1, mean2 = mean(data1), mean(data2)
    # number of paired samples
    n = len(data1)
    # sum squared difference between observations
    d1 = sum([(data1[i]-data2[i])**2 for i in range(n)])
    # sum difference between observations
    d2 = sum([(data1[i]-data2[i]) for i in range(n)])
    # standart deviation of the difference between means
    sd = sqrt((d1-(d2**2 / n)) / (n-1))
    # standart error of the difference between the means
    sed = sd/sqrt(n)
    # calculate t statistic
    t_stat = (mean1 - mean2)/sed
    # degrees of freedom
    df = n-1
    # calculate the critival value
    cv = t.ppf(1.0 - alpha, df)
    # calculate the p value
    p = (1.0-t.cdf(abs(t_stat), df))*2.0
    # return everything
    return t_stat, df, cv, p

# print("ttest pareado: ")
# print(dependent_ttest(data1, data2, 0.95))
# print(stats.ttest_rel(data1, data2))

###############################################################################

from sklearn import preprocessing

max_abs_scaler = preprocessing.MaxAbsScaler()
X_train_maxabs = max_abs_scaler.fit_transform(X_train)
# print(X_train)
# print(X_train_maxabs)
X_test_maxabs = max_abs_scaler.transform(X_test)
# print(X_test)
# print(X_test_maxabs)
# print(max_abs_scaler.scale_)

min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)
# print(X_train)
# print(X_train_minmax)
X_test_minmax = min_max_scaler.transform(X_test)
# print(X_test)
# print(X_test_minmax)
# print(min_max_scaler.scale_) # 1/(max-min)

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(10,20))
X_train_minmax = min_max_scaler.fit_transform(X_train)
# print(X_train)
# print(X_train_minmax)
X_test_minmax = min_max_scaler.transform(X_test)
# print(X_test)
# print(X_test_minmax)
# print(min_max_scaler.scale_) # 1/(max-min)

# Z SCORE
X_scaled = preprocessing.scale(X_train)
# print(X_scaled)
# print(X_scaled.mean(axis=0))
# print(X_scaled.std(axis=0))

scaler = preprocessing.StandardScaler().fit(X_train)
X_train_scaler = scaler.transform(X_train)
print(X_train)
print(X_train_scaler)

X_test_scaler = scaler.transform(X_test)
print(X_test)
print(X_test_scaler)