from statusManager import *
from hillClimbing import hill_climbing
from beamSearch import beam_search
# from simulatedAnnealing import simulated_annealing
# from grasp import grasp
# from genetic import genetic

from trainSet import train_set

from itertools import product
from time import time
import json
# product = produto cartesiano
# print("Hill Climbing:")
# show_result(vt, hill_climbing(vt, sz))

sz = 19 # Tamanho da mochila.
vt = [(1,3), (4,6), (5,7)] # Tuplas (Valor, Tamanho)

metaheuristics = {
    'Hill Climbing': {
        'func': 'hill_climbing',
        'train': False,
        'param': {}
    },
    'Beam Search': {
        'func': beam_search,
        'train': True,
        'param': {
            'k': [10, 25, 50, 100]
        }
    },
    # 'Simulated Annealing': {
    #     'func': simulated_annealing,
    #     'train': True,
    #     'param': {
    #         'temp': [500, 250, 100, 90, 50],
    #         'alfa': [0.99, 0.97, 0.95, 0.9, 0.85, 0.7],
    #         'numIter': [50, 100, 200, 350, 500]
    #     }
    # },
    # 'GRASP': {
    #     'func': grasp,
    #     'train': True,
    #     'param': {
    #         'numIter': [50, 100, 200, 350, 500],
    #         'numBest': [2, 5, 10, 15]
    #     }
    # },
    # 'Genetic Algorithm': {
    #     'func': genetic,
    #     'train': True,
    #     'param': {
    #         'population': [10, 20, 30],
    #         'taxa de crossover': [0.75, 0.85, 0.95],
    #         'taxa de mutação': [0.10, 0.20, 0.30]
    #     }
    # }
}

# # a escolha do hiperparametro será de acordo com a media mornalizada

# print(json.dumps(metaheuristics, indent=4))

def table_comb_X_problems(results, input_set):
    print("\t", end='')
    for r in results.values():
        for p in r.keys():
            print(p, end='\t')
        break
    print()
    for (c,r) in results.items():
        print(c, end='\t', sep='')
        for d in r.values():
            print(d['value'], end='\t')
        print()

def normalize(results):
    for r in results.values():
        keys = list(r.keys())
        break
    norm = {} # Resultados normalizados
    for p in keys:
        best_value = 0
        # Loop para achar o maior valor obtido no problema dentre diferentes combinações.
        for r in results.values():
            if r[p]['value'] > best_value:
                best_value = r[p]['value']
        norm[p] = []
        for r in results.values():
            norm[p].append(r[p]['value']/best_value)
    return norm

def average(normalized_results, index):
    nr = list(normalized_results.values())
    s = sum([l[index] for l in nr])
    return s/len(nr)

def best_hiperparam(hp, normalized_results):
    best_param, best_avg = (), 0
    for (i, c) in enumerate(hp):
            avg = average(normalized_results, i)
            if avg > best_avg:
                best_param, best_avg = c, avg
    return (best_param, best_avg)

for (mh_name, data) in metaheuristics.items():
    if data.get('train'):
        mh = data.get('func')
        param_list = [v for (k,v) in data.get('param').items()]
        hp = list(product(*param_list)) # Combinações de hiperparâmetros
        results = {}
        for c in hp: # Para cada combinação de valores de hiperparâmetros
            results_comb = {} # Cada elemento é o resultado de c aplicado ao problema p.
            for (p, d) in train_set.items():
                begin = time()
                r_mh = mh(d['vt'], d['t'], c) # Resultado da metaheuristica
                end = time()
                elapsed_time = end - begin
                results_comb[p] = {
                    'result': r_mh,
                    'value': calc_value(r_mh, d['vt']),
                    'time': elapsed_time
                }
            results[c] = results_comb
        table_comb_X_problems(results, train_set)
        normalized_results = normalize(results)
        best_hp = best_hiperparam(hp, normalized_results)
        print(best_hp)

        # Gerar boxplot dos resultados alcançados pela metaheurística
        # Gerar boxplot dos tempos alcançados pela metaheurística