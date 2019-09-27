from statusManager import *
from random import randint, random
from math import exp
from hillClimbing import hill_climbing

def probability(s, s_, temp, vt):
    return exp((calc_value(s_, vt)-calc_value(s, vt))/temp)

def simulated_annealing(s, temp, alpha, numIter, vt, sz):
    best = s
    while temp > 1:
        n = neighbors(s, vt, sz)
        for _ in range(numIter):
            if n == []:
                return best
            s_ = n.pop(randint(0,len(n)-1))
            if calc_value(s_, vt) > calc_value(s, vt):
                s = s_
                n = neighbors(s, vt, sz)
                if calc_value(s_, vt) > calc_value(best, vt):
                    best = s
            else:
                if probability(s, s_, temp, vt) > random():
                    s = s_
                    n = neighbors(s, vt, sz)
        temp *= alpha
    return best

# EXEMPLO:
# sz = 19 # Tamanho da mochila.
# vt = [(1,3), (4,6), (5,7)] # Tuplas (Valor, Tamanho)
# temp = 100
# alpha = random()
# numIter = 50
# print("Simulated annealing:")
# print('    Temperatura = ', temp, '\n    Alpha = ', alpha, '\n    Iter =', numIter)
# show_result(vt, simulated_annealing(hill_climbing(vt, sz), temp, alpha, numIter, vt, sz))