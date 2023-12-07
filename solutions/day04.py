import re
from cli import filepath

with open(filepath) as inp:
    lines = inp.read().splitlines()

lines = [line.split('|') for line in lines]
lines = [[line[0].split(':')[1].strip(), line[1].strip()] for line in lines]
lines = [[re.split('\s+', line[0]), re.split('\s+', line[1])] for line in lines]

cards = [line[0] for line in lines]
wins = [line[1] for line in lines]

memory = {}
def count_winning_numbers(card):
    if card in memory:
        return memory[card]
    count = len(list(filter(None, [n in wins[card] for n in cards[card]])))
    memory[card] = count
    return count

# print(count_winning_numbers(0))
# print(count_winning_numbers(1))


path = []
def collect(card):
    wining_numbers = count_winning_numbers(card)
    if wining_numbers == 0:
        path.append(card + 1)
        return
    
    path.append(card + 1)
    for i in range(1, wining_numbers + 1):
        collect(card + i)

for c in range(len(cards)):
    collect(c)
    
print(len(path))
# print(path)
# print(collect(0))