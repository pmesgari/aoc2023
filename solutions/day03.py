from typing import List
from collections import defaultdict, Counter
from cli import filepath


with open(filepath) as inp:
    lines = inp.read().splitlines()

grid = []
for line in lines:
    row = list(line)
    grid.append(row)

dirs = [
    [-1, 0], # north
    [-1, 1], # northeast
    [0, 1], # east
    [1, 1], # southeast
    [1, 0], # south
    [1, -1], # southwest
    [0, -1], # west
    [-1, -1], # northwest
]
def adj(point):
    """Get all valid neighbors of a given point"""
    result = []
    row, col = point
    for d in dirs:
        dr, dc = d
        if (row + dr) < 0 or (row + dr) >= len(grid):
            continue
        if (col + dc) < 0 or (col + dc) >= len(grid[0]):
            continue
        result.append((row + dr, col + dc))
    return result


def is_symbol(point):
    """Checks if the given point is a symbol"""
    row, col = point
    return grid[row][col] != '.' and not grid[row][col].isdigit()

def range_to_number(line, r):
    """Returns the integer value of a range in the given line"""
    start, end = r
    return int(''.join(line[start:end]))


stars = {}
def scan(row: int):
    """Scan the given row for point numbers and register star symbols"""
    i = 0
    j = 0

    line = grid[row]
    result = []
    while i < len(line):
        found = False
        star_symbols = set()
        if line[i].isdigit():
            j = i
            while line[j].isdigit():
                for point in adj((row, j)):
                    if is_symbol(point):
                        found = True
                        r, c = point
                        if grid[r][c] == '*':
                            star_symbols.add((r, c))
                j += 1
                if j >= len(line):
                    break
            if found:
                # print(i, j)
                for s in star_symbols:
                    if s not in stars:
                        stars[s] = set()
                    stars[s].add((row, (i, j)))
                result.append(int(''.join(line[i:j])))
            i = j
        i += 1
    return result

# scan(grid[0], 0)
# scan(grid[1], 1)
# scan(grid[2], 2)
# scan(grid[3], 3)



def solve():
    part_numbers = []
    for idx in range(len(grid)):
        for num in scan(idx):
            part_numbers.append(num)
    print(sum(part_numbers))
    ratios = []
    for val in stars.values():
        if len(val) == 2:
            row, r1 = val.pop()
            v1 = range_to_number(grid[row], r1)
            row, r2 = val.pop()
            v2 = range_to_number(grid[row], r2)
            ratios.append(v1 * v2)
            
    print(sum(ratios))
solve()
