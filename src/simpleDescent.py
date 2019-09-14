from statusManager import *
from random import randint

def simple_descent(status, vt, sz):
    best = status
    n = neighbors(status, vt, sz)
    while calc_value(search_best(vt, n, sz), vt) > calc_value(best, vt):
        s_ = n[randint(0,len(n)-1)]
        if calc_value(s_, vt) > calc_value(best, vt):
            best = s_
            n = neighbors(best, vt, sz)
    return best