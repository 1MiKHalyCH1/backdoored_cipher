def difference_distribution_table(S):
    size = len(S)
    table = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            delta_in = x ^ y
            delta_out = S[x] ^ S[y]
            table[delta_in][delta_out] += 1
    return table

def differential_uniformity(S):
    ddt = difference_distribution_table(S)
    return max(max(map(abs, row)) for row in ddt[1:])
