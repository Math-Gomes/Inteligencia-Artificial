from statusManager import *

def hill_climbing1(vt, t):
    status = [0]*len(vt)
    best = []
    while True:
        sl = expand(status)
        best = search_best(vt, sl, t)
        if best == []:
            break
        status = best
    return status

def hill_climbing(vt, t):
    status = [0]*len(vt)
    vt_ = vt.copy()
    while True:
        vt_ = [e for e in vt_ if e[1] <= t]
        if vt_ == []:
            break
        # i = vt.index(max(vt_))
        max_values = [e for e in vt_ if e[0] == max(vt_)[0]]
        i = vt.index(min(max_values)) # Índice do maior valor com menor peso.
        items = t // get_t(vt, i)
        status[i] = items
        t -= items * get_t(vt, i)
    return status


sz = 22 # Tamanho da mochila.
vt = [(1,3),(5,6),(5,7)]
print("Hill Climbing:")
show_result(vt, hill_climbing(vt, sz))
show_result(vt, hill_climbing1(vt, sz))