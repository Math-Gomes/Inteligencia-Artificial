from statusManager import *
from hillClimbing import hill_climbing
from beamSearch import beam_search
from simulatedAnnealing import simulated_annealing
from grasp import grasp
from genetic import genetic

from problems import train_set, test_set

from output import *

import json
from itertools import product
from time import time
from statistics import mean, stdev
from datetime import datetime
from tabulate import tabulate

metaheuristics = {
    'Hill Climbing': {
        'func': hill_climbing,
        'train': False,
        'param': {},
        'hiperparam': (),
        'hiperparam_train': ()
    },
    'Beam Search': {
        'func': beam_search,
        'train': True,
        'param': {
            'k': [10, 25, 50, 100]
        },
       'hiperparam': (10,)
    },
    'Simulated Annealing': {
        'func': simulated_annealing,
        'train': True,
        'param': {
            'temp': [500, 100, 50],
            'alpha': [0.95, 0.85, 0.7],
            'num_iter': [350, 500]
        },
       'hiperparam': (500, 0.95, 500)
    },
    'GRASP': {
        'func': grasp,
        'train': True,
        'param': {
            'num_iter': [50, 100, 200, 350, 500],
            'num_best': [2, 5, 10, 15]
        },
       'hiperparam': (500, 5)
    },
    'Genetic Algorithm': {
        'func': genetic,
        'train': True,
        'param': {
            'population': [10, 20, 30],
            'crossover_tax': [0.75, 0.85, 0.95],
            'mutation_tax': [0.10, 0.20, 0.30]
        },
       'hiperparam': (30, 0.75, 0.3)
    }
}

def normalize_train(results, hp):
    norm = {} # Resultados normalizados
    times = []

    for p in train_set.keys():
        best_value = 0
        p_times = []

        # Loop para achar o maior valor obtido no problema dentre diferentes combinações.
        for r in results.values():
            if r[p]['value'] > best_value:
                best_value = r[p]['value']

        norm[p] = []
        for r in results.values():
            norm[p].append(r[p]['value'] / best_value)
            p_times.append(r[p]['time'])

        times.append(p_times)

    # Lista de lista em que cada lista representa uma combinação
    # e os elementos são o tempo gasto para um dado problema.
    times = list(map(list, zip(*times)))

    # Lista de listas em que cada lista representa uma combinação
    # e os elementos são o resultado normalizado para um dado problema.
    nr_comb = list(map(list, zip(*norm.values())))

    return list(zip(hp, nr_comb, times)) # (Combinação de hp, result. norm., tempos de exe.)

def normalize_test(results):
    norm = {} # Resultados normalizados
    times = []

    for p in test_set.keys():
        best_value = 0
        p_times = []

        # Loop para achar o maior valor obtido no problema dentre diferentes heurísticas.
        for r in results.values():
            if r[p]['value'] > best_value:
                best_value = r[p]['value']

        norm[p] = []
        for r in results.values():
            norm[p].append(r[p]['value'] / best_value)
            p_times.append(r[p]['time'])

        times.append(p_times)

    # Lista de lista em que cada lista representa uma metaheurística
    # e os elementos são o tempo gasto para uma dado problema.
    times = list(map(list, zip(*times)))

    # Lista de listas em que cada lista representa uma metaheurística
    # e os elementos são o resultado dos problemas aplicados a esta metaheurística.
    nr_mh = list(map(list, zip(*norm.values())))

    return list(zip(results.keys(), nr_mh, times))

def ranking_abs(results):
    rank = {}
    for p in test_set.keys():

        # Procedimento para ordenar os valores obtidos do problema
        # aplicado as metaheuristicas.
        tmp = []
        for mh in metaheuristics.keys():
            tmp.append([mh, results[mh][p]['value']])
        tmp.sort(key = lambda k: k[1], reverse = True)

        # Procedimento para ranquear as metaheuristicas.
        # Se duas metaheuristicas obtém o mesmo valor, elas recebem
        # a mesma colocação i.
        i = 1
        r = [[*tmp[0], i]]
        for (j, e) in enumerate(tmp[1:], start = 1):
            # Verifica se o último elemento já ranqueado tem o mesmo valor que o próximo.
            if e[1] != r[-1][1]:
                i = j+1
            r.append([*e, i])
        r.sort(key = lambda k: k[2])
        rank[p] = r

    return rank

