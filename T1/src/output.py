import json
from datetime import datetime

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

def write_results_file(mh, c, p, results, k_best):
    filename = "results/data_"+mh.replace(" ", "")+".txt"
    now = datetime.now()
    with open(filename, 'a') as f:
        f.write(mh+" "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n")

        f.write("\nRESULTADOS DE CADA COMBINACAO:\n")
        f.write(print_json(results)+"\n")
        # for (c, d) in results.items():
        #     f.write(str(c)+" =\n")
        #     for (p, d1) in d.items():
        #         f.write(p+" = "+json.dumps(d1)+"\n")

        f.write("\nMELHORES HIPERPARAMETROS:\n")
        for (i, e) in enumerate(k_best, start = 1):
            f.write(str(i)+" - "+str(e)+"\n")
        f.write("=============================\n\n")