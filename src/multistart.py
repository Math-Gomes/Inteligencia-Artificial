from statusManager import *
from simpleDescent import simple_descent
from math import inf
from random import randint, seed

def neighbors(status, vt, sz):
    return [s for s in expand(status) if is_valid(vt, s, sz)]

def random_status(vt, sz):
    status = [0]*len(vt)
    while is_valid(vt, status, sz):
        i = randint(0,len(vt)-1)
        status[i] += 1
    status[i] -= 1
    print(status, calc_value(status, vt))
    # status[randint(0,len(vt)-1)] += 1
    return status

def multistart_descent(vt, sz, iterMax):
    best = [0]*len(vt)
    for _ in range(iterMax):
        # s = simple_descent(random_status(vt, sz), vt, sz)
        n = neighbors(best, vt, sz)
        if n == []:
            break
        s = simple_descent(n[randint(0,len(n)-1)], vt, sz)
        # s = n[randint(0,len(n)-1)]
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
    return best