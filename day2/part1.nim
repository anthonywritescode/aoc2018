import os
import strutils
import tables

let lines = strutils.splitLines(readFile(os.paramStr(1)))

var twos, threes: int
for line in lines:
    var counter = initCountTable[char]()
    for c in line:
        counter.inc(c)

    var hasTwo = false
    var hasThree = false
    for k, v in counter:
        if v == 2:
            hasTwo = true
        elif v == 3:
            hasThree = true

    if hasTwo:
        inc twos
    if hasThree:
        inc threes

echo twos * threes
