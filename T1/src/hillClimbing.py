from statusManager import *
import time

def hill_climbing(vt, t, param, max_time):
    status = [0]*len(vt)
    vt_ = vt.copy()
    timeout = time.time() + 60*max_time
    while time.time() < timeout:
        vt_ = [e for e in vt_ if e[1] <= t]
        if vt_ == []:
            break
        max_values = [e for e in vt_ if e[0] == max(vt_)[0]]
        i = vt.index(min(max_values)) # Índice do maior valor com menor peso.
        items = t // get_t(vt, i)
        status[i] = items
        t -= items * get_t(vt, i)
    return status