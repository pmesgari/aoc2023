
import re
import math
from cli import filepath


with open(filepath) as inp:
    lines = inp.read().split('\n\n')

seeds = list(map(lambda x: int(x), re.split('\s+', lines[0].split(':')[1].strip())))

maps = []
for line in lines[1:]:
    maps.append([list(map(lambda x: int(x), re.split('\s+', l))) for l in line.split('\n')[1:]])

i = 0
j = 1
pairs = []
while j < len(seeds):
    pairs.append((seeds[i], seeds[i] + seeds[j]))
    i = j + 1
    j += 2

def apply(s, r, shift):
    """
    inner
      s1----s2
    r1---------r2

    left
           s1---------s2
    r1----------r2

    right
    s1----------s2
           r1---------r2

               outer
    s1---------s2
      r1----r2


    """
    s1, s2 = s
    r1, r2 = r

    left = r1 <= s1 < r2
    right = r1 < s2 <= r2
    outer = s1 < r1 and r2 < s2
    inner = r1 <= s1 and s2 <= r2

    if inner:
        return [(s1 + shift, s2 + shift)], []
    if left:
        return [(s1 + shift, r2 + shift)], [(r2, s2)]
    if right:
        return [(r1 + shift, s2 + shift)], [(s1, r1)]
    if outer:
        return [(r1 + shift, r2 + shift)], [(s1, r1), (r2, s2)]
    return [], []


def process(seeds, m):
    processed = []

    while seeds:
        s1, s2 = seeds.pop(0)
        done = False
        for line in m:
            destination, r1, r_length = line
            r2 = r1 + r_length
            shift = destination - r1

            applied, gaps = apply((s1, s2), (r1, r2), shift)
            if applied or gaps:
                processed += applied
                seeds += gaps
                done = True
                break
        if not done:
            processed.append((s1, s2))
    return processed


ans = math.inf

for p in pairs:
    res = [p]
    for idx, m in enumerate(maps):
        res = process(res, m)
    curr_min = min(res)[0]
    if curr_min < ans:
        ans = curr_min

print(ans)