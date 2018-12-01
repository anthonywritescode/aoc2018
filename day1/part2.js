#!/usr/bin/env nodejs
fs = require('fs');

function compute(s) {
    let val = 0;
    let seen = new Set([val]);

    while (true) {
        for (const line of s.match(/[^\r\n]+/g)) {
            val += parseInt(line, 10);
            if (seen.has(val)) {
                return val;
            } else {
                seen.add(val);
            }
        }
    }
}

(function () {
    if (process.argv.length != 3) {
        console.log(`usage: ${process.argv[1]} FILENAME`);
        process.exit(1);
    }
    let contents = fs.readFileSync(process.argv[2], 'utf8');
    console.log(compute(contents));
}());
