# Advent of Code 2023

Solutions to advent of code 2023 challenges

## Main Takeaways

### Day 1

- First tried extracting the 1-9 and one-nine words using regex matches. But, soon realized my regex approach did not take into account overlapping matches, for example in the string `z7onetwonec`. Tried to figure out overlapping matches with regex, however, it seemed too complicated.
- Resorting to a simple pointer approach seemed like a good solution.

### Day 2

- Initially I missed the remark about putting back the cubes after each set of game is played. 
- Counters are handy for problems like this.