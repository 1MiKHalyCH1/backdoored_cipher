from random import choice

from backdoored_algo.cipher import Cipher
from backdoored_algo.const import S, K
from secret import V, U, rho, teta

ROUNDS = 5
PTS = list(range(1 << 12))

rho_inv = {rho[x]:x for x in rho}


def split(x):
    for v in V:
        if x ^ v in U:
            return v, x ^ v

def get_random_pts():
    return {choice(PTS) for _ in range(15)}

def crack_key(cipher, cosets, keys):
    for u in U:
        k = keys[u]
        u_inv, rho_u_inv = rho_inv[0]^k[0], rho_inv[0]^k[1]
        x = choice(list(cosets[rho_u_inv]))
        y = choice(list(cosets[u_inv]))
        pt = (x << 6) | y
        ct = cipher.encrypt(pt)

        res_x, res_y = split(ct >> 6)[1], split(ct & ((1<<6)-1))[1]

        a = [rho_u_inv, u_inv]
        for i in range(2, ROUNDS):
            a.append(a[-2] ^ rho[k[i] ^ a[-1]])

        if tuple(a[-2:]) == (res_x, res_y):
            for key in cosets[u]:
                if all(Cipher(key, ROUNDS, 12).decrypt(cipher.encrypt(pt)) == pt for pt in get_random_pts()):
                    return key

if __name__ == '__main__':
    cosets = {x:set() for x in U}
    for x in range(len(S)):
        cosets[split(x)[1]].add(x)

    keys = {}
    for u in U:
        k = [u]
        for _ in range(ROUNDS):
            k.append(rho[k[-1]])
        keys[u] = k

    for key in range(1<<6):
        cipher = Cipher(key, ROUNDS, 12)
        assert crack_key(cipher, cosets, keys) == key
    print('Done!')