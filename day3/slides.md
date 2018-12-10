## advent of code 2018
### day 3 - no matter how you slice it

***

[adventofcode.com/2018/day/3](https://adventofcode.com/2018/day/3)

***

### problem description

- now that you've acquired the magical fabric, we must cut it!
- each elf claims a rectangle cut of fabric is the right one
- unfortunately many claims overlap!

***

### part 1

- find how many squares are claimed by two or more
- each claim has an id, left, right, width, height
    - `#123 @ 3,2: 5x4`

***

### part 1

```rawhtml
<table class="noborder"><tr><td>
```

```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```

`X` = overlap

```rawhtml
</td><td>
```

```
........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
```

```rawhtml
</td></tr></table>
```

***

## spoilers

***

### part 1

- parse the inputs
- plot the rectangles on a grid, incrementing counts
- find the number of counts `> 1`

***

### part 1 - code

- create a grid to plot the rectangles on
- arbitrarily sized grid
- alternatively: make a very large fixed sized grid

```python
grid: DefaultDict[int, DefaultDict[int, int]]
grid = collections.defaultdict(lambda: collections.defaultdict(int))
```

***

### part 1 hints

```pycon
>>> d = collections.defaultdict(int)
>>> d[0]
0
>>> d[1] += 1
>>> d
defaultdict(<class 'int'>, {0: 0, 1: 1})
```

***

### part 1 - code

- parse each line and increment the grid

```python
PATTERN = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
```

```python
for line in s.splitlines():
    match = PATTERN.match(line)
    left, top = int(match.group(2)), int(match.group(3))
    width, height = int(match.group(4)), int(match.group(5))

    for x in range(left, left + width):
        for y in range(top, top + height):
            grid[x][y] += 1
```

***

### part 1 - code

iterate through the grid and count the `> 1` squares

```python
total = 0
for _, row in grid.items():
    for val in row.values():
        if val > 1:
            total += 1
return total
```

***

### part 1

```pytest
$ pytest -q day3/part1.py
.                                                                    [100%]
1 passed in 0.01 seconds
```

```console
$ python3 day3/part1.py day3/input.txt
109143
> 287 ms
```

***

### part 2

- ok so lots of stuff overlaps
- but apparently one claim does not! find it!

***

## spoilers!

***

### part 2

- parse claims
- compare each claim against each other claim

***

### part 2

parsing similar to before, but this time parse to a `Claim` class

```python
class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int
```

***

### part 2

- implement an `overlaps` function
- I googled ["rectangle collision detection"](https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection)

```python
    def overlaps(self, other: 'Claim') -> bool:
        """rectangle collision detection"""
        return (
            self.left < other.left + other.width and
            self.left + self.width > other.left and
            self.top < other.top + other.height and
            self.top + self.height > other.top
        )
```

***

### part 2

loop through each claim and find the one without overlap

```python
claims = [Claim.parse(line) for line in s.splitlines()]

for claim in claims:
    for other_claim in claims:
        if claim != other_claim and claim.overlaps(other_claim):
            break
    else:  # else block is run if there's never a `break`
        return claim.id
```

***

### part 2

```pytest
$ pytest -q day3/part2.py
.                                                                    [100%]
1 passed in 0.02 seconds
```

```console
$ python day3/part2.py day3/input.txt
506
> 136 ms
```

***

### see you for day 4!

- [twitch.tv/anthonywritescode](https://twitch.tv/anthonywritescode)
- [github.com/anthonywritescode/aoc2018](https://github.com/anthonywritescode/aoc2018)
