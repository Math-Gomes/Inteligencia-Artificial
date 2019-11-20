import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import *

def create_boxplot(data, fname, x_lbl, y_lbl, x_tick_lbls):
    fig = plt.figure()
    fig.set_size_inches(10,8)
    bp = sns.boxplot(data = data, showmeans = True)
    bp.set(xlabel = x_lbl, ylabel = y_lbl)
    bp.set_xticklabels(x_tick_lbls)
    plt.setp(bp.get_xticklabels(), rotation = 0)
    plt.savefig(fname = fname + '.png')
    plt.savefig(fname = fname + '.svg')

def write_results(results, fname, header):
    # Exibe na tela os resultados.
    for (base, res) in results:
            print(base)
            print(*header)
            for r in res:
                print(r)
            print()

    # Escreve as tabelas (no formato latex) num arquivo.
    # OBS: A biblioteca tabulate deve estar instalada.
    with open(fname, 'a') as f:
        for (base, res) in results:
            f.write('\n' + base + '\n\n')
            f.write(tabulate(res, headers = header, tablefmt = "latex", stralign = "center", numalign = "center") + '\n')
        f.write("\n=============================\n\n")
