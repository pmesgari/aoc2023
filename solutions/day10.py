from cli import filepath

with open(filepath) as inp:
	lines = inp.read().splitlines()

connectors = {
	'|': [[-1, 0], [1, 0]],
	'-': [[0, -1], [0, 1]],
	'L': [[-1, 0], [0, 1]],
	'J': [[-1, 0], [0, -1]],
	'7': [[0, -1], [1, 0]],
	'F': [[0, 1], [1, 0]],
	# 'S': [[1, 0]]
	# 'S': [[-1, 0], [1, 0], [0, -1], [0, 1]]
}

S = None
for row, line in enumerate(lines):
	for col, val in enumerate(line):
		if val == 'S':
			S = (row, col)
			break

print(f'Start at: {S}')

def adj(v, grid, levels, part2=False):
	row, col = v
	c = connectors.get(grid[row][col], None)
	if not c:
		if grid[row][col] == '.' and part2:
			c = [[-1, 0], [1, 0], [0, -1], [0, 1]]
		else:
			return []
	neighbors = []
	for d in c:
		dr, dc = d
		if row + dr < 0 or row + dr >= len(grid):
			continue
		if col + dc < 0 or col + dc >= len(grid[0]):
			continue
		if not part2 and grid[row + dr][col + dc] == '.':
			continue
		# if part2 and (row + dr, col + dc) in levels:
		#     continue
		neighbors.append((row + dr, col + dc))
	return neighbors

def walk(src, grid, part2=False):
	level = {src: 0}
	parent = {src: None}
	i = 1
	frontier = [src]
	while frontier:
		todo = []
		for u in frontier:
			for v in adj(u, grid, level, part2):
				if v not in level:
					level[v] = i
					parent[v] = u
					todo.append(v)
		frontier = todo
		i += 1
	return level, parent

def backtrack(start, parents):
	path = []
	curr = start
	while parents[curr]:
		path.append(curr)
		curr = parents[curr]
	return path

def draw(path, lines):
	mappings = {
		'|': '|',
		'-': '-',
		'L': '└',
		'J': '┘',
		'7': '┐',
		'F': '┌',
		'.': '.',
		'S': 'S'
	}
	grid = []
	for line in lines:
		grid.append([0] * len(line))
	for point in path:
		row, col = point
		grid[row][col] = mappings.get(lines[row][col])
	grid_str = [' '.join(list(map(lambda x: str(x), line))) for line in grid]

	return '\n'.join(grid_str)

def keywithmaxval(d):
	 """ a) create a list of the dict's keys and values; 
		 b) return the key with the max value"""  
	 v = list(d.values())
	 k = list(d.keys())
	 return k[v.index(max(v))]

# find all 4 neighbors of S
dirs = [
	[-1, 0], # above
	[0, 1], # right
	[1, 0], # below
	[0, -1], # left
]

sr, sc = S
sn = []
for d in dirs:
	dr, dc = d
	if sr + dr < 0 or sr + dr >= len(lines):
		continue
	if sc + dc < 0 or sc + dc >= len(lines[0]):
		continue
	sn.append(((sr + dr), (sc + dc)))

# For each neighbor see if S is adjacent to it
allowed = []
for n in sn:
	if S in adj(n, lines, []):
		allowed.append(n)

print(f'Allowed: {allowed}')

# For each allowed starting point walk the pipes and track the exploration
parents = []
levels = []
for start in allowed:
	level, parent= walk(start, lines)
	levels.append(level)
	parents.append(parent)

# Find the furthest point by merging the explorations and taking the minimum
import math
path = {}
for level in levels:
	for node, val in level.items():
		if node not in path:
			path[node] = math.inf
		path[node] = min(path[node], val)

maxkey = keywithmaxval(path)
maxval = path[maxkey]
print(f'Furthest point is {maxkey} with value {maxval + 1}')

# Build the main loop
main_loop = set()
# Start from the furthest point and walk back
for idx, p in enumerate(parents):
	path = backtrack(maxkey, p)
	s = None
	for a in allowed:
		if a in p and p[a] == None:
			s = a
	path.insert(0, s)
	print(draw(path, lines), '\n')
	for n in path:
		main_loop.add(n)

# Add the original starting point
main_loop.add(S)
grid = draw(main_loop, lines)
print(grid)

def expand(grid):
	pass

# find all the outside tiles
out = []
outl, outp = walk((0, 0), lines, part2=True)
for point in outl.keys():
	row, col = point
	if lines[row][col] == '.':
		out.append(point)
