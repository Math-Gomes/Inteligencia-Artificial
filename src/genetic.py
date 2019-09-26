from statusManager import *
from random import random, randint, shuffle
from math import floor, ceil
from itertools import accumulate

# Crossover do tipo "Dois Pontos" para a partir de dois pais, gerar dois filhos.
def crossover(p1, p2):
    sz = len(p1)
    l, u = ceil(sz*0.3), floor(sz*0.7) # Limites inferior e superior do crossover.
    s1, s2 = p1, p2 # Inicializa filho 1 com p1 e filho 2 com p2. 
    tmp1, tmp2 = p1[l:u], p2[l:u] # Faz a slice que representará o crossover.
    s1[l:u], s2[l:u] = tmp2, tmp1 # Atribui as mudanças do estado nos filhos, efetuando o crossover.
    return s1, s2

# Gera a mutação de um estado.
# Inicialmente, é escolhido um valor n de itens do estado que "sofrerão" a
# a mutação. Após isso, n itens aleatórios serão alterados. Essa alteração
# ocorre adicionando uma quantidade aleatória entre 0 e o número máximo
# deste item que ainda cabe na mochila. A mutação não gera estados inválidos.
def mutation(status, vt, sz):
    n = randint(1, len(status)) # Número de itens que sofrerão a mutação.
    item_idx = list(range(len(status))) 
    shuffle(item_idx)
    for _ in range(n):
        s_sz = calc_size(status, vt)
        i = item_idx.pop() # Índice do item a ser alterado.
        count = 0 # Contador de quantos deste item i cabem na mochila.
        while get_t(vt, i)*count + s_sz <= sz:
            count += 1
        count -= 1
        status[i] += randint(0, count) # Quantidade aleatória entre [0,count] é adicionada.
    return status

def initial_population(vt, sz, pop_sz):
    pop = []
    while len(pop) < pop_sz:
        p = mutation([0]*len(vt), vt, sz)
        if not p in pop:
            pop.append(p)
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

def genetic(vt, sz, pop_sz, rt_crossover, rt_mutation, n_generations):
    best = []
    pop = initial_population(vt, sz, pop_sz)
    # for i in pop:
    #     print(i)
    # print()
    for _ in range(n_generations):
        # seleciona os mais aptos (roleta, torneio ou amostragem)
        new_pop = []
        while len(new_pop) < pop_sz:
            new_pop.append(roulette_wheel(vt, sz, pop))
        # for i in new_pop:
        #     show_result(vt, i)

        # gerar novos atraves de crossover e mutacao
        # repor inviaveis
        # avaliar nova populacao
    return best

sz = 19 # Tamanho da mochila.
vt = [(1,3), (4,6), (5,7)] # Tuplas (Valor, Tamanho)

# sz = 132
# vt = [(9, 10), (5, 6), (10, 9), (5, 3), (8, 1), (5, 5), (7, 1), (9, 2), (2, 7), (8, 3), (9, 7), (2, 7), (6, 2), (9, 5), (5, 6)]

# pop = [[5, 0, 0], [0, 3, 0], [0, 2, 0], [4, 0, 0], [2, 0, 1]]
# pop = [[5, 0, 0], [2, 0, 1]]
# for p in pop:
#     show_result(vt, p)
# s = roulette_wheel(vt, sz, pop)
# p = initial_population(vt, sz, pop_sz = 5)
# print(p)
# show_result(vt, mutation([0,2,1], vt, sz))
genetic(vt, sz, pop_sz=10, rt_crossover=0.7, rt_mutation=0.5, n_generations=1)