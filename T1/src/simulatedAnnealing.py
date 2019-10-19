from statusManager import *
from random import randint, random, shuffle
from math import exp
from hillClimbing import *

import time

def probability(s, s_, temp, vt):
    return exp((calc_value(s_, vt)-calc_value(s, vt))/temp)

# max_time => tempo máximo de execução (em minutos)
def simulated_annealing(vt, t, param, max_time):
    (temp, alpha, num_iter,) = param
    s = [0]*len(vt) # hill_climbing1(vt, t, param, max_time)
    best = s
    timeout = time.time() + 60*max_time
    while temp > 1 and time.time() < timeout:
        n = neighbors(s, vt, t)
        for i in range(num_iter):
            if n == []:
                return best
            if  time.time() > timeout:
                break
            shuffle(n)
            s_ = n[-1]
            vs_ = calc_value(s_, vt)
            if vs_ > calc_value(s, vt):
                s = s_
                n = neighbors(s, vt, t)
                if vs_ > calc_value(best, vt):
                    best = s
            elif probability(s, s_, temp, vt) > random():
                s = s_
                n = neighbors(s, vt, t)
        temp *= alpha
    return best