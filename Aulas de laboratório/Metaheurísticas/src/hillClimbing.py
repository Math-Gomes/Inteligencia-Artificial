from statusManager import expand, search_best

def hill_climbing(vt, sz):
    status = [0]*len(vt)
    best = []
    while True:
        sl = expand(status)
        best = search_best(vt, sl, sz)
        if best == []:
            break
        status = best
    return status