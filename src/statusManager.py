def get_v(vt, i): return vt[i][0]

def get_t(vt, i): return vt[i][1]

def calc_value(status, vt):
    return sum([v*get_v(vt, k) for k,v in enumerate(status)])

def calc_size(status, vt):
    return sum([v*get_t(vt, k) for k,v in enumerate(status)])

def expand(status):
    l = []
    for i in range(len(status)):
        l.append(status.copy())
        l[i][i] += 1
    return l

def is_valid(vt, status, sz):
    return calc_size(status, vt) <= sz

def search_best(vt, sl, sz):
    r = [status for status in sl if is_valid(vt, status, sz)]
    r.sort(key = lambda s: calc_value(s, vt))
    if r == []: return []
    return r[-1]

def show_result(vt, status):
    print("(V,T) = ({0:2d},{1:2d}) | Status = {2}\n".format(calc_value(status, vt),calc_size(status, vt),status))