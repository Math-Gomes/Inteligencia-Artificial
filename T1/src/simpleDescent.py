from statusManager import *
from random import randint
import time

def simple_descent(status, vt, sz, timeout):
    best = status
    n = neighbors(status, vt, sz)
    while n != [] and time.time() < timeout:
        s_ = n.pop(randint(0,len(n)-1))
        if calc_value(s_, vt) > calc_value(best, vt):
            best = s_
            n = neighbors(best, vt, sz)
    return best