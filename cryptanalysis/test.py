from math import log2

from linear import linear_approximation_table, linear_uniformity
from differential import difference_distribution_table, differential_uniformity
from const import S

HEADER = f"""\\begin{{table}}[h]
	\\centering
    \\resizebox{{\\linewidth}}{{!}}{{%
	\\begin{{tabular}}{{ c|{' '.join('c' for _ in range(len(S)))}| }}
"""
FOOTER = """
	\end{tabular}}
\end{table}"""

def format_signed(x):
    if x == 0: return ' . '
    x = str(x)
    return ' $' + ' '*(3-len(x)) + x + '$ '

def write_tex_lat(f):
    lat = linear_approximation_table(S)
    indexes = list(range(1<<6))
    f.write(f"   &{'&'.join(' $' + hex(i)[2:].zfill(2) + '$ ' for i in indexes)}\\\\ \\hline\n")
    for i in indexes:
        f.write(f'   {hex(i)[2:].zfill(2)} & {" & ".join(format_signed(lat[i][j]) for j in indexes)} \\\\\n')

def write_tex_ddt(f):
    ddt = difference_distribution_table(S)
    indexes = list(range(1<<6))
    f.write(f"   &{'&'.join(' $' + hex(i)[2:].zfill(2) + '$ ' for i in indexes)}\\\\ \\hline\n")
    for i in indexes:
        f.write(f'   {hex(i)[2:].zfill(2)} & {" & ".join(format_signed(ddt[i][j]) for j in indexes)} \\\\\n')
    
def calculate_pairs(rounds):
    l_u, d_u = linear_uniformity(S), differential_uniformity(S)
    l_pairs = -int(log2(pow(l_u/linear_approximation_table(S)[0][0], rounds)))
    d_pairs = log2(pow(d_u/difference_distribution_table(S)[0][0], rounds))
    print(f'S-box is lineary {l_u}-uniform and differentialy {d_u}-uniform.')
    print(f'It requires:')
    print(f'  linear:       2**{l_pairs} -> {pow(2, l_pairs)} pt-ct pairs')
    print(f'  differential: 2**{d_pairs:.2f} -> {int(pow(2, d_pairs))} pt-ct pairs')
    print()

if __name__ == '__main__':
    rounds = 6
    calculate_pairs(rounds)

    with open('lat.txt', 'w') as f:
        f.write(HEADER)
        write_tex_lat(f)
        f.write(FOOTER)

    with open('ddt.txt', 'w') as f:
        f.write(HEADER)
        write_tex_ddt(f)
        f.write(FOOTER)
