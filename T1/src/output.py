from datetime import datetime
from statistics import mean, stdev
import json
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

def print_json(results):
    new = {}
    for (k,v) in results.items():
        for e in v.values():
            e['result'] = str(e['result'])
        new[str(k)] = v
    return "results = "+json.dumps(new, indent=4)

def write_train_results(mh, c, p, results, k_best, normalized_results):
    filename = "partial_results/r_"+mh.replace(" ", "")+".txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write(mh+" "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")

        f.write("\nRESULTADOS DE CADA COMBINACAO:\n")
        f.write(print_json(results)+"\n")

        f.write("\nRESULTADOS NORMALIZADOS:\n")
        for e in normalized_results:
            f.write(str(e)+"\n")

        f.write("\nMELHORES HIPERPARAMETROS:\n")
        for (i, e) in enumerate(k_best, start = 1):
            (t, n, _) = e
            f.write(str(i)+" - "+str(t)+" - "+str(mean(n))+"\n")
        f.write("=============================\n\n")

def write_test_results(results, table, table_header):
    filename = "results_test/results.txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write("EXECUCAO > "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
        f.write(json.dumps(results, indent=2)+"\n")
        # f.write(tabulate(table, headers = table_header, tablefmt = "psql", stralign = "center", numalign = "center"))
        # f.write("\n\n")
        # f.write(tabulate(table, headers = table_header, tablefmt = "latex", stralign = "center", numalign = "center"))
        f.write("\n")
        f.write("=============================\n\n")

def create_boxplot(data, fname, x_lbl, y_lbl, x_tick_lbls):
    fig = plt.figure()
    fig.set_size_inches(10,8)
    bp = sns.boxplot(data = data, showmeans = True)
    bp.set(xlabel = x_lbl, ylabel = y_lbl)
    bp.set_xticklabels(x_tick_lbls)
    plt.setp(bp.get_xticklabels(), rotation = 30)
    plt.savefig(fname = fname+".png")
    plt.savefig(fname = fname+".svg")

def boxplot_train(mh_name, k_best):
    '''
    Gera boxplot dos resultados normalizados alcançados e dos tempos
    alcançados por uma metaheurística no algoritmo de treino.
    '''
    hp_str = []
    data_values = []
    data_times = []
    for (c, d, t) in k_best:
        hp_str.append(str(c))
        data_values.append(d)
        data_times.append(t)

    print("GERANDO BOXPLOTs DO ALGORITMO DE TREINO...\n")

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

def boxplot_test(normalized_results):
    '''
    Gera boxplot dos resultados normalizados alcançados pelas
    metaheurísticas e dos tempos alcançados pelas metaheurísticas
    no algoritmo de teste.
    '''
    normalized_results.sort(key = lambda k: mean(k[1]), reverse = True) # Ordena pela média dos resultados normalizados.

    mhs = []
    data_values = []
    data_times = []
    for (mh_name, d, t) in normalized_results:
        mhs.append(mh_name)
        data_values.append(d)
        data_times.append(t)

    print("GERANDO BOXPLOTs DO ALGORITMO DE TESTE...\n")

    # Gera boxplot dos resultados normalizados pelas metaheurísticas
    create_boxplot(
        data_values,
        "./results_test/values_test",
        "Metaheuristicas",
        "Resultados dos problemas normalizados",
        mhs
    )
    # Gera boxplot dos tempos alcançados pelas metaheurísticas
    create_boxplot(
        data_times,
        "./results_test/times_test",
        "Metaheuristicas",
        "Tempo de execucao (em segundos)",
        mhs
    )

def table_1(results, normalized_results):
    '''
    Tabela contendo média e desvio padrão absolutos e normalizados,
    e média e desvio padrão dos tempos de execução de todas as metaheurísticas.
    '''
    header = ["METAHEURÍSTICA", "MÉDIA ABSOLUTA","DESVIO PADRÃO ABSOLUTO", "MÉDIA NORMALIZADA", "DESVIO PADRÃO NORMALIZADO", "MÉDIA TEMPO (em segundos)", "DESVIO PADRÃO TEMPO (em segundos)"]
    lines = []

    for (mh_name, nr_mh, _) in normalized_results:
        lines.append([
            mh_name,
            results[mh_name]['values_mean'],
            results[mh_name]['values_stdev'],
            mean(nr_mh),
            stdev(nr_mh),
            results[mh_name]['times_mean'],
            results[mh_name]['times_stdev']
        ])

    lines.sort(key = lambda e: e[3], reverse = True) # Ordena pela média normalizada

    # Se a biblioteca tabulate estiver instalada, retire o comentário desta linha
    # para melhor visualização da tabela.
    # print(tabulate(lines, headers = header, tablefmt = "fancy_grid", stralign = "center", numalign = "center"))
    
    for h in header:
        print(h, end = " / ")
    print()
    for l in lines:
        print("{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5:.3f}\t{6:.3f}".format(*l))
    print("\n")

def table_2(rank_abs_mean):
    '''
    Tabela contendo as metaheurísticas em ordem crescente de média
    de ranqueamento.
    '''
    header = ["POSIÇÃO", "METAHEURÍSTICA", "MÉDIA DE RANQUEAMENTO"]
    lines = []
    for (i, (mh_name, mean_rank)) in enumerate(rank_abs_mean, start = 1):
        lines.append([i, mh_name, mean_rank])

    print("MÉDIA DOS RANQUEAMENTOS DAS METAHEURÍSTICAS SEGUNDO RESULTADO ABSOLUTO")

    # Se a biblioteca tabulate estiver instalada, retire o comentário
    # da linha seguinte para melhor visualização da tabela.
    # print(tabulate(lines, headers = header, tablefmt = "fancy_grid", stralign = "center", numalign = "center"))
    
    for h in header:
        print(h, end = " / ")
    print()
    for l in lines:
        print(*l)
    print("\n")

def table_3(normalized_results):
    '''
    Tabela contendo as metaheurísticas em ordem crescente de média
    dos resultados normalizados.
    '''
    header = ["METAHEURÍSTICA", "MÉDIA NORMALIZADA"]
    lines = []

    for (mh_name, nr_mh, _) in normalized_results:
        lines.append([mh_name, mean(nr_mh)])

    lines.sort(key = lambda e: e[1]) # Ordena pela média normalizada

    print("METAHEURÍSTICAS EM ORDEM CRESCENTE DE MÉDIA DOS RESULTADOS NORMALIZADOS")

    # Se a biblioteca tabulate estiver instalada, retire o comentário
    # da linha seguinte para melhor visualização da tabela.
    # print(tabulate(lines, headers = header, tablefmt = "fancy_grid", stralign = "center", numalign = "center"))

    for h in header:
        print(h, end = " / ")
    print()
    for l in lines:
        print(*l)
    print("\n")