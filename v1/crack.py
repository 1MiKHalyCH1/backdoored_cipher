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

def encrypt(x, y, key):
    keys = [key]
    for _ in range(ROUNDS-1):
        keys.append(K[keys[-1]])
    print(keys)

    for i in keys:
        print(f'x: {split(x)[1]}, y: {split(y)[1]}, i: {split(i)[1]}')
        print(f'{split(y)[1]}', f'{split(x)[1]} ^ {split(S[y])[1]} ^ {split(i)[1]} = {split(x^S[y]^i)[1]}')
        print()
        x, y = y, x^S[y]^i
    print(split(x), split(y))

    return x, y

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
    for x in range(1<<6):
        pt = (x << 6) | S[x]
        ct = cipher.encrypt(pt)
        if check_key(pt, ct):
            right_cosets.add(split(x)[1])

    for coset in right_cosets:
        for key in cosets[coset]:
            if all(Cipher(key, ROUNDS, 12).decrypt(cipher.encrypt((x<<6) | S[x])) == ((x<<6) | S[x]) for x in S):
                return key


if __name__ == '__main__':
    for i in range(1<<6):
        cipher = Cipher(i, ROUNDS, 12)
        assert crack_key(cipher) == i
    print('Done!')