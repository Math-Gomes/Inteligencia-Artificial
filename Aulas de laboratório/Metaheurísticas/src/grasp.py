from statusManager import *
from simpleDescent import simple_descent
from random import random
from itertools import accumulate

# Greedy random construct "comum"
def greedy_random_construct1(vt, t, num_best):
    status = [0]*len(vt)
    while True:
        sl = expand(status)
        sl = k_best_status(sl, vt, t, num_best)
        if sl == []:
            break
        values = [(calc_value(s, vt), s) for s in sl]
        total = sum([v for (v, _) in values])
        ratio = [(v/total, s) for (v, s) in values]
        ratio.sort()
        rt_acc = list(accumulate([v for (v, _) in ratio]))
        r = random()
        for (i, c) in enumerate(rt_acc):
            if r < c:
                status = ratio[i][1].copy()
                break
    return status

# Greedy random construct "matemático"
def greedy_random_construct(vt, t, num_best):
    status = [0]*len(vt)
    vt_ = vt.copy()
    vt_.sort()
    vt_.sort(key = lambda x: x[1])
    while True:
        vt_ = [e for e in vt_ if e[1] <= t]
        if vt_ == []:
            break
        total = sum([v for (v, _) in vt_]) # Soma de todos os valores

        ratio = [(v/total, (v, t_)) for (v, t_) in vt_]
        ratio = ratio[-num_best:]

        # Normaliza as chance de ratio
        total = sum([v for (v, _) in ratio])
        ratio = [(v/total, vt__) for (v, vt__) in ratio]
        rt_acc = list(accumulate([v for (v, _) in ratio]))

        r = random()
        for (i, c) in enumerate(rt_acc):
            if r < c:
                j = vt.index(ratio[i][1])
                items = t // get_t(vt, j)
                status[j] += 1
                t -= get_t(vt, j)
                break
    return status

def grasp(vt, t, num_iter, num_best):
    status = [0]*len(vt)
    best = status
    for _ in range(num_iter):
        status = greedy_random_construct(vt, t, num_best)
        # status = simple_descent(status, vt, t)
        if calc_value(status, vt) > calc_value(best, vt):
            best = status
    return best