## advent of code 2018
### day 4 - DONTSHIP NAME HERE

***

[adventofcode.com/2018/day/4](https://adventofcode.com/2018/day/4)

***

## spoilers

***

### problem description

- DONTSHIP fill this in
- input is _unsorted_

***

### part 1

- find the sleepiest guard (the guard who was asleep the most)
- find what minute they were asleep the most

***

### part 1 sample data

```
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
```

***

### part 1 - sample data

```
#10 .....zzzzzzzzzzzzzzzzzzzz.....zzzzzzzzzzzzzzzzzzzzzzzzz.....
#99 ........................................zzzzzzzzzz..........
#10 ........................zzzzz...............................
#99 ....................................zzzzzzzzzz..............
#99 .............................................zzzzzzzzzz.....
                            ^
```

***

### part 1 - hints

- first things first, `sort` the data
- since the dates are in ISO-8601, you can just string sort
- the dates don't actually matter, just the minute
- sleep / awake events always come in pairs

***

### part 1 - code

```python
EVENT = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\]')
BEGIN_SHIFT = re.compile(rf'{EVENT.pattern} Guard #(\d+) begins shift$')
```

- `EVENT` pattern matches all lines, captures minute
- `BEGIN_SHIFT` pattern captures the guard id

***

### part 1 - code

```python
class Duration(NamedTuple):
    start: int
    end: int

    @property
    def time_asleep(self) -> int:
        return self.end - self.start
```

***

### part 1 - code

```python
guard_sleep_time: Counter[int] = collections.Counter()
durations: DefaultDict[int, List[Duration]] = collections.defaultdict(list)
```

- `Counter`: efficient lookup of highest value by `most_common`

  ```pycon
  >>> Counter({'a': 1, 'b': 5, 'c': 2}).most_common(1)
  [('b', 5)]
  ```

- `defaultdict`: insertion without needing to check existence

  ```pycon
  >>> dct = defaultdict(list)
  >>> dct[0].append(1)
  >>> dict(dct)
  {0: [1]}
  ```

***

### part 1 - state machine

```
===========  start shift  ===========  event (start)   ===================
| initial |      ==>      | looking |       ==>        | looking for end |
===========               ===========                  ===================
                                  |                           |
                             ^=================================

                            start shift                  event (end)
```

***

### part 1 - code

```python
guard = start = -1  # state variables

for line in sorted(s.splitlines()):
    begin_shift_match = BEGIN_SHIFT.match(line)
    event_match = EVENT.match(line)
    assert event_match, line
    if begin_shift_match:
        guard = int(begin_shift_match.group(2))
    elif start == -1:
        start = int(event_match.group(1))
    else:
        duration = Duration(start, int(event_match.group(1)))
        guard_sleep_time[guard] += duration.time_asleep
        durations[guard].append(duration)
        start = -1
```

***

### part 1 - code

```python
(sleepiest, _), = guard_sleep_time.most_common(1)

asleep_times: Counter[int] = collections.Counter()
for duration in durations[sleepiest]:
    asleep_times.update(range(duration.start, duration.end))

(sleepiest_minute, _), = asleep_times.most_common(1)
return sleepiest * sleepiest_minute
```

***

### part 1

```pytest
$ pytest -q day4/part1.py
..                                                                   [100%]
2 passed in 0.03 seconds
```

DONTSHIP: get times from desktop, also fill in README for new solution

```console
$ python day4/part1.py day4/input.txt
60438
> 4744 μs (orig)
60438
> 4263 μs (counter)
```

***

### part 2

- find the sleepiest (guard, minute)
- (instead of sleepiest guard and the minute they were sleepiest)

***

### part 2

easier than part 1?

```python
asleep_times = Counter[Tuple[int, int]] = collections.Counter()
```

key is `(guard, minute)` and value is the count

***

### part 2

record the `(guard, int)` pairs

```python
for line in sorted(s.splitlines()):

    # ... same state machine as before

    else:
        for minute in range(start, int(event_match.group(1)):
            asleep_times[(guard, minute)] += 1
        start = -1
```

***

### part 2

yay counter!

```python
((sleepiest, sleepiest_minute), _), = asleep_times.most_common(1)
return sleepiest * sleepiest_minute
```

***

### part 2

```pytest
$ pytest -q day4/part2.py
..                                                                   [100%]
2 passed in 0.03 seconds
```

DONTSHIP use times from desktop

```console
$ python day4/part2.py day4/input.txt
47989
> 10088 μs
```

***

### see you for day 5!

- [twitch.tv/anthonywritescode](https://twitch.tv/anthonywritescode)
- [github.com/anthonywritescode/aoc2018](https://github.com/anthonywritescode/aoc2018)
