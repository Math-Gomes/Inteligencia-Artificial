from datetime import datetime
from statistics import mean
import json
import seaborn as sns
import matplotlib.pyplot as plt

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
            # print(d['value'], "{0:.2f}".format(d['time']), end='\t')
            print(d['value'], end='\t')
        print()

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

def write_test_results(results):
    filename = "results_test/data.txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write("EXECUCAO > "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
        f.write(json.dumps(results, indent=2))
        f.write("=============================\n\n")

def create_boxplot(data, fname, x_lbl, y_lbl, x_tick_lbls):
    fig = plt.figure()
    fig.set_size_inches(10,8)
    bp = sns.boxplot(data = data, showmeans = True)
    bp.set(xlabel = x_lbl, ylabel = y_lbl)
    bp.set_xticklabels(x_tick_lbls)
    plt.setp(bp.get_xticklabels(), rotation = 45)
    plt.savefig(fname = "./figs/"+fname+".png")
    plt.savefig(fname = "./figs/"+fname+".svg")