from statusManager import show_result
from hillClimbing import hill_climbing
from beamSearch import beam_search
from branchBound import branch_and_bound
from simpleDescent import simple_descent
from deepestDescent import deepest_descent
from multistart import multistart_descent
from random import randint

# Exemplo 1:
sz = 19 # Tamanho da mochila.
vt = [(1,3), (4,6), (5,7)] # Tuplas (Valor, Tamanho)

# Exemplo 2:
# sz = 100 # Tamanho da mochila.
# vt = [(7,5), (10,3), (18,9), (13,2)] # Tuplas (Valor, Tamanho)

# Exemplo 3:
sz = 132
vt = [(9, 10), (5, 6), (10, 9), (5, 3), (8, 1), (5, 5), (7, 1), (9, 2), (2, 7), (8, 3), (9, 7), (2, 7), (6, 2), (9, 5), (5, 6)]

# sz = 100
# vt = []
# for _ in range(15):
#     vt.append((randint(1,10),randint(1,10)))

print(vt)

print("Hill Climbing:")
show_result(vt, hill_climbing(vt, sz))

k = 10
print("Beam Search: (k = {0})".format(k))
show_result(vt, beam_search(vt, sz, k))

# print("Branch and Bound: (Estimativa otimista)")
# show_result(vt, branch_and_bound(vt, sz, opt = True))

# print("Branch and Bound: (Estimativa nao otimista)")
# show_result(vt, branch_and_bound(vt, sz, opt = False))

print("Simple Descent:")
show_result(vt, simple_descent([0]*len(vt), vt, sz))

print("Deepest Descent:")
show_result(vt, deepest_descent([0]*len(vt), vt, sz))

print("Multistart Descent:")
show_result(vt, multistart_descent(vt, sz, iterMax = 10))