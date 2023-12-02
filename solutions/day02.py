from typing import List
from collections import defaultdict, Counter
from cli import filepath


with open(filepath) as inp:
    lines = inp.read().splitlines()


def parse_set(s):
    """Parse a set to a dict of {color: count}"""
    cubes = defaultdict(int)
    for item in s.split(','):
        count, color = item.strip().split(' ')
        cubes[color] += int(count)
    return cubes

# print(parse_set("5 green, 2 blue"))

def play_part1(sets):
    """Try to play the game with the given sets"""
    counter = Counter({'red': 12, 'blue': 14, 'green': 13})
    for cubes in sets:
        # draw the cubes
        counter.subtract(cubes)
        if any([value < 0 for _, value in counter.items()]):
            return False
        # put them back in the bag
        counter.update(cubes)
    return True

def play_part2(sets):
    """Find the fewest number of colors for a game"""
    fewest = defaultdict(lambda: 1)
    for cubes in sets:
        for color, count in cubes.items():
            fewest[color] = max(fewest[color], count)
    power = 1
    for _, value in fewest.items():
        power *= value
    return power

# print(play_part1("8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red".split(';')))
# print(play_part2("8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red".split(';')))


def solve(lines: List[str]):
    """Play the game"""
    possible = []
    power = 0
    for line in lines:
        game, sets = line.split(':')
        _, game_id = game.split(' ')
        sets = [parse_set(s) for s in sets.split(';')]
        if play_part1(sets):
            possible.append(int(game_id))
        power += play_part2(sets)

    print(sum(possible))
    print(power)

solve(lines)