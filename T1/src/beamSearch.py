from statusManager import *
import time

def beam_search(vt, t, param, max_time):
    (k,) = param
    sl = [[0]*len(vt)]
    best = []
    timeout = time.time() + 60*max_time
    while time.time() < timeout:
        new = []
        for s in sl:
            if time.time() > timeout:
                break
            new += expand(s)
        if time.time() > timeout:
            break
        new = k_best_status(new, vt, t, k)
        if new == [] or time.time() > timeout:
            break
        sl = new.copy()
        if calc_value(sl[0], vt) > calc_value(best, vt):
            best = sl[0]
    return best