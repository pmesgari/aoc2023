import re
import math
from collections import deque
from cli import filepath

with open(filepath) as inp:
    lines = inp.read()

commands, nodes = lines.split('\n\n')
commands = list(commands)
nodes = [re.findall('\w{3}', node) for node in nodes.split('\n')]
nodes = {x[0]: x[1:] for x in nodes}


def walk(src, pred=lambda x: x == 'ZZZ'):
    Q = deque([src])
    j = 0
    steps = 0
    while Q:
        node = Q.popleft()
        if pred(node):
            break
        j = j % len(commands)
        command = commands[j]
        if command == 'R':
            Q.appendleft(nodes[node][1])
        elif command == 'L':
            Q.appendleft(nodes[node][0])
        j += 1
        steps += 1
    return steps

print(walk('AAA'))

a_nodes = [key for key, _ in nodes.items() if key.endswith('A') ]
pred = lambda x: x.endswith('Z')
ans = []
for n in a_nodes:
    s = walk(n, pred)
    ans.append(s)

print(math.lcm(*ans))
