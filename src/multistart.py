from statusManager import *
from simpleDescent import simple_descent
from math import inf
from random import randint

def multistart_descent(vt, sz, iterMax):
    best = [0]*len(vt)
    for _ in range(iterMax):
        n = neighbors(best, vt, sz)
        if n == []:
            break
        s = simple_descent(n[randint(0,len(n)-1)], vt, sz)
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
    return best

# Versões do multistart
def multistart_descent1(vt, sz, iterMax):
    best = [0]*len(vt)
    for _ in range(iterMax):
        s = simple_descent(random_status1(vt, sz), vt, sz)
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
    return best

def random_status(vt, sz):
    status = [0]*len(vt)
    while is_valid(vt, status, sz):
        i = randint(0,len(vt)-1)
        status[i] += 1
    status[i] -= 1
    return status

def random_status1(vt, sz):
    status = [0]*len(vt)
    status[randint(0,len(vt)-1)] += 1
    return status