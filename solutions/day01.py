from typing import List
from cli import filepath

with open(filepath) as inp:
    lines = inp.read().splitlines()

words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
def matches(line: str):
    """Tells if the line starts with one-nine words"""
    for w in words:
        if line.startswith(w):
            return w
    return None

def extract(line: str, part2: bool=False):
    """Extract 1-9 digits and/or one-nine words from the line"""
    i = 0
    result = []
    while i < len(line):
        if line[i].isdigit():
            result.append(line[i])
            i += 1
            continue
        if part2:
            match = matches(line[i:])
            if match:
                result.append(line[i:i + len(match)])
                # last character of the current match could be first character of next match
                i += len(match) - 1
                continue

        i += 1
    
    return result

# print(extract("z7onetwonec"))

def first_and_last(items: List[str]):
    """Get the first and last element of items, convert one-nine to digits"""
    first = items[0]
    last = items[-1]

    if first in words:
        first = str(words.index(first) + 1)
    if last in words:
        last = str(words.index(last) + 1)

    return first + last


def calculate(lines, part2=False):
    """Calculate the calibration value"""
    result = 0
    for line in lines:
        value = first_and_last(extract(line, part2))
        result += int(value)
    return result


print(calculate(lines))
print(calculate(lines, True))
