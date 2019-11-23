import seaborn as sns
import matplotlib.pyplot as plt
# from tabulate import *

def create_boxplot(data, fname, x_lbl, y_lbl, x_tick_lbls):
    fig = plt.figure()
    fig.set_size_inches(10,8)
    bp = sns.boxplot(data = data, showmeans = True)
    bp.set(xlabel = x_lbl, ylabel = y_lbl)
    bp.set_xticklabels(x_tick_lbls)
    plt.setp(bp.get_xticklabels(), rotation = 0)
    plt.savefig(fname = fname + '.png')
    # Retire o comentário da linha seguinte caso queira
    # salvar o boxplot no formato .svg
    # plt.savefig(fname = fname + '.svg')

# Exibe os resultados na tela e escreve-os num arquivo.
def write_results(results, fname, header, part):
    with open(fname, 'a') as f:
        if part == 1:
            for (base, res) in results:
                print(base)
                print('='*45)
                print('{0:21s}\t{1}\t{2}'.format(*header))
                f.write('\n' + base + '\n')
                f.write(('='*45) + '\n')
                f.write('{0:21s}\t{1}\t{2}'.format(*header) + '\n')
                for r in res:
                    print('{0:21s}\t{1:.3f}\t{2:.3f}'.format(*r))
                    f.write('{0:21s}\t{1:.3f}\t{2:.3f}'.format(*r) + '\n')
                print()
                f.write('\n')

        if part == 2:
            for (base, res) in results:
                print(base)
                print('='*63)
                print('{0:19s}\t{1}\t{2}\t{3}'.format(*header))
                f.write('\n' + base + '\n')
                f.write(('='*63) + '\n')
                f.write('{0:19s}\t{1}\t{2}\t{3}'.format(*header) + '\n')
                for r in res:
                    print('{0:19s}\t{1:.3f}\t{2:.3f}\t{3}'.format(*r))
                    f.write('{0:19s}\t{1:.3f}\t{2:.3f}\t{3}'.format(*r) + '\n')
                print()
                f.write('\n')

        # Escreve as tabelas (no formato latex) no arquivo.
        # OBS: A biblioteca tabulate deve estar instalada.
        # for (base, res) in results:
        #     f.write('\n' + base + '\n\n')
        #     f.write(tabulate(res, headers = header, tablefmt = "latex", stralign = "center", numalign = "center") + '\n')
        # f.write("\n=============================\n\n")