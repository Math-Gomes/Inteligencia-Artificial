from statusManager import *
from simpleDescent import simple_descent
from random import randint

def greedy_random_construct(vt, sz, sd, m):
    status = [0]*len(vt)
    best = []
    while True:
        sl = expand(status)
        best = sl[randint(0, len(sl)-1)]
        # best = search_best(vt, sl, sz)
        if best == []:
            break
        status = best
    return status

# sd = seed
def grasp(vt, sz, numIter, m, sd):
    best = []
    for _ in range(numIter):
        s = greedy_random_construct(vt, sz, sd, m) # hillclimbing modificado
        s = simple_descent(s, vt, sz)
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
    return best