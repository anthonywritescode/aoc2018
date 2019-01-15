advent of code 2018
===================

https://adventofcode.com/2018

- intro + project template - day 0
    - [youtube](https://www.youtube.com/watch?v=rpCsg3iVGhA)
    - [slides](https://anthonywritescode.github.io/aoc2018/day0/)
    - [slides (markdown)](https://github.com/anthonywritescode/aoc2018/blob/master/day0/slides.md)
- chronal calibration - day 1
    - [youtube](https://www.youtube.com/watch?v=TwaEIBXCWFE)
    - [slides](https://anthonywritescode.github.io/aoc2018/day1/)
    - [slides (markdown)](https://github.com/anthonywritescode/aoc2018/blob/master/day1/slides.md)
- inventory management system - day 2
    - [youtube](https://www.youtube.com/watch?v=ZU_bRzoBwbA)
    - [slides](https://anthonywritescode.github.io/aoc2018/day2/)
    - [slides (markdown)](https://github.com/anthonywritescode/aoc2018/blob/master/day2/slides.md)
- no matter how you slice it - day 3
    - [youtube](https://www.youtube.com/watch?v=r89Bfu7Ccs8)
    - [slides](https://anthonywritescode.github.io/aoc2018/day3/)
    - [slides (markdown)](https://github.com/anthonywritescode/aoc2018/blob/master/day3/slides.md)


### timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day0 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python ./day1/part1.py ./day1/input.txt
587
> 463 μs (oneline)
587
> 962 μs (golf)
587
> 437 μs (for loop)
+ python ./day1/part2.py ./day1/input.txt
83130
> 71237 μs (itertools)
83130
> 82161 μs (non itertools)
+ python ./day2/part1.py ./day2/input.txt
6474
> 2944 μs (counter counter)
6474
> 3224 μs (char subtract)
6474
> 2079 μs (golf)
6474
> 1971 μs (orig)
+ python ./day2/part2.py ./day2/input.txt
mxhwoglxgeauywfkztndcvjqr
> 2655 μs (substrings)
mxhwoglxgeauywfkztndcvjqr
> 2987 ms (difflib)
mxhwoglxgeauywfkztndcvjqr
> 101 ms (orig)
+ python ./day3/part1.py ./day3/input.txt
109143
> 262 ms
+ python ./day3/part2.py ./day3/input.txt
506
> 132 ms
+ python ./day4/part1.py ./day4/input.txt
60438
> 3781 μs (orig)
60438
> 3430 μs (counter)
+ python ./day4/part2.py ./day4/input.txt
47989
> 7153 μs
+ python ./day5/part1.py ./day5/input.txt
9900
> 20292 μs
+ python ./day5/part2.py ./day5/input.txt
4992
> 488 ms
+ python ./day6/part1.py ./day6/input.txt
3647
> 2051 ms
+ python ./day6/part2.py ./day6/input.txt
41605
> 9351 ms
+ python day7/part1.py day7/input.txt
EUGJKYFQSCLTWXNIZMAPVORDBH
> 395 μs (orig)
EUGJKYFQSCLTWXNIZMAPVORDBH
> 157 μs (topo sort)
+ python day7/part2.py day7/input.txt
1014
> 449 μs (orig)
1014
> 234 μs (topo sort)
+ python ./day8/part1.py ./day8/input.txt
47647
> 14382 μs (iterative)
47647
> 18938 μs (recursive)
+ python ./day8/part2.py ./day8/input.txt
23636
> 19253 μs (iterative)
23636
> 16699 μs (recursive)
+ python day9/part1.py day9/input.txt
367802
> 98837 μs (list)
367802
> 10092 μs (deque)
367802
> 25512 μs (circular dlist)
+ python day9/part2.py day9/input.txt
2996043280
> 1912 ms (circular dlist)
2996043280
> 1044 ms (deque)
+ python day10/part1.py day10/input.txt
######..#####...#....#..#....#..#.......######....##.....####.
#.......#....#..#....#..#...#...#.......#........#..#...#....#
#.......#....#..#....#..#..#....#.......#.......#....#..#.....
#.......#....#..#....#..#.#.....#.......#.......#....#..#.....
#####...#####...######..##......#.......#####...#....#..#.....
#.......#....#..#....#..##......#.......#.......######..#..###
#.......#....#..#....#..#.#.....#.......#.......#....#..#....#
#.......#....#..#....#..#..#....#.......#.......#....#..#....#
#.......#....#..#....#..#...#...#.......#.......#....#..#...##
#.......#####...#....#..#....#..######..######..#....#...###.#
> 164 ms (binary search)
######..#####...#....#..#....#..#.......######....##.....####.
#.......#....#..#....#..#...#...#.......#........#..#...#....#
#.......#....#..#....#..#..#....#.......#.......#....#..#.....
#.......#....#..#....#..#.#.....#.......#.......#....#..#.....
#####...#####...######..##......#.......#####...#....#..#.....
#.......#....#..#....#..##......#.......#.......######..#..###
#.......#....#..#....#..#.#.....#.......#.......#....#..#....#
#.......#....#..#....#..#..#....#.......#.......#....#..#....#
#.......#....#..#....#..#...#...#.......#.......#....#..#...##
#.......#####...#....#..#....#..######..######..#....#...###.#
> 22018 ms (orig)
+ python day10/part2.py day10/input.txt
10009
> 165 ms (binary search)
10009
> 21974 ms (orig)
+ python day11/part1.py day11/input.txt
235,35
> 413 ms (brute force)
235,35
> 216 ms (summed-area table)
+ python day11/part2.py day11/input.txt
142,265,7
> 337725 ms (brute force)
142,265,7
> 9039 ms (summed-area table)
+ python day12/part1.py day12/input.txt
2166
> 11588 μs
+ python day12/part2.py day12/input.txt
2100000000061
> 72239 μs
+ python day13/part1.py day13/input.txt
74,87
> 19561 μs
+ python day13/part2.py day13/input.txt
29,74
> 289 ms
+ python day14/part1.py day14/input.txt
7861362411
> 835 ms
+ python day14/part2.py day14/input.txt
20203532
> 40903 ms (orig)
20203532
> 25328 ms (only added slices)
+ python day15/part1.py day15/input.txt
201123
> 644 ms
+ python day15/part2.py day15/input.txt
54188
> 2563 ms
+ python day16/part1.py day16/input.txt
663
> 10518 μs
+ python day16/part2.py day16/input.txt
525
> 11908 μs
+ python day17/part1.py day17/input.txt
39367
> 1310 ms
+ python day17/part2.py day17/input.txt
33061
> 1261 ms
+ python day18/part1.py day18/input.txt
558960
> 245 ms
+ python day18/part2.py day18/input.txt
207900
> 10854 ms
+ python day19/part1.py day19/input.txt
1620
> 8750 ms
+ python day19/part2.py day19/input.txt
15827082
> 1741 ms
+ python day20/part1.py day20/input.txt
3991
> 70684 μs
+ python day20/part2.py day20/input.txt
8394
> 71869 μs
+ python day21/part1.py day21/input.txt
7216956
> 2212 μs
# before optimizing, day21: > 3134163 ms (52 minutes)
+ python day21/part2.py day21/input.txt
14596916
> 19394 μs
+ python day22/part1.py day22/input.txt
9659
> 17959 μs
+ python day22/part2.py day22/input.txt
1043
> 67253 ms
+ python day23/part1.py day23/input.txt
737
> 6942 μs
+ python day24/part1.py day24/input.txt
21070
> 70280 μs
+ python day24/part2.py day24/input.txt
7500
> 9351 ms
+ python day25/part1.py day25/input.txt
377
> 1898 ms
```
