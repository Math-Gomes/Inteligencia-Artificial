import numpy as np
from sklearn import datasets

iris = datasets.load_iris()

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()

knn.fit(X_train, y_train)

KNeighborsClassifier(algorithm='auto',leaf_size=30,metric='minkowski',metric_params=None,n_jobs=None,n_neighbors=5,p=2,weights='uniform')

y_predict = knn.predict(X_test)
y_predict
# array([2, 1, 0, 2, 0, 2, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1,
#        0, 0, 1, 0, 0, 1, 1, 0, 2, 1, 0, 2, 2, 1, 0, 2, 1, 1, 2, 0, 2, 0,
#        0, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2])

y_test
# array([2, 1, 0, 2, 0, 2, 0, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1,
#        0, 0, 2, 0, 0, 1, 1, 0, 2, 1, 0, 2, 2, 1, 0, 1, 1, 1, 2, 0, 2, 0,
#        0, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2])
knn.score(X_test, y_test)

from sklearn.metrics import precision_score, recall_score, f1_score

precision_score(y_pred = y_predict, y_true=y_test, average='macro')
print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='macro'))
print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='micro'))
print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='weighted'))

from sklearn.metrics import confusion_matrix         
confmat = confusion_matrix(y_true=y_test, y_pred=y_predict)
confmat

print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='macro'))
print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='micro'))
print("precision score: %.2f" % precision_score(y_pred = y_predict, y_true=y_test, average='weighted'))

confmat

print("recall score: %.2f" % recall_score(y_pred = y_predict, y_true=y_test, average='macro'))
print("recall score: %.2f" % recall_score(y_pred = y_predict, y_true=y_test, average='micro'))
print("recall score: %.2f" % recall_score(y_pred = y_predict, y_true=y_test, average='weighted'))

print("fmeasure score: %.2f" % f1_score(y_pred = y_predict, y_true=y_test, average='macro'))
print("fmeasure score: %.2f" % f1_score(y_pred = y_predict, y_true=y_test, average='micro'))
print("fmeasure score: %.2f" % f1_score(y_pred = y_predict, y_true=y_test, average='weighted'))

from sklearn.model_selection import cross_val_score
scores = cross_val_score(knn, iris.data, iris.target, cv = 5)
scores
print("Mean: %0.2f Standart Deviation: %0.2f" % (scores.mean(), scores.std()))
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

from sklearn.model_selection import cross_validate
scorings = ['accuracy','precision_macro','recall_macro','f1_macro']
scores = cross_validate(knn, iris.data, iris.target, scoring = scorings, cv = 5)

scores_acc = scores['test_accuracy']
print("Accuracy: %0.2f (+/- %0.2f)" % (scores_acc.mean(), scores_acc.std()*2))

scores_precision = scores['test_precision_macro']
print("Precision macro: %0.2f (+/- %0.2f)" % (scores_precision.mean(), scores_precision.std()*2))

scores_recall = scores['test_recall_macro']
print("Scores recall macro: %0.2f (+/- %0.2f)" % (scores_precision.mean(), scores_precision.std()*2))

scores_f1 = scores['test_f1_macro']
print("f1 macro: %0.2f (+/- %0.2f)" % (scores_precision.mean(), scores_precision.std()*2))

from sklearn.model_selection import GridSearchCV

grade = {'n_neighbors': [1,3,5]}
gs = GridSearchCV(estimator=knn, param_grid=grade, scoring='accuracy', cv = 10)
gs = gs.fit(X_train, y_train)

print(gs.best_score_)
print(gs.best_params_)
print(gs.cv_results_.keys())

grade = {'n_neighbors': list(range(1,11))}
gs = GridSearchCV(estimator=knn, param_grid=grade, scoring='accuracy', cv = 7)
gs = gs.fit(X_train, y_train)

print(gs.best_score_)
print(gs.best_params_)
knn = KNeighborsClassifier(n_neighbors = 10)
knn.fit(X_train, y_train)
KNeighborsClassifier(algorithm='auto',leaf_size=30,metric='minkowski',metric_params=None,n_jobs=None,n_neighbors=10,p=2,weights='uniform')

knn.score(X_test, y_test)