def ranking_abs_mean(rank_abs):
    # rank = {}
    # for mh in metaheuristics.keys():
    #     rank[mh] = []

    # for d in rank_abs.values():
    #     for (mh, _, r) in d:
    #         rank[mh].append(r)

    # for (mh, ranks) in rank.items():
    #     rank[mh] = mean(ranks)
    # # for r in rank.items():
    # #     print(r)

    # tmp = list(rank.items())
    # tmp.sort(key = lambda k: k[1])
    # # for r in tmp:
    # #     print(r)

    # i = 1
    # rank_ = [[i, *tmp[0]]]
    # for e in tmp[1:]:
    #     # Verifica se o último elemento já ranqueado tem o mesmo valor que o próximo.
    #     if e[0] != rank_[-1][1]:
    #         i += 1
    #     rank_.append([i, *e])

    # # TRATAR O EMPATE
    # return rank_

    rank = []
    for r in rank_abs.values():
        # Pega as posições do ranking.
        # Ex: 1. Beam, Hill; 2. GRASP; 3. Simulated, Genético => [1,2,3]
        pos = sorted(set(map(lambda x: x[2], r)))

        # Agrupa as metaheurísticas por posição do ranking.
        rank_aux = [] # [(i, [mh_name for (mh_name, _, p_) in r if p_ == p]) for (i, p) in enumerate(pos, start = 1)]
        for (i, p) in enumerate(pos, start = 1):
            aux = []
            for (mh_name, _, p_) in r:
                if p_ == p:
                    aux.append(mh_name)
            rank_aux.append(aux)
        i = 1
        for (j, e) in enumerate(rank_aux):
            rank_aux[j] = (mean(list(range(i, i+len(e)))), e)
            i += len(e)
            # if len(e) != 1:
                # p = mean(list(range(i, i+len(e)))) # Posição
        rank.append(rank_aux)
    return rank

def ranking_mean(rank):
    pass

def ranking_norm(results):
    pass

def k_best_hiperparams(hp, normalized_results, k):
    k_best = []
    for n in normalized_results:
        (c, nr, _) = n
        avg = mean(nr)
        if len(k_best) < k:
            k_best.append(n)
            k_best.sort(key = lambda t: t[1], reverse = True)
        elif avg > mean(k_best[-1][1]):
            k_best.pop()
            k_best.append(n)
            k_best.sort(key = lambda t: t[1], reverse = True)
    return k_best

