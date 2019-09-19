from statusManager import *
from simpleDescent import simple_descent
from random import randint

def multistart_descent(vt, sz, iterMax):
    best = [0]*len(vt)
    for _ in range(iterMax):
        s = simple_descent(random_status(vt, sz), vt, sz)
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
    return best

def random_status(vt, sz):
    status = [0]*len(vt)
    while is_valid(vt, status, sz):
        i = randint(0,len(vt)-1)
        status[i] += 1
    status[i] -= 1
    return status

# Versões do multistart:

# Um dos passos deste algoritmo é escolher um estado s' aleatoriamente para que
# neste seja aplicado o algoritmo Simple Descent (ou Deepest Descent). Existem
# diferentes maneiras de gerar este s', e nesta implementação foi feita a escolha
# de gerar a vizinhança do estado best, e desta vizinhança selecionar um
# estado aleatório. 
def multistart_descent1(vt, sz, iterMax):
    best = [0]*len(vt)
    n = neighbors(best, vt, sz)
    for _ in range(iterMax):
        if n == []:
            break
        s = simple_descent(n.pop(randint(0, len(n)-1)), vt, sz)
        if calc_value(s, vt) > calc_value(best, vt):
            best = s
            n = neighbors(best, vt, sz)
    return best

def random_status1(vt, sz):
    status = [0]*len(vt)
    status[randint(0,len(vt)-1)] += 1
    return status