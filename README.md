# Advent of Code 2023

Solutions to advent of code 2023 challenges

## Main Takeaways

### Day 1

- First tried extracting the 1-9 and one-nine words using regex matches. But, soon realized my regex approach did not take into account overlapping matches, for example in the string `z7onetwonec`. Tried to figure out overlapping matches with regex, however, it seemed too complicated.
- Resorting to a simple pointer approach seemed like a good solution.

### Day 2

- Initially I missed the remark about putting back the cubes after each set of game is played.
- Counters are handy for problems like this.

### Day 3

The main idea I implemented here is based on a pointer scanning each row. As soon as I see a digit, I start another loop which continues as long as the next item is a digit. In this inner loop I check each digit's neighbors, if I encounter any star symbols, I collect their coordinates. Once I am done collecting all the digits, I check if I have found any star symbols.

If I have found any stars, then I register them in a `stars` dict. Each key of the dict is the `row` and `column` where I found the start. The value for each key is a list of tuples `(row, (i, j))` where `row` tells me which line, and `(i, j)` tells me what range. This `(i, j)` range is later used to retrieve the full number.

Once I am done with scanning, then I look at my `stars` dict and every time I encounter a key with exactly two values, I convert each tuple in the list to a number and then add their product to the result

- The challenging part of this problem was proper implementation of constructing a number from the single digits.

### Day 4

I liked today's challenge because I could practice my skills in implementing a recursive solution. I only realized that we are actually building a tree as we go for part 2. For example encountring a card number 2 would result in the following structure:

```
2
 -> 3
     -> 4
         -> 5
     -> 5
 -> 4
    -> 5
```

The interesting part here is that card number 5 is given to have no further cards, and this is what allows the algorithm to actually terminate. So, it acts as a leaf node.

For my recursive algorithm, I start from a given card, then I count all its winning numbers, if there are no winning numbers then I add this card to my `collection` list and return. If there are winning numbers, then I first add the card I have now to my `collection` list, then for each winning number I start to collect their winning numbers.

For part 2 at first I experienced a slow response. I was suspecting the recursive approach, however, it turned out the increase in response time was due to the `count_winning_numbers` method. It turns out applying `lis(filter(...))` is quite slow. So, I fixed it by keeping track of winning numbers for cards and instead of recalculating it everytime, look it up in the memory dict.

### Day 5

Most challenging day so far, just because adminstering mathematically ranges is tedious and very error prone. Took me a long time to properly implement the logic to find the overlap and non-overlap segments between two ranges.

The main idea here is to take each `(seed, length)` pair and then apply each map to it. While applying a map, two things can happen:

- The seed range overlaps with a given line of the map in one of these four cases:
  - Inner `r1 <= s1 and s2 <= r2`
  ```
        s1--------s2
     r1--------------r2
  ```
  - Left `r1 <= s1 < r2` (s1 is between r1 and r2)
  ```
        s1---------s2
    r1----------r2
  ```
  - Right `r1 < s2 <= r2` (s2 is between r1 and r2)
  ```
     s1-----------s2
          r1-----------r2
  ```
  - Outer `r1 <= s1 and r2 <= s2`
  ```
     s1-----------s2
        r1-----r2
  ```
- There is no overlap with a given line of the map

If there is an overlap, then I extract the overlapped part and find the non-overlapping part(s).

What was overlapped can be considered done, and what is not overlapped should be considered for the next lines.

If we are done processing a seed range against all the map lines and we didn't find any overlapping parts, then we just add the seed range as is to the list of items we have processed. This list of processed items is then used as input to the next map.

- I initially spent a long time trying to apply a binary search algorithm but could not implement one. Since we are looking for a minimum, and that the input data is extremely large, made me think binary search could be applicable. But, I think because of the discontinous ranges, it is not possible to directly apply binary search.
- When working with the seeds and the maps, I used for my seed ranges the format `(start, length)` and for the map lines `(destination, source, length)`. But working with `(start, length)` proved tedious, it made it complicated to pass around the ranges. So, best is to immediately work with applied seed ranges like this: `(start, start + length)`.
- Also, took me again another while to figure out the order of the `if` statements in my `apply` function actually matters. A left overlap can be considered as a superset of an inner overlap. If we first check for a left overlap, we might mistakingly match an inner lap with a left one. Since the outcome of a left and inner overlap are different, everything will be messed up from that point onwards.