# find all possible inside tiles
inside = []
for row, line in enumerate(lines):
	for col, val in enumerate(line):
		if (row, col) in main_loop or (row, col) in out:
			continue
		inside.append((row, col))

tiles = []
for row, line in enumerate(lines):
	for col, val in enumerate(line):
		if lines[row][col] == '.':
			tiles.append((row, col))
# print(inside)

# for each possible inside tile draw a line in each of the four directions
def intercept(point, grid):
	connectors = ['└', '┘', '┐', '┌', '|', '-']
	to_check = []
	def intercept_up():
		rmin = 0
		dr = -1
		dc = 0
		# collect all the connectors along the given direction
		curr = point
		up = []
		while True:
			row, col = curr
			if row + dr >= rmin:
				if grid[row + dr][col + dc] in connectors:
					up.append((row + dr, col + dc))
				curr = (row + dr, col + dc)
			else:
				break
		return up
	
	def intercept_down():
		rmax = len(grid)
		dr = 1
		dc = 0
		curr = point
		down = []
		while True:
			row, col = curr
			if row + dr < rmax:
				if grid[row + dr][col + dc] in connectors:
					down.append((row + dr, col + dc))
				curr = (row + dr, col + dc)
			else:
				break
		return down
	
	def intercept_left():
		cmin = 0
		dr = 0
		dc = -1
		curr = point
		left = []
		while True:
			row, col = curr
			if col + dc >= cmin:
				if grid[row + dr][col + dc] in connectors:
					left.append((row + dr, col + dc))
				curr = (row + dr, col + dc)
			else:
				break
		return left
	
	def intercept_right():
		cmax = len(grid[0])
		dr = 0
		dc = 1
		curr = point
		right = []
		while True:
			row, col = curr
			if col + dc < cmax:
				if grid[row + dr][col + dc] in connectors:
					right.append((row + dr, col + dc))
				curr = (row + dr, col + dc)
			else:
				break
		return right

	up = intercept_up()
	down = intercept_down()
	right = intercept_right()
	left = intercept_left()

	to_check = [up, down, right, left]

	return to_check

def count(intercepts):
	v = ['└', '┘', '┐', '┌', '|']
	h = ['└', '┘', '┐', '┌', '-']
	up, down, right, left = intercepts

	def _count_v(_intercepts):
		_c = 0
		prev = None
		while _intercepts:
			curr = _intercepts.pop(0)
			if not prev:
				rc, cc = curr
				if grid[rc][cc] not in v:
					_c += 1
				prev = curr
				continue
			cr, cc = curr
			pr, pc = prev
			if grid[cr][cc] in v and grid[pr][pc] in v:
				continue
			_c += 1
		return _c

	def _count_h(_intercepts):
		_c = 0
		prev = None
		while _intercepts:
			curr = _intercepts.pop(0)
			if not prev:
				rc, cc = curr
				if grid[rc][cc] not in h:
					_c += 1
				prev = curr
				# _c += 1
				continue
			cr, cc = curr
			pr, pc = prev
			if (grid[cr][cc] in h and grid[pr][pc] in h):
				continue
			_c += 1
		return _c

	cup = _count_v(up)
	cdown = _count_v(down)
	cright = _count_h(right)
	cleft = _count_h(left)

	return [cup, cdown, cright, cleft]

print(inside)
print('\n')

grid = [line.split(' ') for line in grid.split('\n')]
intercepts = intercept((5, 7), grid)
print(intercepts)
print(count(intercepts))

inside_count = 0
for row, line in enumerate(grid):
	for col, val in enumerate(line):
		if (row, col) in main_loop:
			continue

		crosses = 0
		rr, cc = row, col
		while rr >=0 and rr < len(grid) and cc >=0 and cc < len(grid[0]):
			c2 = grid[rr][cc]
			if (rr, cc) in main_loop and grid[rr][cc] != '└' and grid[rr][cc] != '┐':
				crosses += 1
			rr += 1
			cc += 1
		if crosses % 2 == 1:
			inside_count += 1

print(inside_count)


inside_count = 0
for row, col in tiles:
	if (row, col) in main_loop:
		continue

	crosses = 0
	rr, cc = row, col
	while rr >=0 and rr < len(grid) and cc >=0 and cc < len(grid[0]):
		c2 = grid[rr][cc]
		if (rr, cc) in main_loop and grid[rr][cc] != '└' and grid[rr][cc] != '┐':
			crosses += 1
		rr += 1
		cc += 1
	if crosses % 2 == 1:
		inside_count += 1

print(inside_count)

