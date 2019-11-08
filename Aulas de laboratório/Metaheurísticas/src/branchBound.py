from statusManager import *
from hillClimbing import hill_climbing

# Insere na fila com prioridade.
def pq_insert(pq, new, vt):
    pq.append(new)
    pq.sort(key = lambda s: calc_value(s, vt), reverse = True)
    return pq

# Remove o primeiro elemento da fila.
def pq_remove(pq):
    return pq.pop(0)

# Calcula a solução trivial, baseada na estimativa do estado inicial [0,...,0].
def trivial_solution(vt, sz):
    return estimate([0]*len(vt), vt, sz, opt = False)

# Calcula a estimativa de um estado, utilizando como base a razão entre valor
# e peso de um item.
# O estado estimado é gerado ao adicionar ao máximo o item que possui a maior
# razão na mochila.
# Se a estimativa for otimista, o peso da estimativa é maior do que o limite
# da mochila. Caso a estimativa seja não-otimista, o peso do estado é inferior
# ou igual ao da mochila.
# Se opt == True  => estimativa otimista.
# Se opt == False => estimimativa não-otimista.
def estimate(status, vt, sz, opt):
    ratio = [get_v(vt, k)/get_t(vt, k) for k,v in enumerate(vt)]
    est = status.copy() # status estimativa
    i = ratio.index(max(ratio))
    while is_valid(vt, est, sz):
        est[i] += 1
    if opt:
        return est
    est[i] -= 1
    return est

# Se opt == True  => estimativa otimista.
# Se opt == False => estimimativa não-otimista.
def branch_and_bound(vt, sz, opt):
    best = trivial_solution(vt, sz)
    f = [[0]*len(vt)]
    while f != []:
        for s in expand(pq_remove(f)):
            if is_valid(vt, s, sz):
                best_value = calc_value(best, vt)
                if calc_value(estimate(s, vt, sz, opt), vt) > best_value:
                    if calc_value(s, vt) > best_value:
                        best = s
                    pq_insert(f, s, vt)
    return best