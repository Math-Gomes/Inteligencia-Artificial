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

def normalize(results):
    return True

def average(param, normalized_results):
    return True

for (mh_name, data) in metaheuristics.items():
    if data.get('train'):
        mh = data.get('func')
        param_list = [v for (k,v) in data.get('param').items()]
        hp = list(product(*param_list)) # Combinações de hiperparâmetros
        results = {} # Talvez usar results como matriz
        for c in hp: # Para cada combinação de valores de hiperparâmetros
            results_comb = {} # Cada elemento é o resultado de c aplicado ao problema p.
            for (p, t, vt) in train_set:
                begin = time()
                r_mh = mh(vt, t, c) # Resultado da metaheuristica
                end = time()
                elapsed_time = end - begin
                # Talvez add mais dados na tupla do resultado...
                # Por exemplo, utilizar um dicionário e como chave a tupla que define o problema.
                # Ou talvez utilizar results como uma matriz.
                r = [r_mh, elapsed_time]
                results_comb[p] = r
            results[c] = results_comb
        
        # print(results)
        # for (k,v) in results.items():
        #     print(k)
        #     for d in v.items():
        #         print(d)

        # for l in results:
        #     print("=========")
        #     for e in l:
        #         print(e)
        # for i in range(len(results)):
        #     for j in range(len(results[0])):
        #         print(results[i][j], end = ' ')
        #     print()

        # for (p, t, vt) in train_set:
        #     n = normalize(results)

        # best_param, best_avg = (), 0
        # for c in hp:
        #     avg = average(c, n)
        #     if avg > best_avg:
        #         best_param, best_avg = c, avg

        # # Apresentar valores dos hiperparâmetros selecionados para o teste:
        # print(best_param) # (Armazenar esse resultado em alguma estrutura)

        # Gerar boxplot dos resultados alcançados pela metaheurística
        # Gerar boxplot dos tempos alcançados pela metaheurística

# RESULTS |   P1    |    P2    |    P3    |    P4    |
#    C1   |    x    |     x    |     x    |     x    |
#    C2   |    x    |     x    |     x    |     x    |
#    C3   |    x    |     x    |     x    |     x    |
#    C4   |    x    |     x    |     x    |     x    |
#    C5   |    x    |     x    |     x    |     x    |
#    C6   |    x    |     x    |     x    |     x    |
#    C7   |    x    |     x    |     x    |     x    |

# procurar o melhor da tabela
# pra cada celula, dividir ela pelo maior