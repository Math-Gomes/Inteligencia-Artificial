from statusManager import *
from random import randint

def deepest_descent(status, vt, sz):
    best = status
    best_neighbor = search_best(vt, neighbors(status, vt, sz), sz)
    while calc_value(best_neighbor, vt) > calc_value(best, vt):
        best = best_neighbor
        best_neighbor = search_best(vt, neighbors(best, vt, sz), sz)
    return best