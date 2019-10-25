from statusManager import *
from random import random, randint, shuffle
from math import floor, ceil
from itertools import accumulate, combinations
import time

# Crossover do tipo "Dois Pontos" para a partir de dois pais, gerar dois filhos.
def crossover(p1, p2, rt):
    if random() > rt:
        return p1, p2
    sz = len(p1)
    l, u = ceil(sz*0.3), floor(sz*0.7) # Limites inferior e superior do crossover.
    s1, s2 = p1.copy(), p2.copy() # Inicializa filho 1 com p1 e filho 2 com p2. 
    tmp1, tmp2 = p1[l:u].copy(), p2[l:u].copy() # Faz a slice que representará o crossover.
    s1[l:u] = tmp2 # Atribui as mudanças do estado nos filhos, efetuando o crossover.
    s2[l:u] = tmp1
    return s1, s2

# Gera a mutação de um estado.
# Inicialmente, é escolhido um valor n de itens do estado que "sofrerão" a
# a mutação. Após isso, n itens aleatórios serão alterados. Essa alteração
# ocorre adicionando uma quantidade aleatória entre 0 e o número máximo
# deste item que ainda cabe na mochila. A mutação não gera estados inválidos.
def mutation(status, vt, sz, rt):
    if random() > rt:
        return status
    n = randint(1, len(status)) # Número de itens que sofrerão a mutação.
    item_idx = list(range(len(status))) 
    shuffle(item_idx)
    s = status.copy()
    for _ in range(n):
        s_sz = calc_size(s, vt)
        i = item_idx.pop() # Índice do item a ser alterado.
        count = 0 # Contador de quantos deste item i cabem na mochila.
        while get_t(vt, i)*count + s_sz <= sz:
            count += 1
        count -= 1
        s[i] += randint(0, floor(count*0.7)) # Quantidade aleatória entre [0,count] é adicionada.
    return s

# Gera a população inicial, a partir da mutação, por exemplo, do estado [0,0,0].
def initial_population(vt, sz, pop_sz, rt):
    pop = []

    # Adiciona o primeiro elemento na população, garantindo que haverá pelo menos um diferente de [0,...,0].
    while True:
        p = mutation([0]*len(vt), vt, sz, 1)
        if p != [0]*len(vt):
            pop.append(p)
            break

    # Completa a população.
    while len(pop) < pop_sz:
        pop.append(mutation([0]*len(vt), vt, sz, rt))
    return pop

def roulette_wheel(vt, sz, pop):
    values = [(calc_value(p, vt), p) for p in pop]
    s = sum([v for (v,p) in values]) # Soma dos valores dos elementos da população.
    ratio = [(v/s, p) for (v, p) in values]
    ratio.sort()
    rt_acc = list(accumulate([v for (v,p) in ratio])) # Lista com os valores de ratio acumulados.
    r = random()
    for (i, c) in enumerate(rt_acc):
        if r < c:
            return ratio[i][1]

def genetic(vt, t, param, max_time):
    (pop_sz, rt_crossover, rt_mutation) = param
    n_generations = 30
    pop = initial_population(vt, t, pop_sz, rt_mutation)
    best = search_best(vt, pop, t)
    timeout = time.time() + 60*max_time
    for _ in range(n_generations):
        if time.time() > timeout:
            break

        new_pop = []
        while len(new_pop) < pop_sz:
            new_pop.append(roulette_wheel(vt, t, pop).copy())

        diff, equals = [], []
        for p in new_pop:
            if not p in diff:
                diff.append(p)
            else:
                equals.append(p)

        # Mutação é aplicada nos indivíduos que são iguais.
        mut = [mutation(e, vt, t, rt_mutation) for e in equals]

        # Crossover aplicado nos diferentes.
        cross = [crossover(p1, p2, rt_crossover) for (p1, p2) in list(combinations(diff, 2))]
        aux = []
        for (a, b) in cross:
            if is_valid(vt, a, t) and not a in aux:
                aux.append(a)
            if is_valid(vt, b, t) and not b in aux:
                aux.append(b)
        cross = aux

        if time.time() > timeout:
            break

        new_pop = k_best_status(mut+cross, vt, t, pop_sz)

        best_new_pop = search_best(vt, new_pop, t)
        if calc_value(best_new_pop, vt) > calc_value(best, vt):
            best = best_new_pop

        if len(new_pop) < pop_sz:
            n = pop_sz - len(new_pop) # Quantidade de elementos que faltam pra completar a população.
            for e in k_best_status(pop, vt, t, n):
                new_pop.append(e)
                pop.remove(e)
        pop = new_pop
    return best