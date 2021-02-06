from random import choice

from backdoored_algo.cipher import Cipher
from backdoored_algo.const import S, K
from secret import V, U, rho, teta

ROUNDS = 6
PTS = list(range(1 << 12))

rho_inv = {rho[x]:x for x in rho}


def split(x):
    for v in V:
        if x ^ v in U:
            return v, x ^ v

def get_random_pts():
    return {choice(PTS) for _ in range(15)}

def check_key(pt, ct):
    x,     y     = pt >> 6, pt & ((1<<6)-1)
    res_x, res_y = ct & ((1<<6)-1), ct >> 6

    cosets = [split(x)[1]]
    for _ in range(ROUNDS+1):
        cosets.append(rho[cosets[-1]])

    if cosets[-2] == split(res_x)[1] and cosets[-1] == split(res_y)[1]:
        return True

def crack_key(cipher, cosets):
    right_cosets = set()
    pts = {choice(list(items)):u for u,items in cosets.items()}
    pts = {((elem << 6) | S[elem]):v for elem,v in pts.items()}

    for pt, coset in pts.items():
        ct = cipher.encrypt(pt)
        if check_key(pt, ct):
            right_cosets.add(coset)

    for coset in right_cosets:
        for key in cosets[coset]:
            if all(Cipher(key, ROUNDS, 12).decrypt(cipher.encrypt(pt)) == pt for pt in get_random_pts()):
                return key


if __name__ == '__main__':
    cosets = {x:set() for x in U}
    for x in range(len(S)):
        cosets[split(x)[1]].add(x)

    for key in range(1<<6):
        cipher = Cipher(key, ROUNDS, 12)
        assert crack_key(cipher, cosets) == key
    print('Done!')