import re
from cli import filepath


with open(filepath) as inp:
    lines = inp.read().splitlines()

lines = [re.split('\s+', line) for line in lines]
lines = [list(map(lambda v: int(v), line)) for line in lines]

def extrapolate(line, backwards=False):
    values = []
    if backwards:
        values.append(line[0])
        r = line[:-1]
    else:
        values.append(line[-1])
        r = line[1:]

    h = 0
    while True:
        i = 0
        j = 1
        n = []
        while j < len(r):
            n.append(r[j] - r[i])
            i = j
            j += 1
        r = n
        values.append(n[0] if backwards else n[-1])

        if all([v == 0 for v in n]):
            break

    return n, values

ans = 0
for line in lines:
    ans += sum(extrapolate(line)[1])

print(ans)

def reduce(firsts):
    p_last = firsts[-1]
    values = []
    for i in range(len(firsts) - 1, -1, -1):
        p_last = firsts[i] - p_last
        values.append(p_last)
    return values

ans = 0
for line in lines:
    e = extrapolate(line, backwards=True)
    r = reduce(e[1])
    ans += r[-1]

print(ans)
