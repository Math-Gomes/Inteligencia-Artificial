import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_score, train_test_split

from zeroR import ZeroR
from oneR import OneR
from centroid import Centroid
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from output import *

from time import time

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

bases = {
    'Iris': datasets.load_iris(),
    'Digits': datasets.load_digits(),
    'Wine': datasets.load_wine(),
    'Breast Cancer': datasets.load_breast_cancer()
}

classifiers1 = {
    'ZeroR': ZeroR(),
    'OneR': OneR(),
    'Centroid': Centroid(),
    'Naive Bayes Gaussiano': GaussianNB()
}

classifiers2 = {
    'KNN': {
        'func': KNeighborsClassifier,
        'grid': {'n_neighbors': [1, 3, 5, 7, 10]}
    },
    'Árvore de Decisão': {
        'func': DecisionTreeClassifier,
        'grid': {'max_depth': [None, 3, 5, 10]}
    },
    'Rede Neural': {
        'func': MLPClassifier,
        'grid': {'max_iter': [50, 100, 200], 'hidden_layer_sizes': [(15,)]}
    },
    'Floresta de Árvores': {
        'func': RandomForestClassifier,
        'grid': {'n_estimators': [10, 20, 50, 100]}
    }
}

def part1():
    print('Executando parte 1:')

    results = []

    for (b_name, base) in bases.items():
        print(b_name)
        base_results, base_scores = [], []
        for (c_name, classifier) in classifiers1.items():
            print('  ', c_name)
            x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)
            scores = cross_val_score(classifier, base.data, base.target, cv = 10)
            base_scores.append(scores)
            base_results.append([c_name, np.mean(scores), np.std(scores)])
        create_boxplot(base_scores, 'figs/part1_' + b_name, 'CLASSIFICADORES', 'SCORES', classifiers1.keys())
        results.append(base_results)

    write_results(list(zip(bases.keys(), results)), 'results/part1.txt',  ['CLASSIFICADOR', 'MÉDIA', 'DESVIO PADRÃO'])

def part2():
    print('Executando parte 2:')

    results = []

    for (b_name, base) in bases.items():
        print('\n', b_name)
        base_results, base_scores = [], []
        for (c_name, classifier) in classifiers2.items():
            print('  ', c_name)
            gs = GridSearchCV(estimator = classifier['func'](), param_grid = classifier['grid'], scoring='accuracy', cv = 4)
            gs.fit(base.data, base.target)
            best_params = gs.best_params_
            gs = classifier['func'](**gs.best_params_)
            scores = cross_val_score(gs, base.data, base.target, scoring = 'accuracy', cv = 10)
            base_scores.append(scores)
            base_results.append([c_name, np.mean(scores), np.std(scores), best_params])
        create_boxplot(base_scores, 'figs/part2_' + b_name, 'CLASSIFICADORES', 'SCORES', classifiers2.keys())
        results.append(base_results)

    write_results(list(zip(bases.keys(), results)), 'results/part2.txt', ['CLASSIFICADOR', 'MÉDIA', 'DESVIO PADRÃO', 'MELHOR(ES) PARAMETRO(S)'])

if __name__ == "__main__":
    begin = time()
    part1()
    # part2()
    end = time()
    print('Tempo de execucao:', end - begin, 'segundos.')