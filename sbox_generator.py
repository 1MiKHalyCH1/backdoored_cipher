import operator

from itertools import combinations, permutations
from functools import reduce
from random import randint, shuffle
from cryptanalysis.linear import linear_uniformity
from cryptanalysis.differential import differential_uniformity

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

def make_rho(U):
    U = list(U)
    Y = U[:]
    shuffle(Y)
    while any(x==y for x,y in zip(U, Y)):
        shuffle(Y)
    return dict(zip(U, Y))

def dump_configs(S, K, V, U, rho, teta):
    with open('const.py', 'w') as f:
        f.write(f'S = {S}\nK = {K}')
    
    with open('secret.py', 'w') as f:
        f.write(f'''V = {set(V)}\nU = {set(U)}\nrho= {rho}\nteta = {teta}''')

def make_teta(V, U):
    res = list(permutations(V, len(V)))
    shuffle(res)
    keys = list(V)
    teta_S = {u:dict(zip(keys, x)) for u,x in zip(U, res)}
    teta_K = {u:dict(zip(keys, x)) for u,x in zip(U, [x[-1:] + x[:-1] for x in res])}
    return teta_S, teta_K

def make_sbox(V, U, rho, teta, n):
    S = [None] * (1<<n)
    for v in V:
        for u in U:
            S[v^u] = rho[u] ^ teta[u][v]
    return S

def generate_sbox(V, U, n):
    rho= make_rho(U)
    teta_S, teta_K = make_teta(V, U)
    S = make_sbox(V, U, rho, teta_S, n)
    K = make_sbox(V, U, rho, teta_K, n)
    return S, K, rho, teta_S

def generate_V(U, n):
    s = set(range(1<<n)) - set(U)
    while len(s) > 3:
        for x in combinations(s, 3):
            X = span(*x)
            if (X & U) - {0}:
                continue
            if check_partition(partitions(X, U), n):
                yield X
                break
        s -= X

def generate_best_data():
    best_lin, best_dif = 100, 100

    for _ in range(200):
        n = 6
        x, y, z = [randint(1, (1<<n) - 1) for _ in range(3)]
        if x^y == z:
            continue
        U = span(x, y, z)
        if len(U) != 8:
            continue

        for V in generate_V(U, n):
            S, K, rho, teta = generate_sbox(V, U, n)
            lin, dif = linear_uniformity(S), differential_uniformity(S)
            x = list(V)

            if lin <= best_lin and dif <= best_dif and not (lin == best_lin and dif == best_dif):
                best_lin, best_dif = lin, dif
                best_data = S, K, V, U, rho, teta
                print(set(V), set(U))
                print(lin, dif)
                print(best_data)
                print()
                dump_configs(*best_data)

if __name__ == '__main__':
    generate_best_data()
