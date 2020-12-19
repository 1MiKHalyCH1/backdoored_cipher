import operator

from itertools import combinations, permutations
from functools import reduce
from random import shuffle


def span(*basis):
    result = set()
    for n in range(len(basis) + 1):
        for comb in combinations(basis, n):
            result.add(reduce(lambda x,y: x^y, comb, 0))
    return frozenset(result)

def partitions(X, complement_subspace):
    return {frozenset(x ^ i for x in X) for i in complement_subspace}

def check_partition(partition, n):
    res = set()
    for x in partition:
        res.update(x)
    return res == set(range(1<<n))

def make_ro(U):
    U = list(U)
    Y = U[:]
    shuffle(Y)
    while any(x==y for x,y in zip(U, Y)):
        shuffle(Y)
    return dict(zip(U, Y))

def dump_configs(S, K, V, U, ro, teta):
    with open('const.py', 'w') as f:
        f.write(f'S = {S}\nK = {K}')
    
    with open('secret.py', 'w') as f:
        f.write(f'''V = {set(V)}\nU = {set(U)}\nro = {ro}\nteta = {teta}''')

def make_teta(V, U):
    res = list(permutations(V, len(V)))
    shuffle(res)
    keys = list(V)
    teta_S = {u:dict(zip(keys, x)) for u,x in zip(U, res)}
    teta_K = {u:dict(zip(keys, x)) for u,x in zip(U, [x[-1:] + x[:-1] for x in res])}
    return teta_S, teta_K

def make_sbox(V, U, ro, teta, n):
    S = [None] * (1<<n)
    for v in V:
        for u in U:
            S[v^u] = ro[u] ^ teta[u][v]
    return S

def generate_sbox(V, U, n):
    ro = make_ro(U)
    teta_S, teta_K = make_teta(V, U)
    S = make_sbox(V, U, ro, teta_S, n)
    K = make_sbox(V, U, ro, teta_K, n)
    return S, K, ro, teta_S

if __name__ == '__main__':
    n = 6
    res = set()
    U = span(0x01, 0x19, 0x31)
    print(len(U), U)

    s = set(range(1<<n)) - set(U)
    while len(s) > 3:
        for x in combinations(s, 3):
            X = span(*x)
            if (X & U) - {0}:
                continue
            if check_partition(partitions(X, U), n):
                res.add(X)
                break
        s -= X

    res = list(res)
    shuffle(res)

    V = res[0]
    S, K, ro, teta = generate_sbox(V, U, n)

    print(S)
    print(K)
    print(ro)
    print(teta)
    dump_configs(S, K, V, U, ro, teta)

