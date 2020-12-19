from itertools import cycle
from random import getrandbits

from backdoored_algo.cipher import Cipher
from backdoored_algo.const import S, K
from secret import V, U, ro, teta

ROUNDS = 6

ro_inv = {ro[x]:x for x in ro}
S_inv = {S[x]:x for x in S}


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

def crack_key(cipher):
    cosets = {x:set() for x in U}
    for x in range(len(S)):
        cosets[split(x)[1]].add(x)

    right_cosets = set()
    pts = [((x << 6) | S[x]) for x in range(1<<6)]
    for pt in pts:
        ct = cipher.encrypt(pt)
        if check_key(pt, ct):
            right_cosets.add(split(pt >> 6)[1])

    for coset in right_cosets:
        for key in cosets[coset]:
            if all(Cipher(key, ROUNDS, 12).decrypt(cipher.encrypt(pt)) == pt for pt in pts):
                return key


if __name__ == '__main__':
    for key in range(1<<6):
        cipher = Cipher(i, ROUNDS, 12)
        assert crack_key(cipher) == i
    print('Done!')