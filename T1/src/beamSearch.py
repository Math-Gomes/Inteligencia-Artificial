from statusManager import *
import time

def beam_search(vt, sz, param):
    (k,) = param
    sl = [[0]*len(vt)]
    best = []
    timeout = time.time() + 60*1
    while True:
        sl_new = []
        for s in sl:
            sl_new += expand(s)
        sl_new = k_best_status(sl_new,vt,sz,k)
        if sl_new == [] or time.time() > timeout:
            break
        sl = sl_new.copy()
        if calc_value(sl[0], vt) > calc_value(best, vt):
            best = sl[0]
    return best