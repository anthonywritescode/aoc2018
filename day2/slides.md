## advent of code 2018
### day 2 - inventory management system

***

[adventofcode.com/2018/day/2](https://adventofcode.com/2018/day/2)

***

### problem description

- have to find _magic_ fabric in bins!
- the bins have ids which are characters

***

### part 1

- compute a "checksum"
- count boxes which have exactly 2 of any letter
- count boxes which have exactly 3 of any letter
- multiply those together

***

### part 1 - example

```
abcdef   # nothing
bababc   # 2 (a)    3 (b)
abbcde   # 2 (b)
abcccd   #          3 (c)
aabcdd   # 2 (a, d)           (only counts once)
abcdee   # 2 (e)
ababab   #          3 (a, b)  (only counts once)

=> # of 2s: 4
=> # of 3s: 3
=> checksum 3 * 4 => 12
```

***

## spoilers

***

### part 1

- keep track of number of twos and threes
- for each id, figure out the counts of each character
- update the twos and threes counts
- finally return threes times fours

***

### part 1 - hints

`collections.Counter`

```pycon
>>> collections.Counter('cccaab')
Counter({'c': 3, 'a': 2, 'b': 1})
>>> collections.Counter('cccaab').values()
dict_values([3, 2, 1])
```

***

### part 1 solution 1

(psuedo code this time!)

```
twos = threes = 0
for each line in the input
    make a counter of the line
    if some count is 2
        increment twos
    if some count is 3
        increment threes
return threes * twos
```

***

### part 1 alternate solution

not more efficient, just a cool solution a follower found

```
twos = threes = 0
for each line in the input      # aaabbcdddd
    chars = list(line)          # [a, a, a, b, b, c, d, d, d, d]

    chars -= set(chars)         # [a, a, b, d, d, d]
    line_twos = set(chars)      # {a, b, d}

    chars -= set(chars)         # [a, d, d]
    line_threes = set(chars)    # {a, d}

    chars -= set(chars)         # [d]
    line_fours = set(chars)     # {d}

    twos += bool(line_twos - line_threes)
    threes += bool(line_threes - line_fours)

return twos * threes
```

***

### part 2

somewhat unrelated to part 1!

- find the ids which differ by only a character
- return the characters that are the same

***

### part 2 - sample input

```
abcde
fghij  <==
klmno
pqrst
fguij  <==
axcye
wvxyz
```

only differ by the third character, answer is `fgij`

***

## spoilers

***

### part 2 - hints

`zip` is helpful for comparing iterables

```
>>> for c1, c2 in zip('abc', 'def'):
...     print(c1, c2)
...
a d
b e
c f
>>> list(zip([1, 2, 3], [4, 5, 6]))
[(1, 4), (2, 5), (3, 6)]
```

_hint: use this to compare the lines_

***

### part 2 - solution "compare them all"

```
for each line in the input
    for each other line in the input
        answer = ''
        loop through each character in line and other line (zip)
            if they are the same append to answer
        if answer is one shorter than line
            return answer
```

O(N^2) time | O(N) space

***

### part 2 - alternate comparison

`difflib` - compare text!

```pycon
>>> print(''.join(difflib.ndiff(('aaaaabaaaa\n',), ('aaaaacaaaa\n',))))
- aaaaabaaaa
?      ^
+ aaaaacaaaa
?      ^
```

"count the number of ^ characters to see if it is 1 different"

***

### part 2 alternate solution

```
keep track of seen
for each line in the input     # O(N)
    # abcd => bcd, acd, abc
    for each substring of line without a character  # O(M)
        if it is in seen before
            return the answer
        else:
            record the substring as seen
```

O(N \* M) time | O(N \* M) space  (N = number of lines, M = line length)

***

### see you for day 3!

- [twitch.tv/anthonywritescode](https://twitch.tv/anthonywritescode)
- [github.com/anthonywritescode/aoc2018](https://github.com/anthonywritescode/aoc2018)
