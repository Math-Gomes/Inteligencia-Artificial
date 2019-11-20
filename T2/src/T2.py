import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_score, train_test_split

from zeroR import ZeroR
from oneR import OneR
from sklearn.naive_bayes import GaussianNB

from tabulate import *

bases = {
    'iris': datasets.load_iris(),
    'digits': datasets.load_digits(),
    'wine': datasets.load_wine(),
    'breast cancer': datasets.load_breast_cancer()
}

classifiers1 = {
    'ZeroR': ZeroR(),
    'OneR': OneR(),
    'Naive Bayes Gaussiano': GaussianNB()
}

classifiers2 = []

def part1():
    results = []
    print('Executando parte 1:')
    for (base_name, base) in bases.items():
        print(base_name)
        base_results = []
        for (classifier_name, classifier) in classifiers1.items():
            print('  ', classifier_name)
            x_train, x_test, y_train, y_test = train_test_split(base.data, base.target, test_size = 0.4, random_state = 0)
            scores = cross_val_score(classifier, base.data, base.target, cv = 10)
            base_results.append([classifier_name, np.mean(scores), np.std(scores)])
            # print ('CV Accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))
            # print(scores)
        results.append(base_results)
    
    for r in results:
        print(tabulate(r, headers = ['CLASSIFIER', 'MEAN', 'STDEV'], tablefmt = "psql", stralign = "center", numalign = "center"))

def part2():
    pass

if __name__ == "__main__":
    part1()
    part2()