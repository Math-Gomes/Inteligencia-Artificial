from statusManager import *
from hillClimbing import hill_climbing

def pq_insert(pq, new, vt):
    pq.append(new)
    pq.sort(key = lambda s: calc_value(s, vt))
    return pq

def pq_remove(pq):
    return pq.pop(0)

def trivial_solution(vt, sz):
    return hill_climbing(vt,sz)

# Se opt == True,  estimativa otimista
# Se opt == False, estimimativa nao otimista
def estimate(status, vt, maxSZ, opt):
    ratio = [get_v(vt, k)/get_t(vt,k) for k,v in enumerate(vt)]
    sz = calc_size(status, vt)
    result = status.copy()
    while sz <= maxSZ and len(ratio) > 0:
        i = ratio.index(max(ratio))
        result[i] += 1
        sz += get_t(vt, i)
    if opt == True:
        return result
    result[i] -= 1
    return result

# Se opt == True,  estimativa otimista
# Se opt == False, estimimativa nao otimista
def branch_and_bound(vt, sz, opt):
    best = trivial_solution(vt, sz)
    pq = [[0]*len(vt)]
    while pq != []:
        f = pq_remove(pq)
        expanded = expand(f)
        for s in expanded:
            if is_valid(vt, s, sz):
                best_value = calc_value(best, vt)
                if calc_value(estimate(s, vt, sz, opt), vt) > best_value:
                    if calc_value(s, vt) > best_value:
                        best = s
                    pq_insert(pq, s, vt)
    return best