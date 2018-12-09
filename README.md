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
> 10822 μs (substrings)
mxhwoglxgeauywfkztndcvjqr
> 2970 ms (difflib)
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
> 3201 μs
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
+ python ./day7/part1.py ./day7/input.txt
EUGJKYFQSCLTWXNIZMAPVORDBH
> 402 μs
+ python ./day7/part2.py ./day7/input.txt
1014
> 488 μs
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
```
