from statusManager import *
from simpleDescent import simple_descent
from random import randint, random
from itertools import accumulate

def greedy_random_construct(vt, t, num_best):
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
        rt_acc = list(accumulate([v for (v,p) in ratio]))
        r = random()
        for (i, c) in enumerate(rt_acc):
            if r < c:
                status = ratio[i][1].copy()
                break
    return status

def grasp(vt, t, num_iter, num_best, max_time):
    status = [0]*len(vt)
    best = status
    for _ in range(num_iter):
        status = greedy_random_construct(vt, t, num_best)
        status = simple_descent(status, vt, t)
        if calc_value(status, vt) > calc_value(best, vt):
            best = status
    return best

vt = [(1,3),(4,6),(5,7)]
t = 19
num_iter = 3
num_best = 2
max_time = 2

s = grasp(vt, t, num_iter, num_best, max_time)
print(s, calc_value(s, vt))