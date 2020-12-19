from random import choice

from backdoored_algo.cipher import Cipher
from backdoored_algo.const import S, K
from secret import V, U, ro, teta

ROUNDS = 5
PTS = list(range(1 << 12))

ro_inv = {ro[x]:x for x in ro}

def split(x):
    for v in V:
        if x ^ v in U:
            return v, x ^ v

def check_key(pt, ct):
    x,     y     = pt >> 6, pt & ((1<<6)-1)
    res_x, res_y = ct >> 6, ct & ((1<<6)-1)

    cosets = [split(x)[1]]
    for _ in range(ROUNDS):
        cosets.append(ro[cosets[-1]])

    if cosets[-1] == split(res_x)[1]:
        return True

def crack_key(cipher, cosets, keys):
    for u in U:
        k = keys[u]
        k0_inv, k1_inv = ro_inv[0]^k[0], ro_inv[0]^k[1]
        x = choice(list(cosets[k1_inv]))
        y = choice(list(cosets[k0_inv]))
        pt = (x << 6) | y
        ct = cipher.encrypt(pt)

        res_x, res_y = split(ct >> 6)[1], split(ct & ((1<<6)-1))[1]

        if ro_inv[res_x ^ k0_inv] ^ k[3] == ro[res_x ^ k[4]] ^ res_y:
            for key in cosets[u]:
                if all(Cipher(key, ROUNDS, 12).decrypt(cipher.encrypt(pt)) == pt for pt in PTS):
                    return key


if __name__ == '__main__':
    cosets = {x:set() for x in U}
    for x in range(len(S)):
        cosets[split(x)[1]].add(x)

    keys = {}
    for u in U:
        k = [u]
        for _ in range(ROUNDS):
            k.append(ro[k[-1]])
        keys[u] = k

    for key in range(1<<6):
        cipher = Cipher(key, ROUNDS, 12)
        assert crack_key(cipher, cosets, keys) == key
    print('Done!')