import math
from cli import filepath

with open(filepath) as inp:
	lines = inp.read().splitlines()

lines = [list(line) for line in lines]

connector_mappings = {
	'|': '|',
	'-': '-',
	'L': '└',
	'J': '┘',
	'7': '┐',
	'F': '┌',
	'.': '.',
	'S': 'S',
}

connector_dirs = {
	'|': [[-1, 0], [1, 0]],
	'-': [[0, -1], [0, 1]],
	'└': [[-1, 0], [0, 1]],
	'┘': [[-1, 0], [0, -1]],
	'┐': [[0, -1], [1, 0]],
	'┌': [[0, 1], [1, 0]],
	'.': [[-1, 0], [1, 0], [0, -1], [0, 1]],
	'0': [[-1, 0], [1, 0], [0, -1], [0, 1]]
}

MAX_ROW = len(lines)
MAX_COL = len(lines[0])

# do one pass of the entire input to find S and replace all connectors
# with bounding box characters
S = None
for row, line in enumerate(lines):
	for col, val in enumerate(line):
		if val == 'S':
			S = (row, col)
		lines[row][col] = connector_mappings[lines[row][col]]


def print_grid(grid):
	"""print the grid in a human readable manner"""
	print('\n'.join([' '.join(list(map(lambda x: str(x), line))) for line in grid]), '\n')


def adj(v, dirs, maxr, maxc):
	"""
	Given a (row, col) find out which connector this is and return
	all its valid neighbors
	"""
	row, col = v
	neighbors = []
	for d in dirs:
		dr, dc = d
		if row + dr < 0 or row + dr >= maxr:
			continue
		if col + dc < 0 or col + dc >= maxc:
			continue
		neighbors.append((row + dr, col + dc))
	return neighbors

def find_s_connector(S, grid):
	"""
	Given the (row, col) of the S point find out what connector
	can S be replaced with and return the allowed starting positions
	to traverse the main loop
	"""
	# find all 4 neighbors of S
	dirs = [
		[-1, 0], # above
		[0, 1], # right
		[1, 0], # below
		[0, -1], # left
	]

	sn = adj(S, dirs, MAX_ROW, MAX_COL)

	# for each neighbor see if S is adjacent to it
	allowed = []
	for n in sn:
		nr, nc = n
		if grid[nr][nc] == '.':
			continue
		dirs = connector_dirs.get(grid[nr][nc], [])
		if S in adj(n, dirs, MAX_ROW, MAX_COL):
			allowed.append(n)

	# replace S with any of the bending connectors
	# and see if we get the same pair of allowed neighbors
	s_connector = None
	for con, dirs in connector_dirs.items():
		n = adj(S, dirs, MAX_ROW, MAX_COL)
		if all([point in allowed for point in n]):
			s_connector = con
			break
	
	return s_connector, allowed


def walk(src, grid):
	"""
	Do a BFS search on the given grid and return the explored
	points and their parents
	Source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-13-breadth-first-search-bfs/
	"""
	level = {src: 0}
	parent = {src: None}
	i = 1
	frontier = [src]
	while frontier:
		todo = []
		for u in frontier:
			ur, uc = u
			dirs = connector_dirs[grid[ur][uc]]
			for v in adj(u, dirs, MAX_ROW, MAX_COL):
				# we don't want to get back to S again
				if v == S:
					continue
				if v not in level:
					level[v] = i
					parent[v] = u
					todo.append(v)
		frontier = todo
		i += 1
	return level, parent

def backtrack(start, parents):
	"Given a start point find the path"
	path = []
	curr = start
	while parents[curr]:
		path.append(curr)
		curr = parents[curr]
	return path

s_connector, allowed = find_s_connector(S, lines)
lines[S[0]][S[1]] = s_connector

# For each allowed starting point walk the pipes and track the exploration
parents = []
levels = []
for start in allowed:
	level, parent= walk(start, lines)
	levels.append(level)
	parents.append(parent)

# Find the furthest point by merging the explorations and taking the minimum
path = {}
for level in levels:
	for node, val in level.items():
		if node not in path:
			path[node] = math.inf
		path[node] = min(path[node], val)

def find_max_key(d):
	v = list(d.values())
	k = list(d.keys())
	return k[v.index(max(v))]

#### Part 1 ####
maxkey = find_max_key(path)
maxval = path[maxkey]
print(f"Starting at {S}")
print(f'Furthest point is {maxkey} with value {maxval + 1}')
################

def expand_tile(tile):
	if tile == '.':
		return [
			['.', '.', '.'],
			['.', '.', '.'],
			['.', '.', '.']
		]
	if tile == '0':
		return [
			['.', '.', '.'],
			['.', '0', '.'],
			['.', '.', '.']
		]
	if tile == '|':
		return [
			['.', '|', '.'],
			['.', '|', '.'],
			['.', '|', '.']
		]
	if tile == '-':
		return [
			['.', '.', '.'],
			['-', '-', '-'],
			['.', '.', '.']
		]
	if tile == '└':
		return [
			['.', '|', '.'],
			['.', '└', '-'],
			['.', '.', '.']
		]
	if tile == '┘':
		return [
			['.', '|', '.'],
			['-', '┘', '.'],
			['.', '.', '.']
		]
	if tile == '┐':
		return [
			['.', '.', '.'],
			['-', '┐', '.'],
			['.', '|', '.'],
		]
	if tile == '┌':
		return [
			['.', '.', '.'],
			['.', '┌', '-'],
			['.', '|', '.'],
		]


def expand_line(line, grid):
	"""Given a single line, expand everything on the line to a 3x3 size"""
	lines = [
		[],
		[],
		[]
	]
	for tile in grid[line]:
		expansion = expand_tile(tile)
		for idx, e in enumerate(expansion):
			lines[idx] += e
	return lines


def expand_grid(grid):
	lines = []
	for idx, _ in enumerate(grid):
		el = expand_line(idx, grid)
		for l in el:
			lines.append(l)
	return lines

def flood(src, grid):
	level = {src: 0}
	parent = {src: None}
	i = 1
	frontier = [src]
	# we need to recompute our max because we expanded the grid
	MAX_ROW = len(grid)
	MAX_COL = len(grid[0])
	while frontier:
		todo = []
		for u in frontier:
			ur, uc = u
			dirs = connector_dirs[grid[ur][uc]]
			for v in adj(u, dirs, MAX_ROW, MAX_COL):
				if v not in level and v not in ['|', '-', '└', '┘', '┐', '┌']:
					level[v] = i
					parent[v] = u
					todo.append(v)
		frontier = todo
		i += 1
	return level, parent

def build(path, lines):
	grid = []
	for line in lines:
		grid.append(['0'] * len(line))
	for point in path:
		row, col = point
		grid[row][col] = lines[row][col]
	return grid

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
	grid = build(path, lines)
	for n in path:
		main_loop.add(n)

# Add the original starting point
main_loop.add(S)
grid = build(main_loop, lines)
# print_grid(grid)

# Flood fill the expanded grid
expanded_grid = expand_grid(grid)
fl, fp = flood((0, 0), expanded_grid)

# Replace each flooded point with a dot
for point in fl.keys():
	row, col = point
	expanded_grid[row][col] = '.'

# Count the remaining zeros
ans = 0
for line in expanded_grid:
	for val in line:
		if val == '0':
			ans += 1
print(f'Total number of tiles in the main loop: {ans}')