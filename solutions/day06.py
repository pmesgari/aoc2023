import re
import math
from cli import filepath

with open(filepath) as inp:
    lines = inp.read().splitlines()

times = list(map(lambda x: int(x), re.split('\s+', lines[0])[1:]))
distances = list(map(lambda x: int(x), re.split('\s+', lines[1])[1:]))

def solve(distances, times):
    count = []
    for idx, tmax in enumerate(times):
        dmax = distances[idx]
        th1 = int((tmax + math.sqrt(math.pow(tmax, 2) - 4 * dmax)) // 2)
        th2 = int((tmax - math.sqrt(math.pow(tmax, 2) - 4 * dmax)) // 2)
        if th1 < th2 and (tmax - th2) * th2 <= dmax:
            th2 -= 1
        elif (tmax - th1) * th1 == dmax:
            th1 -= 1

        count.append(th1 - th2)
    return count

count = solve(distances, times)
ans = 1
for c in count:
    ans = ans * c
print(ans)

times = [int(''.join([str(t) for t in times]))]
distances = [int(''.join([str(d) for d in distances]))]

count = solve(distances, times)
ans = 1
for c in count:
    ans = ans * c
print(ans)
