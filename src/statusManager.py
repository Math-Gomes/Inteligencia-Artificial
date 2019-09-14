def get_v(vt, i): return vt[i][0]

def get_t(vt, i): return vt[i][1]

# Calcula o valor de um estado.
def calc_value(status, vt):
    return sum([v*get_v(vt, k) for k,v in enumerate(status)])

# Calcula o peso de um estado.
def calc_size(status, vt):
    return sum([v*get_t(vt, k) for k,v in enumerate(status)])

# Cria uma lista correspondente à expansão de um estado.
# Exemplo: Se estado = [0,0,0], sua expansão será [[1,0,0],[0,1,0],[0,0,1]].
def expand(status):
    sl = []
    for i in range(len(status)):
        sl.append(status.copy())
        sl[i][i] += 1
    return sl

# Cria uma lista correspondente à regressão de um estado.
# Exemplo: Se estado = [1,1,1],
# sua regressão será [[0,1,1], [1,0,1], [1,1,0]].
def regress(status):
    sl = []
    for i in range(len(status)):
        sl.append(status.copy())
        sl[i][i] -= 1
    # Remove de sl o estado que possuir algum elemento menor que zero:
    sl = list(filter(lambda s: not any(i < 0 for i in s), sl))
    return sl

# Verifica se um estado é válido, ou seja, se o peso deste não ultrapassa a
# capacidade da mochila.
def is_valid(vt, status, sz):
    return calc_size(status, vt) <= sz

# Procura o melhor estado de uma lista de estados.
# O melhor estado é aquele que possui o maior valor, entretanto, se houver
# empate neste quesito, é escolhido aquele que possui menor peso.
def search_best(vt, sl, sz):
    vs = list(filter(lambda s: is_valid(vt, s, sz), sl)) # valid status
    if vs == []:
        return []
    vs.sort(key = lambda s: calc_value(s, vt))
    best = list(filter(lambda s: calc_value(s, vt) == calc_value(vs[-1], vt), vs))
    best.sort(key = lambda s: calc_size(s, vt))
    return best[0]

# Gera a vizinhança de um estado, que é composta pelos estados válidos de sua
# expansão e retrocesso.
def neighbors(status, vt, sz):
    e = list(filter(lambda s: is_valid(vt, s, sz), expand(status)))
    r = list(filter(lambda s: is_valid(vt, s, sz), regress(status)))
    return e + r

# Exibe o valor, peso e a configuração de um estado.
def show_result(vt, status):
    print("(V,T) = ({0:2d},{1:2d}) | Status = {2}\n".format(calc_value(status, vt),calc_size(status, vt),status))