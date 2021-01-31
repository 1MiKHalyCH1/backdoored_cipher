def linear_approximation_table(S):
    size = len(S)
    table = [[0 for _ in range(size)] for _ in range(size)]
    for in_mask in range(size):
        for out_mask in range(size):
            res = - size // 2
            for x in range(size):
                y = S[x]
                x_masked, y_masked = x & in_mask, y & out_mask
                if not ((bin(x_masked)[2:].count('1') + bin(y_masked)[2:].count('1')) % 2):
                    res += 1
            table[in_mask][out_mask] = res

    return table

def linear_uniformity(S):
    lat = linear_approximation_table(S)
    return max(max(map(abs, row)) for row in lat[1:])