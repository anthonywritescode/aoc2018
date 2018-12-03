## advent of code 2018
### day 1 - chronal calibration

***

[adventofcode.com/2018/day/1](https://adventofcode.com/2018/day/1)

***

### problem description

- zapped back in time to solve the changing of santa's history
- day 1 you must calibrate your time travel device!

***

### example input

Inputs are a series of signed integers one per line

```
+1   #  0  =>  1
-2   #  1  => -1
+3   # -1  =>  2
+1   #  2  =>  3
```

***

### actual input

- everyone gets their own input*
- mine was 1004 lines, yours may vary

```rawhtml
<small>* not totally unique -- based on start time</small>
```

***

### part 1

- run through the list and print the final value

- `+1  +1  +1` results in ` 3`
- `+1  +1  -2` results in ` 0`
- `-1  -2  -3` results in `-6`

***

## **SPOILERS AHEAD**

***

### part 1 - in words

- keep track of the current frequency (starting at 0)
- parse the input line by line
- add the parsed value to the current frequency
- at the end produce the final value

***

### part 1 - code

keep track of the current frequency

```python
def compute(s: str) -> int:
    val = 0

    ...
```

***

### part 1 - code

parse the input line by line

```python
    for line in s.splitlines():
        ..
```

- could use `s.split('\n')` as well
- `splitlines()` is more portable and has fewer edgecases

***

### `splitlines()`

```pycon
>>> 'foo\nbar\n'.split('\n')
['foo', 'bar', '']
>>> 'foo\nbar\n'.splitlines()
['foo', 'bar']
>>> 'foo\r\nbar'.split('\n')
['foo\r', 'bar']
>>> 'foo\r\nbar'.splitlines()
['foo', 'bar']
```

***

### part 1 - code

add the parsed value to the current frequency

```python
for line in s.splitlines():
    val += int(line)
```

`int(...)` does the heavy lifting for parsing here so we don't have to!

***

### part 1 - code

at the end produce the final value

```python
def compute(s: str) -> int
    val = 0

    for line in s.splitlines():
        val += int(line)

    return val
```

***

### part 1 - running

```pytest
$ pytest -q day1/part1.py
....                                                                 [100%]
4 passed in 0.01 seconds
```

```console
$ python day1/part1.py day1/input.txt
587
```

***

### part 1 - other solutions

functional programming one liner

```python
def compute(s: str) -> int:
    return sum(int(line) for line in s.splitlines())
```

code golf

```python
lambda s:eval(f'({s})')
```

***

### part 2

- the device keeps producing the instructions in a loop
- find the first time a frequency is hit more than once

```
+1  #  0 =>  1
-2  #  1 => -1
+3  # -1 =>  2
+1  #  2 =>  3
(at this point the device starts again)
+1  #  3 =>  4
-2  #  4 =>  2 (which has been seen before!)
```

***

### part 2

- `+1, -1` first reaches `0` twice
- `+3, +3, +4, -2, -4` first reaches `10` twice
- `-6, +3, +8, +5, -6` first reaches `5` twice
- `+7, +7, -2, -7, -4` first reaches `14` twice

***

## **SPOILERS AHEAD**

***

### part 2 - in words

- keep track of the current value and all already seen
- parse line by line (repeatedly)
    - add to the current value
    - if it's seen before you're done
    - otherwise record it has been seen

***

### part 2 - code

keep track of the current value and all already seen

```python
def compute(s: str) -> int:
    val = 0
    seen = {val}

    ...
```

***

### part 2 - code

parse line by line repeatedly

```python
while True:
    for line in s.splitlines():
        ...
```

or

```python
for line in itertools.cycle(s.splitlines()):
    ...
```

***

### `itertools.cycle`

```pycon
>>> import itertools
>>> iterator = itertools.cycle((1, 2, 3))
>>> next(iterator)
1
>>> next(iterator)
2
>>> next(iterator)
3
>>> next(iterator)
1
>>> next(iterator)
2
>>> next(iterator)
3
```

***

### part 2 - code

update and check

```python
for line in itertools.cycle(s.splitlines()):
    val += int(line)

    if val in seen:
        return val
    else:
        seen.add(val)
```

***

### part 2 - code

```python
def compute(s: str) -> int:
    val = 0
    seen = {val}

    for line in itertools.cycle(s.splitlines()):
        val += int(line)

        if val in seen:
            return val
        else:
            seen.add(val)
```

***

### part 2 - running

```pytest
$ pytest -q day1/part2.py
.....                                                                [100%]
5 passed in 0.01 seconds
```

```console
$ python day1/part2.py day1/input.txt
83130
```

***

### see you for day 2!

- [twitch.tv/anthonywritescode](https://twitch.tv/anthonywritescode)
- [github.com/anthonywritescode/aoc2018](https://github.com/anthonywritescode/aoc2018)
