from itertools import combinations
from cli import filepath


with open(filepath) as inp:
    lines = inp.read().splitlines()

galaxies = []
for row, line in enumerate(lines):
    for col in range(len(line)):
        if line[col] == '#':
            galaxies.append((row, col))

row_space = [True] * len(lines)
col_space = [True] * len(lines[0])
for gal in galaxies:
    row, col = gal
    row_space[row] = False
    col_space[col] = False

pairs = list(combinations(galaxies, 2))

def manhattan(pair):
    p1, p2 = pair
    r1, c1 = p1
    r2, c2 = p2

    return abs(r2 - r1) + abs(c2 - c1)

def expand(galaxy, space, scale=2):
    row, col = galaxy
    rs, cs = space

    c1 = sum(rs[:row])
    c2 = sum(cs[:col])

    if c1:
        row = row + (c1 * (scale - 1))
    if c2:
        col = col + (c2 * (scale - 1))

    return (row, col)

def apply(scale):
    ans = 0
    for p in pairs:
        p1, p2 = p
        pe1 = expand(p1, (row_space, col_space), scale)
        pe2 = expand(p2, (row_space, col_space), scale)
        ans += manhattan((pe1, pe2))

    print(ans)

apply(2)
apply(1000000)
