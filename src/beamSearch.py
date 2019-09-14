from statusManager import *

# Seleciona os k melhores estados (aqueles que possuem maior valor)
# de uma lista de estados.
def k_best_status(sl, vt, sz, k):
    sl = list(filter(lambda s: is_valid(vt, s, sz), sl))
    sl.sort(key = lambda s: calc_value(s, vt), reverse = True)
    return sl[:k]

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