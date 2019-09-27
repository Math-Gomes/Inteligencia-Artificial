from statusManager import *

def beam_search(vt, sz, k):
    sl = [[0]*len(vt)]
    best = []
    while True:
        sl_new = []
        for s in sl:
            sl_new += expand(s)
        sl_new = k_best_status(sl_new,vt,sz,k)
        if sl_new == []:
            break
        sl = sl_new.copy()
        if calc_value(sl[0], vt) > calc_value(best, vt):
            best = sl[0]
    return best