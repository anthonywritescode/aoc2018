import os
import strutils

let lines = strutils.splitLines(readFile(os.paramStr(1)).strip())

for line in lines:
    for candidate in lines:
        var c = 0
        var lastc = -1
        for i in 0..<len(line):
            if line[i] != candidate[i]:
                c += 1
                lastc = i
        if c == 1:
            var copy = "" & line
            copy.delete(lastc, lastc)
            echo copy
            quit(0)
