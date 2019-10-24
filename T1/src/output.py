from datetime import datetime
from statistics import mean
import json
import seaborn as sns
import matplotlib.pyplot as plt
from prettytable import PrettyTable

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

def write_test_results(results, table):
    filename = "results_test/data.txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write("EXECUCAO > "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")
        f.write(json.dumps(results, indent=2)+"\n")
        f.write(table.get_string()+"\n")
        f.write(table.get_html_string()+"\n")
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

def create_table(results, normalized_results):
    titles = ["METAHEURISTICA", "MEDIA ABS", "DP ABS", "MEDIA NORM", "DP NORM", "MEDIA TEMPO", "DP TEMPO"]
    table = PrettyTable(titles)
    lines = []
    for (mh_name, mean_n, stdev_n) in normalized_results:
        lines.append([
            mh_name,
            results[mh_name]['values_mean'], results[mh_name]['values_stdev'],
            mean_n, stdev_n,
            results[mh_name]['times_mean'], results[mh_name]['times_stdev']
        ])
        table.add_row(lines[-1])

    # print(table)
    # print(table.get_html_string())

    # print("METAHEURISTICA\tMEDIA_ABS\tSTDEV_ABS\tMEDIA_NORM\tSTDEV_NORM\tMEDIA_TEMPO\tSTDEV_TEMPO")
    # for l in lines:
    #     print("{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5:.3f}\t{6:.3f}".format(*l))

    return table