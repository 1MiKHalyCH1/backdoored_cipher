from backdoored_algo.const import S, K
from backdoored_algo.utils import int_to_blocks, blocks_to_int, invert_S
from itertools import cycle

S_inv = invert_S(S)

class Cipher:
    def __init__(self, key, rounds, block_size):
        self._rounds = rounds
        self._keys = self._expand_key(key)
        self._block_size = block_size
        self._half_block_size = block_size >> 1

    def _expand_key(self, key):
        keys = [key]
        for _  in range(self._rounds-1):
            keys.append(K[keys[-1]])
        return keys

    def _encrypt_block(self, block):
        L, R = block >> self._half_block_size, block & ((1 << self._half_block_size) - 1)
        for i in range(self._rounds):
            L, R = R, L ^ (S[R] ^ self._keys[i])
        return (L << self._half_block_size) | R

    def _decrypt_block(self, block):
        L, R = block >> self._half_block_size, block & ((1 << self._half_block_size) - 1)
        for i in range(self._rounds):
            R, L = L, R ^ (S[L] ^ self._keys[self._rounds - i - 1])
        return (L << self._half_block_size) | R

    def encrypt(self, pt):
        pt_blocks = int_to_blocks(pt, self._block_size)
        ct_blocks = [self._encrypt_block(block) for block in pt_blocks]
        return blocks_to_int(ct_blocks, self._block_size)

    def decrypt(self, ct):
        ct_blocks = int_to_blocks(ct, self._block_size)
        pt_blocks = [self._decrypt_block(block) for block in ct_blocks]
        return blocks_to_int(pt_blocks, self._block_size)