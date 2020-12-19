def int_to_blocks(x, block_size):
    blocks = []
    while x:
        x, block = x >> block_size, x & ((1<<block_size) - 1)
        blocks.append(block)
    return [0] if not blocks else blocks[::-1]

def blocks_to_int(blocks, block_size):
    x = 0
    for block in blocks:
        x = (x << block_size) | block
    return x

def invert_S(S):
    return [S.index(i) for i in range(len(S))]