from statusManager import *
from hillClimbing import hill_climbing
from beamSearch import beam_search
from simulatedAnnealing import simulated_annealing
from grasp import grasp
# from genetic import genetic

from problems import train_set, test_set

from output import *

from itertools import product
from time import time
import statistics
import json
from datetime import datetime

metaheuristics = {
    'Hill Climbing': {
        'func': hill_climbing,
        'train': False,
        'param': {},
        'hiperparam': ()
    },
    # 'Beam Search': {
    #     'func': beam_search,
    #     'train': True,
    #     'param': {
    #         'k': [10, 25, 50, 100]
    #     },
    #    'hiperparam': ()
    # },
    # 'Simulated Annealing': {
    #     'func': simulated_annealing,
    #     'train': True,
    #     'param': {
    #         'temp': [500, 250, 100, 90, 50],
    #         'alfa': [0.99, 0.97, 0.95, 0.9, 0.85, 0.7],
    #         'num_iter': [50, 100, 200, 350, 500]
    #     },
    #    'hiperparam': ()
    # },
    # 'GRASP': {
    #     'func': grasp,
    #     'train': True,
    #     'param': {
    #         'num_iter': [50, 100, 200, 350, 500],
    #         'num_best': [2, 5, 10, 15]
    #     },
    #    'hiperparam': ()
    # },
    # 'Genetic Algorithm': {
    #     'func': genetic,
    #     'train': True,
    #     'param': {
    #         'population': [10, 20, 30],
    #         'crossover_tax': [0.75, 0.85, 0.95],
    #         'mutation_tax': [0.10, 0.20, 0.30]
    #     },
    #    'hiperparam': ()
    # }
}

def normalize(results):
    keys = list(results.values())[0].keys()
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

def average(normalized_results, comb_index):
    n = normalized_results.values()
    s = sum([l[comb_index] for l in n])
    return s/len(n)

def k_best_hiperparams(hp, normalized_results, k):
    best_param, best_avg = (), 0
    k_best = []
    for (i, c) in enumerate(hp):
        avg = average(normalized_results, i)
        if len(k_best) < k:
            k_best.append((c, avg))
            k_best.sort(key = lambda t: t[1], reverse = True)
        elif avg > k_best[-1][1]:
            k_best.pop()
            k_best.append((c, avg))
            k_best.sort(key = lambda t: t[1], reverse = True)
    return k_best

def best_hiperparam(hp, normalized_results):
    return k_best_hiperparams(hp, normalized_results, 1)[0]

def train_hill_climbing():
    mh_name = "Hill Climbing"
    data = metaheuristics[mh_name]
    mh = data.get('func')
    results = {}
    max_time = 2
    print(mh_name)
    for (p, d) in train_set.items():
        print("  ", p) # Printa o nome do problema em execução
        begin = time()
        r_mh = mh(d['vt'], d['t'], (), max_time) # Resultado da metaheuristica
        end = time()
        elapsed_time = end - begin
        results[p] = {
            'result': r_mh,
            'value': calc_value(r_mh, d['vt']),
            'time': elapsed_time
        }

    new = {}
    for (p,d) in results.items():
        d['result'] = str(d['result'])
        new[p] = d

    filename = "results/data_"+mh_name.replace(" ", "")+".txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write(mh_name+" "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
        f.write("\nRESULTADOS:\n")
        f.write("results = "+json.dumps(new, indent=4)+"\n")

def train():
    max_time = 2 # Tempo máx. de exec. de uma meta heurística no treino: 2 minutos.
    for (mh_name, data) in metaheuristics.items():
        if data.get('train'):
            print(mh_name)
            mh = data.get('func')
            param_list = [v for (k,v) in data.get('param').items()]
            hp = list(product(*param_list)) # Combinações de hiperparâmetros
            print("NUMERO DE COMBINACOES: ", len(hp))
            results = {}
            for (i, c) in enumerate(hp, start=1): # Para cada combinação de valores de hiperparâmetros
                print(i) # Printa a i-ésima combinação em execução
                results_comb = {} # Cada elemento é o resultado de c aplicado ao problema p.
                for (p, d) in train_set.items():
                    print("  ", p) # Printa o nome do problema em execução
                    begin = time()
                    r_mh = mh(d['vt'], d['t'], c, max_time) # Resultado da metaheuristica
                    end = time()
                    elapsed_time = end - begin
                    results_comb[p] = {
                        'result': r_mh,
                        'value': calc_value(r_mh, d['vt']),
                        'time': elapsed_time
                    }
                results[c] = results_comb
            # print_json(results)
            print()
            # table_comb_X_problems(results, train_set)
            print()

            normalized_results = normalize(results)
            k_best = k_best_hiperparams(hp, normalized_results, 10)

            print("MELHORES HIPERPARAMETROS:")
            for (i, e) in enumerate(k_best, start=1):
                print(i, e, sep=' - ')

            write_results_file(mh_name, c, p, results, k_best)
            print()

            # Gerar boxplot dos resultados alcançados pela metaheurística
            # Gerar boxplot dos tempos alcançados pela metaheurística

def test():
    max_time = 5 # Tempo máx. de exec. de uma meta heurística no teste: 5 minutos.
    results = {}
    for (mh_name, data) in metaheuristics.items():
        print(mh_name)
        mh = data.get('func')
        results_mh = {} # Cada elemento é o resultado da meta heurística aplicada ao problema p.
        hp = data.get('hiperparam') # Hiperparâmetro escolhido para a metaheurística.
        print("HIPERPARAMETROS:", hp)
        for (p, d) in test_set.items():
            print("  ", p) # Printa o nome do problema em execução
            begin = time()
            r_mh = mh(d['vt'], d['t'], hp, max_time) # Resultado da metaheuristica
            end = time()
            elapsed_time = end - begin
            results_mh[p] = {
                'result': r_mh,
                'value': calc_value(r_mh, d['vt']),
                'time': elapsed_time
            }

        # Obter média absoluta e desvio padrão das execuções
        
        # Obter média e desvio padrão dos tempos de execução
        times = [d['time'] for d in results_mh.values()]
        results_mh['mean_times'] = statistics.mean(times)
        results_mh['stdev_times'] = statistics.stdev(times)

        results[mh_name] = results_mh

    print(json.dumps(results, indent=2))
    # for (p, d) in test_set:
    #     # Normalizar resultados alcançados pelas metaheurísticas
    #     pass

    # Obter média e desvio padrão dos resultados normalizados de cada metaheurística

    # Gerar tabela contendo média e desvio padrão absolutos e normalizados,
    # e média e desvio padrão dos tempos de execução de todas as metaheurísticas

    # for (p, d) in test_set:
    #     # Fazer ranqueamento das metaheurísticas segundo resultado absoluto
    #     # Fazer ranqueamento das metaheurísticas segundo resultado normalizado
    #     pass

    # Obter média dos ranqueamentos das metaheurísticas segundo resultado absoluto

    # Apresentar as metaheurísticas em ordem crescente de média de ranqueamento

    # Obter média dos ranqueamentos das metaheurísticas segundo resultado normalizado

    # Apresentar as metaheurísticas em ordem crescente de média de ranqueamento

    # Gerar boxplot dos resultados alcançados pelas metaheurísticas

    # Gerar boxplot dos tempos alcançados pelasa metaheurísticas

if __name__ == '__main__':
    train()
    # test()
    # train_hill_climbing()

# a escolha do hiperparametro será de acordo com a media mornalizada
# TO DO:
# fazer latex
# add parametro do tempo maximo no genetico
# verificar nas anotacoes se tem algo a alterar nos algoritmos
# revisar os algoritmos e ver se está tudo certo