def train():
    now = datetime.now()
    print("ALGORITMO DE TREINO :: INICIO DA EXEC. => "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")

    max_time = 2 # Tempo máx. de exec. de uma meta heurística no treino: 2 minutos.
    for (mh_name, data) in metaheuristics.items():
        if data.get('train'):
            mh = data.get('func')
            param_list = [v for (k,v) in data.get('param').items()]
            hp = list(product(*param_list)) # Combinações de hiperparâmetros
            results = {}
            print(mh_name)
            print("NUMERO DE COMBINACOES: ", len(hp))
            for (i, c) in enumerate(hp, start=1): # Para cada combinação de valores de hiperparâmetros
                print(i) # Printa a i-ésima combinação em execução
                results_comb = {} # Cada elemento é o resultado de c aplicado ao problema p.
                for (p, d) in train_set.items():
                    print("  ", p) # Printa o nome do problema em execução

                    begin = time()
                    r_mh = mh(d['vt'], d['t'], c, max_time) # Resultado da metaheuristica
                    end = time()

                    elapsed_time = end - begin
                    sz = calc_size(r_mh, d['vt'])

                    results_comb[p] = {
                        'result': r_mh,
                        'value': calc_value(r_mh, d['vt']),
                        'size': sz,
                        'ratio_size': sz / d['t'],
                        'time': elapsed_time
                    }
                results[c] = results_comb

            print("\n")

            nr = normalize_train(results, hp) # n = resultados normalizados
            k_best = k_best_hiperparams(hp, nr, 10)
            k_best.sort(key = lambda t: mean(t[1]), reverse = True)

            print("MELHORES HIPERPARAMETROS:")
            for (i, e) in enumerate(k_best, start=1):
                (c, n, _) = e
                print(i, c, mean(n), sep=' - ')

            write_train_results(mh_name, c, p, results, k_best, nr)

            hp_str = []
            data_values = []
            data_times = []
            for (c, d, t) in k_best:
                hp_str.append(str(c))
                data_values.append(d)
                data_times.append(t)

            # Gera boxplot dos resultados alcançados (normalizados) pela metaheurística
            create_boxplot(
                data_values,
                "./figs/values_"+mh_name.replace(" ", ""),
                "Combinações de hiperparâmetros",
                "Resultados dos problemas normalizados",
                hp_str
            )
            # Gera boxplot dos tempos alcançados pela metaheurística
            create_boxplot(
                data_times,
                "./figs/times_"+mh_name.replace(" ", ""),
                "Combinações de hiperparâmetros",
                "Tempo de execucao (em segundos)",
                hp_str
            )
            metaheuristics[mh_name]['hiperparam_train'] = k_best[0][0]

def test():
    now = datetime.now()
    print("ALGORITMO DE TESTE :: INICIO DA EXEC. => "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")

    max_time = 5 # Tempo máx. de exec. de uma meta heurística no teste: 5 minutos.
    results = {}
    for (mh_name, data) in metaheuristics.items():
        mh = data.get('func')
        results_mh = {} # Cada elemento é o resultado da meta heurística aplicada ao problema p.

        hp = data.get('hiperparam') # Hiperparâmetro escolhido para a metaheurística (selecionado após treino prévio).
        # hp = data.get('hiperparam_train') # Tire o comentário caso queira rodar com o hp obtido no treino.

        print(mh_name)
        print("HIPERPARAMETRO:", hp)
        for (p, d) in test_set.items():
            print("  ", p)

            begin = time()
            r_mh = mh(d['vt'], d['t'], hp, max_time) # Resultado da metaheuristica
            end = time()

            elapsed_time = end - begin
            sz = calc_size(r_mh, d['vt'])

            results_mh[p] = {
                # 'result': r_mh,
                'value': calc_value(r_mh, d['vt']),
                'size': sz,
                'ratio_size': sz / d['t'],
                'time': elapsed_time
            }

        values = [d['value'] for d in results_mh.values()]
        times  = [d['time' ] for d in results_mh.values()]

        # Média absoluta e desvio padrão das execuções
        results_mh['values_mean' ] = mean(values)
        results_mh['values_stdev'] = stdev(values)

        # Média e desvio padrão dos tempos de execução
        results_mh['times_mean' ] = mean(times)
        results_mh['times_stdev'] = stdev(times)

        print("Values :: mean> {0:.3f} ; stdev> {1:.3f}".format(results_mh['values_mean'], results_mh['values_stdev']))
        print("Times  :: mean> {0:.3f} ; stdev> {1:.3f}".format(results_mh[ 'times_mean'], results_mh[ 'times_stdev']))
        print()
        # print(results_mh)
        results[mh_name] = results_mh

    nr = normalize_test(results)
    # print(nr, end = "\n\n")

    # Tabela contendo média e desvio padrão absolutos e normalizados,
    # e média e desvio padrão dos tempos de execução de todas as metaheurísticas
    header = ["METAHEURÍSTICA", "MÉDIA ABSOLUTA","DESVIO PADRÃO ABSOLUTO", "MÉDIA NORMALIZADA", "DESVIO PADRÃO NORMALIZADO", "MÉDIA TEMPO (em segundos)", "DESVIO PADRÃO TEMPO (em segundos)"]
    table = create_table(results, nr)
    print(tabulate(table, headers = header, tablefmt = "fancy_grid", stralign = "center", numalign = "center"))

    # write_test_results(results, table, header)

    # Ranqueamento das metaheurísticas segundo resultado absoluto
    rank_abs = ranking_abs(results)
    print("RANQUEAMENTO DAS METAHEURÍSTICAS SEGUNDO RESULTADO ABSOLUTO")
    for r in rank_abs.items():
        print(r)
    print()

    # Ranqueamento das metaheurísticas segundo resultado normalizado
    # ???
    # rank_norm = ranking_norm(results)

    # Obter média dos ranqueamentos das metaheurísticas segundo resultado absoluto
    # Apresentar as metaheurísticas em ordem crescente de média de ranqueamento
    rank_abs_mean = ranking_abs_mean(rank_abs)
    for r in rank_abs_mean:
        print(r)
    print()

    # Obter média dos ranqueamentos das metaheurísticas segundo resultado normalizado
    # Apresentar as metaheurísticas em ordem crescente de média de ranqueamento
    rank_mean = []
    for mh_name in metaheuristics.keys():
        r_m = [mh_name, []] # Rankings de uma metaheurística
        for r_p in rank_abs_mean:
            for (r, mhs) in r_p:
                if mh_name in mhs:
                    r_m[1].append(r)
                    break
        rank_mean.append(r_m)

    for r in rank_mean:
        r[1] = mean(r[1])
    rank_mean.sort(key = lambda k: k[1])
    for r in rank_mean:
        print(r)

    nr.sort(key = lambda k: mean(k[1]), reverse = True)

    data_values = []
    data_times = []
    for (_, d, t) in nr:
        data_values.append(d)
        data_times.append(t)

    # Gera boxplot dos resultados normalizados pelas metaheurísticas
    create_boxplot(
        data_values,
        "./results_test/values_test",
        "Metaheuristicas",
        "Resultados dos problemas normalizados",
        metaheuristics.keys()
    )
    # Gera boxplot dos tempos alcançados pelas metaheurísticas
    create_boxplot(
        data_times,
        "./results_test/times_test",
        "Metaheuristicas",
        "Tempo de execucao (em segundos)",
        metaheuristics.keys()
    )

if __name__ == '__main__':
    # train()
    test()

# https://tableconvert.com/?output=latex